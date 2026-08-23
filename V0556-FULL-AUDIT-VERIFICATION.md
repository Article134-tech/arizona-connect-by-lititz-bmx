# Arizona Connect v0.55.6 — Full Arizona Nexus / Presentation Integrity Verification

**Disposition:** STRUCTURAL / DATA / INTERACTION / PACKAGE-CANDIDATE PASS. HOSTED VISUAL SMOKE CHECK REMAINS REQUIRED.

## Public / supporting firewall

- **151** public Arizona claims.
- **33** supporting evidence records preserved separately rather than discarded.
- Every retained public claim contains a directly understandable Arizona BMX nexus in the claim wording itself.
- All **184** inherited claim IDs remain inspectable across the two layers.
- `AZ-PUB-0026` and `AZ-PUB-0029` received same-source wording refinements so their Arizona nexus is explicit; no source authority was expanded.
- `AZ-PUB-0081` joined the support-only layer after the full nexus sweep showed that its Federal Register sentence identifies the London Bridge BMX Association officer but does not itself establish the Arizona/Lake Havasu nexus.

## Timeline

- **77** published Arizona milestones.
- **4** open questions.
- **13** settled context-only chronology records preserved in the supporting Timeline archive and removed from the primary historical chronology.
- No settled primary Timeline record depends on a support-only claim.

## Navigation / interaction

- All **239** Research + Atlas HTML pages expose an explicit local **Arizona Connect Home** route.
- Sub-app logo/brand links no longer eject the user to the parent Lititz BMX Connection app.
- Whole-card interaction is retained for governed claim, supporting, category, source, track, event, media, Timeline and track-profile claim surfaces where a card has one primary destination.
- Long-list pagination is required and present on **7** surfaces: public claims, supporting evidence, categories, Source Directory, track explorer, Event Register and Recovery Register.
- Each paginated surface provides Previous / Next, numbered pages and `Showing X-Y of N` at the top and bottom.

## Source routing

- Claim-list and supporting-list source buttons are synchronized to the canonical claim-page source route.
- Verified claim-specific PDF page targets are propagated to track-profile evidence links when that source appears there.
- **60** PDF-like claim/source routes were reviewed: **57** deep-link to verified supporting pages.
- Three remain canonical-document-only because an exact physical page offset was not verified and was not guessed:
  - `AZ-PUB-0151` — CYMPO Prescott Valley study PDF.
  - `AZ-PUB-0165` — Arizona Memory Project Prescott Valley fact sheet viewer.
  - `AZ-PUB-0186` — Arizona Memory Project 2009 transportation study viewer.

## Presentation integrity corrections

- Removed the contaminated Research Register Home feature block that mixed Chandler, Roadrunner and unrelated evidence-boundary text.
- Category totals are recalculated from the 151-public-claim layer only.
- Source Directory now distinguishes public Arizona claim use from supporting-evidence use.
- Chandler profiles no longer contradict the resolved same-site continuity bridge; exact historical course geometry and organizational lineage remain separately bounded.
- Visible active release labels are synchronized to **v0.55.6**.

## Governed-data boundary

Relative to deployed v0.55.5, only two previously governed current-data files are intentionally changed:

- `data/public-claims-current.json` — public/support classification plus the two bounded Arizona-nexus wording refinements.
- `data/arizona-history-timeline-current.json` — primary/support chronology separation.

All other files covered by the inherited 92-file governed-data baseline are byte-identical. Geographic Absolute assets are byte-identical to the v0.55.5 baseline.

## Automated verification

- v0.55.6 release guard: **PASS**.
- Full-tree adversarial audit: **PASS — 11,111 assertions**.
- JavaScript syntax checked with Node across active product JavaScript.
- Every JSON file parses.
- Internal local links resolve.
- No duplicate HTML IDs found.
- New-tab links retain `rel="noopener"`.
- No stale v0.55.5 active UI labels, stale 184-public-claim presentation, or old Timeline/Relationships/Recovery/Event release labels remain in active product UI.

## Deployment package protocol

- The deployment ZIP contains **working-tree payload only**. Repository metadata (`.git`) is intentionally excluded.
- The existing clone's `.git` directory remains untouched during deployment.
- Deployment remains the established replace-matching-files workflow: select the entire extracted package payload, copy it into the repository root, and replace matching destination files.
- The package-root `SHA256SUMS.txt` covers every payload file except the ledger itself and contains no `.git` paths.

## Remaining gate

The hosted visual/mobile smoke test remains required after GitHub Pages deployment. It must specifically inspect launcher fit, Arizona Connect Home navigation, all pagination families, Source Directory public/support labels, Chandler profiles, representative supporting records, Timeline counts, and representative exact-page evidence links.
