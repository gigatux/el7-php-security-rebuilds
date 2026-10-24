# Testing and explicit limits

Internal candidate evidence, not production or publication acceptance. Full
vendor PHPT runs are **not all green**; both actual runners returned exit 2,
although both complete RPM builds returned 0.

| Changed family | Total | PASS | SKIP | XFAIL | FAIL | WARN |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PHP74 | 15901 | 9157 | 6701 | 33 | 9 | 1 |
| PHP81 | 17740 | 10322 | 7397 | 8 | 12 | 1 |

Original failures remain counted. PHP74 has eight intentionally disabled
upload-progress fixtures and one hard-OOM newline difference. PHP81 has eight
upload-progress fixtures, three hard-OOM/output-buffer/Fiber expectations, and
one EL7 OpenSSL error-code expectation. Separate unchanged-body focused fixtures
confirm the intended hard-exit output (PHP74 1/1; PHP81 3/3). Independent OOM
checks prove neither unsafe shutdown/output callback nor continued execution.
PHP81's OpenSSL failure reproduces on unchanged 8.1.29 with a byte-identical diff:
expected 04099079, EL7 returns 040A1079 for OAEP decoding failure. No crypto or
original expectation was changed. WARN is an upstream XFAIL test that passed;
it is not silently recategorised.

Additional all-built-extension/current-security/TLS/FPM runs:

| Family | Total | PASS | SKIP | FAIL | WARN |
| --- | ---: | ---: | ---: | ---: | ---: |
| PHP74 | 387 | 343 | 41 | 2 | 1 |
| PHP81 | 416 | 366 | 47 | 2 | 1 |

Their resource-heavy SOAP tests pass separately with appropriate bounded memory
(PHP74 QName 1/1 under 10 GiB; PHP81 large-response 1/1 under 8 GiB). The general
PHP74 run's SOAP child hit its 3 GiB limit; the original test itself is unchanged.
The second failure in each suite is an FPM reload test requiring pcntl inside
FPM: this packaging deliberately supplies pcntl only in CLI. Its CLI skip-check
does not establish FPM capability. No pcntl was added to shipped FPM merely to
green that test; ordinary/concurrent reload tests and FPM recovery passed.
PHP81's other supplemental failure is the unchanged-baseline OpenSSL case above.

Both families pass the actual upstream IPv6 ACL security test: a localhost `::1`
client is accepted against `::1` and rejected against `::dead:beef`, with the
explicit rejection log checked. The IPv4-mapped companion also passes. Array,
redirect, TLS CN/SAN/wildcard and stream regressions have individual outcomes in
the inventory. Platform-only, unavailable database service, later-library-only
and absent test-tool skips are disclosed, not called passes.

Test-only modules built unprivileged against installed signed candidates pass
PHP74's three DOM/SimpleXML/XMLReader entity-loader tests and PHP81's three
observer regressions. These test modules are not shipped or installed for users.

A separate unchanged PHP81 `sapi/fpm/tests/gh8646.phpt` follow-up passes 1/1,
exit 0, with the already-built test-only zend_test loaded inside the actual
installed signed-candidate FPM and OPcache enabled. Ten requests retain a stable
class map-pointer value. The historical supplemental SKIP remains unchanged;
the three CLI observer tests are not represented as this FPM invariant check.

Each signed family passed exact old → new → old → new native RPM previews and
transactions (19/17 companions), preserving deliberately changed configuration,
INI order, external modules and unrelated installed packages. Imagick PNG,
mcrypt encryption/decryption, ZipArchive, XMLRPC, PDO SQLite, DOM, mbstring and
ICU operations were exercised at each state. FPM normal/fatal/OOM replacement,
sessions and ordinary multipart uploads passed, while upload progress remained
disabled even when enabled in the fixture INI. No mixed companion EVRs occurred.

Native EL7 verifies every candidate signature. Source RPM contents match exact
final inputs (84 PHP74 members, 49 PHP81). Both source RPMs have legacy
`ARCH=x86_64` with `SOURCEPACKAGE=1`, matching the old source format. Both CLI
ELFs require at most GLIBC 2.15, within EL7 2.17; no new host library requirement.

Carried families retain the original published test evidence only; their bytes
were not rebuilt or their full suites rerun. Existing verifier unit tests and
90-RPM content/native-signature checks are recorded separately. Rootless fixtures
do not establish systemd boot, production workload or InterWorx/Apache integration.
The installation procedure remains an explicit acceptance boundary.
