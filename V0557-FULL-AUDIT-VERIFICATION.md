# Arizona Connect v0.55.7 — Full Source Integrity / Mobile Layout Audit

**Disposition:** STRUCTURAL / SOURCE-ROUTING / PRESERVATION-METADATA / PACKAGE PASS. HOSTED VISUAL SMOKE CHECK REQUIRED.

## Corrections
- 42 / 42 track profiles: map explanatory caption moved out of the map image container into normal flow.
- 184 / 184 claim/supporting record pages: every source route explicitly labels its precision.
- Source-route registry: 207 rendered claim/source relationships.
  - 55 exact PDF page targets.
  - 16 exact text/section targets.
  - 136 honest page/document-level routes.
- Verified USA BMX section targeting added for Debbi Kalsow (4 records), Kim Hayashi (4 records), and Debbie Kelley / Black Mountain (5 records).
- Known precision-unresolved routes remain page-level rather than guessed: AZ-PUB-0151/AZ-SRC-0095, AZ-PUB-0165/AZ-SRC-0109, AZ-PUB-0186/AZ-SRC-0133.
- Fragile-source preservation registry: 8 source IDs supporting 10 single-source records. Preservation state remains **PENDING**; this public package does not republish full third-party source content.
- Mobile long-URL containment added for source cards/routes.
- Browse Claims and Atlas track-profile source links synchronized to the claim-specific target.

## Invariants
- 151 public Arizona claims.
- 33 supporting evidence records.
- 42 tracks — 11 current / 31 historical.
- 77 Timeline milestones + 4 open questions.
- 28 events; 17 relationships; 19 media routes.
- All inherited `data/` files are byte-identical to deployed v0.55.6. The only new data controls are `evidence-route-overrides-v0557.json` and `source-preservation-v0557.json`.
- Geographic Absolute SVG/mask are byte-identical to v0.55.6.

## Automated verification
- Focused regression audit: **976 / 976 PASS**.
- Full-tree adversarial audit: **6,387 / 6,387 PASS**.
- Public-facing HTML pages: **249**.
- JavaScript syntax: **11 / 11 PASS**.
- Duplicate HTML IDs: **0**.
- Broken internal links: **0**.
- Unsafe target-blank links: **0**.

## Hosted visual gate
After deployment, verify on mobile: Chandler/another track map caption sits below the image; Kalsow opens at her section; Hayashi and Kelley routes open at their sections; long Facebook URL remains contained; preservation record links render correctly.
