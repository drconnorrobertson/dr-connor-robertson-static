#!/usr/bin/env python3
"""
Build script for drconnorrobertson.com static site.
Fetches all content from WP REST API, downloads images locally,
and generates a complete static site with full SEO optimization.

Usage:
  python3 build.py              # fetches from WP API, generates into dist/
  python3 build.py --no-fetch   # uses cached posts_cache.json
"""

import json, os, re, html, sys, time, hashlib
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import urlparse, urljoin

BASE_DIR = Path(__file__).parent
DIST = BASE_DIR / "dist"
SITE_URL = "https://drconnorrobertson.com"
WP_API = "https://drconnorrobertson.com/wp-json/wp/v2"
CACHE_FILE = BASE_DIR / "posts_cache.json"
IMAGE_DIR = DIST / "images"
WP_DOMAIN = "drconnorrobertson.com"

# Google Search Console verification (update with your actual code)
GSC_VERIFICATION = ""  # e.g. "google1234567890abcdef.html"
GSC_META = ""  # e.g. '<meta name="google-site-verification" content="...">'

# ── Image download helpers ─────────────────────────────────────

downloaded_images = {}  # maps original URL -> local path

def url_to_local_path(url):
    """Convert an image URL to a local file path under /images/."""
    parsed = urlparse(url)
    # Use the path from wp-content/uploads onward, or hash the URL
    path = parsed.path
    if "/wp-content/uploads/" in path:
        # Keep the uploads path structure: images/2024/01/filename.jpg
        local = path.split("/wp-content/uploads/")[-1]
    else:
        # For other URLs, use a hash-based name preserving extension
        ext = os.path.splitext(path)[1] or ".jpg"
        name_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        basename = os.path.basename(path) or f"img-{name_hash}{ext}"
        local = basename
    return f"/images/{local}"

def download_image(url):
    """Download an image and save it locally. Returns the local path."""
    if url in downloaded_images:
        return downloaded_images[url]

    local_path = url_to_local_path(url)
    full_path = DIST / local_path.lstrip("/")

    # Skip if already downloaded in this build
    if full_path.exists():
        downloaded_images[url] = local_path
        return local_path

    try:
        req = Request(url, headers={"User-Agent": "StaticSiteBuilder/1.0"})
        resp = urlopen(req, timeout=15)
        data = resp.read()

        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(data)
        downloaded_images[url] = local_path
        return local_path
    except Exception as e:
        print(f"    WARN: failed to download {url}: {e}")
        return None

def rewrite_image_urls(html_content):
    """Find all image URLs in HTML content, download them, and rewrite to local paths."""
    if not html_content:
        return html_content

    # Match src attributes pointing to WordPress uploads
    def replace_src(match):
        prefix = match.group(1)
        url = match.group(2)
        suffix = match.group(3)
        if WP_DOMAIN in url or "wp-content/uploads" in url:
            local = download_image(url)
            if local:
                return f'{prefix}{local}{suffix}'
        return match.group(0)

    # Match src="..." and srcset="..."
    result = re.sub(
        r'(src=["\'])([^"\']+)(["\'])',
        replace_src,
        html_content
    )

    # Handle srcset (multiple URLs with sizes)
    def replace_srcset(match):
        prefix = match.group(1)
        srcset = match.group(2)
        suffix = match.group(3)

        parts = []
        for entry in srcset.split(","):
            entry = entry.strip()
            if not entry:
                continue
            tokens = entry.split()
            url = tokens[0]
            size = tokens[1] if len(tokens) > 1 else ""
            if WP_DOMAIN in url or "wp-content/uploads" in url:
                local = download_image(url)
                if local:
                    parts.append(f"{local} {size}".strip())
                else:
                    parts.append(entry)
            else:
                parts.append(entry)
        return f'{prefix}{", ".join(parts)}{suffix}'

    result = re.sub(
        r'(srcset=["\'])([^"\']+)(["\'])',
        replace_srcset,
        result
    )

    # Also catch background-image: url(...) in inline styles
    def replace_bg(match):
        prefix = match.group(1)
        url = match.group(2)
        suffix = match.group(3)
        if WP_DOMAIN in url or "wp-content/uploads" in url:
            local = download_image(url)
            if local:
                return f'{prefix}{local}{suffix}'
        return match.group(0)

    result = re.sub(
        r'(url\(["\']?)([^)"\']+)(["\']?\))',
        replace_bg,
        result
    )

    return result


# ── Fetch helpers ──────────────────────────────────────────────

def fetch_json(url):
    req = Request(url, headers={"User-Agent": "StaticSiteBuilder/1.0"})
    for attempt in range(3):
        try:
            resp = urlopen(req, timeout=30)
            return json.loads(resp.read().decode("utf-8")), resp.headers
        except Exception as e:
            if attempt == 2:
                raise
            print(f"  retry {attempt+1} for {url}: {e}")
            time.sleep(2)

def fetch_all_posts():
    """Fetch every post from the WP REST API with full content and embedded media."""
    all_posts = []
    page = 1
    while True:
        url = f"{WP_API}/posts?per_page=100&page={page}&_embed"
        print(f"  fetching page {page}...")
        try:
            data, headers = fetch_json(url)
        except Exception as e:
            print(f"  stopped at page {page}: {e}")
            break
        if not data:
            break
        for p in data:
            parsed = urlparse(p["link"])
            # Get featured image from _embedded
            featured_img = ""
            try:
                media = p.get("_embedded", {}).get("wp:featuredmedia", [{}])
                if media and len(media) > 0:
                    featured_img = media[0].get("source_url", "")
            except (KeyError, IndexError, TypeError):
                pass

            all_posts.append({
                "slug": p["slug"],
                "title": p["title"]["rendered"],
                "date": p["date"],
                "relative_url": parsed.path,
                "excerpt": p["excerpt"]["rendered"],
                "content": p["content"]["rendered"],
                "categories": p["categories"],
                "featured_image": featured_img,
            })
        total = headers.get("X-WP-TotalPages", "1")
        if page >= int(total):
            break
        page += 1
    return all_posts

def fetch_all_pages():
    """Fetch all WordPress pages to capture any custom page content."""
    all_pages = []
    page = 1
    while True:
        url = f"{WP_API}/pages?per_page=100&page={page}&_embed"
        print(f"  fetching pages (page {page})...")
        try:
            data, headers = fetch_json(url)
        except Exception as e:
            print(f"  stopped at page {page}: {e}")
            break
        if not data:
            break
        for p in data:
            parsed = urlparse(p["link"])
            all_pages.append({
                "slug": p["slug"],
                "title": p["title"]["rendered"],
                "relative_url": parsed.path,
                "content": p["content"]["rendered"],
            })
        total = headers.get("X-WP-TotalPages", "1")
        if page >= int(total):
            break
        page += 1
    return all_pages

