# Testing and known dispositions

Original vendor `%check` specs mask the test runner's non-zero status. A successful
RPM build therefore does **not** mean every PHPT passed. Recorded full-suite
results, with no failure suppressed from these counts:

| Family | Total | PASS | SKIP | XFAIL | FAIL | WARN |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 7.4 | 15796 | 9127 | 6624 | 33 | 11 | 1 |
| 8.1 | 17628 | 10291 | 7315 | 8 | 13 | 1 |
| 8.2 | 18781 | 10990 | 7782 | 6 | 2 | 1 |
| 8.3 SCL | 19650 | 11532 | 8097 | 7 | 13 | 1 |
| 8.3 system | 19650 | 11532 | 8097 | 7 | 13 | 1 |

7.4 failures comprise eight intentional upload-progress changes, two expired
SNI leaf fixtures and the deliberate OOM newline. Fresh SNI fixtures keep peer
verification and the real clock; adjusted newline-only expectations give three
targeted passes. 8.1 failures similarly include deliberate disabled upload
progress and hard OOM/output-buffer/Fiber shutdown behaviour, plus expired SNI
fixtures. Five targeted follow-ups and three separately compiled observer tests
pass; no observer test extension is shipped or installed for users.

8.2's two failures are the older timezone spelling and EL7 OpenSSL error-code
expectations, reproduced on the old-binary baseline. Four targeted checks pass,
including IPv4/IPv6 SAN paths. 8.3's 13 failures comprise ten timezone-spelling
expectations, one EL7 OpenSSL error-code expectation, one multicast default
interface assumption under network isolation and one locale expectation. Fifteen
targeted checks pass for each family with bounded fixture-only adjustments.
The printed GH14930 diff is a documented upstream XFAIL, not an extra failure.
No OS tzdata, crypto operation, security response or ABI was changed to green a
test. WARN results are retained, not recategorised as passes.

Disposable-container checks covered exact 19/17/18/18/13 core closures with
existing external extension fixtures, signature enforcement, module loading,
RPM verification, FPM normal/fatal/OOM worker recovery, sessions and uploads,
and exact rollback/forward transactions including `rpm --test`. System PHP also
passed Apache/mod_php recovery checks after fixing an isolated test-fixture
module-loading problem. FFI payload checks cover parser directives and libc
`strlen`. Raw environment/operational logs are not public release assets.

This evidence is bounded, not an assertion of all-green upstream suites or
universal customer-application compatibility. Test locally before deployment.
