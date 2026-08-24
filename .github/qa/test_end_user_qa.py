import tempfile
import unittest
from pathlib import Path
import end_user_qa


class EndUserQATests(unittest.TestCase):
    def make_site(self, files):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        for rel, text in files.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')
        self.addCleanup(td.cleanup)
        return root

    def test_flags_track_profile_developer_explanation(self):
        root = self.make_site({
            'atlas/tracks/AZ-TRK-0001/index.html': '<html><body><div class="tp-kicker">HOW THIS PROFILE WORKS</div><div class="tp-evidence-flow"></div></body></html>'
        })
        issues = end_user_qa.scan_site(root)
        joined = '\n'.join(issues)
        self.assertIn('HOW THIS PROFILE WORKS', joined)
        self.assertIn('tp-evidence-flow', joined)

    def test_flags_claim_admission_metadata(self):
        root = self.make_site({
            'research/claims/AZ-PUB-0001/index.html': '<html><body><div class="record-meta"><div>Admission <b>PASS</b></div></div></body></html>'
        })
        issues = end_user_qa.scan_site(root)
        self.assertTrue(any('Admission PASS' in issue for issue in issues))

    def test_flags_stale_public_version(self):
        root = self.make_site({'index.html': '<html><body>Arizona Connect 0.55.7</body></html>'})
        issues = end_user_qa.scan_site(root, expected_version='0.55.8')
        self.assertTrue(any('stale version' in issue for issue in issues))

    def test_flags_missing_arizona_home_on_deep_public_page(self):
        root = self.make_site({'research/claims/AZ-PUB-0001/index.html': '<html><body><a href="../../index.html">Register Home</a></body></html>'})
        issues = end_user_qa.scan_site(root)
        self.assertTrue(any('Arizona Connect Home' in issue for issue in issues))

    def test_accepts_clean_public_copy(self):
        root = self.make_site({
            'atlas/tracks/AZ-TRK-0001/index.html': '<html><body><a href="../../../index.html">Arizona Connect Home</a><h2>Documented claims</h2></body></html>',
            'research/claims/AZ-PUB-0001/index.html': '<html><body><a href="../../../index.html">Arizona Connect Home</a><div>Evidence type</div><div>Confidence HIGH</div><h2>Limits of the evidence</h2></body></html>',
            'index.html': '<html><body>Arizona Connect 0.55.8</body></html>'
        })
        issues = end_user_qa.scan_site(root, expected_version='0.55.8')
        self.assertEqual([], issues)

    def test_flags_track_claims_system_summary(self):
        root = self.make_site({
            'atlas/tracks/AZ-TRK-0001/index.html': '<html><body><a href="../../../index.html">Arizona Connect Home</a><p>2 governed public claims currently connect to this profile. The wording below comes from the admitted Research Register record and retains its evidence boundary.</p></body></html>'
        })
        issues = end_user_qa.scan_site(root)
        self.assertTrue(any('system-facing track claims summary' in issue for issue in issues))

    def test_flags_governed_metric_on_primary_surface(self):
        root = self.make_site({
            'atlas/events/index.html': '<html><body><div class="metric"><span>28 Governed events</span></div></body></html>'
        })
        issues = end_user_qa.scan_site(root)
        self.assertTrue(any('internal metric label' in issue for issue in issues))


if __name__ == '__main__':
    unittest.main()