def fetch_all_media():
    """Fetch all media items from WP to ensure we have every image."""
    all_media = []
    page = 1
    while True:
        url = f"{WP_API}/media?per_page=100&page={page}"
        print(f"  fetching media (page {page})...")
        try:
            data, headers = fetch_json(url)
        except Exception as e:
            print(f"  stopped at page {page}: {e}")
            break
        if not data:
            break
        for m in data:
            all_media.append({
                "id": m["id"],
                "source_url": m.get("source_url", ""),
                "alt_text": m.get("alt_text", ""),
                "title": m.get("title", {}).get("rendered", ""),
            })
        total = headers.get("X-WP-TotalPages", "1")
        if page >= int(total):
            break
        page += 1
    return all_media

def fetch_categories():
    """Fetch category data."""
    url = f"{WP_API}/categories?per_page=100"
    data, _ = fetch_json(url)
    return {c["id"]: c["name"] for c in data}


# ── Design System ─────────────────────────────────────────────

SOCIAL_LINKS = {
    "LinkedIn": "https://www.linkedin.com/in/dr-connor-robertson",
    "Facebook": "https://www.facebook.com/therealconnorrobertson",
    "X (Twitter)": "https://x.com/DrConnorRE",
    "YouTube": "https://www.youtube.com/connorrobertsonacquisitions",
    "Crunchbase": "https://www.crunchbase.com/person/dr-connor-robertson",
    "Instagram": "https://www.instagram.com/creative_acquisitions/",
    "Behance": "https://www.behance.net/connorrobertson10#",
    "Tumblr": "https://www.tumblr.com/drconnorrobertsonre",
    "Flipboard": "https://flipboard.com/@DrConnorRobert",
}

NAV_ITEMS = [
    ("About", "/about/"),
    ("Speaker", "/speaker/"),
    ("Blog", "/blog/"),
    ("Books", "/books/"),
    ("Press & Media", "/press-media/"),
]

RESOURCE_HUBS = [
    ("Business Acquisitions & Scaling", "/blog/hub-business-acquisitions-scaling-dr-connor-robertson/"),
    ("Leadership & Legacy", "/blog/hub-leadership-legacy-dr-connor-robertson/"),
    ("Influence & Authority", "/blog/hub-influence-authority-dr-connor-robertson/"),
    ("Mindset & Systems", "/blog/hub-mindset-momentum-systems-dr-connor-robertson/"),
    ("Pittsburgh Business", "/blog/hub-pittsburgh-business-real-estate-dr-connor-robertson/"),
]

PRESS_ARTICLES = [
    ("Building Businesses with Purpose: A Modern Framework for Entrepreneurial Impact", "https://nywire.com/building-businesses-with-purpose-a-modern-framework-for-entrepreneurial-impact/", "NY Wire"),
    ("Dr. Connor Robertson on Turning Underperforming Companies into Category Leaders", "https://nywire.com/dr-connor-robertson-on-turning-underperforming-companies-into-category-leaders/", "NY Wire"),
    ("The Case for Nonprofit Partnerships in the Private Sector", "https://blknews.com/the-case-for-nonprofit-partnerships-in-the-private-sector/", "BLK News"),
    ("Philanthropy Isn't Just a Tax Deduction, It's an Operating Principle", "https://blknews.com/philanthropy-isnt-just-a-tax-deduction-its-an-operating-principle/", "BLK News"),
    ("Why Every Business Should Document Its Legacy Even in the Early Stages", "https://entertainmentpost.com/why-every-business-should-document-its-legacy-even-in-the-early-stages/", "Entertainment Post"),
    ("The Role of Private Sector Problem Solvers in Philanthropic Ecosystems", "https://famoustimes.com/the-role-of-private-sector-problem-solvers-in-philanthropic-ecosystems/", "Famous Times"),
    ("How to Build a Scalable Marketing System for Any Business", "https://famoustimes.com/how-to-build-a-scalable-marketing-system-for-any-business/", "Famous Times"),
    ("How Local Businesses Can Lead Community Renewal Without Government Grants", "https://theamericannews.com/how-local-businesses-can-lead-community-renewal-without-government-grants/", "The American News"),
    ("Why Direct Response Still Works: Dr Connor Robertson's Playbook for Owners", "https://economicinsider.com/why-direct-response-still-works-dr-connor-robertsons-playbook-for-owners/", "Economic Insider"),
]

BOOKS = [
    ("Buying Wealth", "A straightforward guide to ownership and practical wealth-building. Learn how to buy assets that produce cash flow, use leverage responsibly, and build disciplined systems for growth.", "https://play.google.com/store/books/details/Dr_Connor_Robertson_Buying_Wealth?id=Dw2HEQAAQBAJ", "Google Play"),
    ("The 7 Minute Phone Call", "Replace hesitation with action. Connect like a human being again. In seven minutes, you can build more trust than a dozen emails ever will.", "https://play.google.com/store/books/details/Dr_Connor_Robertson_The_7_Minute_Phone_Call?id=9QyHEQAAQBAJ", "Google Play"),
    ("PadSplit Playbook: Scaling Affordable Housing Through Shared Living", "A practical, experience driven guide for property owners, operators, and housing focused entrepreneurs who want to understand how PadSplit works in real life.", "https://play.google.com/store/books/details/Dr_Connor_Robertson_Padsplit_Playbook_Scaling_Affo?id=9sSqEQAAQBAJ", "Google Play"),
    ("Buy The Building, Keep The Profits", "A clear and practical guide that helps business owners understand why the real money is not only in running a successful company but in owning the real estate that company occupies.", "https://play.google.com/store/books/details/Dr_Connor_Robertson_Buy_the_Building_Keep_the_Prof?id=MRWfEQAAQBAJ", "Google Play"),
    ("Creative Acquisitions: The Playbook for Modern Dealmakers", "A practical, operator focused guide for entrepreneurs who want to buy real businesses using flexible, creative, and durable acquisition strategies.", "https://www.barnesandnoble.com/w/creative-acquisitions-by-dr-connor-robertson-connor-robertson/1148958050", "Barnes & Noble"),
]


# ── CSS ───────────────────────────────────────────────────────

