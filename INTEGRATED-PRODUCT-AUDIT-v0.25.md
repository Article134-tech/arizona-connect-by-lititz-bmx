# Arizona Connect v0.25 — Integrated Product Audit / Regroup

**Date:** 2026-08-20  
**Disposition:** **PASS — INTEGRATED PRODUCT BASELINE; LIVE DEPLOYMENT SMOKE TEST PENDING**

## Why this regroup happened

The interface recovery sequence had reached a natural stop point. Launcher, Atlas, track profiles, Timeline, Relationships, Recovery, and Methodology had each been repaired separately. v0.25 therefore audits them as one application before any deployment action.

## Governed state reconciled

- Track census: **25**
- Public claims: **60**
- Registered location records: **25**
- Published map points: **12**
- Intentionally unpinned: **13**
- Published Timeline milestones: **33**
- Optional open Timeline questions: **5**
- Event records: **11**
- Relationship entities: **25**
- Admitted relationship edges: **15**
- Media routes: **19**

## Cross-layer result

**PASS.** Timeline claim/track/event references resolve. Relationship endpoints and claim crosswalks resolve. Media track links resolve. All 25 governed track IDs have permanent track-profile routes. Atlas pins exactly match the records with registered coordinates.

## Geographic Absolute

**PASS.** The public Atlas publishes exactly the 12 records with registered A4 latitude/longitude. The other 13 records remain unpinned. No location record was added, moved, inferred, or promoted in v0.25.

## Navigation / static integrity

- HTML pages: **98**
- Broken local references: **0**
- Duplicate HTML IDs: **0**
- Images missing alt attributes: **0**
- Unsafe `target="_blank"` links: **0**
- Governed cross-register reference failures: **0**

## Drift found and corrected

The audit found **release-control drift, not research/product-architecture failure**:

1. Root launcher footer still displayed `Arizona Connect 0.16`.
2. Atlas footer still displayed `v0.17 interface recovery`.
3. README opened by describing the superseded one-profile v0.18 checkpoint.
4. `DEPLOY.md` still described the old v0.15 state and incorrectly said approved PWA assets still needed to be imported.
5. Service-worker cache key was still `v0.16-shell-recovery`, which could allow a previously visited origin to momentarily reuse stale component assets after a later deployment.

v0.25 corrects those five release/integration issues. **No research record, claim, coordinate, Timeline item, relationship, media record, profile evidence boundary, or approved primary visual layout was changed.**

## Supporting surfaces

Events and Media remain valid first-class supporting Atlas routes. They use the earlier Atlas-family presentation rather than the later hero treatment, but static navigation and governed counts reconcile and no product-breaking defect was found. This is not treated as a release blocker.

## Browser boundary

The immediately preceding component checkpoints include desktop/mobile browser QA for the newly recovered surfaces. The present environment blocks direct browser navigation by administrator policy, so v0.25 does not fabricate a new live-browser result. Because v0.25 changes only release text/documentation plus the service-worker cache key, the remaining browser requirement is the explicit **post-deployment live smoke test** in `DEPLOY.md`.

## Baseline decision

**v0.25 is the new integrated regroup baseline.**

Future work should be additive and evidence-driven. Do not reopen the approved launcher, Atlas geography, track-profile hierarchy, Timeline, Relationships, Recovery, or Methodology merely to make them look different.
