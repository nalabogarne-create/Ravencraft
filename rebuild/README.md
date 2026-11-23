# Ravencraft — realistic scene rebuild

This is an isolated development branch. The public game on main remains unchanged.

## Direction

Replace the primitive bedroom with a coherent PBR environment, not more procedural geometry. First two confirmed CC0 models: Gothic Bed 01 and Gothic Cabinet 01 from Poly Haven. Each model must be downloaded, inspected and hosted in this repository before being referenced by the game. No speculative third-party hotlinks.

## Acceptance tests

1. Both actual GLB files are stored at their local paths and load without CORS or 404 errors.
2. Imported models replace the old meshes instead of overlapping them.
3. Proper lighting makes wood grain and carved surfaces visible on Android.
4. Player controls, hugs, and collision checks remain functional.
5. Compare a phone screenshot against the desired IMVU-style reference before merging.

## Next implementation

Build a separate preview scene on this branch with a real PBR floor, lighting, and the two GLBs. Only merge into main after the user verifies screenshots. The old geometric fireplace must not be presented as an imported model.