CSS = """
:root{--bg:#000;--bg2:#0a0a0a;--card:#111;--text:#fff;--text2:#b0b0b0;--muted:#888;--border:#222;--r:8px;--mw:1200px;--t:.3s ease}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'DM Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:var(--text);text-decoration:none;transition:opacity var(--t)}a:hover{opacity:.8}
img{max-width:100%;height:auto;display:block}
.ctn{max-width:var(--mw);margin:0 auto;padding:0 24px}

/* Header */
.hdr{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(0,0,0,.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}
.hdr-in{max-width:var(--mw);margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:72px}
.logo{font-size:18px;font-weight:700;letter-spacing:-.02em;white-space:nowrap}
.logo a{color:var(--text)}
.nav{display:flex;align-items:center;gap:28px;list-style:none}
.nav a{font-size:14px;font-weight:500;color:var(--text2);transition:color var(--t)}
.nav a:hover{color:var(--text);opacity:1}
.nav-cta{display:inline-block;padding:8px 20px;background:var(--text);color:#000!important;border-radius:var(--r);font-size:14px;font-weight:600;transition:transform var(--t),box-shadow var(--t)}
.nav-cta:hover{transform:translateY(-1px);box-shadow:0 4px 20px rgba(255,255,255,.15);opacity:1}
.mob-tog{display:none;background:0 0;border:none;color:var(--text);font-size:24px;cursor:pointer}
.has-dd{position:relative}
.dd{display:none;position:absolute;top:100%;left:0;background:#111;border:1px solid var(--border);border-radius:var(--r);padding:8px 0;min-width:240px;z-index:100}
.has-dd:hover .dd{display:block}
.dd a{display:block;padding:8px 20px;font-size:13px;color:var(--text2)}
.dd a:hover{color:var(--text);background:rgba(255,255,255,.05)}

/* Hero */
.hero{position:relative;min-height:90vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px;overflow:hidden}
.hero-bg{position:absolute;inset:0;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#0a0a0a 100%);z-index:0}
.hero-bg::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(255,255,255,.03) 0%,transparent 70%)}
.hero-ct{position:relative;z-index:1;max-width:800px}
.hero h1{font-size:clamp(40px,6vw,72px);font-weight:700;letter-spacing:-.03em;margin-bottom:20px;line-height:1.1}
.hero .tag{font-size:clamp(16px,2vw,20px);color:var(--text2);margin-bottom:36px;line-height:1.6}
.hero-btn{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}
.hero-img{width:180px;height:180px;border-radius:50%;object-fit:cover;margin:0 auto 32px;border:3px solid rgba(255,255,255,.15)}
.btn-p{display:inline-block;padding:14px 32px;background:var(--text);color:#000;border-radius:var(--r);font-weight:600;font-size:15px;transition:transform var(--t),box-shadow var(--t)}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(255,255,255,.15);opacity:1}
.btn-s{display:inline-block;padding:14px 32px;background:rgba(0,0,0,.48);color:var(--text);border:1px solid rgba(255,255,255,.2);border-radius:var(--r);font-weight:600;font-size:15px;transition:background var(--t)}
.btn-s:hover{background:rgba(255,255,255,.1);opacity:1}

/* Featured */
.feat{padding:48px 0;text-align:center;border-bottom:1px solid var(--border)}
.feat h3{font-size:12px;text-transform:uppercase;letter-spacing:3px;color:var(--muted);margin-bottom:32px}
.feat-logos{display:flex;align-items:center;justify-content:center;gap:48px;flex-wrap:wrap;opacity:.7}
.feat-logos img{height:32px;width:auto;filter:brightness(0) invert(1);opacity:.7}
.feat-logos span{font-size:16px;font-weight:600;color:var(--text2);letter-spacing:1px}

/* Sections */
.sec{padding:80px 0}.sec-dk{background:var(--bg2)}
.sec-t{font-size:clamp(28px,4vw,48px);font-weight:700;letter-spacing:-.02em;margin-bottom:20px;line-height:1.2}
.sec-sub{color:var(--text2);font-size:17px;max-width:700px;margin-bottom:48px}

/* Pillars */
.pills{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:32px;margin-top:48px}
.pill{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:40px 32px;transition:transform var(--t),border-color var(--t)}
.pill:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.15)}
.pill h3{font-size:22px;font-weight:700;margin-bottom:16px}
.pill p{color:var(--text2);font-size:15px;line-height:1.7}

/* Quote */
.quote{padding:80px 0;text-align:center;background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.quote-t{font-size:clamp(20px,3vw,32px);font-weight:500;font-style:italic;max-width:800px;margin:0 auto 24px;line-height:1.5}
.quote-a{color:var(--muted);font-size:15px}
.quote-a strong{color:var(--text2);font-weight:600}

/* Page Hero */
.pg-hero{padding:140px 24px 60px;text-align:center;background:linear-gradient(180deg,#000 0%,var(--bg2) 100%)}
.pg-hero h1{font-size:clamp(32px,5vw,56px);font-weight:700;letter-spacing:-.02em;margin-bottom:16px}
.pg-hero p{color:var(--text2);font-size:17px;max-width:700px;margin:0 auto}

/* Stats */
.stats{display:flex;gap:48px;justify-content:center;flex-wrap:wrap;margin:48px 0}
.stat{text-align:center}.stat-n{font-size:48px;font-weight:700}.stat-l{font-size:13px;color:var(--muted);margin-top:4px}
.about-photo{text-align:center;margin-bottom:32px}.about-photo img{width:220px;height:220px;border-radius:50%;object-fit:cover;border:4px solid var(--border)}

/* Grid blocks */
.agrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:40px;margin-top:48px}
.ablock h3{font-size:22px;font-weight:700;margin-bottom:12px}
.ablock p{color:var(--text2);font-size:15px;line-height:1.8}

/* Blog */
.bgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}
.bcard{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden;transition:transform var(--t),border-color var(--t);display:flex;flex-direction:column}
.bcard:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.15)}
.bcard-img{width:100%;height:200px;object-fit:cover}
.bcard-body{padding:24px 32px 32px}
.bcard h3{font-size:18px;font-weight:600;margin-bottom:12px;line-height:1.4}
.bcard .exc{color:var(--text2);font-size:14px;line-height:1.7;flex:1;margin-bottom:16px}
.bcard .meta{font-size:12px;color:var(--muted)}
.pag{display:flex;gap:8px;justify-content:center;margin-top:48px;flex-wrap:wrap}
.pag a,.pag span{display:inline-block;padding:8px 16px;border:1px solid var(--border);border-radius:var(--r);font-size:14px;color:var(--text2)}
.pag .cur{background:var(--text);color:#000;border-color:var(--text);font-weight:600}

/* Post */
.post{max-width:760px;margin:0 auto;padding:120px 24px 80px}
.post-feat{width:100%;max-height:480px;object-fit:cover;border-radius:12px;margin-bottom:32px}
.post h1{font-size:clamp(28px,4vw,42px);font-weight:700;letter-spacing:-.02em;margin-bottom:12px;line-height:1.2}
.post .pm{color:var(--muted);font-size:14px;margin-bottom:40px;padding-bottom:24px;border-bottom:1px solid var(--border)}
.post .pb{font-size:16px;line-height:1.85;color:var(--text2)}
.post .pb h2{font-size:26px;font-weight:700;color:var(--text);margin:48px 0 16px}
.post .pb h3{font-size:20px;font-weight:600;color:var(--text);margin:36px 0 12px}
.post .pb p{margin-bottom:20px}
.post .pb ul,.post .pb ol{margin:16px 0 20px 24px}
.post .pb li{margin-bottom:8px}
.post .pb blockquote{border-left:3px solid var(--text);padding:16px 24px;margin:24px 0;background:rgba(255,255,255,.03);border-radius:0 var(--r) var(--r) 0;font-style:italic}
.post .pb a{text-decoration:underline;text-underline-offset:3px}
.post .pb img{border-radius:var(--r);margin:24px 0}

/* Books */
.bkgrid{display:grid;gap:40px;margin-top:48px}
.bk{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:40px;display:flex;flex-direction:column;gap:16px;transition:border-color var(--t)}
.bk:hover{border-color:rgba(255,255,255,.15)}
.bk h3{font-size:24px;font-weight:700}
.bk p{color:var(--text2);font-size:15px;line-height:1.8}
.bk-cta{display:inline-block;padding:12px 28px;background:var(--text);color:#000;border-radius:var(--r);font-weight:600;font-size:14px;align-self:flex-start;margin-top:8px;transition:transform var(--t)}
.bk-cta:hover{transform:translateY(-2px);opacity:1}

/* Speaker */
.saud{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin:48px 0}
.acard{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:32px}
.acard h3{font-size:20px;font-weight:700;margin-bottom:12px}
.acard p{color:var(--text2);font-size:14px;line-height:1.7}
.topics{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;margin:48px 0}
.tcard{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:32px}
.tcard h3{font-size:18px;font-weight:600;margin-bottom:12px}
.tcard p{color:var(--text2);font-size:14px;line-height:1.7}

/* Press */
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}
.pcard{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:32px;display:flex;flex-direction:column;justify-content:space-between;transition:transform var(--t),border-color var(--t)}
.pcard:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.15)}
.pcard h3{font-size:17px;font-weight:600;margin-bottom:12px;line-height:1.5}
.pcard .src{color:var(--muted);font-size:13px;margin-bottom:16px}
.pcard .rl{font-size:13px;font-weight:600;color:var(--text)}

/* Contact */
.cform{max-width:640px;margin:0 auto;padding-top:40px}
.fg{margin-bottom:20px}
.fg label{display:block;font-size:14px;font-weight:500;margin-bottom:6px;color:var(--text2)}
.fg input,.fg select,.fg textarea{width:100%;padding:12px 16px;background:var(--card);border:1px solid var(--border);border-radius:15px;color:var(--text);font-family:inherit;font-size:15px;transition:border-color var(--t)}
.fg input:focus,.fg select:focus,.fg textarea:focus{outline:0;border-color:rgba(255,255,255,.3)}
.fg textarea{resize:vertical;min-height:120px}
.fr{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.fsub{display:inline-block;padding:14px 40px;background:var(--text);color:#000;border:none;border-radius:15px;font-family:inherit;font-size:15px;font-weight:600;cursor:pointer;transition:transform var(--t)}
.fsub:hover{transform:translateY(-2px)}

/* Footer */
.ftr{background:var(--bg);border-top:1px solid var(--border);padding:64px 0 32px}
.ftr-top{display:grid;grid-template-columns:2fr 1fr 1fr;gap:48px;margin-bottom:48px}
.ftr-tag{color:var(--text2);font-size:15px;margin-top:12px;line-height:1.6}
.ftr-col h4{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;color:var(--muted)}
.ftr-col ul{list-style:none}.ftr-col li{margin-bottom:10px}
.ftr-col a{color:var(--text2);font-size:14px}.ftr-col a:hover{color:var(--text)}
.ftr-btm{text-align:center;padding-top:32px;border-top:1px solid var(--border);color:var(--muted);font-size:13px}

/* Responsive */
@media(max-width:768px){
.nav{display:none}.mob-tog{display:block}
.nav.active{display:flex;flex-direction:column;position:absolute;top:72px;left:0;right:0;background:rgba(0,0,0,.95);padding:24px;gap:16px;border-bottom:1px solid var(--border)}
.hdr-in{padding:0 16px}.hero{min-height:70vh;padding:100px 16px 60px}
.ftr-top{grid-template-columns:1fr;gap:32px}.stats{gap:24px}
.fr{grid-template-columns:1fr}.bgrid{grid-template-columns:1fr}.pills{grid-template-columns:1fr}
.dd{position:static;border:none;background:transparent;padding-left:16px}
}
"""

