#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

PUBLIC_ROOTS = ('atlas/', 'research/')
SYSTEM_PATTERNS = (
    r'\bgoverned\b',
    r'governing trust section',
    r'Open governing source',
    r'event object governs',
    r'Lititz governs the catalog record',
    r'\bA[12] authority\b',
    r'\bB[12](?: \+ [ABC][12])*[^.]{0,40}authority\b',
    r'\bLocation state\b',
    r'\bRecord type\b',
    r'\bbaseline\b',
    r'\binterface\b',
    r'\blayers?\b',
    r'\bcensus\b',
    r'Geographic Absolute',
    r'REGISTERED LOCATION LAYER',
    r'Evidence lane',
    r'relationship edges?',
    r'open controls?',
    r'L1_INTERNAL_CONTROL',
    r'LINK_ONLY',
    r'source-governed',
    r'admitted to the public evidence layer',
    r'public-history status',
    r'machine-readable',
    r'The Timeline does not manufacture days',
    r'IMAGE NOT REPRODUCED IN THIS RELEASE',
    r'this release does not treat',
    r'future releases',
    r'\bAtlas admits\b',
    r'\b(?:SITE_POINT_APPROXIMATE|EXACT_TRACK_POINT|CITY_ONLY_NO_POINT)\b',
    r'\bEvidence boundary:',
)


def visible_text(raw: str) -> str:
    raw = re.sub(r'<script\b[^>]*>.*?</script>', ' ', raw, flags=re.I | re.S)
    raw = re.sub(r'<style\b[^>]*>.*?</style>', ' ', raw, flags=re.I | re.S)
    raw = re.sub(r'<code\b[^>]*>.*?</code>', ' ', raw, flags=re.I | re.S)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    return ' '.join(unescape(raw).split())


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return default


def canonical_counts(root: Path) -> dict[str, int]:
    public = load_json(root / 'data/public-claims-current.json', [])
    supporting = load_json(root / 'data/supporting-evidence-current.json', [])
    tracks = load_json(root / 'data/arizona-track-census-r1.json', [])
    timeline = load_json(root / 'data/arizona-history-timeline-current.json', [])
    events = load_json(root / 'data/arizona-events-current.json', [])
    source_ids = set()
    for row in list(public) + list(supporting):
        source_ids.update(row.get('source_ids', []))
    return {
        'public': len(public),
        'supporting': len(supporting),
        'tracks': len(tracks),
        'milestones': sum(1 for r in timeline if not r.get('question')),
        'questions': sum(1 for r in timeline if r.get('question')),
        'events': len(events),
        'sources': len(source_ids),
    }


def attr(tag: str, name: str) -> str | None:
    m = re.search(rf'\b{name}\s*=\s*["\']([^"\']*)["\']', tag, flags=re.I)
    return m.group(1) if m else None


def local_target(root: Path, source: Path, href: str) -> tuple[Path | None, str]:
    parts = urlsplit(href)
    if parts.scheme or parts.netloc or href.startswith(('mailto:', 'tel:', 'javascript:')):
        return None, ''
    fragment = unquote(parts.fragment)
    path_part = unquote(parts.path)
    if not path_part:
        target = source
    else:
        target = (source.parent / path_part).resolve()
        if target.is_dir():
            target = target / 'index.html'
    return target, fragment


def scan_fragments(root: Path) -> list[str]:
    issues = []
    target_cache: dict[Path, tuple[str, set[str]]] = {}
    for source in sorted(root.rglob('*.html')):
        rel = source.relative_to(root).as_posix()
        if not rel.startswith(PUBLIC_ROOTS):
            continue
        raw = source.read_text(encoding='utf-8', errors='ignore')
        for href in re.findall(r'href\s*=\s*["\']([^"\']+)["\']', raw, flags=re.I):
            target, fragment = local_target(root, source, href)
            if target is None:
                continue
            if not target.exists():
                issues.append(f'{rel}: missing local target for {href}')
                continue
            if fragment:
                cached = target_cache.get(target)
                if cached is None:
                    t = target.read_text(encoding='utf-8', errors='ignore')
                    ids = set(re.findall(r'(?<![-\w])id\s*=\s*["\']([^"\']+)["\']', t, flags=re.I))
                    cached = (t, ids)
                    target_cache[target] = cached
                if fragment not in cached[1]:
                    issues.append(f'{rel}: missing local fragment target for {href}')
    return issues


