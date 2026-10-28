"""Offline checks for reviewed CDN references and local runtime asset drift."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import base64, hashlib, json, re, sys

class Resources(HTMLParser):

    def __init__(self):
        super().__init__()
        self.resources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        url = attrs.get('src') if tag == 'script' else attrs.get('href') if tag == 'link' and attrs.get('rel') == 'stylesheet' else None
        if url and url.startswith(('http:', 'https:', '//')):
            self.resources.append((tag, url, attrs))

def checkDependencies(root):
    root = Path(root).resolve()
    issues = []
    manifest = json.loads((root / 'docs/frontend-dependencies.json').read_text(encoding='utf-8'))
    declared = {item['url']: item for item in manifest['remoteResources']}
    observed = set()
    pages = list(root.glob('*.html'))
    if not pages:
        issues.append('No root HTML documents found')
    for page in pages:
        parser = Resources()
        parser.feed(page.read_text(encoding='utf-8'))
        for tag, url, attrs in parser.resources:
            observed.add(url)
            item = declared.get(url)
            if item is None:
                issues.append(f'{page.name}: unreviewed external resource {url}')
                continue
            if urlsplit(url).scheme != 'https':
                issues.append(f'{page.name}: HTTPS required')
            if item.get('dynamicFontStylesheet'):
                if tag != 'link' or urlsplit(url).hostname != 'fonts.googleapis.com':
                    issues.append(f'{page.name}: font exception cannot cover this resource')
                continue
            if re.search('@(?:next|latest|\\^|~)|[*/](?:latest|next)(?:/|$)', url) or not re.search('\\d+\\.\\d+\\.\\d+', url):
                issues.append(f'{page.name}: exact version required')
            if 'cdn.ckeditor.com/' in url:
                issues.append(f'{page.name}: retired CKEditor resource')
            integrity = item.get('integrity', '')
            try:
                algorithm, value = integrity.split('-', 1)
                assert algorithm in ['sha256', 'sha384', 'sha512']
                assert len(base64.b64decode(value, validate=True)) == hashlib.new(algorithm).digest_size
            except (ValueError, AssertionError):
                issues.append(f'{page.name}: valid reviewed SRI required')
            if attrs.get('integrity') != integrity or attrs.get('crossorigin') != 'anonymous':
                issues.append(f'{page.name}: SRI or crossorigin drift for {url}')
    for url in declared.keys() - observed:
        issues.append(f'Unused manifest entry: {url}')
    for item in manifest.get('localAssets', []):
        target = (root / item['path']).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            issues.append(f"Local asset missing or outside root: {item['path']}")
            continue
        digest = hashlib.sha256(target.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        if digest != item['sha256LF']:
            issues.append(f"Local asset changed: {item['path']}")
    return issues
if __name__ == '__main__':
    findings = checkDependencies(Path(__file__).resolve().parents[1])
    for finding in findings:
        print(finding)
    print('FAIL' if findings else 'PASS: reviewed resource versions, SRI and local asset hashes')
    sys.exit(bool(findings))
