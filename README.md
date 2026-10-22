# EL7 emergency rebuilds for PHP

Independent GigaTux x86_64 RPM rebuilds derived from Remi packaging, prepared
on 21 October 2026 for CVE-2026-109618 and CVE-2026-109619. These are **not
official Remi or InterWorx packages**, and do not provide CentOS 7, RHEL 7 or
other end-of-life operating-system security support. They are a one-off emergency
bridge, not a maintained distribution or a promise of future fixes.

For the CentOS 7 stragglers: a little breathing room, not a reason to get comfortable.

| Existing package family | Source version | Scope | Published binary closure |
| --- | --- | --- | ---: |
| SCL `php74-php-*` | 7.4.33 | Two official emergency CVE backports; retained Remi patches | 19 |
| SCL `php81-php-*` | 8.1.29 | Two official emergency CVE backports; retained Remi patches | 17 |
| SCL `php82-php-*` | 8.2.35 | Complete upstream fixed same-minor release | 18 |
| SCL `php83-php-*` | 8.3.36 | Complete upstream fixed same-minor release | 18 |
| Unprefixed system `php-*` | 8.3.36 | Complete upstream fixed same-minor release | 13 |

PHP 7.4 and 8.1 remain EOL: these backports address **only these two CVEs**,
not every later vulnerability. The emergency backports disable session
upload-progress callbacks and deliberately hard-exit the worker on allocator
OOM, bypassing unsafe output/shutdown callbacks. Applications may observe an
aborted response and worker replacement. Do not restore that unsafe behaviour.

The release contains only the 85 binary RPMs in the tested existing-package
closures and their five complete source RPMs. Debug packages, unused SAPIs,
additional extensions and vendor panel RPMs are not included. Existing devel
packages occur in some tested closures; do not install new development packages
merely to match a list. The closure is not a universal dependency bundle: retain
and check the host's existing compatible external extensions and OS libraries.

See [INSTALL.md](INSTALL.md), [BUILD.md](BUILD.md), [PATCHES.md](PATCHES.md),
[TESTING.md](TESTING.md) and [LICENSING.md](LICENSING.md). Exact filenames,
sizes and SHA-256 hashes are in `release-assets.json`; source URLs, pinned recipe
commits and hashes are in `provenance.json` and `recipes/`.

New publication docs and the verifier are MIT-licensed, copyright 2026 GigaTux;
see `LICENSE` for the exact scope. Upstream code, patches, RPM components and
copied packaging keep their own licences and credits.

## Trust and scope

Signing-key fingerprint: **89D4 24E8 7773 D278 B864 19DB EFA7 C343 D46B D47D**.
The public-key file SHA-256 is
`0624b9a201588b3ae5fc291e23553e53527af2e0365e3dfeada34a134d907d5c`.
Authenticate this fingerprint through an independently trusted publication before
importing it. The historical key UID says “Local private build only - not Remi”;
it identifies the original build key, not an upstream or Remi endorsement.
The key expires on 22 October 2027 at 12:00:00 UTC; it is not a promise of ongoing maintenance.
RPM bytes and original signatures are unchanged.

`SHA256SUMS` is a new **subset** index with a detached RSA/SHA-256 signature.
Verify that signature using the independently authenticated public key; hashes
downloaded alongside packages are not authentication on their own. Original per-family
signed manifests are retained under `original-manifests/`; they also list
unpublished build outputs. Their signatures authenticate matching included RPMs,
but do not imply that every original output is available in this release.

Keep the `el7-php-security-rebuilds-20261021-publication.tar.gz` archive with the
RPMs: it contains the licences, notices, recipes and guidance that accompany this
distribution. Its checksum is in the signed release index. The archive omits
the index itself to avoid a self-referential checksum.

Testing was performed in a specific EL7 environment. Compatibility with every
CentOS 7/RHEL 7-derived host, third-party module or application is not asserted.
No warranty, vendor endorsement or continuing support is offered.

This product includes PHP software, freely available from
<http://www.php.net/software/>.
