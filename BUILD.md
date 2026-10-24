# Rebuilding the candidate

Use the complete source RPM and exact expanded recipe, not an old EL7 spec with
a selection of newer CVE patches. `recipes/<family>/srpm-input-hashes.json` lists
the precise source members. SHA-256 values authenticate bytes only after the
corresponding signing identity and signature have been verified.

The repository and lean recipe archive deliberately omit raw upstream tarballs:
they already exist inside each matching complete signed SRPM. The complete
`srpm-input-hashes.json` includes those members; `source-hashes.json` lists only
the files expanded in the repository. Do not copy the lean tree into an empty
topdir and assume it contains an upstream archive.

Select the family's exact source RPM from `release-assets.json`, authenticate
its signing identity and native RPM signatures, and inspect `rpm2cpio "$SRPM" |
cpio -itv` before extraction. Require unique flat regular member names, with no
absolute paths, traversal or links. In a fresh disposable topdir's SOURCES
directory, extract with `rpm2cpio "$SRPM" | cpio -idm --no-absolute-filenames`,
move `php.spec` into SPECS, and check **every** member (including its upstream
tarball) against `srpm-input-hashes.json`. This reconstructs the exact complete
inputs for the commands below. Alternatively rebuild the authenticated complete
SRPM directly with the same family/dist definitions and pinned dependencies.
Do not substitute a newly downloaded archive without matching its recorded hash.

## Input authentication

Current Remi source RPMs use Ed25519 key
`2E375FE24EDFF0F2E0D8E165ED5B58C5BEFA00E2`, independently matched to the official
Remi homepage and KEYS.txt. Native EL7 RPM 4.11 cannot import this key. The two
pinned vendor SRPMs passed stock RPM 6.0.2 in the official maintained image
`fedora@sha256:43b29f65a41eb9c35e1cd5323e3bdf3b655c2357a9f4f1ff2f9c2798e5045d80`:
fresh key database, only that fingerprint, network disabled, read-only inputs.
Both signature, signed-header SHA-256 and payload SHA-256 checks passed. A
single-byte payload-corrupted copy was rejected despite its valid header.

PHP 7.4.33's upstream RSA signature verifies with official historical key
`5A52880781F755608BF815FC910DEB46F53EA312` and was made while valid.

**PHP 8.1.34 direct-upstream signature verification is unsatisfied.** Its
16 December 2025 signature uses Ben Ramsey's key
`39B641343D8C104B2B146DC3F9C39DC0B9698544`, published as expiring 24 November
2025: signing occurred after expiry. Fresh official keyring/signature retrieval
did not cure this. No expiry flag was suppressed and no historical-validity
claim is made. Accepted source provenance is instead the fully verified current
Remi SRPM authenticating the exact archive, whose SHA-256 independently matches
official PHP HTTPS release metadata. `provenance.json` records the chain.

Our output RPMs use a different RSA/SHA-256 key and pass native EL7 header and
whole-package signatures/digests. Source-vendor verification and output-package
verification are separate requirements. Old native SHA-1/MD5 digest fields are
not used as substitutes for the RSA/SHA-256 signature authenticating the package.

## Isolated EL7 build

Original base: official amd64 CentOS 7 image manifest
`sha256:dead07b4d8ed7e29e98de0f4504d87e8880d4347859d839686a31da35a3b532f`.
Rootless Docker; unprivileged compilation; serial builders limited to six CPUs,
10 GiB RAM and 512 PIDs. No privileged mode, host network, Docker socket,
credentials, customer data or signing-key mounts. Compilation/tests are offline;
fixtures use loopback only. Do not replace production or host libraries.

Pinned dependency NEVRAs are under each recipe. The retained authenticated EL7
vault/EPEL/Remi builder supplies GCC 4.8, glibc 2.17, OpenSSL 1.0.2 and ICU 73.2.
Keep normal HTTPS and RPM GPG verification enabled when acquiring dependencies.

For an absolute topdir and family (`php74` or `php81`), run as its builder UID:

```sh
rpmbuild --define "_topdir $TOP" --define "scl $FAMILY" \
  --define 'dist .el7.remi' --define '_default_patch_fuzz 0' -bp "$TOP/SPECS/php.spec"
rpmbuild --define "_topdir $TOP" --define "scl $FAMILY" \
  --define 'dist .el7.remi' -bs "$TOP/SPECS/php.spec"
rpmbuild --define "_topdir $TOP" --define "scl $FAMILY" \
  --define 'dist .el7.remi' --define '_smp_mflags -j6' \
  --define '_default_patch_fuzz 0' -ba "$TOP/SPECS/php.spec"
```

The final specs print `UPSTREAM_TEST_EXIT` before vendor failure reporting.
An RPM build exit 0 does not mean its PHPT runner passed. Preserve original
FAIL/SKIP/XFAIL/WARN output and relevant focused regression evidence.

Sign only in a separate controlled signer with your own independently managed
key. No private key is included. Builds are source-reproducible recipes, not a
claim of bit-for-bit identical binary output. Carried families retain the
original recipes/evidence and exact original RPM bytes, not a new build claim.
