#!/usr/bin/env python3
"""Tell IndexNow (Bing, Yandex, and others) about new or updated pages.

Waits until each URL is live first, so search engines don't fetch a 404.

  python3 tools/indexnow.py --since <git-rev>     pages whose source changed since that commit
  python3 tools/indexnow.py <url> [<url> ...]     specific URLs
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://hotfixdaily.com"


def key() -> str:
    for f in ROOT.glob("*.txt"):
        if re.fullmatch(r"[0-9a-f]{32}", f.stem) and f.read_text().strip() == f.stem:
            return f.stem
    raise SystemExit("No IndexNow key file at the site root.")


def changed_urls(since: str) -> list[str]:
    out = subprocess.run(["git", "diff", "--name-only", f"{since}..HEAD", "--", "content/"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    urls = []
    for line in out.splitlines():
        line = line.strip()
        if not (ROOT / line).exists():
            continue
        m = re.fullmatch(r"content/issues/issue-(\d+)\.md", line)
        if m:
            n = f"{int(m.group(1)):03d}"
            if (ROOT / "issues" / n / "index.html").exists():
                urls += [f"{BASE}/issues/{n}/", f"{BASE}/", f"{BASE}/issues/"]
            continue
        m = re.fullmatch(r"content/pages/(.+)\.html", line)
        if m and m.group(1) not in ("404", "welcome", "confirmed"):
            route = m.group(1)
            urls.append(f"{BASE}/" if route == "index" else f"{BASE}/{route}/")
    return list(dict.fromkeys(urls))


def wait_until_live(url: str, tries: int = 30) -> bool:
    for _ in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=15) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(10)
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since")
    ap.add_argument("urls", nargs="*")
    args = ap.parse_args()
    urls = args.urls or (changed_urls(args.since) if args.since else [])
    if not urls:
        print("Nothing new to announce.")
        return 0
    live = [u for u in urls if wait_until_live(u)]
    if not live:
        print("Nothing went live in time; skipping.")
        return 1
    k = key()
    payload = {"host": "hotfixdaily.com", "key": k, "keyLocation": f"{BASE}/{k}.txt", "urlList": live}
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow: {r.status} for {len(live)} URL(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
