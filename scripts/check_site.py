"""Check document shells, duplicate IDs and local HTML resource/link targets.

Uses only the Python standard library. Remote URLs and placeholder '#' links
are not fetched. This is not a complete HTML5 conformance or browser test.
"""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os
import sys


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.duplicates = []
        self.references = []
        self.shell = {name: 0 for name in ("html", "head", "body", "title")}
        self.doctype = False
        self.inTitle = False
        self.title = ""
        self.feed(path.read_text(encoding="utf-8-sig"))
        self.close()

    def handle_decl(self, decl):
        self.doctype |= decl.lower().strip() == "doctype html"

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag in self.shell:
            self.shell[tag] += 1
        if tag == "title":
            self.inTitle = True
        identity = values.get("id")
        if identity:
            if identity in self.ids:
                self.duplicates.append(identity)
            self.ids.add(identity)
        for attribute in ("href", "src", "poster"):
            value = values.get(attribute)
            if value:
                self.references.append((self.getpos()[0], value))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self.inTitle = False

    def handle_data(self, data):
        if self.inTitle:
            self.title += data


def exactPath(root, target):
    """Check filename casing even on a case-insensitive local filesystem."""
    current = root
    for part in target.relative_to(root).parts:
        if not current.is_dir() or part not in {p.name for p in current.iterdir()}:
            return False
        current /= part
    return current.exists()


def checkSite(root):
    root = root.resolve()
    entries = sorted(root.glob("*.html"))
    if not entries:
        return ["No root HTML documents found."], 0, 0
    pages = {}
    errors = []
    checked = 0

    def load(path):
        if path not in pages:
            pages[path] = Page(path)
        return pages[path]

    for entry in entries:
        page = load(entry)
        label = entry.relative_to(root).as_posix()
        if not page.doctype:
            errors.append(f"{label}: missing HTML doctype")
        for tag, count in page.shell.items():
            if count != 1:
                errors.append(f"{label}: expected one {tag} element, found {count}")
        if not page.title.strip():
            errors.append(f"{label}: empty document title")
        for identity in page.duplicates:
            errors.append(f"{label}: duplicate id '{identity}'")
        for line, value in page.references:
            url = urlsplit(value)
            if url.scheme or url.netloc or value == "#":
                continue
            pathText = unquote(url.path)
            candidate = ((root / pathText.lstrip("/")) if pathText.startswith("/")
                         else (entry.parent / pathText)) if pathText else entry
            target = Path(os.path.abspath(candidate))
            if not target.is_relative_to(root) or not target.resolve().is_relative_to(root):
                errors.append(f"{label}:{line}: local reference escapes repository: {value}")
                continue
            checked += 1
            if not exactPath(root, target):
                errors.append(f"{label}:{line}: missing local target or incorrect case: {value}")
                continue
            if url.fragment and target.suffix.lower() in (".html", ".svg"):
                if unquote(url.fragment) not in load(target).ids:
                    errors.append(f"{label}:{line}: missing fragment target: {value}")
    return errors, len(entries), checked


if __name__ == "__main__":
    repository = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors, documents, references = checkSite(repository)
    for error in errors:
        print(error)
    if errors:
        print(f"FAIL: {len(errors)} issue(s) in {documents} HTML documents.")
        sys.exit(1)
    print(f"PASS: {documents} HTML documents and {references} local references checked.")
