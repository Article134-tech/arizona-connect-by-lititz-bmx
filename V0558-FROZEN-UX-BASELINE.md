# Arizona Connect v0.55.8 — Frozen UX Baseline

## Governing rule
v0.55.8 is the frozen user-experience baseline for Arizona Connect content-growth releases. Ordinary v0.56.x growth may add or deepen governed content but may not alter the frozen interaction/style assets without an explicit UX hotfix decision.

## Automated control
`.github/qa/ux_baseline_v0558.json` records SHA-256 controls for 19 interaction/style assets. `timeline.js` is checked in `timeline_logic` mode so the governed chronology data block may grow while the frozen timeline behavior remains unchanged. GitHub Pages deployment runs this guard before deployment.

## Content-growth invariants
- Geographic Absolute remains separately governed.
- Public claims require an independently understandable Arizona BMX nexus.
- Supporting evidence remains separate from public claims.
- Existing end-user QA, navigation, pagination and evidence-route precision requirements remain release gates.
- Content growth does not authorize silent UX redesign.
