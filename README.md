# Argo CD for srelens

Native srelens extension with explicitly granted, host-confirmed GitOps actions. This repository owns the manifest, tests,
documentation and independent releases. Discovery metadata lives in
[srelens/extensions](https://github.com/srelens/extensions).

## Preview compatibility

This version requires the declarative action host from
[srelens #551](https://github.com/srelens/srelens/issues/551), extension API `^0.3`.
The exact tested host commit is recorded in `compatibility.json`. Earlier API
hosts cannot install this version; no compatibility alias is provided.
The Kubernetes controllers and matching CRDs must already be installed.

## Install

Once this version is published in the catalog, install it through a compatible
host's app catalog. Review the requested read and write grants before installing
or updating. Connect the desired cluster and open the extension's pages.

Official release assets include `manifest.json`, its detached Ed25519 signature
`manifest.json.sig`, and `SHA256SUMS`. The host verifies the publisher and retains
control of grants, cluster scope, credentials, rendering and mutation confirmation.
Reading a kind does not implicitly authorize writes; each declared action needs
its primitive's explicit grant, and each mutation uses the host confirmation.

## Pages

- Applications

## Development

Use Python 3 and the Rust toolchain required by the pinned srelens checkout.
Clone `srelens/srelens` into `.host`, check out `hostRevision` from
`compatibility.json`, then run:

```sh
python3 -m unittest discover -s tests
python3 scripts/validate.py
python3 scripts/package.py --version 0.3.1
```

Validation uses the actual srelens manifest parser and capability broker. It
registers operations without querying a cluster. CI pins the host revision so an
upstream branch change cannot silently redefine compatibility. Update that pin
only after checking the new contract. Preserve the extension ID on updates.

## Releases

Increment the manifest version and changelog. Run the **Release signed app
package** workflow with that version after validation. It publishes a signed
manifest and `.srelens-extension` package containing the official logo, with
checksums. Update the signed catalog with the version, manifest/package asset
URLs and checksums, and the tested host revision. Catalog inclusion grants
no permissions and may point to independently maintained community repositories.

## Declared actions

Refresh status, Hard refresh and Sync are declared for Applications. Sync is
refused while an operation is already present, never enables pruning, and uses
the hook strategy rather than replacement.

Availability is shown before confirmation; the host rechecks preconditions and
reviewed resource identity before writing. This manifest cannot execute arbitrary
code or change the host guards.

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

The signed `.srelens-extension` package includes the official Argo CD icon from [CNCF artwork](https://github.com/cncf/artwork/tree/main/projects/argo/icon/color). Project names and logos belong to their respective owners. Updating from a manifest-only installation installs the packaged logo.
