#!/usr/bin/env python3
"""Migrate HTML pages to shared site.css / site.js design system."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN_MOCKUP = ROOT / "design-mockup"

PLAYFAIR_LINK = re.compile(
    r'<link\s+href="https://fonts\.googleapis\.com/css2\?'
    r'family=Playfair\+Display[^"]*"\s+rel="stylesheet"\s*>',
    re.IGNORECASE,
)

STYLE_BLOCK = re.compile(r"<style[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)

FONT_LINKS = """  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/site.css">"""

DUPLICATE_PRECONNECT = re.compile(
    r'(<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*)'
    r'\s*<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*',
    re.IGNORECASE,
)

SITE_JS = '<script src="/site.js" defer></script>'

# Inline scripts handled by site.js
NAV_IIFE = re.compile(
    r"<script>\s*\(function\s*\(\)\s*\{[^<]*nav-toggle[^<]*\}\)\(\);\s*</script>",
    re.DOTALL | re.IGNORECASE,
)
COOKIE_IIFE = re.compile(
    r"<script>\s*\(function\s*\(\)\s*\{[^<]*cc_analytics[^<]*\}\)\(\);\s*</script>",
    re.DOTALL | re.IGNORECASE,
)
CONTACT_SCRIPT = re.compile(
    r"<script>\s*function toggleFaq[\s\S]*?</script>",
    re.DOTALL,
)
TOGGLE_FAQ_ONLY = re.compile(
    r"<script>\s*function toggleFaq\(btn\)[\s\S]*?</script>",
    re.DOTALL,
)

FOOTER_BROKEN = re.compile(
    r'(<li><a href="/services/#hr-support">HR Support</a>)\s*'
    r'(<a href="/recruitment-support/">Recruitment Support</a></li>)',
    re.IGNORECASE,
)

NAV_LOGO = re.compile(
    r'(<a\s+href="/"\s+class="nav-logo"[^>]*>\s*'
    r'<img\s+src="/logo\.png"[^>]*>\s*)'
    r'(</a>)',
    re.IGNORECASE | re.DOTALL,
)

WORDMARK = '<span class="nav-wordmark">Crawford Consultancy</span>'


def should_skip(path: Path) -> bool:
    try:
        path.relative_to(DESIGN_MOCKUP)
        return True
    except ValueError:
        return False


def update_head(html: str) -> str:
    html = STYLE_BLOCK.sub("", html)
    if "/site.css" not in html:
        if 'rel="preconnect"' not in html:
            html = html.replace(
                "</head>",
                '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
                '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                + FONT_LINKS + "\n</head>",
                1,
            )
        else:
            html = html.replace("</head>", FONT_LINKS + "\n</head>", 1)
    if PLAYFAIR_LINK.search(html):
        html = PLAYFAIR_LINK.sub(FONT_LINKS, html, count=1)
    html = DUPLICATE_PRECONNECT.sub(r"\1", html)
    return html


def update_nav(html: str) -> str:
    if "nav-wordmark" not in html:

        def add_wordmark(m: re.Match[str]) -> str:
            return m.group(1) + WORDMARK + "\n    " + m.group(2)

        html = NAV_LOGO.sub(add_wordmark, html)
    return html


def fix_footer(html: str) -> str:
    return FOOTER_BROKEN.sub(
        r'\1</li>\n          <li>\2',
        html,
    )


def remove_inline_scripts(html: str) -> str:
    html = CONTACT_SCRIPT.sub("", html)
    html = NAV_IIFE.sub("", html)
    html = COOKIE_IIFE.sub("", html)
    html = TOGGLE_FAQ_ONLY.sub("", html)
    return html


def ensure_site_js(html: str) -> str:
    if "/site.js" in html:
        return html
    if "</body>" in html:
        return html.replace("</body>", SITE_JS + "\n</body>", 1)
    return html + "\n" + SITE_JS


def migrate_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = original
    updated = update_head(updated)
    updated = update_nav(updated)
    updated = fix_footer(updated)
    updated = remove_inline_scripts(updated)
    updated = ensure_site_js(updated)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if should_skip(path):
            continue
        if migrate_file(path):
            changed.append(str(path.relative_to(ROOT)).replace("\\", "/"))
    print(f"Migrated {len(changed)} file(s):")
    for name in changed:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
