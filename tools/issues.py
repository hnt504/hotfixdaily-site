"""Hotfix Daily issue Markdown: parsing and rendering.

Ported unchanged from the bots' build/build.py (Oct 22, 2026), so issue pages,
feeds and the Kit email come out exactly as they did before. See PUBLISHING.md
for the Markdown format.
"""
import datetime
import html
import json
import os
import re
import urllib.parse

BASE = "https://hotfixdaily.com"
LABELS = {"MODEL", "AGENTS", "CODING", "GAME DEV", "DEVTOOLS", "REPO"}
WARN = []


def esc(s):  # attribute / meta escape (matches original build)
    return html.escape(s, quote=True)

def tesc(s):  # body text escape
    return html.escape(s, quote=False)

# ---------------------------------------------------------------- markdown
def inline(s, rel=True):
    """`code`, **bold**, *italic*, [text](url). Raw HTML is escaped."""
    out, i = [], 0
    pat = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\*(.+?)\*|\[([^\]]+)\]\(([^)\s]+)\)")
    for m in pat.finditer(s):
        out.append(tesc(s[i:m.start()]))
        if m.group(1) is not None:
            out.append("<code>%s</code>" % tesc(m.group(1)))
        elif m.group(2) is not None:
            out.append("<strong>%s</strong>" % inline(m.group(2), rel))
        elif m.group(3) is not None:
            out.append("<em>%s</em>" % inline(m.group(3), rel))
        else:
            r = ' rel="noopener"' if rel else ""
            out.append('<a href="%s"%s>%s</a>' % (esc(m.group(5)), r, inline(m.group(4), rel)))
        i = m.end()
    out.append(tesc(s[i:]))
    return "".join(out)

