import sys, json, tempfile, unittest, hashlib, base64
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_dependencies import checkDependencies

class DependencyPolicyTests(unittest.TestCase):

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        (self.root / 'docs').mkdir()
        self.url = 'https://cdn.example.test/library@1.2.3/library.js'
        self.sri = 'sha384-' + base64.b64encode(bytes(48)).decode()
        self.manifest = {'remoteResources': [{'url': self.url, 'integrity': self.sri}], 'localAssets': []}

    def tearDown(self):
        self.folder.cleanup()

    def fixture(self, url=None, integrity=None):
        (self.root / 'index.html').write_text(f'<script src="{url or self.url}" integrity="{integrity or self.sri}" crossorigin="anonymous"></script>', encoding='utf-8')
        (self.root / 'docs/frontend-dependencies.json').write_text(json.dumps(self.manifest), encoding='utf-8')
        return checkDependencies(self.root)

    def testPinnedResource(self):
        self.assertEqual(self.fixture(), [])

    def testUnregisteredScript(self):
        self.assertTrue(self.fixture(url='https://unexpected.test/runtime.js'))

    def testSriDrift(self):
        self.assertTrue(self.fixture(integrity='sha256-invalid'))

    def testFloatingVersion(self):
        self.url = self.url.replace('@1.2.3', '@next')
        self.manifest['remoteResources'][0]['url'] = self.url
        self.assertTrue(self.fixture())

    def testFontExceptionCannotAuthorizeScript(self):
        self.url = 'https://fonts.googleapis.com/runtime.js'
        self.manifest['remoteResources'] = [{'url': self.url, 'dynamicFontStylesheet': True}]
        self.assertTrue(self.fixture())

    def testLocalAssetDrift(self):
        (self.root / 'runtime.js').write_text('changed', encoding='utf-8')
        self.manifest['localAssets'] = [{'path': 'runtime.js', 'sha256LF': hashlib.sha256(b'original').hexdigest()}]
        self.assertTrue(self.fixture())
if __name__ == '__main__':
    unittest.main()
