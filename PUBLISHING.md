# Publishing Hotfix Daily

**Short version: put the issue Markdown in `content/issues/`, push it to `main`, then build the
email from the same file and send it through Kit.** GitHub rebuilds and validates the whole
site, deploys it, and pings IndexNow. Nothing else needs to run.

This replaces the old box pipeline (`/workspace/hotfix/build/publish.sh`, `build.py`,
`validate.py`, `indexnow.py`, and the live HTML in `/workspace/hotfix/site`). Retire those.
**Don't write or patch HTML anywhere in the repo.** Generated pages are overwritten on every
build. If an issue or page does arrive as finished HTML, the build imports it back into
`content/` so nothing is lost, but that's a safety net, not the process.

## What lives where

| Path | What it is | Edit it? |
|---|---|---|
| `content/issues/issue-NNN.md` | Issues, in the format below | Yes |
| `content/pages/<path>.html` | Every other page: front matter (title, description, structured data) plus the page body. `content/pages/guides/mcp-servers.html` becomes `/guides/mcp-servers/`. | Yes |
| `templates/` | The shared head, header and footer (`base.html`), the issue page, feeds and llms files | For design changes |
| `assets/`, `downloads/`, `favicon.*` | CSS, JS, images, the Starter Stack PDF | Yes |
| `site.yml` | Sitemap order and a few site settings | Rarely |
| `tools/` | Build, validator, issue parser and Kit email renderer, IndexNow | Rarely |
| `index.html`, `issues/`, `guides/`, `tools/<name>/`, `about/`... `feed.xml`, `rss.xml`, `sitemap.xml`, `llms.txt`, `llms-full.txt` | **Generated.** Rebuilt on every push. | **No** |

## The daily issue

1. Write `content/issues/issue-NNN.md` (format below) and push it to `main`.
2. Build the Kit email from the same file:

   ```bash
   pip install -r requirements.txt               # once
   python3 tools/build.py --email NNN            # writes email/issue-NNN.html (not committed)
   python3 tools/build.py --email NNN --stdout   # or print it
   ```

3. Send that HTML as the Kit broadcast. If Kit fails, don't use another sender.

Within a couple of minutes of the push, `/issues/NNN/` is live and the archive, homepage
"Latest issue" block, welcome/confirmed links, both feeds, the sitemap, `llms.txt` and
`llms-full.txt` are updated. To check first, run `python3 tools/build.py --check`.

## Issue Markdown format

```markdown
# Hotfix Daily: The Daily AI Builder Digest
<!-- title: Hotfix Daily #2: Short punchy SEO title (optional, up to 70 chars) -->
<!-- description: Optional meta description, up to 160 chars -->
**Issue #2 · Thursday, Oct 22, 2026**

One-line lede.

[Read this issue on the web](https://hotfixdaily.com/issues/002/) · [Sponsor Hotfix Daily](https://hotfixdaily.com/sponsor/)

---

[AGENTS]
**1. Item headline**
Summary sentence(s). Inline `code`, **bold**, *italic* and [links](https://…) work.
*Why builders care:* One line.
[source](https://primary-source.example)

[MODEL]
**2. …** (5 items, each with its own label line)

---

### Sponsor            ← optional, rendered as a labeled box
**Acme**: one line. [Try it](https://…)

### Hotfix of the Day
One practical fix the reader can do in minutes.
[source](https://…)
```

- Topic labels, exactly one per item: `[MODEL]`, `[AGENTS]`, `[CODING]`, `[GAME DEV]`, `[DEVTOOLS]`, `[REPO]`. An unknown or missing label prints a warning.
- The `**Issue #N · Weekday, Mon D, YYYY**` line sets the number and date. Keep it.
- `<!-- draft -->` anywhere keeps the issue off the site.
- The "Read this issue on the web" link is for the email; the web page leaves it out automatically.
- Don't put raw HTML in issues. It's escaped.

## Editing pages and guides

Edit the body of `content/pages/<path>.html` like any HTML. The front matter on top holds
what goes in the page's `<head>`:

```yaml
---
title: What is MCP, and which MCP servers are worth adding? (Oct 2026)
description: A sourced guide to MCP ...
og_type: article          # optional; default website
noindex: true             # optional
updated: 2026-10-21       # optional; sitemap date (default: the file's last commit)
jsonld:                   # optional page-specific structured data, as JSON strings
- '{"@context":"https://schema.org","@type":"Article", ...}'
listing:                  # optional; puts the page in the guide/tool lists
  kind: guide             # guide | tool | extra
  order: 70               # position in the lists
  home_title: MCP tools worth knowing   # shows a homepage card with this title
  index_title: ...        # optional, guides index card title (default: title)
  index_blurb: ...        # optional, card text (default: description)
  llms_title: ...         # optional, llms.txt title (default: title)
  llms_blurb: ...         # optional, llms.txt text (default: description)
---
```

- **Adding a guide** is one file: `content/pages/guides/<slug>.html` with a `listing:` block.
  The homepage card, the guides index card and structured data, `llms.txt` and the sitemap
  all pick it up. (The guide text in `llms-full.txt` and the "Want the bigger picture?" line
  on issue pages are still written by hand in `templates/`.)
- **FAQs:** write them as `<details><summary>Question</summary><p>Answer</p></details>`.
  The FAQPage structured data is rebuilt from them on every build, so just edit the FAQ.
- The header, footer and shared head are in `templates/base.html`.
- Pages marked `dynamic: true` (home, archive, welcome, confirmed, guides index) contain
  `{{ ... }}` placeholders that the build fills in. Leave those in place.

## Checks

`tools/validate_site.py` (the same validator as before) runs after every build: strict HTML5
parse, unique ids, internal links and #anchors, JSON-LD, feeds, sitemap and `llms.txt`. If it
fails, the build doesn't publish and GitHub emails the repo owner. The log is in the repo's
Actions tab.

## Settings that used to be in build.py

- Kit form `10075086` and the signup boxes: in the page bodies and `templates/issue.html`
- GoatCounter and the footer: `templates/base.html`
- Impact site verification: `site.yml`
- Kit email layout: `render_email` in `tools/issues.py`
- IndexNow: the key file at the root; the workflow pings automatically
