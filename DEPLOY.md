# Arizona Connect v0.25 — Deployment Checklist

## Candidate

**Integrated product checkpoint:** v0.25

This package has passed static, cross-register, package-integrity, and prior component browser QA. Live publication remains a separate owner-controlled step.

## GitHub Pages

1. Create or choose the intended Arizona Connect repository.
2. Copy the complete contents of this folder to repository root.
3. Keep `.github/workflows/pages.yml` and `.nojekyll`.
4. In GitHub → Settings → Pages, select **GitHub Actions**.
5. Commit and push to `main` only when explicitly authorized.
6. Wait for the Pages deployment action to finish.
7. Run the live smoke test below before treating the URL as released.

## Required live smoke test

### Launcher
- Boot/wake completes.
- Arizona Research Register opens.
- Arizona BMX Atlas opens.
- Arizona BMX Hall of Fame opens as the external destination.
- Timeline entrance opens the Arizona BMX History Timeline.
- Resume remembers a previously opened internal app.
- Archive, YouTube, Spotify, Facebook, GitHub, and Donate destinations open correctly.
- Lititz BMX logo route returns to Connection: by Lititz BMX.

### Atlas
- Current, Historical, and Accessible List views work.
- All published map markers remain inside the Arizona boundary.
- Current / site-approximate / historical point distinctions are visible.
- A deliberately unpinned record stays unpinned.
- Track search and filters work.
- One current, one historical, and one recovery profile open correctly.

### Timeline / Relationships / Recovery / Methodology
- Timeline shows 33 published milestones by default and keeps 5 open questions opt-in.
- Date precision remains visible in Timeline drilldown.
- Black Mountain relationship view exposes only its admitted local edges.
- A zero-edge entity remains able to display zero edges without invented connections.
- Recovery search/filter works and does not create map points.
- Methodology links to the Research Register and Recovery Desk.

### Research Register
- 60 public claims are reachable.
- One Baseline A claim opens its claim record and governed source route.
- One Expansion 51–60 claim opens its claim record and governed source route.
- Evidence boundary, authority, and confidence remain visible.
- Correction route opens.

### Browser / device
- No console errors on launcher, Register, Atlas, representative track profile, Timeline, Relationships, Recovery, Methodology, Events, or Media.
- Phone portrait has no horizontal overflow.
- Desktop has no unintended horizontal overflow.
- Keyboard focus states work.
- Reduced-motion mode remains usable.

## PWA / cache state

The exact approved production Connection icon assets and service-worker architecture are present. v0.25 bumps the Arizona Connect service-worker cache key to force a clean integrated refresh while preserving the existing shell strategy.

## Release boundary

Deployment does not change evidence status. The product remains:

**ACTIVE HISTORICAL CENSUS — NOT COMPLETE**

No live release may be described as historically complete, Hall-of-Fame selection activity, or resolution of the governed OPEN lineage/location questions.
