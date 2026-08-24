#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from html import unescape
from pathlib import Path

FORBIDDEN_EXACT = (
    'HOW THIS PROFILE WORKS',
    'One track record. Every claim still leads back to evidence.',
    'Public and supporting layers remain separate.',
    'RECORD BOUNDARY',
    'RECOVERY CONTROL',
    'OPEN LINEAGE CONTROL',
    'CORRECTION PATHWAY',
    'The record is allowed to improve.',
    'Distinct original routes',
)

PUBLIC_HTML_PREFIXES = ('atlas/', 'research/')


def visibleish_text(raw: str) -> str:
    raw = re.sub(r'<script\b[^>]*>.*?</script>', ' ', raw, flags=re.I | re.S)
    raw = re.sub(r'<style\b[^>]*>.*?</style>', ' ', raw, flags=re.I | re.S)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    return ' '.join(unescape(raw).split())


def is_deep_public_html(rel: str) -> bool:
    return rel.endswith('.html') and rel.startswith(PUBLIC_HTML_PREFIXES) and rel.count('/') >= 2


def scan_site(root: Path, expected_version: str = '0.55.8') -> list[str]:
    root = Path(root)
    issues: list[str] = []
    for path in sorted(root.rglob('*.html')):
        rel = path.relative_to(root).as_posix()
        raw = path.read_text(encoding='utf-8', errors='ignore')
        text = visibleish_text(raw)

        if rel.startswith('atlas/tracks/'):
            for phrase in FORBIDDEN_EXACT:
                if phrase.lower() in text.lower():
                    issues.append(f'{rel}: forbidden visitor-facing phrase: {phrase}')
            if 'tp-evidence-flow' in raw:
                issues.append(f'{rel}: forbidden visitor-facing component: tp-evidence-flow')
            if re.search(r'governed public claims? currently connect to this profile|admitted Research Register record', text, flags=re.I):
                issues.append(f'{rel}: system-facing track claims summary')

        if rel in {'atlas/events/index.html', 'atlas/media/index.html', 'atlas/index.html'}:
            if re.search(r'>[^<]*Governed (?:events|media routes|census records)[^<]*<', raw, flags=re.I):
                issues.append(f'{rel}: internal metric label uses Governed')

        if rel.startswith('research/claims/') and rel != 'research/claims/index.html':
            if re.search(r'Admission\s+PASS', text, flags=re.I):
                issues.append(f'{rel}: public claim metadata exposes Admission PASS')

        if is_deep_public_html(rel) and 'Arizona Connect Home' not in text:
            issues.append(f'{rel}: missing Arizona Connect Home route')

        if expected_version and '0.55.7' in text:
            issues.append(f'{rel}: stale version 0.55.7; expected {expected_version}')

    root_index = root / 'index.html'
    if root_index.exists() and expected_version:
        text = visibleish_text(root_index.read_text(encoding='utf-8', errors='ignore'))
        if f'Arizona Connect {expected_version}' not in text:
            issues.append(f'index.html: public version label is not Arizona Connect {expected_version}')
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description='Arizona Connect end-user QA release gate')
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--version', default='0.55.8')
    args = parser.parse_args()
    issues = scan_site(Path(args.root), expected_version=args.version)
    if issues:
        print(f'END-USER QA FAIL: {len(issues)} issue(s)')
        for issue in issues:
            print(f'- {issue}')
        return 1
    print('END-USER QA PASS: 0 issues')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
