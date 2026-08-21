# Arizona Connect v0.20 — Geographic Absolute Control

Date: 2026-08-20

## Owner requirement
Arizona geography is authoritative. The Atlas may not visually imply track locations outside Arizona or display neighboring-state geography as part of the Arizona location layer.

## Hard rules
- Arizona-only cartographic frame: no neighboring-state, Mexico, California, Nevada, Utah, New Mexico or other surrounding geography is displayed inside the location map.
- One projection for boundary and points.
- Geographic limits: N 37.3°, S 31.1°, W 115.0°, E 108.7°.
- Projection: equirectangular location-map frame with N/S stretching already embodied in the SVG geometry.
- Every rendered point comes only from the governed A4 location register.
- Exact points remain exact; site-approximate remains explicitly approximate; exact historical remains historical.
- Records without a defensible point remain unpinned.
- Every published point must pass a point-inside-Arizona mask test before packaging.

## Cartographic reference
Display geometry is derived from `USA Arizona location map.svg` by NordNordWest / Wikimedia Commons. The source documents explicit geographic limits and an equirectangular Arizona location-map projection and states that the map uses U.S. National Imagery and Mapping Agency, World Data Base II and U.S. Geological Survey data. The v0.20 derivative removes all surrounding geography and retains only the Arizona state shape plus a clipped one-degree geographic reference grid.

## v0.20 result
Mapped governed records: 12
Inside-Arizona checks passed: 12/12
Outside-Arizona mapped records: 0
Unpinned governed records: 13

This control is stricter than v0.19. Visual containment is not enough: marker coordinates and the displayed state boundary must share the same georeferenced frame.
