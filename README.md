# Arizona Connect by Lititz BMX — v0.56.1

## Current release

Content Expansion 2 on the frozen v0.55.8 UX baseline.

- 173 public Arizona claims
- 33 supporting evidence records preserved separately
- 43 track records — 11 current / 32 historical
- 83 published Timeline milestones + 4 open questions
- 30 event records
- 17 evidence-bounded relationships
- 135 governed source IDs
- 18 mapped / 25 intentionally unpinned
- Geographic Absolute existing coordinates unchanged; J&M BMX enters as CITY_ONLY_NO_POINT

Release rule: a public claim must be independently understandable as an Arizona BMX fact. National/out-of-state chronology and recovery/spatial context remain inspectable as supporting evidence rather than inflating the public claim register.
## Presentation / interaction gates

- Every Arizona subpage exposes an explicit **Arizona Connect Home** route; sub-app logos return to Arizona Connect rather than ejecting to the parent Lititz BMX Connection app.
- Long public lists are paginated with **Previous / Next, numbered pages, and Showing X-Y of N at top and bottom**: public claims, supporting evidence, categories, source directory, track explorer, event register, and recovery register.
- Governed track/event/claim/source tiles use whole-card primary interaction while preserving visible links and keyboard access.
- Claim-specific source routes distinguish EXACT PAGE/SECTION TARGETS from PAGE-LEVEL SOURCES. Verified USA BMX text-fragment targets are used for the Debbi Kalsow, Kim Hayashi and Debbie Kelley shared Hall of Fame articles. No page number or section target is invented.
- Fragile single-source routes are registered in a preservation queue with explicit custody/republication boundaries; no full third-party source content is republished by this public package.
- Track-profile map captions flow beneath the map on mobile instead of overlaying the image; long source URLs wrap inside their cards.
- Source Directory distinguishes public Arizona claim usage from supporting-evidence usage.


- Public presentation copy is screened for developer/data-model narration before Pages deployment; the automated end-user QA gate runs in GitHub Actions.
