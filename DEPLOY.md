# Deploy — Arizona Connect v0.55.7

Full replacement release. Preserve the repository `.git` directory and replace the working-tree payload with the verified v0.55.7 stage.

Expected current state after replacement is determined by diff against the deployed v0.55.6 tree; do not commit if unexpected deletions appear outside the governed replacement set.

Hosted smoke test must verify: launcher fit/version, Arizona Connect Home navigation on mobile, track-profile map-caption flow, long source URL containment, Debbi Kalsow/Kim Hayashi/Debbie Kelley exact-section routing, preservation-record links for fragile sources, pagination, and representative PDF deep links.