# ── Template helpers ──────────────────────────────────────────

FONT_LINK = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">'

def esc(s):
    return html.escape(str(s))

def strip_tags(s):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '', s)
    return html.unescape(text).strip()

def nav_html():
    items = ""
    for label, href in NAV_ITEMS:
        items += f'<li><a href="{href}">{label}</a></li>'
    # Resources dropdown
    dd = "".join(f'<a href="{h}">{l}</a>' for l, h in RESOURCE_HUBS)
    items += f'<li class="has-dd"><a href="/blog/complete-resource-index-dr-connor-robertson/">Resources</a><div class="dd">{dd}</div></li>'
    items += '<li><a href="/contact/" class="nav-cta">Contact Connor</a></li>'
    return items

def header(title, desc="", canonical="/", extra="", og_image="", og_type="website"):
    if not desc:
        desc = "Dr. Connor Robertson is a Pittsburgh-based entrepreneur, educator, and philanthropist."
    can = f'<link rel="canonical" href="{SITE_URL}{canonical}">' if canonical else ""
    og_img_tag = ""
    if og_image:
        if og_image.startswith("/"):
            og_img_tag = f'<meta property="og:image" content="{SITE_URL}{og_image}">'
        else:
            og_img_tag = f'<meta property="og:image" content="{og_image}">'
    gsc = f"\n{GSC_META}" if GSC_META else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{can}
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{SITE_URL}{canonical}">
<meta property="og:site_name" content="Dr. Connor Robertson">
<meta property="og:locale" content="en_US">
{og_img_tag}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:site" content="@DrConnorRE">
<meta name="author" content="Dr. Connor Robertson">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">{gsc}
{FONT_LINK}
<style>{CSS}</style>
{extra}
</head>
<body>
<header class="hdr"><div class="hdr-in">
<div class="logo"><a href="/">Dr. Connor Robertson</a></div>
<nav><ul class="nav" id="nv">{nav_html()}</ul></nav>
<button class="mob-tog" onclick="document.getElementById('nv').classList.toggle('active')" aria-label="Menu">&#9776;</button>
</div></header>
"""

def footer():
    social = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL_LINKS.items())
    pages = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in [("/","Home"),("/about/","About"),("/speaker/","Speaker"),("/press-media/","Press & Media"),("/contact/","Contact")])
    return f"""
