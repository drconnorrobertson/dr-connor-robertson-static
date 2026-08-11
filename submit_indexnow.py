#!/usr/bin/env python3
"""Submit every URL in dist/sitemap.xml to IndexNow.

IndexNow is a shared submission endpoint honoured by Bing, Yandex, Seznam and
Naver. Brave Search is deliberately not covered here: Brave runs an independent
index and publishes no URL-submission or sitemap-ping endpoint for site owners,
so the only levers there are an explicit Bravebot allow in robots.txt (see
robots_txt() in build.py) and the sitemap reference.

Usage:
    python3 submit_indexnow.py            # submit
    python3 submit_indexnow.py --dry-run  # print what would be sent
"""

import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_DIR = Path(__file__).parent
SITEMAP = BASE_DIR / "dist" / "sitemap.xml"
HOST = "drconnorrobertson.com"
SITE_URL = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/indexnow"

# Must match INDEXNOW_KEY in build.py, and be reachable at /<key>.txt.
KEY = "023251f41de1d8833a0e76d2c1799807"


def sitemap_urls():
    if not SITEMAP.exists():
        sys.exit("dist/sitemap.xml not found -- run `python3 build.py` first.")
    return re.findall(r"<loc>(.*?)</loc>", SITEMAP.read_text())


def key_is_live():
    """IndexNow rejects the batch unless /<key>.txt serves the key."""
    try:
        with urlopen(f"{SITE_URL}/{KEY}.txt", timeout=20) as r:
            return r.read().decode().strip() == KEY
    except (HTTPError, URLError) as e:
        print(f"  key file check failed: {e}")
        return False


def submit(urls):
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": f"{SITE_URL}/{KEY}.txt",
        "urlList": urls,
    }).encode()
    req = Request(ENDPOINT, data=payload, method="POST",
                  headers={"Content-Type": "application/json; charset=utf-8"})
    with urlopen(req, timeout=30) as r:
        return r.status, r.read().decode()


def main():
    urls = sitemap_urls()
    print(f"{len(urls)} URLs in sitemap")
    if "--dry-run" in sys.argv:
        print("\n".join(urls))
        return
    print(f"Checking {SITE_URL}/{KEY}.txt ...")
    if not key_is_live():
        sys.exit(f"Key file is not live yet. Deploy first, then re-run.")
    print("  key verified")
    try:
        status, body = submit(urls)
        print(f"IndexNow responded {status} {body!r}")
        print("200/202 means the batch was accepted for processing.")
    except HTTPError as e:
        print(f"IndexNow rejected the batch: {e.code} {e.read().decode()[:300]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
