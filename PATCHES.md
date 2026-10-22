# Patch and packaging provenance

All five SRPMs contain the complete upstream source archive, build spec,
packaging patches, configuration templates and licence notices. Original Remi
recipe commits are pinned in `provenance.json`; each final spec, spec delta,
source/spec hash inventory and dependency NEVRA inventory is in `recipes/`.
Retain vendor changelogs and credits; these are local derivatives, not new
official Remi releases.

* PHP 7.4: complete official emergency commit
  `712e60f9edfd03f0960fc4fc3c2c375f42b90aa2`. Four addition-only hunks already
  present identically in the vendor CVE-2023-0662 patch are removed from the
  rebased emergency patch to avoid applying them twice. The rest of the vendor
  stack is preserved. The rebased patch is in the SRPM; the original official
  patch is retained separately under `patches/` for comparison.
* PHP 8.1: complete official emergency commit
  `1d7dec178a094e6e75b229ce22754045f8c6070a`, retaining vendor patches.
* PHP 8.2/8.3: official fixed full source releases, not partial backports.
  EL7's OpenSSL 1.0.2 compatibility patch aliases `ASN1_STRING_get0_data` to
  the existing `ASN1_STRING_data` accessor below API version 1.1.0, rather than
  transplanting a newer ABI.
* PHP 8.3 SCL and system: FFI parser calls use `(strncmp)(...)` so that
  `ZEND_STRL` expands correctly without triggering the old libc macro wrapper.
  Refreshed vendor patch contexts match the new source;
  source and delta hashes document these changes. See the exact spec deltas
  for EL7 LSAPI packaging; LSAPI binaries are not in the published closure.

The source is not stripped or re-signed for publication. RPM release strings
carry `gigatux20261021` to distinguish the derivative. Upstream tarball detached
signatures and public upstream keyring are retained in each SRPM. PHP 8.1's
historic signature is cryptographically valid but its key is now expired: this
is explicitly disclosed, not a reason to bypass verification. GitHub commit API
responses originally reported verified signed commits; that is remote HTTPS
attestation, not a claim of local signed-commit verification.
