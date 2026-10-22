# Rebuilding from the source RPMs

The SRPM is the complete build input, not just a patch download. Start with a
fresh, disposable EL7 x86_64 builder. Do not build or fetch dependencies on a
production server. This is an EOL environment; isolate it accordingly.

The original builder used the amd64 Docker Official Image `centos` manifest
`sha256:dead07b4d8ed7e29e98de0f4504d87e8880d4347859d839686a31da35a3b532f`,
with rootless Docker, at most six CPUs, 10 GiB RAM and 512 PIDs. No privileged
mode, host network, Docker socket or host secrets were mounted. Compile as an
unprivileged UID, not container root. Network is needed only for authenticated
source/dependency retrieval and is disabled during compilation.

## Inputs and authentication

Authenticate the downloaded SRPM as described in INSTALL.md. Extract it into a
fresh topdir, without executing its scriptlets:

```sh
mkdir -p "$TOP"/{SOURCES,SPECS}
cd "$TOP/SOURCES"
rpm2cpio "$SRPM" | cpio -idm --no-absolute-filenames
mv php.spec ../SPECS/
```

Check the SRPM member list before extraction; reject absolute names, traversal
and unexpected members. `recipes/<family>/source-hashes.json` records the final
spec and source input hashes. Some entries are original recipe/reference files
not used by the spec; do not mistake them for missing active build inputs.
The exact final spec is also supplied under `recipes/<family>/SPECS/`.
`srpm-input-hashes.json` is the exact SRPM-member hash inventory; non-tarball
inputs are supplied under each recipe's `SOURCES/`. The larger
`source-hashes.json` also records historical reference files from the build tree.

Verify the upstream tarball's detached signature using the official PHP release
keys, matching fingerprints with <https://www.php.net/gpg-keys.php>:

| Version | Verified signing fingerprint |
| --- | --- |
| 7.4.33 | `5A52880781F755608BF815FC910DEB46F53EA312` |
| 8.1.29 | `39B641343D8C104B2B146DC3F9C39DC0B9698544` |
| 8.2.35 | `E60913E4DF209907D8E30D96659A97C9CF2A795A` |
| 8.3.36 | `4B1FC0D9DF92321CED9F615DBEC555E22A143553` |

The last entry is a signing subkey of
`AFD8691FDAEDF03BDF6E460563F15A9B715376CA`. The 8.1 historic signature is
valid but its key is now expired. Inspect the signature date and official key
history rather than suppressing the warning. Compare the source SHA-256 with
`provenance.json` and the official PHP release metadata. The latter records URLs
and original emergency patch hashes as well as pinned Remi recipe commits.

## Dependencies and build

Dependency inventories under `recipes/<family>/build-dependencies.txt` pin the
installed NEVRAs used for each build. Base repositories were HTTPS CentOS
7.9.2009 vault (os/updates/extras), archived Fedora EPEL 7 and Remi EL7
safe/main archives. Keep TLS verification and RPM GPG checking enabled.
Authenticate repository keys independently: Remi EL7
`1EE04CCE88A4AE4AA29A5DF5004E6F4700F97F56`; EPEL7
`91E97D7C4A5E96F17F3E888F6A2FAEA2352C64E5`. Use the CentOS base-image
distribution key for vault packages. No new yum repository server is supplied.

In that disposable builder only, install `rpm-build`, `yum-utils`,
`scl-utils-build`, `redhat-rpm-config`, GCC/G++, make, patch, tar and xz, and
resolve the final spec's BuildRequires with `yum-builddep`. SCL builds additionally
need their matching `php74-build`, `php81-build`, `php82-build` or `php83-build`
package; system PHP is unprefixed. Pass the same `scl` and `dist` definitions to
dependency resolution and rpmbuild. Compare every resolved NEVRA with the saved
inventory before proceeding: current archive contents are not assumed identical.

As the unprivileged builder, with network disabled:

```sh
# FAMILY is php74, php81, php82, php83 or php-system; TOP is an absolute topdir.
args=(--define "_topdir $TOP" --define 'dist .el7.remi'
      --define '_smp_mflags -j6' --define '_default_patch_fuzz 0')
if [ "$FAMILY" != php-system ]; then args+=(--define "scl $FAMILY"); fi
rpmbuild "${args[@]}" -bp "$TOP/SPECS/php.spec"
rpmbuild "${args[@]}" -bs "$TOP/SPECS/php.spec"
rpmbuild "${args[@]}" -ba "$TOP/SPECS/php.spec"
```

These command examples use Bash. Do not use short-circuit build stages or omit
the full patch-stack preparation. Record `%check` output separately: the vendor
spec masks failures, so the RPM exit code alone is insufficient. TESTING.md
records the original failures and follow-up dispositions. Re-run package,
module, FPM and exact-closure transaction checks before accepting a rebuild.

This is a source-reproducibility recipe, not a bit-for-bit reproducible-build
claim: timestamps, build host and signatures differ. Sign your own rebuilt RPMs
with your own independently managed key; no private signing key is distributed.
