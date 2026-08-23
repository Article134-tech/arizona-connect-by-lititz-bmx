# Deploy — Arizona Connect v0.55.6

Full replacement release. Preserve the repository `.git` directory and replace the working-tree payload with the verified v0.55.6 stage.

Expected current state after replacement is determined by diff against the deployed v0.55.5 tree; do not commit if unexpected deletions appear outside the governed replacement set.

Hosted smoke test must verify: launcher fit/version, Arizona Connect Home navigation on mobile, Research Register public/supporting split, pagination, Timeline counts, Chandler continuity wording, track-profile claim/source routes, and representative PDF deep links.
