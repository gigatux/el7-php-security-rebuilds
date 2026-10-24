# Installation: preserve the existing family and routing

**Administrator-scoped guidance, not an automatic updater.** Authenticate the
published bundle and qualify the procedure for the actual host and panel version.
Successful RPM tests do not prove that a panel's generated runtime mappings are
correct. Candidate preparation is not publication or installation approval.

1. Before a transaction or package scriptlet can restart FPM, back up configuration,
   ownership/permissions, service settings and working pool/socket/Apache mappings.
   Record actual installed NEVRAs, exact companion closure, external modules,
   INI order and authenticated rollback RPMs. Review scriptlet restart effects
   and prepare the rollback before changing packages.
   Preserve applications' current branches; never substitute system PHP for SCL
   or upgrade customers to another language branch just to fit this bundle.
2. Authenticate signing identity independently, then verify the selected RPMs
   with native `rpmkeys --checksig --verbose`. Require valid signatures and
   digests, never NOKEY or verification-disabling flags. Run the unchanged
   `verify-release.py` against the complete 90-RPM asset directory too. A hash
   file beside the download is not authenticated until its signature is checked.
3. Select only the exact already-used family closure. Preview the precise
   transaction and reject mixed companion EVRs, unrelated OS changes, missing
   extensions or unexpected configuration replacement. Do not use `--nodeps`,
   `--force`, broad updates or add unused modules. Test whole-family rollback
   and forward upgrade first, one family at a time. Rollback reintroduces older
   vulnerabilities. An RPM update is not permission for a PHP-major upgrade.

## InterWorx: package origin, pools and Apache must remain coherent

Direct local installation can lose or change Yum repository-origin identity.
The panel's cached provider identity can then produce an `installed` socket
prefix instead of the previous provider namespace. An available-version refresh
may expose this same-branch change; it does not itself make the live listener and
Apache backend agree. This risk applies across **SCL families and system PHP**.
A version label or cache display is not the actual runtime. These generic RPMs
have no InterWorx-specific scriptlets and do not repair panel routing for you.

Use the supported native origin/cache/provider workflow for the actual panel
version, keeping configuration changes scoped to the affected family. If a cache
refresh has wider reach, assess those mappings too; that is not authority to
regenerate untargeted runtime configuration. Inspect before and after any
refresh: configured FPM listen endpoint, live socket owner and FPM PID/executable,
Apache's actual backend endpoint, and the intended site's runtime and UID must
agree. Preserve default, inactive and mixed-runtime exceptions rather than
normalising them blindly. Qualifying one family does not certify every other
active SCL/system runtime or constitute panel-vendor endorsement.

Where the existing same-runtime mapping is sound, retain its pool/socket/vhost
namespace. A package-only update need not change Apache routing or trigger an
Apache graceful reload. If a reviewed mapping change is necessary, prepare the
matching pool/listener before switching its backend, validate configuration, and
coordinate only the affected service actions. Neither a vhost-only edit nor a
cache-display-only fix establishes coherence. There is no universally safe blind
global refresh/reset command supplied here.

Do not forge YumDB `from_repo`, invent a dummy origin, impersonate Remi with a
repository name, add socket aliases/wrappers or apply a global panel reset.
Recheck actual FPM identity/version, extensions, live routing and representative
application health using existing private/local probes; do not add public PHP
diagnostic files. No application/database migration or SSH-policy change is a
dependency of installing these same-family packages.

On failure restore the whole matching package family and the corresponding
configuration/cache/pools and Apache mappings together. Validate the restored
listener and backend before resuming traffic. Do not proceed to the next family
while the first is unhealthy; keep a reviewed maintenance/rollback window.

The public signing fingerprint is unchanged:
`89D424E87773D278B86419DBEFA7C343D46BD47D`. The refreshed public certificate
extends its expiry to 22 October 2027. The original fixture RPMDB certificate
already verifies the new RSA/SHA-256 packages, and current-certificate import was
tested in isolation. Do not infer a production trust-store change is required
or authorised: compare the actual local certificate during the private preflight
and review any same-identity public-certificate refresh explicitly.
