# Arizona Connect v0.55.8 — End-User QA Control

## Purpose
v0.55.8 adds an explicit visitor-experience release gate. Public pages must present Arizona BMX history, evidence, uncertainty and source routes without narrating the underlying database architecture to the visitor.

## Standing visitor rules
- A first-time visitor should understand what a page is for without developer explanation.
- Deep pages must expose a clear Arizona Connect Home route.
- Interactive cards and titles must behave as their appearance suggests.
- Long lists require pagination and range status.
- Source links must accurately describe their precision: exact page/section when verified, page/document level when not.
- Evidence limits remain visible, but internal release mechanics such as Admission PASS are not public-facing content.
- Supporting evidence remains available without being presented as a standalone Arizona BMX claim.
- Mobile layouts must avoid text/image overlap, horizontal overflow and unusable tap targets.
- Version labels must match the deployed build.

## v0.55.8 presentation changes
- Removed the “HOW THIS PROFILE WORKS / One track record…” explainer block from all 42 track profiles.
- Replaced track-profile system labels such as RECORD BOUNDARY, RECOVERY CONTROL, OPEN LINEAGE CONTROL and CORRECTION PATHWAY with visitor language.
- Removed Admission PASS from all public/supporting claim detail pages while preserving evidence type, source class and confidence.
- Simplified Atlas, Timeline, Events, Relationships, Recovery, Media and Research Register landing copy where it described internal layers, crosswalks, gates or record mechanics rather than the history.
- Preserved claim text, evidence limits, source URLs, source precision labels, preservation states, coordinates and governed data.

## Automated release gate
`.github/qa/end_user_qa.py` runs in GitHub Actions before the Pages artifact is uploaded. Its unit tests run immediately before the site scan.

The gate blocks known visitor-facing regressions including:
- the removed track-profile explainer block;
- Admission PASS on claim pages;
- stale public version labels;
- missing Arizona Connect Home routes on deep public pages;
- system-facing track-claim summaries;
- selected internal metric labels on primary public surfaces.
