# Arizona Connect v0.38 — Archival-Site Recovery 1 Control

**Disposition: RELEASE CANDIDATE — NOT SEALED**

## Governing decision

Continue from sealed v0.37 without changing any inherited location object, mapped coordinate, location-state value, Arizona boundary asset or launcher asset. v0.38 converts the highest-priority Reid/Randolph questions into explicit municipal and archival retrieval routes and adds bounded Old Home Manor municipal-property context. No recovered source reaches the course-level geography threshold.

## Evidence gained

- **AZ-PUB-0153 / AZ-SRC-0097 — City of Tucson 1977 Class C custody route.** The City catalog states that 1977 Class C building records, including parks buildings and recreation centers, are generally no longer held at Maps and Records and are instead at the City Architect's Office at the Thomas O. Price Service Center. This is an archival-custody instruction only; it does not prove a Randolph Park BMX drawing exists there.
- **AZ-PUB-0154 / AZ-SRC-0098 — Randolph Park field-book targets.** The City index identifies Randolph Park records in T14S R14E Section 16, including book 0174 “TOPOGRAPHY AND LAYOUT” and book 0677 pages 35–79 “TOPOG, X-SECTIONS, BM CIRCUITS.” The index does not label BMX or date a dirt-course footprint.
- **AZ-PUB-0155 / AZ-SRC-0099 — University of Arizona near-period aerial holdings.** The holdings guide lists Tucson aerial sets for 1974, 1978, 1979–1980 and 1980. No image from those sets is admitted here as course evidence.
- **AZ-PUB-0156 / AZ-SRC-0100 — Pima County section-indexed aerial route.** The county archive provides selected approximately 1979–2002 aerial imagery with township/range/section lookup. Coverage begins after the attributed 1977 Randolph Park BMX evidence; no section image is used to move the point.
- **AZ-PUB-0157 / AZ-SRC-0101 — Old Home Manor municipal chronology.** Chino Valley's adopted General Plan states that the Town acquired the more-than-800-acre Old Home Manor property in 1979. BMX activity is not backdated to the acquisition.
- **AZ-PUB-0158 / AZ-SRC-0102 — Old Home Manor property geometry.** The Town's water master plan constrains the modern property area and publishes a whole-property centroid. It does not identify the unnamed BMX track documented in the separate 2009 witness.

## Geographic Absolute

- All **40** v0.37 location-register objects remain exactly unchanged.
- All **18** mapped coordinate/state records remain unchanged.
- New v0.38 points: **0**.
- `data/arizona-location-register-a4.json`, `data/arizona-location-register-a4-r1.json` and `data/arizona-location-register-a4.csv` remain byte-identical to v0.37.
- `atlas/arizona-geographic-absolute.svg` and `atlas/arizona-geographic-mask.png` remain byte-identical to v0.37.
- Reid Park remains at its existing park-property **SITE_POINT_APPROXIMATE**. No bandshell-sector promotion is made.

## Surface repair

The v0.38 audit found that claim pages `AZ-PUB-0139` through `AZ-PUB-0152` had inherited one Heritage Park evidence-boundary paragraph despite correct governed JSON. All 14 pages were regenerated from their own governed records. The release gate now compares every rendered claim boundary against the corresponding JSON value; current result is **158/158 exact parity**.

The same reconciliation pass corrected stale current-state values in `README.md` and `manifest.json`; current public and machine-readable release metrics now agree.

## Runtime gate

Structural/data QA is **53/53 PASS**. Runtime/visual browser QA is **not satisfied** in this execution environment because the only installed Chromium is governed by a mandatory enterprise `URLBlocklist=["*"]`. Both local `file://` and local HTTP test routes return `net::ERR_BLOCKED_BY_ADMINISTRATOR` before Arizona Connect is loaded. The system policy is not modified or bypassed.

v0.38 therefore remains a **release candidate**, not a sealed release, until the same candidate bytes can be rendered in an environment where the local package is permitted to load.
