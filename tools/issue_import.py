"""Convert a published issue page back into issue Markdown.

Only used by the safety net, when an issue arrives as finished HTML in
issues/NNN/ with no content/issues/issue-NNN.md beside it.
"""

from __future__ import annotations

import html
import re


def _md(fragment: str) -> str:
    """Inline HTML from an issue page -> the inline Markdown it was rendered from."""
    s = re.sub(r"<code>(.*?)</code>", lambda m: "`" + html.unescape(m.group(1)) + "`", fragment)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s)
    s = re.sub(r'<a href="([^"]*)"[^>]*>(.*?)</a>', lambda m: f"[{m.group(2)}]({html.unescape(m.group(1))})", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def issue_html_to_markdown(page: str) -> str:
    title = html.unescape(re.search(r"<title>([^<]*)</title>", page).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', page).group(1))
    kicker = re.search(r'<p class="kicker">Issue #(\d+) · <time datetime="[^"]*">([^<]*)</time></p>', page)
    lede = re.search(r'<p class="lede">(.*?)</p>', page)
    out = ["# Hotfix Daily: The Daily AI Builder Digest", f"<!-- title: {title} -->", f"<!-- description: {desc} -->",
           f"**Issue #{kicker.group(1)} · {html.unescape(kicker.group(2))}**", "", _md(lede.group(1)) if lede else ""]
    after_lede = page[lede.end():] if lede else page
    for p in re.findall(r"^<p>(.*?)</p>$", after_lede.split('<section class="ctabox', 1)[0], re.M):
        out += ["", _md(p)]
    out += ["", "---", ""]
    for art in re.findall(r'<article class="item" id="i\d+">([\s\S]*?)</article>', page):
        label = re.search(r'<span class="chip">([^<]*)</span>', art)
        head = re.search(r'<h2><span class="n">(\d+)</span>\s*(.*?)</h2>', art)
        if label:
            out.append(f"[{html.unescape(label.group(1))}]")
        out.append(f"**{head.group(1)}. {_md(head.group(2))}**")
        for p in re.findall(r"^<p>(.*?)</p>$", art, re.M):
            out.append(_md(p))
        why = re.search(r'<p class="why"><strong>Why builders care:</strong>\s*(.*?)</p>', art)
        if why:
            out.append(f"*Why builders care:* {_md(why.group(1))}")
        src = re.search(r'<p class="src"><a href="([^"]*)"', art)
        if src:
            out.append(f"[source]({html.unescape(src.group(1))})")
        out.append("")
    sponsor = re.search(r'<aside class="item" id="sponsor"[^>]*>([\s\S]*?)</aside>', page)
    hotd = re.search(r'<aside class="hotd"[^>]*>([\s\S]*?)</aside>', page)
    out += ["---", ""]
    if sponsor:
        out.append("### Sponsor")
        out += [_md(p) for p in re.findall(r"^<p>(.*?)</p>$", sponsor.group(1), re.M)]
        out.append("")
    if hotd:
        out.append("### Hotfix of the Day")
        out += [_md(p) for p in re.findall(r"^<p>(.*?)</p>$", hotd.group(1), re.M)]
        src = re.search(r'<p class="src"><a href="([^"]*)"', hotd.group(1))
        if src:
            out.append(f"[source]({html.unescape(src.group(1))})")
    return "\n".join(out).rstrip() + "\n"
