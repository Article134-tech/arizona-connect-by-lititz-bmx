# Arizona Connect v0.44 — Heritage Park Geographic Correction 1 Control

## Governing decision

Correct the inherited v0.35 Heritage Park BMX source-attribution error before further growth. Preserve the track identity, correct the directory city/contact evidence to Phoenix/Kathy Scott, reject the unrelated Prescott municipal-park bridge, and withdraw the Prescott geographic point.

## Evidence correction

- May 1985 BMX Action Arizona directory: **Phoenix, Heritage Park BMX — Kathy Scott — 602-861-6070 / 602-578-5620**.
- Recovered June 1985 BMX Plus! Arizona directory: Heritage Park BMX is not repeated; **Mesa BMX — Kathy Zosky and Debbie Cotton — 602-778-5629** appears instead.
- The v0.35 Prescott / Kathy Zosky / Debbie Cotton Heritage Park interpretation is therefore withdrawn.
- Arizona State Parks / City of Prescott Heritage Park records remain true Prescott municipal records but are rejected as site evidence for the Phoenix BMX identity.

## Geographic Absolute

- `AZ-TRK-0128` is the sole location-state change: `SITE_POINT_APPROXIMATE` → `CITY_ONLY_NO_POINT`.
- Withdrawn coordinate: `34.6133572, -112.4404465`.
- No Phoenix replacement point is admitted.
- All other 39 v0.43 location objects must remain exactly unchanged.
- Arizona SVG boundary and mask must remain byte-for-byte unchanged.

## Explicit non-findings

No exact Phoenix Heritage Park BMX site, operator/ownership role, opening/closing span, sanction continuity, or documented relationship to Desert Edge BMX, Roadrunner Raceway, or another Phoenix track is claimed.

## QA / runtime disposition

- Working-tree structural/data QA: **352/352 PASS**.
- Loopback HTTP serving: **PASS — HTTP 200**.
- Chromium runtime/visual gate: **OPEN / ENVIRONMENT BLOCKED**. The installed browser refuses root execution unless its sandbox is disabled. No sandbox, browser or network security control is weakened to force a pass.
- Release disposition: **RC1 — NOT SEALED** until browser/visual QA can run in an allowed environment.
