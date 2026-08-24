#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def baseline_digest(path: Path, mode: str = 'full') -> str:
    data = path.read_bytes()
    if mode == 'full':
        return _sha256_bytes(data)
    if mode == 'timeline_logic':
        text = data.decode('utf-8')
        replaced, n = re.subn(r'^const TIMELINE_DATA=\[.*?\];\n', 'const TIMELINE_DATA=[__CONTENT__];\n', text, count=1, flags=re.S)
        if n != 1:
            raise ValueError(f'{path}: TIMELINE_DATA block not found for timeline_logic mode')
        return _sha256_bytes(replaced.encode('utf-8'))
    raise ValueError(f'unsupported baseline mode: {mode}')


def verify_baseline(root: Path, manifest_path: Path, release: str | None = None) -> list[str]:
    root = Path(root)
    manifest_path = Path(manifest_path)
    payload = json.loads(manifest_path.read_text(encoding='utf-8'))
    issues: list[str] = []
    overrides = payload.get('authorized_overrides', {}).get(release, {}) if release else {}
    for rel, spec in payload.get('files', {}).items():
        if rel in overrides:
            spec = overrides[rel]
        path = root / rel
        if not path.is_file():
            issues.append(f'{rel}: missing frozen UX asset')
            continue
        if isinstance(spec, str):
            expected, mode = spec, 'full'
        else:
            expected = spec['sha256']
            mode = spec.get('mode', 'full')
        try:
            actual = baseline_digest(path, mode)
        except Exception as exc:
            issues.append(f'{rel}: baseline digest error: {exc}')
            continue
        if actual != expected:
            issues.append(f'{rel}: frozen UX asset changed ({actual} != {expected})')
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify Arizona Connect frozen UX baseline assets')
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--manifest', default='.github/qa/ux_baseline_v0558.json')
    parser.add_argument('--release', default=None, help='Apply explicitly authorized correction hashes for this release')
    args = parser.parse_args()
    root = Path(args.root)
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = root / manifest
    issues = verify_baseline(root, manifest, release=args.release)
    if issues:
        print(f'FROZEN UX BASELINE FAIL: {len(issues)} issue(s)')
        for issue in issues:
            print(f'- {issue}')
        return 1
    print('FROZEN UX BASELINE PASS: 0 changes to frozen interaction/style assets')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