def scan_claim_titles(root: Path) -> list[str]:
    issues = []
    page = root / 'research/claims/index.html'
    if not page.exists():
        return issues
    raw = page.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'<article\b(?P<tag>[^>]*)>(?P<body>.*?)</article>', raw, flags=re.I | re.S):
        tag, body = m.group('tag'), m.group('body')
        if 'data-claim-card' not in tag:
            continue
        cid = attr('<article ' + tag + '>', 'data-claim-id') or 'UNKNOWN'
        h3 = re.search(r'<h3\b[^>]*>(.*?)</h3>', body, flags=re.I | re.S)
        expected = f'{cid}/index.html'
        if not h3 or not re.search(rf'<a\b[^>]*href=["\']{re.escape(expected)}["\']', h3.group(1), flags=re.I | re.S):
            issues.append(f'research/claims/index.html: {cid} claim title is not directly linked to {expected}')
        claim_id = re.search(r'<(?:div|span)\b[^>]*class=["\'][^"\']*\bclaim-id\b[^"\']*["\'][^>]*>(.*?)</(?:div|span)>', body, flags=re.I | re.S)
        if not claim_id or not re.search(rf'<a\b[^>]*href=["\']{re.escape(expected)}["\'][^>]*>\s*{re.escape(cid)}\s*</a>', claim_id.group(1), flags=re.I | re.S):
            issues.append(f'research/claims/index.html: {cid} claim ID is not directly linked to {expected}')
    return issues


def scan_supporting_anchors(root: Path) -> list[str]:
    issues = []
    p = root / 'research/supporting/index.html'
    if not p.exists():
        return issues
    raw = p.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'<article\b(?P<tag>[^>]*)>', raw, flags=re.I | re.S):
        if 'data-support-card' not in m.group('tag'):
            continue
        tag = '<article ' + m.group('tag') + '>'
        cid = attr(tag, 'data-claim-id')
        if cid and attr(tag, 'id') != cid:
            issues.append(f'research/supporting/index.html: supporting record {cid} lacks matching id fragment')
    return issues


def scan_manifest_counts(root: Path) -> list[str]:
    issues = []
    manifest_path = root / 'manifest.json'
    if not manifest_path.exists():
        return issues
    c = canonical_counts(root)
    m = load_json(manifest_path, {})
    checks = [
        ('manifest public claim count', m.get('claims'), c['public']),
        ('manifest supporting evidence count', m.get('supporting_evidence'), c['supporting']),
        ('manifest track count', m.get('atlas', {}).get('records'), c['tracks']),
        ('manifest timeline milestone count', m.get('atlas', {}).get('timeline', {}).get('published_milestones'), c['milestones']),
        ('manifest timeline question count', m.get('atlas', {}).get('timeline', {}).get('open_questions'), c['questions']),
        ('manifest event count', m.get('atlas', {}).get('phase5_events', {}).get('event_records'), c['events']),
        ('manifest current-release public claim count', m.get('atlas', {}).get('current_release', {}).get('public_claims'), c['public']),
        ('manifest current-release source count', m.get('atlas', {}).get('current_release', {}).get('governed_source_ids'), c['sources']),
        ('manifest current-release track count', m.get('atlas', {}).get('current_release', {}).get('track_records'), c['tracks']),
        ('manifest current-release milestone count', m.get('atlas', {}).get('current_release', {}).get('timeline_milestones'), c['milestones']),
        ('manifest current-release question count', m.get('atlas', {}).get('current_release', {}).get('timeline_open_questions'), c['questions']),
        ('manifest current-release event count', m.get('atlas', {}).get('current_release', {}).get('event_records'), c['events']),
        ('manifest research public claim count', m.get('research_register', {}).get('public_claims'), c['public']),
        ('manifest research source count', m.get('research_register', {}).get('current_source_ids'), c['sources']),
    ]
    for label, actual, expected in checks:
        if actual is not None and actual != expected:
            issues.append(f'{label}: {actual} != canonical {expected}')
    return issues


