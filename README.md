# Argo CD for srelens

Native, read-only srelens extension. This repository owns the manifest, tests,
documentation and independent releases. Discovery metadata lives in
[srelens/extensions](https://github.com/srelens/extensions).

## Preview compatibility

This initial version requires the extension-platform build from
[srelens PR #508](https://github.com/srelens/srelens/pull/508).
The exact tested host commit is recorded in `compatibility.json`; API requirement:
`^0.1`. Do not assume released app versions include this platform yet.
The Kubernetes controllers and matching CRDs must already be installed.

## Install

1. Download `manifest.json` and `SHA256SUMS` from this repository's release.
2. Verify with `sha256sum -c SHA256SUMS` (macOS: `shasum -a 256 -c SHA256SUMS`).
3. In the compatible desktop app, enable developer mode in Settings → Extensions.
4. Paste the manifest JSON, review its requested read permissions, and install.
5. Connect the desired cluster and open the extension's pages.

No Freelens archive, third-party renderer, or npm package is required. Checksums
verify file integrity; these preview manifests are unsigned. The app owns grant
review, credentials, settings persistence, rendering and lifecycle enforcement.
The catalog is not yet integrated into the app installer.

## Pages

- Applications

## Development

Use Python 3 and the Rust toolchain required by the pinned srelens checkout.
Clone `srelens/srelens` into `.host`, check out `hostRevision` from
`compatibility.json`, then run:

```sh
python3 -m unittest discover -s tests
python3 scripts/validate.py
python3 scripts/package.py --version 0.1.0
```

Validation uses the actual srelens manifest parser and capability broker. It
registers operations without querying a cluster. CI pins the host revision so an
upstream branch change cannot silently redefine compatibility. Update that pin
only after checking the new contract. Preserve the extension ID on updates.

## Releases

Increment the manifest version and changelog through a PR. Run the **Release
preview manifest** workflow with that version after validation. It publishes a
versioned manifest and checksums, then submit a separate catalog PR with the new
version, asset URL, checksum and tested host revision. Catalog inclusion grants
no permissions and may point to independently maintained community repositories.

## Next

Rich host-rendered details and guarded actions depend on additions to the native
srelens contract. See [ROADMAP.md](ROADMAP.md). This preview exposes reads only.

## Publisher signatures

Official releases include a detached Ed25519 signature, `manifest.json.sig`,
over the exact bytes of `manifest.json`. The public key is in
`signing-public.pem` and pinned in the srelens host. SHA256SUMS detects download
corruption; the signature authenticates the publisher. Installation still
requires explicit permission review.

The release workflow requires the repository secret `APP_SIGNING_PRIVATE_KEY`
(PKCS#8 PEM) and fails if it is absent or does not match the published key.
Never commit the private key. Rotate by publishing a host trust-key update
before releasing manifests signed by the replacement key.
