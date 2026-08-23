# Deploy — Arizona Connect v0.55.5 Interaction / Pagination / Evidence Correction Audit

This package is a cumulative interface hotfix applied directly over the already-published **v0.55.4** tree. It does not replace or revise governed Arizona research data.

Hard gates:
- **184 governed public claims / 126 source routes** rendered.
- **42 tracks: 11 current / 31 historical / 0 leads**.
- **18 Geographic Absolute points / 24 intentionally unpinned**.
- All **92 `/data/` files** remain byte-identical to the v0.55.4 baseline.
- Geographic Absolute SVG, mask, coordinates and location states remain unchanged.
- Timeline: **90 milestones + 4 questions**.
- Events: **28**.
- Relationships: **17** across **29 governed entities**.
- Media routes: **19**.
- Root launcher visibly identifies **Arizona Connect 0.55.5** and includes the short-desktop viewport-fit correction.
- Whole governed track, Timeline, claim/category, event, media and track-profile claim tiles expose their primary drilldown across the tile surface while preserving nested links/buttons.
- Browse Claims paginates at **20 records per page** with Previous / Next, numbered pages and **Showing X–Y of N** status at the top and bottom; filtering recalculates pagination and resets to page 1.
- All **60 PDF-like claim/source relationships** are governed: **57** deep-link to verified physical supporting pages and **3** remain canonical-only because their physical PDF offsets could not be verified. No page number is guessed.
- Every public claim retains a source route and evidence boundary.
- Browser sandbox/security policy must not be weakened to manufacture a runtime pass.

Deployment protocol:
1. Apply the v0.55.5 hotfix contents directly over the published v0.55.4 repository tree.
2. GitHub Desktop must show **252 changed paths: 251 modified / 1 new / 0 deleted** before commit.
3. The sole new file is `atlas/tile-navigation.js`.
4. Commit and push only after the delta matches exactly.
5. After GitHub Pages deploys, perform the hosted visual/runtime smoke check listed in the companion verification report before calling the release final.

Recovery provenance remains inspectable in the dedicated control files and is not erased by presentation cleanup.