def scan_surface_counts(root: Path, expected_version: str) -> list[str]:
    issues = []
    c = canonical_counts(root)

    # Required current-state text on the major public entry surfaces.
    required = {
        'index.html': [f'Arizona Connect {expected_version}', f'{c["public"]} public Arizona claims', f'{c["supporting"]} supporting evidence records'],
        'research/index.html': [f'{c["public"]} public Arizona claims'],
        'research/claims/index.html': [f'Browse all {c["public"]} public Arizona claims'],
        'atlas/index.html': [f'{c["tracks"]} track profiles', f'{c["public"]} public Arizona claims'],
    }
    for rel, needles in required.items():
        p = root / rel
        if not p.exists():
            continue
        text = visible_text(p.read_text(encoding='utf-8', errors='ignore'))
        for n in needles:
            if n not in text:
                issues.append(f'{rel}: canonical display value missing: {n}')

    # Every count-shaped phrase on these summary surfaces must agree with
    # canonical data. This catches stale copy even when the correct number
    # happens to appear somewhere else on the same page.
    surface_rules = {
        'research/index.html': [
            (r'Browse (\d+) public claims', c['public'], 'browse-public-claims'),
            (r'(\d+) source records', c['sources'], 'source-records'),
            (r'(\d+) public Arizona claims', c['public'], 'public-claims'),
            (r'(\d+) supporting evidence records', c['supporting'], 'supporting-records'),
        ],
        'atlas/index.html': [
            (r'(\d+) track profiles', c['tracks'], 'track-profiles'),
            (r'(\d+) public Arizona claims', c['public'], 'public-claims'),
            (r'(\d+) published milestones', c['milestones'], 'published-milestones'),
            (r'(\d+) optional open research questions', c['questions'], 'open-questions'),
            (r'(\d+) event records', c['events'], 'event-records'),
        ],
        'atlas/events/index.html': [
            (r'(\d+) event records', c['events'], 'event-records'),
        ],
        'atlas/methodology/index.html': [
            (r'(\d+) track profiles', c['tracks'], 'track-profiles'),
            (r'(\d+) public Arizona claims', c['public'], 'public-claims'),
            (r'(\d+) supporting evidence records', c['supporting'], 'supporting-records'),
        ],
    }
    for rel, rules in surface_rules.items():
        p = root / rel
        if not p.exists():
            continue
        text = visible_text(p.read_text(encoding='utf-8', errors='ignore'))
        for pattern, expected, label in rules:
            for m in re.finditer(pattern, text, flags=re.I):
                actual = int(m.group(1))
                if actual != expected:
                    issues.append(f'{rel}: stale {label} count {actual}; canonical {expected}')

    timeline = root / 'atlas/timeline/index.html'
    if timeline.exists():
        raw = timeline.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'<strong\b[^>]*data-count(?:=["\'][^"\']*["\'])?[^>]*>\s*(\d+)\s*</strong>', raw, flags=re.I | re.S)
        if not m:
            issues.append('atlas/timeline/index.html: timeline milestone counter not found')
        elif int(m.group(1)) != c['milestones']:
            issues.append(f'atlas/timeline/index.html: stale timeline milestone count {m.group(1)}; canonical {c["milestones"]}')

    events = root / 'atlas/events/index.html'
    if events.exists():
        text = visible_text(events.read_text(encoding='utf-8', errors='ignore'))
        if f'{c["events"]} event records' not in text:
            issues.append(f'atlas/events/index.html: canonical event count missing: {c["events"]} event records')

    methodology = root / 'atlas/methodology/index.html'
    if methodology.exists():
        text = visible_text(methodology.read_text(encoding='utf-8', errors='ignore'))
        if f'{c["public"]} public Arizona claims' not in text:
            issues.append(f'atlas/methodology/index.html: canonical public claim count missing: {c["public"]} public Arizona claims')

    return issues


