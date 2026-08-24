# Deploy — Arizona Connect v0.55.8

Full replacement release. Preserve the repository `.git` directory and replace the working-tree payload with the verified v0.55.8 stage.

Expected current state after replacement is determined by diff against the deployed v0.55.7 tree; do not commit if unexpected deletions appear outside the governed replacement set.

Hosted smoke test must verify: launcher fit/version, Arizona Connect Home navigation on mobile, representative track profiles after removal of developer-facing explainer blocks, claim-page metadata without Admission PASS, map-caption flow, source routing/preservation controls, pagination, and representative PDF deep links.