<footer class="ftr"><div class="ctn">
<div class="ftr-top">
<div><div class="logo" style="font-size:20px;margin-bottom:4px">Dr. Connor Robertson</div>
<p class="ftr-tag">Building Businesses. Empowering People. Transforming Communities.</p></div>
<div class="ftr-col"><h4>Pages</h4><ul>{pages}</ul></div>
<div class="ftr-col"><h4>Follow Connor</h4><ul>{social}</ul></div>
</div>
<div class="ftr-btm">&copy; {datetime.now().year} Dr. Connor Robertson. All Rights Reserved.</div>
</div></footer>
</body></html>"""


# ── Page builders ─────────────────────────────────────────────

def page_home():
    person_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Dr. Connor Robertson",
        "url": SITE_URL,
        "image": f"{SITE_URL}/images/connor-robertson-headshot.jpg",
        "jobTitle": "Entrepreneur, Real Estate Innovator, Educator & Philanthropist",
        "description": "Canadian-born entrepreneur, real estate innovator, educator, and philanthropist based in Pittsburgh.",
        "address": {"@type": "PostalAddress", "addressLocality": "Pittsburgh", "addressRegion": "PA", "addressCountry": "US"},
        "sameAs": list(SOCIAL_LINKS.values()) + [
            "https://elixirconsultinggroup.com",
            "https://thepittsburghwire.com",
            "https://theprospectingshow.com",
        ],
        "knowsAbout": ["Entrepreneurship", "Real Estate", "Business Strategy", "Philanthropy", "Leadership", "Business Acquisitions", "Short-Term Rentals"],
        "alumniOf": {"@type": "EducationalOrganization", "name": "University"},
        "memberOf": [
            {"@type": "Organization", "name": "Social Venture Partners"},
            {"@type": "Organization", "name": "Habitat for Humanity"}
        ],
        "founder": [
            {"@type": "Organization", "name": "Elixir Consulting Group", "url": "https://elixirconsultinggroup.com"},
            {"@type": "Organization", "name": "The Pittsburgh Wire", "url": "https://thepittsburghwire.com"},
        ]
    })

    website_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Dr. Connor Robertson",
        "url": SITE_URL,
        "description": "Official website of Dr. Connor Robertson - entrepreneur, educator, and philanthropist based in Pittsburgh, PA.",
        "publisher": {"@type": "Person", "name": "Dr. Connor Robertson"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_URL}/blog/?s={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }
    })

    extra = f'<script type="application/ld+json">{person_schema}</script>\n<script type="application/ld+json">{website_schema}</script>'
    pillars = [
        ("Entrepreneur", "Dr. Connor Robertson is a visionary business leader who co-founded a leading real estate firm transforming the vacation and short-term rental market through innovation, technology, and strategy."),
        ("Educator", "Dr. Robertson shares his expertise as a speaker and mentor, simplifying complex business principles into actionable methods that inspire entrepreneurs and professionals alike."),
        ("Philanthropist", "Dr. Robertson actively supports Social Venture Partners and Habitat for Humanity, championing social initiatives that improve education, housing, and community development globally."),
    ]
    pcards = "".join(f'<div class="pill"><h3>{t}</h3><p>{d}</p></div>' for t, d in pillars)
    return header("Dr. Connor Robertson | Pittsburgh Entrepreneur & Business Strategist",
        "Dr. Connor Robertson is a Pittsburgh-based entrepreneur, educator, and philanthropist helping entrepreneurs scale businesses, build legacies, and create lasting impact.",
        "/", extra, og_image="/images/connor-robertson-headshot.jpg") + f"""
<section class="hero"><div class="hero-bg"></div><div class="hero-ct">
<h1>Dr. Connor Robertson</h1>
<p class="tag">Helping entrepreneurs scale businesses, build legacies, and create lasting impact.</p>
<div class="hero-btn"><a href="/contact/" class="btn-p">Contact</a><a href="/about/" class="btn-s">About</a></div>
</div></section>
<section class="feat"><div class="ctn">
<h3>As Featured On</h3>
<div class="feat-logos"><span>CXO Dispatch</span><span>C-Suite Brief</span><span>NY Wire</span><span>BLK News</span><span>Famous Times</span><span>Economic Insider</span></div>
</div></section>
<section class="sec"><div class="ctn">
<h2 class="sec-t">Dr. Connor Robertson is a Canadian-born entrepreneur, real estate innovator, educator, philanthropist, and speaker.</h2>
<div class="pills">{pcards}</div>
</div></section>
<section class="quote"><div class="ctn">
<p class="quote-t">"Real success comes from creating impact that lasts longer than you do."</p>
<p class="quote-a"><strong>Dr. Connor Robertson</strong><br>Entrepreneur, Real Estate Innovator, Educator &amp; Philanthropist</p>
</div></section>
""" + footer()


def page_about():
    person_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Dr. Connor Robertson",
        "url": f"{SITE_URL}/about/",
        "image": f"{SITE_URL}/images/connor-robertson-headshot.jpg",
        "jobTitle": "Entrepreneur, Real Estate Innovator, Educator & Philanthropist",
        "description": "Dr. Connor Robertson is a visionary entrepreneur and educator focused on innovation and impact, based in Pittsburgh, PA.",
        "address": {"@type": "PostalAddress", "addressLocality": "Pittsburgh", "addressRegion": "PA", "addressCountry": "US"},
        "sameAs": list(SOCIAL_LINKS.values()),
        "knowsAbout": ["Entrepreneurship", "Real Estate", "Business Strategy", "Philanthropy", "Leadership"],
    })
    extra = f'<script type="application/ld+json">{person_schema}</script>'
    return header("About Dr. Connor Robertson | Entrepreneur, Strategist & Media Founder",
        "Dr. Connor Robertson is a visionary entrepreneur and educator focused on innovation and impact.",
        "/about/", extra, og_image="/images/connor-robertson-headshot.jpg") + """