def scan_unpinned_routes(root: Path) -> list[str]:
    issues = []
    locations = load_json(root / 'data/arizona-location-register-a4-r1.json', [])
    for row in locations:
        if row.get('lat') is not None and row.get('lon') is not None:
            continue
        tid = row.get('track_id')
        if not tid:
            continue
        p = root / f'atlas/tracks/{tid}/index.html'
        if not p.exists():
            continue
        raw = p.read_text(encoding='utf-8', errors='ignore')
        if f'?track={tid}#explore' not in raw or 'Back to track explorer' not in visible_text(raw):
            issues.append(f'{p.relative_to(root).as_posix()}: unpinned track does not return to focused Track Explorer')
    return issues


def scan_atlas_all(root: Path) -> list[str]:
    p = root / 'atlas/index.html'
    if not p.exists():
        return []
    raw = p.read_text(encoding='utf-8', errors='ignore')
    ok = bool(re.search(r'<button\b[^>]*data-view=["\']all["\'][^>]*aria-pressed=["\']true["\'][^>]*>\s*All\s*</button>', raw, flags=re.I | re.S))
    if not ok:
        ok = bool(re.search(r'<button\b[^>]*aria-pressed=["\']true["\'][^>]*data-view=["\']all["\'][^>]*>\s*All\s*</button>', raw, flags=re.I | re.S))
    return [] if ok else ['atlas/index.html: Atlas ALL view is missing or not default']


def scan_recovery_routes(root: Path) -> list[str]:
    issues = []
    recovery = root / 'atlas/recovery/index.html'
    if not recovery.exists():
        return issues
    rraw = recovery.read_text(encoding='utf-8', errors='ignore')
    track_ids = set(re.findall(r'data-track=["\'](AZ-TRK-\d+)["\']', rraw, flags=re.I))
    for tid in sorted(track_ids):
        p = root / f'atlas/tracks/{tid}/index.html'
        if not p.exists():
            continue
        raw = p.read_text(encoding='utf-8', errors='ignore')
        for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']*recovery/index\.html[^"\']*)["\'][^>]*>(.*?)</a>', raw, flags=re.I | re.S):
            label = visible_text(m.group(2))
            if re.search(r'recovery|open questions|still unknown', label, flags=re.I) and f'?track={tid}#desk' not in m.group(1):
                issues.append(f'{p.relative_to(root).as_posix()}: generic recovery link for {tid}; expected track-specific target')
    return issues


def scan_system_language(root: Path) -> list[str]:
    issues = []
    for p in sorted(root.rglob('*.html')):
        rel = p.relative_to(root).as_posix()
        if not rel.startswith(PUBLIC_ROOTS):
            continue
        text = visible_text(p.read_text(encoding='utf-8', errors='ignore'))
        for pattern in SYSTEM_PATTERNS:
            m = re.search(pattern, text, flags=re.I)
            if m:
                snippet = text[max(0, m.start()-55):m.end()+90]
                issues.append(f'{rel}: system-facing visitor language: {snippet}')
                break
    return issues



RUNTIME_PATTERNS = (
    r'governed track record',
    r'governed points?',
    r'admitted public edge',
    r'governed entity layer',
    r'Phase \d+ relationship admitted',
    r'No separate public claim admitted',
    r'Evidence boundary:',
    r'evidence crosswalk',
    r'Open-question layer',
    r'manufacture a milestone',
    r'Timeline does not invent',
    r'Date state: OPEN',
    r'Date precision:',
    r'governed level',
    r'public relationships admitted',
    r'admitted edge',
    r'location_state\.replaceAll',
    r'status\.replaceAll',
)


def _ids_from_html(path: Path, pattern: str) -> list[str]:
    if not path.exists():
        return []
    raw = path.read_text(encoding='utf-8', errors='ignore')
    return re.findall(pattern, raw, flags=re.I | re.S)


