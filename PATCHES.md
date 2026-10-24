# Complete vendor stacks and minimal EL7 changes

PHP 7.4 uses authenticated Remi `7.4.33-31`; PHP 8.1 uses authenticated Remi
`8.1.34-6` with upstream 8.1.34. Exact specs, source-member hashes and complete
patch inputs are in `recipes/`. `testing/` inventories active effective files
and the PHPT outcomes, including conditional/inapplicable tests.

All active vendor security patches were retained and applied with zero fuzz and
no rejects. PHP74 Patch243 and PHP81 Patch214 already provide the October
CVE-2026-109618/CVE-2026-109619 minimal mitigation. The old local Patch990 is
**not** additionally applied. Patch filenames alone are not coverage evidence.

Local changes for the rebuilt PHP74/PHP81 families are limited to:

1. Increasing local release values, retaining existing package families and ABI.
2. Three ICU BuildRequires thresholds: 74 to 73, matching existing EL7 ICU 73.2.
3. PHP74 Patch991: execute the pkg-config ICU-version check, rather than testing
   whether a quoted command string is non-empty. This selects working C++11 on
   GCC 4.8/ICU73 instead of incorrectly selecting C++17. No security hunk changes.
4. Printing the real PHPT make-test exit status before unchanged vendor failure
   reporting. Tests/security responses are not weakened.

No Oracle dependency adaptation was needed: OCI8 is inactive for these closures,
and both current specs parse on native EL7 without changing that condition.
No unused Oracle component or new host library stack was added.

Carried PHP82/PHP83/system recipes retain their original EL7 compatibility
patches and original signed bytes; those historical deltas were not reworked.

The expanded vendor baseline includes array-merge overflow, redirect credential
isolation, full-width IPv6 FPM ACL comparison, TLS name matching, SOAP and stream
fixes, as well as intervening PHP 8.1 upstream security updates. See the exact
patch inventories and test dispositions rather than interpreting this list as
an exhaustive vulnerability assessment or a future-support commitment.

PHP74/81 exported dynamic CLI symbols and public PHP/Zend/PDO ABI provides match
the original accepted builds. Existing external modules were loaded and exercised.
Generic RPMs contain no site-specific InterWorx repair scripts. The stock FPM
service source only drops obsolete `syslog.target` ordering; its network ordering
and other service directives remain. Source and package delta evidence records it.
