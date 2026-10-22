# Instructions for AI agents working in this repo

Read `PUBLISHING.md` before changing anything. The essentials:

- Issues are Markdown in `content/issues/issue-NNN.md`. Publish by adding one and pushing to `main`.
- Every other page is `content/pages/<path>.html` (front matter + body). Edit those, never the generated
  HTML at the repo root (`index.html`, `issues/`, `guides/`, `tools/<name>/`, feeds, sitemap, llms files).
- Build the Kit email with `python3 tools/build.py --email NNN`; don't commit the `email/` folder.
- Run `python3 tools/build.py --check` and `python3 tools/validate_site.py` before pushing.