def plain(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.replace("**", "").replace("`", "").replace("*", "")

SRC_RE = re.compile(r"^\[source\]\((\S+)\)\s*$", re.I)

def parse_issue(path):
    raw = open(path, encoding="utf-8").read()
    d = {"path": path, "raw": raw, "draft": "<!-- draft -->" in raw}
    m = re.search(r"<!--\s*title:\s*(.*?)\s*-->", raw); d["title"] = m.group(1) if m else None
    m = re.search(r"<!--\s*description:\s*(.*?)\s*-->", raw); d["description"] = m.group(1) if m else None
    m = re.search(r"\*\*Issue #(\d+)\s*·\s*([A-Za-z]+, [A-Za-z]{3} \d{1,2}, \d{4})\*\*", raw)
    if m:
        d["num"] = int(m.group(1)); d["date_h"] = m.group(2)
        d["date"] = datetime.datetime.strptime(m.group(2).split(", ", 1)[1], "%b %d, %Y").date()
    else:
        d["num"] = int(re.search(r"issue-(\d+)", path).group(1))
        dt = datetime.date.fromtimestamp(os.path.getmtime(path)); d["date"] = dt
        d["date_h"] = dt.strftime("%A, %b ") + str(dt.day) + dt.strftime(", %Y")
        WARN.append("WARNING: no '**Issue #N · Day, Mon D, YYYY**' line in %s; using file mtime" % path)
    d["slug"] = "%03d" % d["num"]
    lines = raw.splitlines()
    d["h1"] = next((l[2:].strip() for l in lines if l.startswith("# ")), "Hotfix Daily: The Daily AI Builder Digest")
    # split into sections on '---'
    body = [l for l in lines if not l.startswith("# ") and not re.match(r"\s*<!--.*-->\s*$", l)]
    secs, cur = [], []
    for l in body:
        if l.strip() == "---":
            secs.append(cur); cur = []
        else:
            cur.append(l)
    secs.append(cur)
    intro = secs[0]
    paras = [p for p in "\n".join(intro).split("\n\n") if p.strip()]
    paras = [p.strip() for p in paras if not re.match(r"\*\*Issue #", p.strip())]
    d["lede"] = paras[0] if paras else ""
    d["intro_extra"] = paras[1:]
    # items
    items, label = [], None
    item_text = "\n".join("\n".join(s) for s in secs[1:])
    d["items"], d["sponsor"], d["hotd"] = [], None, None
    blocks = re.split(r"\n(?=### )", "\n" + item_text)
    for blk in blocks:
        blk = blk.strip("\n")
        if not blk.strip():
            continue
        if blk.startswith("### "):
            title = blk.splitlines()[0][4:].strip()
            rest = [l for l in blk.splitlines()[1:] if l.strip()]
            src = None
            if rest and SRC_RE.match(rest[-1]):
                src = SRC_RE.match(rest[-1]).group(1); rest = rest[:-1]
            sec = {"title": title, "paras": rest, "src": src}
            if "sponsor" in title.lower():
                d["sponsor"] = sec
            elif "hotfix of the day" in title.lower() or "try this" in title.lower() or "tip" in title.lower():
                d["hotd"] = sec
            else:
                WARN.append("WARNING: unknown section '### %s' ignored" % title)
            continue
        # numbered items
        cur = None
        for l in blk.splitlines():
            s = l.strip()
            if not s:
                continue
            mlab = re.match(r"^\[([A-Z][A-Z ]+)\]$", s)
            mhead = re.match(r"^(?:\*\*|#{2,3} )(\d+)\.\s*(?:\[([A-Z][A-Z ]+)\]\s*)?(.+?)(?:\*\*)?$", s)
            if mlab:
                label = mlab.group(1); continue
            if mhead:
                cur = {"n": int(mhead.group(1)), "label": mhead.group(2) or label, "head": mhead.group(3).strip(), "body": [], "why": None, "src": None}
                label = None
                items.append(cur); continue
            if cur is None:
                continue
            mw = re.match(r"^\*Why builders care:\*\s*(.*)$", s)
            ms = SRC_RE.match(s)
            if mw: cur["why"] = mw.group(1)
            elif ms: cur["src"] = ms.group(1)
            else: cur["body"].append(s)
    for it in items:
        if it["label"] not in LABELS:
            WARN.append("WARNING: issue %s item %d has %s label" % (d["slug"], it["n"], "no" if not it["label"] else "unknown '%s'" % it["label"]))
            if not it["label"]: it["label"] = "DEVTOOLS"
    d["items"] = items
    if not d["title"]:
        d["title"] = "Hotfix Daily #%d: %s" % (d["num"], items[0]["head"] if items else "The daily AI builder digest")
        WARN.append("WARNING: no <!-- title: --> comment; generated '%s'" % d["title"])
    if not d["description"]:
        dsc = "Hotfix Daily #%d: %s." % (d["num"], "; ".join(plain(i["head"]) for i in items))
        d["description"] = dsc if len(dsc) <= 160 else dsc[:157].rsplit(" ", 1)[0] + "…"
    return d

def issue_md_path(n):
    return os.path.join(DIGEST, "issue-%03d.md" % int(n))

# ---------------------------------------------------------------- email
CHIP = ('<span style="display:inline-block;font:600 11px/1.6 Menlo,Consolas,monospace;letter-spacing:.06em;'
        'color:#6b7280;border:1px solid #e5e7eb;border-radius:4px;padding:0 5px">%s</span>')

def render_email(d):
    o = ["<h1>%s</h1>" % tesc(d["h1"]),
         "<p><strong>Issue #%d · %s</strong></p>" % (d["num"], tesc(d["date_h"])),
         "<p>%s</p>" % inline(d["lede"])]
    o += ["<p>%s</p>" % inline(p) for p in d["intro_extra"]]
    o.append("<hr>")
    for it in d["items"]:
        parts = [CHIP % tesc(it["label"]), "<strong>%d. %s</strong>" % (it["n"], inline(it["head"])), inline(" ".join(it["body"]))]
        if it["why"] is not None: parts.append("<em>Why builders care:</em> " + inline(it["why"]))
        if it["src"]: parts.append('<a href="%s">source</a>' % esc(it["src"]))
        o.append("<p>" + "<br>".join(parts) + "</p>")
    o.append("<hr>")
    sp = d["sponsor"]
    if sp:
        inner = '<p style="margin:0 0 6px;font:700 12px/1.4 Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;color:#6b7280">Sponsor</p>'
        inner += "".join('<p style="margin:6px 0">%s</p>' % inline(p) for p in sp["paras"])
        o.append('<div style="border:1px solid #e5e7eb;border-radius:8px;padding:12px 16px;margin:18px 0">%s</div>' % inner)
    h = d["hotd"]
    if h:
        inner = '<p style="margin:0 0 6px;font:700 12px/1.4 Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;color:#d2470f">Hotfix of the Day</p>'
        inner += "".join('<p style="margin:6px 0">%s</p>' % inline(p) for p in h["paras"])
        if h["src"]: inner += '<p style="margin:6px 0"><a href="%s">source</a></p>' % esc(h["src"])
        o.append('<div style="border:1px solid #e5e7eb;border-left:3px solid #d2470f;border-radius:8px;padding:12px 16px;margin:18px 0">%s</div>' % inner)
    o.append('<hr><p style="font-size:13px;color:#666">You are getting this because you subscribed at <a href="https://hotfixdaily.com/">hotfixdaily.com</a>. Want to reach AI builders? <a href="https://hotfixdaily.com/sponsor/">Sponsor Hotfix Daily</a>.</p>')
    return "\n".join(o)


def render_items_html(d):
    o = []
    for it in d["items"]:
        o.append('<article class="item" id="i%d"><p class="lbl"><span class="chip">%s</span></p><h2><span class="n">%d</span> %s</h2>' % (it["n"], tesc(it["label"]), it["n"], inline(it["head"])))
        o.append("<p>%s</p>" % inline(" ".join(it["body"])))
        if it["why"] is not None:
            o.append('<p class="why"><strong>Why builders care:</strong> %s</p>' % inline(it["why"]))
        if it["src"]:
            o.append('<p class="src"><a href="%s" rel="noopener">Source</a></p>' % esc(it["src"]))
        o.append("</article>")
    sp = d["sponsor"]
    if sp:
        o.append('<aside class="item" id="sponsor" aria-label="Sponsor"><p class="lbl"><span class="chip">SPONSOR</span></p>')
        o += ["<p>%s</p>" % inline(p) for p in sp["paras"]]
        o.append("</aside>")
    h = d["hotd"]
    if h:
        o.append('<aside class="hotd" id="hotd" aria-label="Hotfix of the Day"><h2>Hotfix of the Day</h2>')
        o += ["<p>%s</p>" % inline(p) for p in h["paras"]]
        if h["src"]:
            o.append('<p class="src"><a href="%s" rel="noopener">Source</a></p>' % esc(h["src"]))
        o.append("</aside>")
    return o

def intro_links_html(d):
    return ["<p>%s</p>" % inline(p) for p in d["intro_extra"]]

def jdump(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def pager(n, prev_num, next_num):
    a = '<a href="/issues/%03d/">← Issue #%d</a>' % (prev_num, prev_num) if prev_num else "<span></span>"
    b = '<a href="/issues/%03d/">Issue #%d →</a>' % (next_num, next_num) if next_num else "<span></span>"
    return '<nav class="pager" aria-label="More issues">%s<a href="/issues/">All issues</a>%s</nav>' % (a, b)

def feed_content(d):
    return "\n".join(intro_links_html(d) + render_items_html(d)) + "\n"

def llms_full_section(d):
    raw = d["raw"]
    body = re.sub(r"^# .*\n", "", raw, count=1)
    body = re.sub(r"<!--.*?-->", "", body)
    return "## %s\nURL: %s/issues/%s/ · Date: %s\n\n%s\n" % (d["title"], BASE, d["slug"], d["date"].isoformat(), body.rstrip("\n"))


def hotd_teaser(d):
    if not d["hotd"] or not d["hotd"]["paras"]:
        return None
    t = plain(d["hotd"]["paras"][0])
    if len(t) > 150:
        t = t[:148].rsplit(" ", 1)[0] + "…"
    return t
