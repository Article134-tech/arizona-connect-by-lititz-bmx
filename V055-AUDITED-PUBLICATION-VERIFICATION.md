# Arizona Connect v0.55 — Audited Publication Verification

**Release posture:** Audited publication candidate. Public-facing release state is separated from recovery provenance. Reserved legacy claim slots remain absent rather than reconstructed without evidence.

## Governed public state
- 184 publishable public claims
- 126 governed source IDs used by published claims
- 42 tracks — 11 current / 31 historical / 0 discovery leads
- 90 published Timeline milestones + 4 open research questions
- 28 events
- 17 evidence-bounded relationships
- 29 relationship-graph entities
- 19 media routes
- 18 mapped / 24 intentionally unpinned location records

## Adversarial release audit
- 43 / 43 PASS
- Public release identity/count parity: PASS
- Claim/source/track crosswalk parity: PASS
- Outer Limits historical/corroboration-open parity: PASS
- Current Recovery questions Q002–Q005 only: PASS
- No internal recovery/HOLD incident language in public HTML: PASS
- Reserved legacy claim routes AZ-PUB-0182–0184 absent: PASS

## Structural audit
- 16 / 16 PASS
- JSON parsing: PASS (93 files at audit time before this report was added)
- Local HTML links: PASS (239 pages, zero broken)
- Duplicate HTML IDs: zero
- Images missing alt attributes: zero
- target=_blank links missing noopener: zero
- Governed claim/track/entity/relationship/timeline references: resolved
- 42 permanent track profiles: present
- Relationship endpoints: all 17 resolve through 29 graph entities
- Relationship filters: all 14 governed relationship types exposed
- Geographic register: 42 / 18 mapped / 24 unpinned
- Mapped-coordinate Arizona range sanity: PASS

## JavaScript
- 9 / 9 JavaScript files pass `node --check`.

## HTTP smoke test
The following key routes returned HTTP 200 from a local static server:
- `/index.html`
- `/research/index.html`
- `/research/claims/AZ-PUB-0018/index.html` (Debbi Kalsow)
- `/research/claims/AZ-PUB-0185/index.html` (Scottsdale spatial witness)
- `/research/claims/AZ-PUB-0186/index.html` (Manzanita / Desert Sunset distinct facilities)
- `/research/claims/AZ-PUB-0187/index.html` (Coppertown / Barbara Hagan)
- `/atlas/index.html`
- `/atlas/relationships/index.html`
- `/atlas/recovery/index.html`
- `/atlas/timeline/index.html`
- `/atlas/tracks/AZ-TRK-0114/index.html` (Outer Limits)
- `/atlas/tracks/AZ-TRK-0007/index.html` (Lake Havasu City BMX)
- `/atlas/tracks/AZ-TRK-0111/index.html` (SARA Park BMX Raceway)

## Live-source adversarial spot checks — 2026-08-22
- Debbi Kalsow: official USA BMX 2018 Hall of Fame page supports the governed 1982 ABA National No.1 Girl wording and explicitly says 1982 was the first year ABA added that girls National No.1 title. Boundary remains ABA-specific.
  Source: https://www.usabmx.com/news-and-media/6/2018-07-11/National-BMX-Hall-of-Fame---Class-of-2018?id=1610
- Scottsdale: BMX Plus! June 1987 directly reports the Scottsdale jail was across the street from the Scottsdale Jaycees Rodeo BMX Park. No coordinate/site-boundary inference is added.
  Source: https://previouspage.co.uk/magazines/BMX%20Plus/issues/242-june-nineteen-eighty-seven
- Tucson: Pascua Yaqui Tribe Small Area Transportation Study maps Desert Sunset BMX and Manzanita Park BMX separately; contemporaneous Tucson cycling inventory separately lists Manzanita BMX Raceway and Desert Sunset BMX Track with different recurring race nights. No lineage/ownership/coordinate inference is added.
  Sources: https://azmemory.azlibrary.gov/assets/displaypdf/97028 ; https://www.bicycletucson.com/wp-content/uploads/2011/08/ECON_LIST_TucsonVelo.pdf
- Coppertown: Copper Basin News, March 12, 2025, states Barbara Lynn Hagan ran Granny's Snack Shack at the Coppertown BMX track. No date of operation, BMX ownership, sanction chronology, or exact-site inference is added.
  Source: https://copperarea.com/wp-content/uploads/3_12_25-Copper-Basin-News.pdf

## Visual/runtime boundary
A sandbox-intact Chromium render was attempted in the available container environment. Chromium hung before a reliable visual result could be produced. Browser security was not weakened and `--no-sandbox` was not used. Therefore the rendered visual gate is **UNAVAILABLE IN THIS ENVIRONMENT**, not PASS and not FAIL.

Before broad external announcement, perform one hosted GitHub Pages visual smoke check of the launcher, Research Register, Debbi claim page, Atlas, Relationships, Recovery, Timeline, Outer Limits profile, Lake Havasu City profile, and SARA Park profile.

## Release decision
No known governed-data, graph-reference, stale-count, public-label, local-link, or package-integrity blocker remains after the expanded static audit. The only unproven release gate is rendered visual inspection in this environment.
