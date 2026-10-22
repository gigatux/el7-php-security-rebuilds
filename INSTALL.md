# Installation: select the existing family, not every asset

This is an administrator-reviewed emergency transaction, not a general `yum
update`. First record installed RPM NEVRAs, enabled extensions, service units and
the current FPM/Apache configuration. Back up configuration and arrange a tested
snapshot or your own authenticated old RPM closure for rollback. Old vulnerable
vendor rollback sets are deliberately not redistributed here.

1. Choose exactly ONE existing package family from `release-assets.json`. SCL
   paths and units are separate from unprefixed system PHP; do not substitute one
   for another. Select its exact installed companion-package closure, preserving
   same-EVR requirements. Do not add unused SAPIs/devel packages. If the host
   needs an unpublished companion RPM, stop: this release is not its closure.
2. Verify the public-key fingerprint independently before trust. In a disposable
   GnuPG home, import the supplied public key and verify the corresponding
   `original-manifests/<family>/SHA256SUMS.asc` against `SHA256SUMS`. Check each
   selected filename's hash against that authenticated original manifest. The
   original manifest has extra entries: missing unpublished entries are not a
   reason to skip checking the files you will install. Also check the release
   subset index, authenticating its detached signature when supplied.
3. With the trusted key imported into the appropriate RPM database, run
   `rpmkeys --checksig --verbose` on every explicitly selected RPM. Require valid
   signatures and digests, not `NOKEY`. Never disable GPG or digest checking.
   Source rebuilders must authenticate the PHP upstream tarball signatures too;
   see BUILD.md and provenance.json.
4. On a disposable clone of the host first, preview the exact explicit file list
   with `rpm -Uvh --test <selected-RPM-files>`. Inspect dependencies, conflicts,
   scriptlets (`rpm -qp --scripts <file>`) and exact EVR coupling. Do not accept
   automatic OS-library upgrades, unexpected package additions or missing
   extension dependencies. Repeat the preview on the target before any install.
5. Arrange a maintenance window: RPM scriptlets can restart FPM. Validate all
   affected FPM configurations and, for unprefixed mod_php, Apache configuration.
   Apply only the reviewed explicit transaction; restart only the exact affected
   units when needed. Do not run a broad service restart or broad `yum update`.
6. Confirm RPM versions and verification, CLI and loaded modules, actual FPM
   pool configurations, application health, sessions/uploads, and worker recovery
   after failures. A clean CLI check is not an application acceptance test.

Rollback is another exact reviewed transaction using your saved old packages or
snapshot, configuration and dependency closure. Preview downgrade dependencies
and service effects before executing; remember rollback restores vulnerabilities.
If the preview cannot resolve without unrelated upgrades, stop rather than
bypassing package safeguards.