def _compare_ids(label: str, actual: list[str], expected: list[str]) -> list[str]:
    issues = []
    aset, eset = set(actual), set(expected)
    if len(actual) != len(aset):
        issues.append(f'{label}: duplicate DOM IDs detected')
    if aset != eset:
        missing = sorted(eset - aset)
        extra = sorted(aset - eset)
        detail = []
        if missing:
            detail.append('missing ' + ', '.join(missing[:12]) + (' …' if len(missing) > 12 else ''))
        if extra:
            detail.append('extra ' + ', '.join(extra[:12]) + (' …' if len(extra) > 12 else ''))
        issues.append(f'{label}: canonical/DOM mismatch ({"; ".join(detail)})')
    return issues


def scan_dom_record_parity(root: Path) -> list[str]:
    issues = []
    public = load_json(root / 'data/public-claims-current.json', [])
    tracks = load_json(root / 'data/arizona-track-census-r1.json', [])
    timeline = load_json(root / 'data/arizona-history-timeline-current.json', [])
    events = load_json(root / 'data/arizona-events-current.json', [])

    claim_actual = _ids_from_html(root / 'research/claims/index.html', r'data-claim-card\b[^>]*data-claim-id=["\']([^"\']+)["\']|data-claim-id=["\']([^"\']+)["\'][^>]*data-claim-card\b')
    claim_actual = [a or b for a, b in claim_actual]
    claim_expected = [str(r.get('claim_id')) for r in public if r.get('claim_id')]
    issues.extend(_compare_ids('public claim DOM IDs', claim_actual, claim_expected))

    track_raw = (root / 'atlas/index.html').read_text(encoding='utf-8', errors='ignore') if (root / 'atlas/index.html').exists() else ''
    track_actual = re.findall(r'<[^>]*data-track-card\b[^>]*id=["\']card-([^"\']+)["\']|<[^>]*id=["\']card-([^"\']+)["\'][^>]*data-track-card\b', track_raw, flags=re.I | re.S)
    track_actual = [a or b for a, b in track_actual]
    track_expected = [str(r.get('id')) for r in tracks if r.get('id')]
    issues.extend(_compare_ids('track DOM IDs', track_actual, track_expected))

    timeline_actual = _ids_from_html(root / 'atlas/timeline/index.html', r'<article\b[^>]*class=["\'][^"\']*chrono-item[^"\']*["\'][^>]*data-id=["\']([^"\']+)["\']|<article\b[^>]*data-id=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*chrono-item')
    timeline_actual = [a or b for a, b in timeline_actual]
    timeline_expected = [str(r.get('timeline_id')) for r in timeline if r.get('timeline_id')]
    issues.extend(_compare_ids('timeline DOM IDs', timeline_actual, timeline_expected))

    event_actual = _ids_from_html(root / 'atlas/events/index.html', r'<article\b[^>]*class=["\'][^"\']*event-card[^"\']*["\'][^>]*id=["\']([^"\']+)["\']|<article\b[^>]*id=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*event-card')
    event_actual = [a or b for a, b in event_actual]
    event_expected = [str(r.get('event_id')) for r in events if r.get('event_id')]
    issues.extend(_compare_ids('event DOM IDs', event_actual, event_expected))

    # Source Directory is source-centric but source IDs are assembled from
    # claim/supporting records, so count parity is the stable canonical gate.
    source_ids = set()
    for row in list(public) + list(load_json(root / 'data/supporting-evidence-current.json', [])):
        source_ids.update(row.get('source_ids', []))
    source_raw = (root / 'research/sources/index.html').read_text(encoding='utf-8', errors='ignore') if (root / 'research/sources/index.html').exists() else ''
    source_count = len(re.findall(r'data-source-card\b', source_raw, flags=re.I))
    if source_raw and source_count != len(source_ids):
        issues.append(f'source DOM count: {source_count} != canonical {len(source_ids)}')
    if source_raw:
        source_actual = []
        for tag in re.findall(r'<article\b[^>]*data-source-card\b[^>]*>|<article\b[^>]*data-search=["\'][^"\']+["\'][^>]*data-source-card\b[^>]*>', source_raw, flags=re.I | re.S):
            search_value = attr(tag, 'data-search') or ''
            m = re.search(r'\bAZ-(?:ATL-)?SRC-\d+\b', search_value, flags=re.I)
            if m:
                source_actual.append(m.group(0).upper())
        issues.extend(_compare_ids('source DOM IDs', source_actual, sorted(source_ids)))

    categories = root / 'research/categories/index.html'
    if categories.exists() and public:
        raw = categories.read_text(encoding='utf-8', errors='ignore')
        actual_categories = []
        for href in re.findall(r'href=["\']([^"\']*claims/index\.html\?[^"\']*category=[^"\']+)["\']', raw, flags=re.I):
            vals = parse_qs(urlsplit(href).query).get('category', [])
            if vals:
                actual_categories.append(vals[0])
        expected_categories = sorted({str(r.get('category')) for r in public if r.get('category')})
        issues.extend(_compare_ids('category DOM values', actual_categories, expected_categories))

    recovery = root / 'atlas/recovery/index.html'
    if recovery.exists():
        raw = recovery.read_text(encoding='utf-8', errors='ignore')
        card_tags = re.findall(r'<button\b[^>]*class=["\'][^"\']*\brecovery-card\b[^"\']*["\'][^>]*>', raw, flags=re.I | re.S)
        card_count = len(card_tags)
        m = re.search(r'<strong\b[^>]*data-count(?:=["\'][^"\']*["\'])?[^>]*>\s*(\d+)\s*</strong>', raw, flags=re.I | re.S)
        if m and int(m.group(1)) != card_count:
            issues.append(f'recovery displayed count: {m.group(1)} != recovery cards {card_count}')
        card_ids = [attr(tag, 'data-track') for tag in card_tags]
        card_ids = [x for x in card_ids if x]
        data_match = re.search(r'<script\b[^>]*id=["\']recoveryData["\'][^>]*>(.*?)</script>', raw, flags=re.I | re.S)
        if data_match:
            try:
                recovery_data = json.loads(unescape(data_match.group(1)))
            except json.JSONDecodeError:
                issues.append('recovery DOM IDs: embedded recoveryData is not valid JSON')
            else:
                expected_recovery = [str(r.get('id')) for r in recovery_data if r.get('id')]
                issues.extend(_compare_ids('recovery DOM IDs', card_ids, expected_recovery))
    return issues


