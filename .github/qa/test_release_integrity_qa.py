import json
import tempfile
import unittest
from pathlib import Path

import release_integrity_qa


class ReleaseIntegrityQATests(unittest.TestCase):
    def make_site(self, files):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        for rel, text in files.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(text, (dict, list)):
                p.write_text(json.dumps(text), encoding='utf-8')
            else:
                p.write_text(text, encoding='utf-8')
        self.addCleanup(td.cleanup)
        return root

    def test_claim_title_must_link_to_its_claim_page(self):
        root = self.make_site({
            'data/public-claims-current.json': [{'claim_id': 'AZ-PUB-0207'}],
            'research/claims/index.html': '<article data-claim-card data-claim-id="AZ-PUB-0207"><h3>Claim title</h3><a class="primary" href="AZ-PUB-0207/index.html">Open</a></article>',
            'research/claims/AZ-PUB-0207/index.html': '<h1>Claim</h1>',
        })
        issues = release_integrity_qa.scan_site(root, expected_version='0.56.2')
        self.assertTrue(any('claim title is not directly linked' in x for x in issues))

    def test_local_fragment_must_resolve(self):
        root = self.make_site({
            'research/sources/index.html': '<a href="../supporting/index.html#AZ-PUB-0017">AZ-PUB-0017</a>',
            'research/supporting/index.html': '<article data-support-card data-claim-id="AZ-PUB-0017"></article>',
        })
        issues = release_integrity_qa.scan_site(root, expected_version='0.56.2')
        self.assertTrue(any('missing local fragment target' in x for x in issues))

    def test_displayed_counts_must_match_canonical_data(self):
        root = self.make_site({
            'data/public-claims-current.json': [{'claim_id': 'A'}, {'claim_id': 'B'}],
            'data/supporting-evidence-current.json': [{'claim_id': 'S'}],
            'data/arizona-track-census-r1.json': [{'id': 'T'}],
            'data/arizona-history-timeline-current.json': [{'timeline_id': 'M', 'question': False}, {'timeline_id': 'Q', 'question': True}],
            'data/arizona-events-current.json': [{'event_id': 'E'}],
            'manifest.json': {'version':'0.56.2','claims': 99, 'supporting_evidence': 1, 'atlas': {'records': 1, 'timeline': {'published_milestones':1,'open_questions':1}, 'phase5_events': {'event_records':1}, 'current_release': {'public_claims':99,'supporting_evidence_records':1,'track_records':1,'timeline_milestones':1,'timeline_open_questions':1,'event_records':1}}},
            'index.html': '<body>Arizona Connect 0.56.2</body>',
        })
        issues = release_integrity_qa.scan_site(root, expected_version='0.56.2')
        self.assertTrue(any('manifest public claim count' in x for x in issues))

    def test_unpinned_track_must_return_to_focused_track_explorer(self):
        root = self.make_site({
            'data/arizona-location-register-a4-r1.json': [{'track_id':'AZ-TRK-0132','location_state':'CITY_ONLY_NO_POINT','lat':None,'lon':None}],
            'atlas/tracks/AZ-TRK-0132/index.html': '<a href="../../index.html">← Back to Arizona map</a>',
        })
        issues = release_integrity_qa.scan_site(root, expected_version='0.56.2')
        self.assertTrue(any('unpinned track does not return to focused Track Explorer' in x for x in issues))

    def test_atlas_map_must_offer_all_as_default(self):
        root = self.make_site({
            'atlas/index.html': '<div class="map-toolbar"><button class="view-button active" data-view="current" aria-pressed="true">Current</button><button data-view="historical">Historical</button></div>',
        })
        issues = release_integrity_qa.scan_site(root, expected_version='0.56.2')
        self.assertTrue(any('Atlas ALL view is missing or not default' in x for x in issues))

    def test_recovery_links_must_target_specific_track(self):
        root = self.make_site({
            'atlas/recovery/index.html': '<button class="recovery-card" id="recovery-AZ-TRK-0132" data-track="AZ-TRK-0132"></button>',
            'atlas/tracks/AZ-TRK-0132/index.html': '<a href="../../recovery/index.html">Open recovery work →</a>',
        })
        issues = release_integrity_qa.scan_site(root, expected_version='0.56.2')
        self.assertTrue(any('generic recovery link' in x for x in issues))

    def test_flags_system_facing_visitor_language(self):
        root = self.make_site({
            'atlas/timeline/index.html': '<section><strong>DATE PRECISION IS EVIDENCE</strong><p>The interface does not manufacture an exact day.</p></section>',
            'atlas/index.html': '<span class="map-state">A4 REGISTERED LOCATION LAYER</span>',
        })
        issues = release_integrity_qa.scan_site(root, expected_version='0.56.2')
        joined = '\n'.join(issues)
        self.assertIn('system-facing visitor language', joined)
        self.assertIn('REGISTERED LOCATION LAYER', joined)

    def test_system_language_scan_ignores_code_filenames(self):
        root = self.make_site({
            'atlas/index.html': '<section><h2>Download the project data.</h2><code>arizona-track-census-r1.json</code><span>Tracks</span></section>',
        })
        issues = release_integrity_qa.scan_system_language(root)
        self.assertEqual([], issues)

    def test_flags_broader_internal_process_language(self):
        root = self.make_site({
            'atlas/index.html': '<p>Location state</p><p>Record type</p>',
            'atlas/methodology/index.html': '<span>Methodology · v0.56.2 governing trust section</span><p>The Timeline does not manufacture days.</p>',
            'atlas/tracks/AZ-TRK-0001/index.html': '<a>Open governing source ↗</a><span>A1 authority</span>',
            'atlas/events/index.html': '<p>This event object governs the period announcement only.</p>',
            'atlas/media/index.html': '<p>IMAGE NOT REPRODUCED IN THIS RELEASE</p>',
            'research/claims/AZ-PUB-0001/index.html': '<p>display an access date and recheck before future releases.</p>',
        })
        issues = release_integrity_qa.scan_system_language(root)
        joined = '\n'.join(issues)
        for phrase in ('Location state', 'governing trust section', 'Open governing source', 'event object governs', 'THIS RELEASE', 'future releases'):
            self.assertIn(phrase.lower(), joined.lower())

    def test_key_surface_stale_counts_are_detected(self):
        root = self.make_site({
            'data/public-claims-current.json': [{'claim_id': f'P{i}'} for i in range(3)],
            'data/supporting-evidence-current.json': [{'claim_id': 'S1'}],
            'data/arizona-track-census-r1.json': [{'id': 'T1'}, {'id': 'T2'}],
            'data/arizona-history-timeline-current.json': [
                {'timeline_id':'M1','question':False}, {'timeline_id':'M2','question':False},
                {'timeline_id':'Q1','question':True}],
            'data/arizona-events-current.json': [{'event_id':'E1'}, {'event_id':'E2'}],
            'research/index.html': '<a>Browse 2 public claims</a><span>9 source records</span>',
            'atlas/index.html': '<p>1 published milestones plus 1 optional open research questions.</p>',
            'atlas/timeline/index.html': '<div class="timeline-count"><strong data-count>1</strong><span>milestones</span></div>',
            'atlas/events/index.html': '<span>1 event records</span>',
            'atlas/methodology/index.html': '<div class="gate-stat"><b>2</b> public Arizona claims · 1 supporting evidence records</div>',
        })
        issues = release_integrity_qa.scan_surface_counts(root, '0.56.2')
        joined = '\n'.join(issues)
        self.assertIn('research/index.html', joined)
        self.assertIn('atlas/index.html', joined)
        self.assertIn('atlas/timeline/index.html', joined)
        self.assertIn('atlas/events/index.html', joined)
        self.assertIn('atlas/methodology/index.html', joined)

    def test_dom_records_must_match_canonical_datasets(self):
        root = self.make_site({
            'data/public-claims-current.json': [{'claim_id': 'P1'}, {'claim_id': 'P2'}],
            'data/arizona-track-census-r1.json': [{'id': 'T1'}, {'id': 'T2'}],
            'data/arizona-history-timeline-current.json': [
                {'timeline_id':'M1','question':False}, {'timeline_id':'M2','question':False}, {'timeline_id':'Q1','question':True}],
            'data/arizona-events-current.json': [{'event_id':'E1'}, {'event_id':'E2'}],
            'research/claims/index.html': '<article data-claim-card data-claim-id="P1"></article>',
            'atlas/index.html': '<article data-track-card id="card-T1"></article>',
            'atlas/timeline/index.html': '<article class="chrono-item" data-id="M1"></article><article class="chrono-item" data-id="Q1"></article>',
            'atlas/events/index.html': '<article class="event-card" id="E1"></article>',
        })
        issues = release_integrity_qa.scan_dom_record_parity(root)
        joined = '\n'.join(issues)
        self.assertIn('public claim DOM IDs', joined)
        self.assertIn('track DOM IDs', joined)
        self.assertIn('timeline DOM IDs', joined)
        self.assertIn('event DOM IDs', joined)

    def test_runtime_javascript_must_not_generate_system_facing_copy(self):
        root = self.make_site({
            'atlas/timeline/timeline.js': 'const msg = "No governed track record is attached. Timeline does not invent a marker.";',
            'atlas/relationships/relationships-v022.js': 'const empty = "No admitted public edge in this governed entity layer.";',
        })
        issues = release_integrity_qa.scan_runtime_language(root)
        joined = '\n'.join(issues).lower()
        self.assertIn('governed track record', joined)
        self.assertIn('admitted public edge', joined)

    def test_recovery_display_count_must_match_recovery_cards(self):
        root = self.make_site({
            'atlas/recovery/index.html': '<strong data-count>30</strong><button class="recovery-card" data-track="T1"></button><button class="recovery-card" data-track="T2"></button>',
        })
        issues = release_integrity_qa.scan_dom_record_parity(root)
        self.assertTrue(any('recovery displayed count' in x for x in issues))

    def test_category_cards_must_match_canonical_public_categories(self):
        root = self.make_site({
            'data/public-claims-current.json': [
                {'claim_id':'P1','category':'Tracks / A'},
                {'claim_id':'P2','category':'Tracks / B'},
            ],
            'research/categories/index.html': '<article data-category-card><a href="../claims/index.html?category=Tracks%20%2F%20A">Browse</a></article><article data-category-card><a href="../claims/index.html?category=Tracks%20%2F%20OLD">Browse</a></article>',
        })
        issues = release_integrity_qa.scan_dom_record_parity(root)
        self.assertTrue(any('category DOM values' in x for x in issues))

    def test_source_cards_must_match_canonical_source_ids_not_just_count(self):
        root = self.make_site({
            'data/public-claims-current.json': [{'claim_id':'P1','source_ids':['AZ-SRC-0001','AZ-SRC-0002']}],
            'research/sources/index.html': '<article data-source-card data-search="AZ-SRC-0001 host"></article><article data-source-card data-search="AZ-SRC-9999 host"></article>',
        })
        issues = release_integrity_qa.scan_dom_record_parity(root)
        self.assertTrue(any('source DOM IDs' in x for x in issues))

    def test_recovery_cards_must_match_embedded_recovery_records(self):
        root = self.make_site({
            'atlas/recovery/index.html': '<strong data-count>1</strong><button class="recovery-card" data-track="T1"></button><script id="recoveryData" type="application/json">[{"id":"T1"},{"id":"T2"}]</script>',
        })
        issues = release_integrity_qa.scan_dom_record_parity(root)
        self.assertTrue(any('recovery DOM IDs' in x for x in issues))

    def test_claim_id_must_also_link_to_its_claim_page(self):
        root = self.make_site({
            'data/public-claims-current.json': [{'claim_id': 'AZ-PUB-0207'}],
            'research/claims/index.html': '<article data-claim-card data-claim-id="AZ-PUB-0207"><div class="claim-id">AZ-PUB-0207</div><h3><a class="claim-title-link" href="AZ-PUB-0207/index.html">Claim</a></h3></article>',
            'research/claims/AZ-PUB-0207/index.html': '<h1>Claim</h1>',
        })
        issues = release_integrity_qa.scan_claim_titles(root)
        self.assertTrue(any('claim ID is not directly linked' in x for x in issues))

    def test_flags_internal_location_enum_and_atlas_admission_language(self):
        root = self.make_site({
            'atlas/tracks/T1/index.html': '<p>The Atlas admits only a SITE_POINT_APPROXIMATE for this track.</p>',
        })
        issues = release_integrity_qa.scan_system_language(root)
        joined = '\n'.join(issues)
        self.assertIn('Atlas admits', joined)

    def test_flags_evidence_boundary_label_in_public_copy(self):
        root = self.make_site({
            'research/claims/index.html': '<div>Evidence boundary: exact site remains open.</div>',
        })
        issues = release_integrity_qa.scan_system_language(root)
        self.assertTrue(any('Evidence boundary' in x for x in issues))


if __name__ == '__main__':
    unittest.main()
