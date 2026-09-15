# 0.2.0 — detail links

Renamed the `rowActions` contribution to `detailLinks`, the read-only links in a resource's detail view
([srelens#537](https://github.com/srelens/srelens/issues/537)). Validated against srelens commit `5360059fee16560d33c05e742a95b3b64421602c`.
A host without the rename refuses this manifest, and a host with it refuses 0.1.0. There is no alias:
no extension had gone live.

# 0.1.0 — initial native preview

Extracted the existing native Argo CD manifest from srelens commit `29ef2ea1ce3327fd67e9d21980878653e04fe422`.
Requires the PR #508 extension-platform build; read-only and unsigned.
