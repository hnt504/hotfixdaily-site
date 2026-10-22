#!/usr/bin/env python3
"""Validate the built Hotfix Daily site (ported from the bots' validate.py).

Checks: strict HTML5 parse (html5lib), unique ids, internal links + #anchors resolve,
every JSON-LD block parses, feed.xml/rss.xml/sitemap.xml are well-formed and parse with
feedparser, sitemap URLs exist on disk, llms.txt links exist, IndexNow key file present.
  validate.py [--external]     --external also HEADs outbound links (slow, informational)
Exit 0 = OK. Non-zero = ERROR lines printed.
"""
import os, re, sys, json, glob, urllib.parse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

SITE = os.environ.get("HOTFIX_SITE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = "https://hotfixdaily.com"
errors, warns = [], []

class Collect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.jsonld, self._js, self._buf = [], [], [], False, []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.append(a["id"])
        for k in ("href", "src"):
            if a.get(k): self.links.append(a[k])
        if tag == "script" and a.get("type") == "application/ld+json":
            self._js, self._buf = True, []
    def handle_data(self, data):
        if self._js: self._buf.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self._js:
            self.jsonld.append("".join(self._buf)); self._js = False

def path_for(url_path):
    p = urllib.parse.unquote(url_path.split("#")[0].split("?")[0])
    full = os.path.join(SITE, p.lstrip("/"))
    if p.endswith("/") or os.path.isdir(full):
        full = os.path.join(full, "index.html")
    return full

def main():
    try:
        import html5lib
    except ImportError:
        html5lib = None; warns.append("html5lib missing: strict parse skipped")
    pages = {}
    for f in sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)):
        if any(part in f for part in ("/.git/", "/content/", "/templates/", "/email/", "/node_modules/")): continue
        rel = os.path.relpath(f, SITE)
        src = open(f, encoding="utf-8").read()
        if html5lib:
            try:
                html5lib.HTMLParser(strict=True, namespaceHTMLElements=False).parse(src)
            except Exception as e:
                errors.append("%s: HTML5 parse error: %s" % (rel, e))
        c = Collect(); c.feed(src)
        dup = {i for i in c.ids if c.ids.count(i) > 1}
        if dup: errors.append("%s: duplicate ids %s" % (rel, sorted(dup)))
        for j in c.jsonld:
            try: json.loads(j)
            except Exception as e: errors.append("%s: bad JSON-LD: %s" % (rel, e))
        if "<title>" not in src: errors.append("%s: no <title>" % rel)
        pages[f] = c
    # internal links + anchors
    for f, c in pages.items():
        rel = os.path.relpath(f, SITE)
        for l in c.links:
            if l.startswith(BASE): l = l[len(BASE):] or "/"
            if re.match(r"^(https?:|mailto:|tel:|data:|javascript:|//)", l): continue
            if l.startswith("#"):
                if l[1:] and l[1:] not in c.ids: errors.append("%s: anchor %s not found" % (rel, l))
                continue
            if not l.startswith("/"):
                l = urllib.parse.urljoin("/" + rel.replace("index.html", ""), l)
            tgt = path_for(l)
            if not os.path.exists(tgt):
                errors.append("%s: broken internal link %s" % (rel, l)); continue
            if "#" in l and tgt.endswith(".html"):
                frag = l.split("#", 1)[1]
                if frag:
                    tc = pages.get(tgt)
                    if tc is not None and frag not in tc.ids:
                        errors.append("%s: anchor %s not found" % (rel, l))
    # XML
    for x in ("feed.xml", "rss.xml", "sitemap.xml"):
        p = os.path.join(SITE, x)
        try: ET.parse(p)
        except Exception as e: errors.append("%s: XML error: %s" % (x, e))
    try:
        import feedparser
        for x in ("feed.xml", "rss.xml"):
            fp = feedparser.parse(os.path.join(SITE, x))
            if fp.bozo: errors.append("%s: feedparser: %s" % (x, fp.bozo_exception))
            if not fp.entries: errors.append("%s: no entries" % x)
            for e in fp.entries:
                if not os.path.exists(path_for(e.link.replace(BASE, "") or "/")):
                    errors.append("%s: entry link %s has no page" % (x, e.link))
    except ImportError:
        warns.append("feedparser missing: feed parse skipped")
    # sitemap urls exist
    try:
        for loc in re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()):
            if not os.path.exists(path_for(loc.replace(BASE, "") or "/")):
                errors.append("sitemap.xml: %s has no page" % loc)
    except FileNotFoundError:
        errors.append("sitemap.xml missing")
    # llms.txt
    for x in ("llms.txt", "llms-full.txt"):
        p = os.path.join(SITE, x)
        if not os.path.exists(p): errors.append("%s missing" % x); continue
        if x == "llms.txt":
            for u in re.findall(r"\((https://hotfixdaily\.com[^)\s]*)\)", open(p, encoding="utf-8").read()):
                if not os.path.exists(path_for(u.replace(BASE, "") or "/")):
                    errors.append("llms.txt: %s has no page" % u)
    # every issue page is in archive/sitemap/feeds
    sm = open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()
    arch = open(os.path.join(SITE, "issues", "index.html"), encoding="utf-8").read()
    for d in sorted(glob.glob(os.path.join(SITE, "issues", "[0-9][0-9][0-9]"))):
        n = os.path.basename(d)
        if "/issues/%s/" % n not in sm: errors.append("sitemap.xml missing /issues/%s/" % n)
        if 'href="/issues/%s/"' % n not in arch: errors.append("issues/index.html missing /issues/%s/" % n)
    # IndexNow key file
    keys = [f for f in os.listdir(SITE) if re.fullmatch(r"[0-9a-f]{32}\.txt", f)]
    if not keys: errors.append("no IndexNow key file (<32 hex>.txt) at site root")
    for k in keys:
        if open(os.path.join(SITE, k)).read().strip() != k[:-4]:
            errors.append("IndexNow key file %s content does not match its name" % k)
    if "--external" in sys.argv:
        import requests
        seen = set()
        for c in pages.values():
            for l in c.links:
                if l.startswith("http") and not l.startswith(BASE) and l not in seen:
                    seen.add(l)
                    try:
                        r = requests.head(l, allow_redirects=True, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
                        if r.status_code >= 400: warns.append("external %s -> %s" % (l, r.status_code))
                    except Exception as e:
                        warns.append("external %s -> %s" % (l, type(e).__name__))
    for w in warns: print("WARNING:", w)
    for e in errors: print("ERROR:", e)
    print("validate: %d pages, %d errors, %d warnings" % (len(pages), len(errors), len(warns)))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
