# Arizona Connect v0.22 — Relationship Explorer Recovery Control

## Purpose

Rebuild the Phase 7 relationship layer as a first-class Arizona BMX Atlas interface without changing the governed entity or relationship datasets.

## Locked evidence rules

- Governed entities remain **25**.
- Public relationship edges remain **15**.
- No new edge may be inferred from geography, reputation, chronology, naming similarity or visual proximity.
- Every rendered edge retains the governed relationship type, confidence, claim crosswalk and evidence boundary.
- Missing edges are not negative claims.
- Relationship direction is presentation of the governed `from` → `to` record, not automatic proof of ownership, causation or complete chronology.
- HIGH, HIGH RETROSPECTIVE, MEDIUM-HIGH and control/object states remain visually distinct.
- Track nodes retain direct links to the governed track profiles.
- Claim-linked edges retain direct routes into the Arizona Research Register.

## Presentation rule

The primary graph is local to the selected entity rather than a force-directed display of all 25 entities. This prevents screen proximity from being mistaken for a historical relationship. Only admitted edges touching the selected entity are drawn.

## Preservation boundary

This checkpoint changes only the Relationships presentation layer plus Relationships-specific CSS/JavaScript and documentation. The approved Arizona Connect home, Atlas home, v0.20 geographic-absolute system, v0.21 Timeline, track profiles, Research Register and all governed data remain unchanged.