<section class="pg-hero"><div class="ctn">
<h1>About Dr. Connor Robertson</h1>
<p>Entrepreneur, educator, philanthropist, co-founder of a leading real estate firm, and global advocate for community development.</p>
</div></section>
<section class="sec"><div class="ctn">
<div class="about-photo"><img src="/images/connor-robertson-headshot.jpg" alt="Dr. Connor Robertson" loading="lazy"></div>
<p class="sec-sub" style="max-width:900px">Dr. Connor Robertson is a visionary entrepreneur and educator who has built and scaled ventures focused on innovation and impact. Through his leadership in real estate and his work with organizations like Social Venture Partners and Habitat for Humanity, Dr. Robertson drives meaningful change, supporting sustainable housing, education, and social equity across communities in North America and beyond.</p>
<div class="stats">
<div class="stat"><div class="stat-n">150+</div><div class="stat-l">Homes built through Habitat for Humanity</div></div>
<div class="stat"><div class="stat-n">40+</div><div class="stat-l">Global branches supported through SVP</div></div>
<div class="stat"><div class="stat-n">10K+</div><div class="stat-l">Individuals impacted through community initiatives</div></div>
</div>
<div class="agrid">
<div class="ablock"><h3>Building Businesses That Transform Communities</h3>
<p>Dr. Connor Robertson's entrepreneurial journey began with a vision -- to combine innovation and impact. As co-founder of a leading real estate firm, he redefined the short-term rental space through cutting-edge technology, operational excellence, and a people-first approach. His passion for community growth and real estate development fuels his mission to create sustainable value while improving lives.</p></div>
<div class="ablock"><h3>Empowering Entrepreneurs Through Education</h3>
<p>Beyond business, Dr. Robertson is an educator and speaker dedicated to teaching entrepreneurs how to lead with purpose. Through mentoring, speaking engagements, and digital platforms, he shares insights on leadership, motivation, and entrepreneurship -- simplifying complex strategies into actionable success frameworks that empower others to thrive.</p></div>
<div class="ablock"><h3>A Legacy of Service and Social Impact</h3>
<p>Deeply rooted in giving back, Dr. Robertson's philanthropic work with Social Venture Partners and Habitat for Humanity has transformed communities across North America. Whether building homes or supporting nonprofits that uplift at-risk youth, his contributions embody a commitment to sustainable, meaningful change that strengthens both people and place.</p></div>
</div></div></section>
""" + footer()


def page_speaker():
    return header("Book Dr. Connor Robertson | Keynote Speaker on Business & AI",
        "Book Dr. Connor Robertson for your next event. Expert keynote speaker on entrepreneurship, real estate, and leadership.", "/speaker/") + """
<section class="pg-hero"><div class="ctn">
<h1>Speaking Engagements</h1>
<p>Connor is passionate about sharing his experiences and advice with audiences that are ready to grow.</p>
</div></section>
<section class="sec"><div class="ctn">
<h2 class="sec-t">Audiences Connor Connects With</h2>
<div class="saud">
<div class="acard"><h3>Entrepreneurs</h3><p>Learn how to transform ideas into impactful, scalable ventures.</p></div>
<div class="acard"><h3>Real Estate Leaders</h3><p>Gain insights on leveraging technology and strategy to maximize returns.</p></div>
<div class="acard"><h3>Changemakers</h3><p>Discover how to align business success with lasting social impact.</p></div>
</div></div></section>
<section class="sec sec-dk"><div class="ctn">
<h2 class="sec-t">Subject Matter Expertise</h2>
<div class="topics">
<div class="tcard"><h3>Building a Real Estate Business That Creates Change</h3><p>Discover the steps to launch, grow, and scale a socially conscious real estate firm -- one that drives profit, purpose, and positive impact through innovation and leadership.</p></div>
<div class="tcard"><h3>Leading with Purpose and Integrity</h3><p>Learn how to cultivate authentic leadership by balancing empathy with execution -- empowering your team and community while driving measurable business success.</p></div>
<div class="tcard"><h3>Merging Entrepreneurship and Philanthropy</h3><p>Master the art of integrating business excellence with social responsibility. Dr. Robertson's approach teaches how purpose-driven ventures can fuel long-term, sustainable transformation.</p></div>
</div></div></section>
<section class="sec"><div class="ctn">
<h2 class="sec-t">Request a Booking</h2>
<div class="cform">
<form action="https://formspree.io/f/xdkobkzz" method="POST">
<div class="fr"><div class="fg"><label>First Name</label><input type="text" name="first_name" required></div><div class="fg"><label>Last Name</label><input type="text" name="last_name" required></div></div>
<div class="fg"><label>Email</label><input type="email" name="email" required></div>
<div class="fg"><label>Company</label><input type="text" name="company"></div>
<div class="fg"><label>Event Size</label><input type="number" name="event_size" min="0"></div>
<div class="fg"><label>Budget</label><input type="text" name="budget"></div>
<div class="fg"><label>Event Date</label><input type="date" name="event_date"></div>
<div class="fg"><label>Speaking Request</label><textarea name="speaking_request" rows="4"></textarea></div>
<button type="submit" class="fsub">Submit</button>
</form></div></div></section>
""" + footer()


def page_books():
    cards = ""
    book_schema_items = []
    for title, desc, url, store in BOOKS:
        cards += f'<div class="bk"><h3>{esc(title)}</h3><p>{esc(desc)}</p><a href="{url}" target="_blank" rel="noopener" class="bk-cta">Get Your Copy Now</a></div>\n'
        book_schema_items.append({
            "@type": "Book",
            "name": title,
            "author": {"@type": "Person", "name": "Dr. Connor Robertson"},
            "description": desc,
            "url": url,
        })
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Books by Dr. Connor Robertson",
        "url": f"{SITE_URL}/books/",
        "mainEntity": book_schema_items,
    })
    extra = f'<script type="application/ld+json">{schema}</script>'
    return header("Books by Dr. Connor Robertson | Business & Entrepreneurship",
        "Explore books by Dr. Connor Robertson on wealth building, business acquisitions, and entrepreneurship.", "/books/", extra) + f"""
