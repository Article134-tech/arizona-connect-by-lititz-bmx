# Arizona Connect v0.39 — Archival-Site Recovery 2 Control

## Disposition

**RELEASE CANDIDATE — RC1. NOT SEALED.**

Structural/data state passes. The browser runtime gate cannot execute because the available Chromium runtime is intercepted by a mandatory organization policy before local Arizona Connect content loads.

## Governing decision

Continue from v0.38 RC1 without changing any inherited geography, track identity or lineage boundary. Resolve the actual dates and roles of the Randolph Park field-book leads, add the current City custody route, repair public count drift, and preserve the exact-course question as open.

## Evidence gained

- **Field Book 0174:** City of Tucson detail record identifies the Randolph Park “TOPOGRAPHY AND LAYOUT” book as **May 1, 1926**. It is older base geometry, not contemporaneous BMX evidence.
- **Field Book 0677:** City detail record identifies the Randolph Park “TOPOG, X-SECTIONS, BM CIRCUITS” pages as **January 1, 1951**. It is older survey geometry, not contemporaneous BMX evidence.
- **Field Book 1118:** City detail record identifies the **RANDOLPH PARK REC. CENTER SITE** survey as **June 1, 1966**, with preliminary, boundary and bench-circuit roles. This is a materially closer pre-BMX spatial-control record, but it still does not label a BMX course.
- **Current custody:** City PRO request **REQ-0723-04090**, completed July 27, 2023, states that files at 900 S Randolph Way are restricted and that historical Reid Park / Randolph Park / Reid Park Zoo plans and documents have been uploaded in OnBase.

## Evidence boundary

No admitted record labels the 1977 BMX dirt course, proves that the Recreation Center survey area was the BMX footprint, establishes one unchanged Randolph/Reid course through time, or supports an exact-course coordinate.

## Geographic Absolute

- All **40** inherited v0.38 location objects remain exactly equal.
- All **18** mapped records retain the same latitude, longitude and location-state values.
- **0** v0.39 coordinate admissions.
- **22** records remain intentionally unpinned.
- `data/arizona-location-register-a4.json`, `data/arizona-location-register-a4-r1.json`, `data/arizona-location-register-a4.csv`, `atlas/arizona-geographic-absolute.svg`, and `atlas/arizona-geographic-mask.png` remain byte-for-byte unchanged from v0.38 RC1.
- Locked launcher assets remain byte-for-byte unchanged.

## Surface reconciliation

v0.39 also repairs inherited presentation drift:

- Source Directory headline corrected from stale **98** to governed **108** source routes.
- Source Directory regenerated as **108 unique source-ID cards**; the five duplicated `AZ-ATL-SRC-*` cards are removed.
- Research Register metrics corrected to **162 public claims / 50 frozen baseline / 112 additive admitted / 108 source routes**.
- Atlas home Timeline metric corrected from stale **80** to governed **81** published milestones.
- All **162** claim pages retain exact rendered evidence-boundary parity with their governed JSON records.

## Runtime gate

A v0.39 local HTTP preflight was attempted in the installed managed Chromium runtime. Navigation was intercepted before product code loaded:

- resulting page: `chrome-error://chromewebdata/`
- page message: `127.0.0.1 is blocked — Your organization doesn’t allow you to view this site`
- network failure: `net::ERR_BLOCKED_BY_ADMINISTRATOR`

No policy was modified or bypassed. Runtime/visual pass remains **BLOCKED**, not failed.
