# Deploy — Arizona Connect v0.56.1

Full replacement release. This cumulative package contains Content Expansion 1 and Content Expansion 2 on the frozen v0.55.8 UX baseline. The deployment package excludes repository metadata. Use the established replacement protocol: extract the package, select everything in the package root, copy it into the existing repository root, and choose **Replace the files in the destination**. Do not manually delete repository files first.

Because v0.56.0 was continued into v0.56.1 before deployment, the verified GitHub Desktop gate is measured directly against the deployed v0.55.8 baseline. Do not commit if the delta differs from that release gate or shows any deleted files.

Hosted smoke test must verify the new content-growth surfaces without reopening the frozen v0.55.8 UX baseline: J&M BMX in Tempe, Holbrook/Navajo County chronology, Scottsdale site narrowing, Yuma legal/site context, updated counts and pagination, representative evidence routes, and Arizona Connect Home navigation.