<section class="pg-hero"><div class="ctn">
<h1>Books</h1><p>Practical guides on wealth building, real estate, and entrepreneurship by Dr. Connor Robertson.</p>
</div></section>
<section class="sec"><div class="ctn"><div class="bkgrid">{cards}</div></div></section>
""" + footer()


def page_press():
    cards = ""
    for title, url, source in PRESS_ARTICLES:
        cards += f'<div class="pcard"><div><h3>{esc(title)}</h3><p class="src">{esc(source)}</p></div><a href="{url}" target="_blank" rel="noopener" class="rl">Read &rarr;</a></div>\n'
    return header("Press & Media | Dr. Connor Robertson in the News",
        "Dr. Connor Robertson in the press. Featured in CXO Dispatch, C-Suite Brief, NY Wire, and more.", "/press-media/") + f"""
<section class="pg-hero"><div class="ctn">
<h1>Press &amp; Media</h1><p>Dr. Connor Robertson's insights and features across leading publications.</p>
</div></section>
<section class="sec"><div class="ctn">
<div class="feat" style="padding:48px 0;margin-bottom:48px;border-bottom:none"><div class="feat-logos"><span>CXO Dispatch</span><span>C-Suite Brief</span><span>NY Wire</span><span>BLK News</span><span>Famous Times</span><span>Economic Insider</span></div></div>
<div class="pgrid">{cards}</div>
</div></section>
""" + footer()


def page_contact():
    return header("Contact Dr. Connor Robertson | Business Inquiries & Speaking",
        "Get in touch with Dr. Connor Robertson for business inquiries, speaking engagements, press, and partnerships.", "/contact/") + """
<section class="pg-hero"><div class="ctn">
<h1>Don't Hesitate To Reach Out</h1><p>Business inquiries, speaking engagements, press, partnerships, and more.</p>
</div></section>
<section class="sec"><div class="ctn"><div class="cform">
<form action="https://formspree.io/f/xdkobkzz" method="POST">
<div class="fr"><div class="fg"><label>First Name *</label><input type="text" name="first_name" required></div><div class="fg"><label>Last Name *</label><input type="text" name="last_name" required></div></div>
<div class="fg"><label>Email *</label><input type="email" name="email" required></div>
<div class="fg"><label>Company</label><input type="text" name="company"></div>
<div class="fg"><label>Website</label><input type="url" name="website"></div>
<div class="fg"><label>Phone</label><input type="tel" name="phone"></div>
<div class="fg"><label>Purpose *</label><select name="purpose" required><option value="">Select...</option><option>General Contact</option><option>Learn More About Connor</option><option>Book Connor For Event</option><option>Press &amp; Media Inquiry</option><option>Partnership</option><option>Other</option></select></div>
<div class="fg"><label>Message</label><textarea name="message" rows="5"></textarea></div>
<button type="submit" class="fsub">Submit</button>
</form></div></div></section>
""" + footer()


def page_blog_index(posts, page_num, total_pages):
    per_page = 24
    start = (page_num - 1) * per_page
    batch = posts[start:start + per_page]
    cards = ""
    for p in batch:
        exc = strip_tags(p.get("excerpt", ""))
        if len(exc) > 200:
            exc = exc[:200] + "..."
        try:
            dt = datetime.fromisoformat(p["date"]).strftime("%B %d, %Y")
        except:
            dt = ""
        # Featured image for card
        feat_img = ""
        if p.get("featured_image"):
            local = downloaded_images.get(p["featured_image"], "")
            if local:
                feat_img = f'<img src="{local}" alt="{esc(strip_tags(p["title"]))}" class="bcard-img" loading="lazy">'
        cards += f'<a href="{p["relative_url"]}" class="bcard">{feat_img}<div class="bcard-body"><h3>{p["title"]}</h3><p class="exc">{esc(exc)}</p><span class="meta">{dt}</span></div></a>\n'
    pag = '<div class="pag">'
    for i in range(1, min(total_pages + 1, 20)):
        href = "/blog/" if i == 1 else f"/blog/page/{i}/"
        if i == page_num:
            pag += f'<span class="cur">{i}</span>'
        else:
            pag += f'<a href="{href}">{i}</a>'
    if total_pages > 19:
        pag += f'<span>... {total_pages}</span>'
    pag += '</div>'
    sfx = f" - Page {page_num}" if page_num > 1 else ""
    can = "/blog/" if page_num == 1 else f"/blog/page/{page_num}/"
    return header(f"Blog | Dr. Connor Robertson on Business, AI & Pittsburgh{sfx}",
        "Insights on entrepreneurship, real estate, leadership, and Pittsburgh business from Dr. Connor Robertson.", can) + f"""
<section class="pg-hero"><div class="ctn"><h1>Blog, Leadership &amp; Entrepreneurship</h1></div></section>
<section class="sec"><div class="ctn"><div class="bgrid">{cards}</div>{pag}</div></section>
""" + footer()


def page_post(p):
    try:
        dt = datetime.fromisoformat(p["date"]).strftime("%B %d, %Y")
    except:
        dt = ""
    exc = strip_tags(p.get("excerpt", ""))[:200]

    # Featured image
    feat_img_html = ""
    og_image = ""
    if p.get("featured_image"):
        local = downloaded_images.get(p["featured_image"], p["featured_image"])
        feat_img_html = f'<img src="{local}" alt="{esc(strip_tags(p["title"]))}" class="post-feat" loading="lazy">'
        og_image = local

    # Rewrite images in post content
    content = rewrite_image_urls(p["content"])

    # Article schema
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["title"],
        "author": {"@type": "Person", "name": "Dr. Connor Robertson", "url": SITE_URL},
        "datePublished": p["date"],
        "dateModified": p["date"],
        "publisher": {
            "@type": "Person",
            "name": "Dr. Connor Robertson",
            "url": SITE_URL,
        },
        "description": exc,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE_URL}{p['relative_url']}"},
        "image": f"{SITE_URL}{og_image}" if og_image and og_image.startswith("/") else og_image,
    })
    extra = f'<script type="application/ld+json">{schema}</script>'
    return header(f'{p["title"]} | Dr. Connor Robertson', exc, p["relative_url"], extra,
                  og_image=og_image, og_type="article") + f"""
