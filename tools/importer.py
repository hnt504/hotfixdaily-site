"""Turn published Hotfix Daily pages back into source files.

Used once to move the hand-built site into content/, and by the build as a
safety net: a page or issue published as finished HTML (the old way) is pulled
back into content/ instead of being overwritten.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import yaml

COMMON_LD = re.compile(r'"@type":\s*"(Organization|WebSite)"')


def front_matter(meta: dict, body: str) -> str:
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=10_000)
    return f"---\n{fm}---\n{body.rstrip()}\n"


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    return (yaml.safe_load(fm) or {}), body.lstrip("\n")


def route_of(rel: str) -> str:
    """'guides/mcp-servers/index.html' -> 'guides/mcp-servers'; 'index.html' -> 'index'; '404.html' -> '404'."""
    rel = rel.replace("\\", "/")
    if rel == "index.html":
        return "index"
    if rel.endswith("/index.html"):
        return rel[: -len("/index.html")]
    return rel[: -len(".html")]


def parse_page(path: Path) -> tuple[dict, str]:
    doc = path.read_text(encoding="utf-8")
    head = doc[doc.index("<head>"):doc.index("</head>")]

    def meta(pattern):
        m = re.search(pattern, head)
        return html.unescape(m.group(1)) if m else None

    info = {
        "title": meta(r"<title>([^<]*)</title>"),
        "description": meta(r'<meta name="description" content="([^"]*)"'),
    }
    og_type = meta(r'<meta property="og:type" content="([^"]*)"')
    if og_type and og_type != "website":
        info["og_type"] = og_type
    if 'name="robots" content="noindex"' in head:
        info["noindex"] = True
    ld = [m.group(1) for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', head)
          if not COMMON_LD.search(m.group(1)[:120])]
    if ld:
        info["jsonld"] = ld
    start = doc.index('<main id="main">') + len('<main id="main">')
    end = doc.rindex("</main>")
    return info, doc[start:end].strip("\n")


def import_page(root: Path, rel: str) -> Path:
    info, body = parse_page(root / rel)
    dest = root / "content" / "pages" / f"{route_of(rel)}.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    old_meta = split_front_matter(dest.read_text(encoding="utf-8"))[0] if dest.exists() else {}
    dest.write_text(front_matter({**old_meta, **info}, body), encoding="utf-8")
    return dest
