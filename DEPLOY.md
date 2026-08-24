# Deploy — Arizona Connect v0.56.2

Full replacement correction release. This package starts from deployed v0.56.1 and preserves its research corpus while repairing release-integrity and visitor-facing defects. The deployment package excludes repository metadata. Use the established replacement protocol: extract the package, select everything in the package root, copy it into the existing repository root, and choose **Replace the files in the destination**. Do not manually delete repository files first.

The verified GitHub Desktop gate for this package is measured directly against deployed v0.56.1. Do not commit if the delta differs from that release gate or shows any deleted files.

Hosted smoke test must verify the corrected interaction paths without reopening the frozen v0.55.8 UX baseline: Atlas All/Current/Historical, an unpinned Track Explorer return, AZ-PUB-0207 title and ID links, a Supporting Evidence fragment, a track-specific Recovery route, Timeline drilldown, and Arizona Connect Home navigation.