<article class="post">
{feat_img_html}
<h1>{p["title"]}</h1>
<p class="pm">{dt} &middot; Dr. Connor Robertson</p>
<div class="pb">{content}</div>
<div style="margin-top:48px;padding-top:24px;border-top:1px solid var(--border)"><a href="/blog/" style="font-size:14px;color:var(--muted)">&larr; Back to Blog</a></div>
</article>
""" + footer()


# ── File writers ──────────────────────────────────────────────

def write(path, content):
    full = DIST / path.lstrip("/")
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")

def sitemap(posts):
    now = datetime.now().strftime("%Y-%m-%d")
    entries = ""
    for u, prio in [("/", "1.0"), ("/about/", "0.9"), ("/speaker/", "0.8"), ("/books/", "0.8"),
                     ("/press-media/", "0.7"), ("/contact/", "0.7"), ("/blog/", "0.9")]:
        entries += f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq><priority>{prio}</priority></url>\n"
    for p in posts:
        d = p["date"][:10]
        entries += f'  <url><loc>{SITE_URL}{p["relative_url"]}</loc><lastmod>{d}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>'


# ── Main ──────────────────────────────────────────────────────

def main():
    no_fetch = "--no-fetch" in sys.argv

    print("=" * 60)
    print("Building drconnorrobertson.com static site")
    print("=" * 60)

    # Fetch posts
    if no_fetch and CACHE_FILE.exists():
        print("\n[1/8] Loading cached posts...")
        with open(CACHE_FILE) as f:
            posts = json.load(f)
        print(f"  Loaded {len(posts)} posts from cache")
    else:
        print("\n[1/8] Fetching posts from WP API (with _embed for full media)...")
        posts = fetch_all_posts()
        print(f"  Fetched {len(posts)} posts")
        with open(CACHE_FILE, "w") as f:
            json.dump(posts, f)
        print("  Cached to posts_cache.json")

    # Fetch pages content
    print("\n[2/8] Fetching WP pages...")
    wp_pages = []
    if not no_fetch:
        try:
            wp_pages = fetch_all_pages()
            print(f"  Fetched {len(wp_pages)} pages")
        except Exception as e:
            print(f"  Could not fetch pages: {e}")

    # Clean dist
    print("\n[3/8] Preparing output directory...")
    if DIST.exists():
        import shutil
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # Download all media assets
    print("\n[4/8] Downloading images from WordPress...")
    img_count = 0

    # Download featured images from posts
    for p in posts:
        if p.get("featured_image"):
            result = download_image(p["featured_image"])
            if result:
                img_count += 1

    # Scan post content for image URLs and download them
    for p in posts:
        content = p.get("content", "")
        # Find all image URLs in content
        urls = re.findall(r'(?:src|srcset)=["\']([^"\']+)["\']', content)
        for url_str in urls:
            # srcset can have multiple URLs separated by commas
            for part in url_str.split(","):
                part = part.strip().split()[0]  # get URL, drop size descriptor
                if WP_DOMAIN in part or "wp-content/uploads" in part:
                    result = download_image(part)
                    if result:
                        img_count += 1

    # Scan page content too
    for pg in wp_pages:
        content = pg.get("content", "")
        urls = re.findall(r'(?:src|srcset)=["\']([^"\']+)["\']', content)
        for url_str in urls:
            for part in url_str.split(","):
                part = part.strip().split()[0]
                if WP_DOMAIN in part or "wp-content/uploads" in part:
                    result = download_image(part)
                    if result:
                        img_count += 1

    # Try to download all media from WP media library
    if not no_fetch:
        try:
            all_media = fetch_all_media()
            print(f"  Found {len(all_media)} media items in WP library")
            for m in all_media:
                if m.get("source_url"):
                    result = download_image(m["source_url"])
                    if result:
                        img_count += 1
        except Exception as e:
            print(f"  Could not fetch media library: {e}")

    print(f"  Downloaded {img_count} images total ({len(downloaded_images)} unique)")

    # Static pages
    print("\n[5/8] Generating static pages...")
    write("index.html", page_home())
    write("about/index.html", page_about())
    write("speaker/index.html", page_speaker())
    write("books/index.html", page_books())
    write("press-media/index.html", page_press())
    write("contact/index.html", page_contact())
    print("  6 static pages generated")

    # Blog posts
    print(f"\n[6/8] Generating {len(posts)} blog post pages...")
    for i, p in enumerate(posts):
        rel = p["relative_url"].strip("/")
        if rel:
            write(f"{rel}/index.html", page_post(p))
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{len(posts)}...")
    print(f"  {len(posts)} post pages generated")

    # Blog index with pagination
    print("\n[7/8] Generating blog index pages...")
    per_page = 24
    total_pages = max(1, -(-len(posts) // per_page))
    for pg in range(1, total_pages + 1):
        if pg == 1:
            write("blog/index.html", page_blog_index(posts, pg, total_pages))
        else:
            write(f"blog/page/{pg}/index.html", page_blog_index(posts, pg, total_pages))
    print(f"  {total_pages} index pages generated")

    # SEO files
    print("\n[8/8] Generating SEO and config files...")
    write("sitemap.xml", sitemap(posts))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    write("404.html", header("Page Not Found | Dr. Connor Robertson", "", "") + """
<section class="pg-hero" style="min-height:60vh;display:flex;align-items:center"><div class="ctn" style="text-align:center">
<h1>404</h1><p style="margin-top:16px">The page you're looking for doesn't exist.</p>
<a href="/" class="btn-p" style="margin-top:32px;display:inline-block">Go Home</a>
</div></section>
""" + footer())

    # Google Search Console verification file
    if GSC_VERIFICATION:
        write(GSC_VERIFICATION, f"google-site-verification: {GSC_VERIFICATION}")
        print(f"  GSC verification file: {GSC_VERIFICATION}")

    # Vercel config in dist
    vercel = {
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": [
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "X-Frame-Options", "value": "DENY"},
                {"key": "X-XSS-Protection", "value": "1; mode=block"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
            ]},
            {"source": "/images/(.*)", "headers": [
                {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"},
            ]},
        ]
    }
    write("vercel.json", json.dumps(vercel, indent=2))
    print("  sitemap.xml, robots.txt, 404.html, vercel.json")

    total_files = sum(1 for _ in DIST.rglob("*") if _.is_file())
    print(f"\n{'=' * 60}")
    print(f"Build complete! {total_files} files in dist/")
    print(f"Images downloaded: {len(downloaded_images)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
