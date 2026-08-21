# Arizona Connect v0.15 — External Target Audit

**Audit date:** 2026-08-20
**Scope:** critical navigation and representative public-source routes.

## Critical destinations

- **Connection: by Lititz BMX** — VERIFIED IDENTITY / PRODUCTION REPOSITORY. Public GitHub repository exists and describes the mobile-first installable Connection environment, exact approved logo, responsive layouts, accessibility, reduced-motion support, and GitHub Pages deployment.
- **Lititz BMX Archive** — VERIFIED LIVE. `https://www.lititzbmx.com/` currently resolves to the Lititz BMX Google Sites archive.
- **Spotify** — VERIFIED ROUTE. The configured Fireside BMX Chat show route resolves.
- **GitHub / Article134-tech** — VERIFIED LIVE. The account currently exposes the Connection, Public Knowledge Register, Global BMX Research Atlas, Games, and sitemap repositories.
- **Arizona BMX Hall of Fame** — TARGET IDENTITY CORROBORATED. An independently indexed 2025 Arizona BMX Hall of Fame event explicitly publishes `www.azbmxhof.org/events/...` as its ticket/site route. Direct fetch was unavailable in this tool environment, so the final click remains a deployment smoke-test item; the URL was not substituted.
- **YouTube** — ROUTE CORROBORATED by the live Lititz BMX Archive, which publishes the exact `@LititzBMX17543` channel link. Direct crawler fetch was unavailable.
- **PayPal** — REDIRECT OBSERVED to PayPal's PayPalMe route; final browser click remains a deployment smoke-test item.
- **Facebook** — dynamic/social destination; final browser click remains a deployment smoke-test item.

## Representative research/source spot checks

Fresh public checks in the hardening pass confirmed:
- current Chandler BMX 2026 result pages at 298 S McQueen Rd;
- the 2020 USA BMX Western Region Top-10 page naming Chandler #3 and Black Mountain #4;
- the 2024 USA BMX Debbie Kelley/Pete Kelley/Black Mountain retrospective;
- the 2021 Arizona State Final Weekend schedule with Sports Park and Chandler dates.

## Release rule

A failed crawler fetch is not silently converted into a dead-link claim. Dynamic/social routes are explicitly left for the live deployment smoke test.
