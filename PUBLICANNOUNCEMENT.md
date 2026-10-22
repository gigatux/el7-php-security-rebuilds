# Draft announcement — share once the release is live

**One-off EL7 emergency rebuilds for PHP — 21 October 2026**

Still planning a migration away from CentOS 7? GigaTux has prepared independent
Remi-derived EL7 x86_64 RPM rebuilds addressing CVE-2026-109618 and
CVE-2026-109619: PHP 7.4.33/8.1.29 with the two official emergency backports,
and full PHP 8.2.35/8.3.36 releases, with complete corresponding source RPMs.

Release: https://github.com/gigatux/el7-php-security-rebuilds/releases/tag/2026-10-21

These are not official Remi/InterWorx packages or full EL7 security support.
7.4/8.1 remain EOL, with intentional upload-progress and hard-OOM behaviour
changes. Only the 85 binaries from the tested existing-package closures are
published, not a universal dependency bundle. Check the source, signatures,
failure dispositions and installation guidance before trying them on your host.
Migration to supported PHP and OS versions remains necessary.

Suggested GitHub description: Independent one-off EL7 x86_64 rebuilds for PHP
addressing CVE-2026-109618/109619; Remi-derived packaging, complete source RPMs.

Suggested topics: `centos7`, `el7`, `php`, `rpm`, `security`, `cve`, `remi`.
Optional later channels: GigaTux blog, relevant administrator forums and social
posts. This file is a draft, not authority to post or edit production websites.
