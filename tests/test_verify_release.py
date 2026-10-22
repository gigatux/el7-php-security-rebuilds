import importlib.util
import json
import pathlib
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('verify_release', pathlib.Path(__file__).parents[1] / 'verify-release.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ManifestChecks(unittest.TestCase):
    def rejected(self, rows, message):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            index = root / 'index.json'
            index.write_text(json.dumps(rows))
            with self.assertRaisesRegex(ValueError, message):
                module.verify(root, index)

    def test_traversal(self):
        self.rejected([{'name': '../not-an-asset'}], 'Unsafe')

    def test_missing_asset(self):
        self.rejected([{'name': 'missing.rpm'}], 'Missing')

    def test_empty_manifest(self):
        self.rejected([], 'Incorrect binary count')


if __name__ == '__main__':
    unittest.main()
