#!/usr/bin/env python3
"""Small validation script for the generated static site."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlparse


class LinkAssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.assets: list[str] = []
        self.forms: list[dict[str, str]] = []
        self.inputs: list[dict[str, str]] = []
        self.labels_for: set[str] = set()
        self.images_alt_missing: list[str] = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])
        if tag in {"img", "script"} and data.get("src"):
            self.assets.append(data["src"])
        if tag == "link" and data.get("href") and data.get("rel") == "stylesheet":
            self.assets.append(data["href"])
        if tag == "form":
            self.forms.append(data)
        if tag in {"input", "textarea", "select"}:
            self.inputs.append(data)
        if tag == "label" and data.get("for"):
            self.labels_for.add(data["for"])
        if tag == "img" and not data.get("alt"):
            self.images_alt_missing.append(data.get("src", "<unknown>"))


def local_path(public: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or url.startswith("mailto:") or url.startswith("tel:") or url.startswith("#"):
        return None
    path = urldefrag(parsed.path)[0]
    if not path or path == "/":
        return public / "index.html"
    rel = path.lstrip("/")
    candidate = public / rel
    if path.endswith("/"):
        return candidate / "index.html"
    return candidate


def main() -> int:
    public = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not public.exists():
        print(f"Missing build directory: {public}", file=sys.stderr)
        return 1

    errors: list[str] = []
    pages = list(public.rglob("*.html"))
    if not pages:
        errors.append("No HTML pages generated")

    contact_html = ""
    for page in pages:
        parser = LinkAssetParser()
        text = page.read_text(encoding="utf-8")
        parser.feed(text)
        if page.as_posix().endswith("/contact/index.html"):
            contact_html = text

        if parser.images_alt_missing:
            errors.append(f"{page}: images missing alt text: {parser.images_alt_missing}")

        for href in parser.links:
            target = local_path(public, href)
            if target and not target.exists():
                errors.append(f"{page}: broken internal link {href} -> {target}")
        for src in parser.assets:
            target = local_path(public, src)
            if target and not target.exists():
                errors.append(f"{page}: missing local asset {src} -> {target}")

    required_pages = ["index.html", "about/index.html", "classes/index.html", "instructors/index.html", "contact/index.html"]
    for rel in required_pages:
        if not (public / rel).exists():
            errors.append(f"Required page missing: {rel}")

    if not contact_html:
        errors.append("Contact page missing")
    else:
        for field in ['name', 'email', 'phone', 'message']:
            if not re.search(rf'name=[\"\']?{field}[\"\']?', contact_html):
                errors.append(f"Contact form missing field name={field}")
        if not re.search(r'name=[\"\']?website[\"\']?', contact_html) or 'honeypot' not in contact_html:
            errors.append("Contact form missing honeypot field")
        if 'required' not in contact_html or not re.search(r'type=[\"\']?email[\"\']?', contact_html):
            errors.append("Contact form missing basic client-side validation")
        if 'https://example.com/contact' not in contact_html:
            errors.append("Placeholder form endpoint not rendered as expected")

    if errors:
        print("Site validation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    print(f"Validated {len(pages)} HTML pages: internal links, assets, contact form, and alt text look good.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
