#!/usr/bin/env python3
"""Check local release bytes; authenticate signatures separately (INSTALL.md)."""
import hashlib
import json
import pathlib
import sys


def verify(directory, index):
    rows = json.loads(index.read_text())
    expected = {'php74': 19, 'php81': 17, 'php82': 18, 'php83': 18, 'php-system': 13}
    names = set()
    for row in rows:
        name = row['name']
        if pathlib.PurePosixPath(name).name != name or name in names:
            raise ValueError('Unsafe or repeated asset name: ' + name)
        names.add(name)
        package = directory / name
        if package.is_symlink() or not package.is_file():
            raise ValueError('Missing or unsafe asset: ' + name)
        if package.stat().st_size != row['bytes']:
            raise ValueError('Size mismatch: ' + name)
        if hashlib.sha256(package.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('SHA-256 mismatch: ' + name)
    for family, count in expected.items():
        selected = [row for row in rows if row['family'] == family]
        if sum(row['kind'] == 'binary' for row in selected) != count:
            raise ValueError('Incorrect binary count: ' + family)
        if sum(row['kind'] == 'source' for row in selected) != 1:
            raise ValueError('Incorrect source count: ' + family)
    if len(rows) != 90 or set(path.name for path in directory.glob('*.rpm')) != names:
        raise ValueError('Unexpected or missing RPM assets')
    return len(rows)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: python3 verify-release.py RELEASE_ASSET_DIRECTORY')
    count = verify(pathlib.Path(sys.argv[1]), pathlib.Path(__file__).with_name('release-assets.json'))
    print(str(count) + ' RPM hashes, sizes, names and family counts match; signatures still require verification.')
