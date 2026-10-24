# EL7 PHP security rebuild candidate

**Internal review candidate — not a published release or production-installation claim.**

Independent GigaTux x86_64 builds derived from Remi packaging. These are not
official Remi or InterWorx packages. PHP 7.4, PHP 8.1 and EL7 remain end of life;
this is neither comprehensive security support nor a promise of future fixes.

| Existing family | Candidate baseline | Binary closure | Treatment |
| --- | --- | ---: | --- |
| `php74-php-*` | Complete Remi 7.4.33-31 stack | 19 | Rebuilt for EL7 |
| `php81-php-*` | Upstream 8.1.34 plus complete Remi -6 stack | 17 | Rebuilt for EL7 |
| `php82-php-*` | 8.2.35 | 18 | Exact signed bytes carried from 2026-10-21 |
| `php83-php-*` | 8.3.36 | 18 | Exact signed bytes carried from 2026-10-21 |
| System `php-*` | 8.3.36 | 13 | Exact signed bytes carried from 2026-10-21 |

The bundle contains 85 selected binary RPMs and five complete source RPMs.
`release-assets.json` pins every byte; `carried-forward-assets.json` identifies
the 52 unchanged RPMs. Reused families were not rebuilt or re-signed.

### What changed

The PHP74 baseline advances from Remi 7.4.33-15 to the complete 7.4.33-31 stack;
PHP81 advances from 8.1.29 to 8.1.34 plus the complete Remi -6 stack. This corrects
the stale-source gap raised in issue #1, rather than merely reapplying two CVE
patches. The accepted EL7 adaptations retain ICU73 and correct PHP74's one-line
ICU compiler-version check. The 38 new RPMs are 36 binaries and two complete
SRPMs; PHP82/PHP83/system's 52 original signed RPMs remain byte-identical.

Package installation and panel routing are separate checks. Local RPM origin
changes can alter a cached provider's socket namespace without changing its PHP
branch. [INSTALL.md](INSTALL.md) explains scoped verification of the actual FPM
listener, PID/executable and Apache backend, preserving existing runtime choices.
No automatic global panel repair or certification of all runtimes is implied.

The original 2026-10-21 release is immutable. Its 7.4/8.1 builds were a narrow
two-CVE bridge, not the current complete vendor security baseline. This candidate
corrects that stale-baseline issue; it does not yet supersede a public release.
No release date, tag or installation success is implied by its preparation.

The October minimal mitigation intentionally disables session upload-progress
callbacks. Allocator OOM hard-exits without unsafe PHP shutdown/output callbacks;
FPM replaces that worker. Ordinary uploads and sessions were tested separately.
Do not re-enable unsafe behaviour to restore old test expectations.

Read [BUILD.md](BUILD.md), [PATCHES.md](PATCHES.md), [TESTING.md](TESTING.md) and
[INSTALL.md](INSTALL.md). Full upstream suites are **not all green**. Source
authentication for 8.1.34 has an explicitly disclosed expired upstream signature;
the reviewed vendor-SRPM/independent PHP archive-hash chain is documented instead.

The public certificate fingerprint is
`89D424E87773D278B86419DBEFA7C343D46BD47D`. Authenticate it independently; merely
including a key beside an RPM does not establish trust. No private key is supplied.