def scan_runtime_language(root: Path) -> list[str]:
    issues = []
    for p in sorted(root.rglob('*.js')):
        rel = p.relative_to(root).as_posix()
        if not rel.startswith(PUBLIC_ROOTS):
            continue
        raw = p.read_text(encoding='utf-8', errors='ignore')
        for pattern in RUNTIME_PATTERNS:
            m = re.search(pattern, raw, flags=re.I)
            if m:
                snippet = raw[max(0, m.start()-60):m.end()+100].replace('\n', ' ')
                issues.append(f'{rel}: system-facing runtime language: {snippet}')
    return issues

def scan_site(root: Path, expected_version: str = '0.56.2') -> list[str]:
    root = Path(root).resolve()
    issues = []
    issues.extend(scan_claim_titles(root))
    issues.extend(scan_supporting_anchors(root))
    issues.extend(scan_fragments(root))
    issues.extend(scan_manifest_counts(root))
    issues.extend(scan_surface_counts(root, expected_version))
    issues.extend(scan_unpinned_routes(root))
    issues.extend(scan_atlas_all(root))
    issues.extend(scan_recovery_routes(root))
    issues.extend(scan_system_language(root))
    issues.extend(scan_dom_record_parity(root))
    issues.extend(scan_runtime_language(root))
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description='Arizona Connect release-integrity QA')
    ap.add_argument('root', nargs='?', default='.')
    ap.add_argument('--version', default='0.56.2')
    args = ap.parse_args()
    issues = scan_site(Path(args.root), expected_version=args.version)
    if issues:
        print(f'RELEASE INTEGRITY QA FAIL: {len(issues)} issue(s)')
        for issue in issues:
            print(f'- {issue}')
        return 1
    print('RELEASE INTEGRITY QA PASS: 0 issues')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
