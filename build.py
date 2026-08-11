#!/usr/bin/env python3
"""
Build script for drconnorrobertson.com static site. Updated 2026-05-18.
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
# Canonical origin. Vercel serves the site on the www host and 307s the apex to
# it, so canonicals, og:url, sitemap entries and schema @ids all have to use www
# -- pointing them at the apex makes every canonical a redirect. If the Vercel
# primary domain is ever flipped to the apex, change this one constant (and HOST
# in submit_indexnow.py) back.
SITE_URL = "https://www.drconnorrobertson.com"
WP_API = "https://drconnorrobertson.com/wp-json/wp/v2"
CACHE_FILE = BASE_DIR / "posts_cache.json"
IMAGE_DIR = DIST / "images"
WP_DOMAIN = "drconnorrobertson.com"
WP_DOMAIN_WWW = "www.drconnorrobertson.com"

# Google Search Console verification (update with your actual code)
GSC_VERIFICATION = ""  # e.g. "google1234567890abcdef.html"
GSC_META = ""  # e.g. '<meta name="google-site-verification" content="...">'

# IndexNow ownership key. Served as /<key>.txt containing the key itself, which
# is how api.indexnow.org verifies that a submission comes from the site owner.
# Brave Search has no equivalent submission endpoint -- see robots_txt().
INDEXNOW_KEY = "023251f41de1d8833a0e76d2c1799807"

# ââ Headshot images from Google Drive ââââââââââââââââââââââââââââ
HEADSHOT_IMAGES = {
    "connor-hero.jpg": "1pb9Ywj8ZSLsCWY_6BKE7dYVT5CB_wkBG",
    "connor-about.jpg": "1WZWhF4DprYQ0KJuT1QG06-fqujAt6vqu",
    "connor-blog-author.jpg": "1jAbDQ0gTk_ANkmNp4Ap2bHq933W-6A6d",
    "connor-press.jpg": "18lXsfBp9lonA8ss_Y-AN1rAWbIzhRi6s",
    "connor-contact.jpg": "1XXXo2oazNGXMthB5x4DbzWMKsd1-BfSH",
    "connor-book.jpg": "13Z1Mqrpx_e7lqZASXrOXcyqj22yvFkbx",
    "connor-business.jpg": "1Ist8cAStzUkigCe4UkW8rvREvAzUyEMc",
    "connor-casual.jpg": "179JJmOJKD1KhRezl1kk-h5wI02SchuuD",
    "connor-blazer.jpg": "1r6zKRQC5QLUrvOnRDhSrtju8M5Y3_9_r",
    "connor-headshot.jpg": "1kO8f_3H8YObT-Upz2bJ6S3X8O0S997tU",
    "connor-bold.jpg": "1GXH5DvI-DlwcTKW2j37WTwXeb7NhrNM7",
    "dr-connor-robertson-headshot.jpg": "local_upload",
}

# Ã¢ÂÂÃ¢ÂÂ Image download helpers Ã¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂ

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


def download_headshots():
    """Copy headshot images from repo images/ dir to dist/images/, falling back to Drive download."""
    local_images = BASE_DIR / "images"
    for filename, file_id in HEADSHOT_IMAGES.items():
        dest = IMAGE_DIR / filename
        if dest.exists():
            print(f"  [skip] {filename} already exists")
            continue
        # Try local repo copy first
        local_src = local_images / filename
        if local_src.exists():
            import shutil
            shutil.copy2(str(local_src), str(dest))
            print(f"  [copy] {filename} from local images/")
            continue
        # Fall back to Google Drive download
        result = download_from_drive(file_id, dest)
        if result:
            print(f"  [download] {filename} from Google Drive")
        else:
            print(f"  [FAIL] {filename} could not be downloaded")

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


# Ã¢ÂÂÃ¢ÂÂ Fetch helpers Ã¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂ

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


# Ã¢ÂÂÃ¢ÂÂ Design System Ã¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂ

# ââ Verified profiles âââââââââââââââââââââââââââââââââââââââââââââ
# Every URL below was fetched and confirmed to (a) return content and (b) belong
# to this Connor Robertson before being added. Anything that 404s, fails TLS, or
# resolves to a different person is listed in DEAD_OR_UNVERIFIED below with the
# reason -- sameAs pointing at dead hosts weakens entity resolution rather than
# strengthening it, so it is deliberately kept out of the graph.

SOCIAL_LINKS = {
    "LinkedIn": "https://www.linkedin.com/in/dr-connor-robertson",
    "Medium": "https://medium.com/@dr.connor.robertson",
    "Substack": "https://substack.com/@drconnorrobertson1",
    "X (Twitter)": "https://x.com/DrConnorRE",
    "YouTube": "https://www.youtube.com/@drconnorrobertson",
    "Threads": "https://www.threads.net/@drconnorrobertson",
    "Tumblr": "https://drconnorrobertson.tumblr.com/",
    "Spotify": "https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX",
    "Apple Podcasts": "https://podcasts.apple.com/us/podcast/the-prospecting-show-with-dr-connor-robertson/id1488353384",
    "Facebook": "https://www.facebook.com/therealconnorrobertson",
    "Instagram": "https://www.instagram.com/creative_acquisitions/",
    "TikTok": "https://www.tiktok.com/@dr.connor.robertson",
    "Crunchbase": "https://www.crunchbase.com/person/dr-connor-robertson",
    "Flipboard": "https://flipboard.com/@DrConnorRobert",
    "Skool": "https://www.skool.com/@connor-robertson-5397",
}

# Podcast directory listings for The Prospecting Show. Directory pages are strong
# sameAs signals because they independently restate the host/publisher name.
PODCAST_PROFILES = [
    "https://creators.spotify.com/pod/show/the-prospecting-show",
    "https://www.listennotes.com/podcasts/the-prospecting-show-dr-connor-robertson-H5KQ8GhA924/",
    "https://podnews.net/podcast/ibprx",
]

# Domains Connor owns and that currently serve a live page.
OWNED_WEBSITES = [
    "https://www.elixirconsultinggroup.com",
    "https://www.thepittsburghwire.com",
    "https://www.prospectingshow.com",
    "https://thegrantfinder.com",
    "https://www.buyingwealthbook.com",
    "https://builttorunbook.com",
    "https://www.seymourmaison.com",
]

# Checked and deliberately excluded. Revisit once the hosting is fixed or the
# domain is registered, then move the entry up into OWNED_WEBSITES.
DEAD_OR_UNVERIFIED = {
    "theprospectingshow.com": "no TLS listener on :443; :80 forwards to Spotify. Use prospectingshow.com.",
    "drconnorrobertsonbooks.com": "no TLS listener on :443; :80 returns an empty 204. Book links point at /books/ instead.",
    "buythebuildingbook.com": "not registered (whois: no match)",
    "creativeacquisitionsbook.com": "not registered (whois: no match)",
    "7minutephonecallbook.com": "not registered (whois: no match)",
    "padsplitplaybook.com": "not registered (whois: no match)",
}

# WordPress post bodies still link at hosts from DEAD_OR_UNVERIFIED. Those links
# render into dist and fail for readers and crawlers alike, so every post body is
# passed through this map on the way out. Keys are matched as bare substrings so
# both the http and https forms get caught. Value None means drop the anchor and
# keep its text, which is the right move when there is no live replacement.
DEAD_LINK_REWRITES = {
    "https://theprospectingshow.com": "https://prospectingshow.com",
    "http://theprospectingshow.com": "https://prospectingshow.com",
    "https://www.theprospectingshow.com": "https://prospectingshow.com",
    "https://drconnorrobertsonbooks.com": f"{SITE_URL}/books/",
    "http://drconnorrobertsonbooks.com": f"{SITE_URL}/books/",
    "https://www.drconnorrobertsonbooks.com": f"{SITE_URL}/books/",
    "https://buythebuildingbook.com": f"{SITE_URL}/books/",
    "https://creativeacquisitionsbook.com": f"{SITE_URL}/books/",
    "https://7minutephonecallbook.com": f"{SITE_URL}/books/",
    "https://padsplitplaybook.com": f"{SITE_URL}/books/",
}


def rewrite_dead_links(html_content):
    """Point post-body links at live hosts. Returns (html, number of rewrites)."""
    n = 0
    for dead, live in DEAD_LINK_REWRITES.items():
        # Only rewrite the href target, not prose that happens to name the domain.
        for quoted in (f'href="{dead}"', f'href="{dead}/"', f"href={dead}", f"href={dead}/"):
            if quoted in html_content:
                n += html_content.count(quoted)
                repl = f'href="{live}"' if quoted.startswith('href="') else f"href={live}"
                html_content = html_content.replace(quoted, repl)
    return html_content, n


dead_links_rewritten = 0


def normalize_dashes(html_content):
    """Replace the double-hyphen em dash stand-in with a comma.

    WordPress bodies carry ' -- ' from the original drafts. It reads as a typo
    once rendered, so it is normalized on the way out. HTML comment delimiters
    are never spaced on both sides, so they cannot match this pattern.
    """
    return html_content.replace(" -- ", ", ")

# Third-party coverage. Referenced rather than owned, but still corroborates the
# entity, so it stays in sameAs.
PRESS_PROFILES = [
    "https://www.tasteterminal.com/2026/04/16/connor-robertson-on-ai-marketing-strategy-how-connor-robertson-helps-entrepreneurs-build-audiences-and-close-more-deals/",
    "https://fictiontalk.com/2026/04/16/connor-robertson-on-business-acquisitions-why-connor-robertson-says-buying-beats-building-for-most-entrepreneurs/",
    "https://newsblaze.com/business/latest-business/connor-robertson-on-ai-and-business-growth-how-connor-robertson-helps-entrepreneurs-use-artificial-intelligence-to-outpace-the-competition_213548/",
    "https://www.theroguemag.com/business/connor-robertson-on-prospecting-systems-how-connor-robertson-builds-a-predictable-pipeline-for-entrepreneurs/",
    "https://www.inentertainment.co.uk/connor-robertson-on-the-author-platform-how-connor-robertson-built-a-business-development-engine-through-publishing/",
    "https://finance.yahoo.com/sectors/technology/articles/elixir-consulting-group-launches-business-112900872.html",
    "https://www.theglobeandmail.com/investing/markets/markets-news/Newsfile/1681496/elixir-consulting-group-launches-business-automation-advisory-service-for-small-and-mid-sized-business-owners/",
    "https://markets.businessinsider.com/news/stocks/elixir-consulting-group-launches-business-automation-advisory-service-for-small-and-midsized-business-owners-1036100299",
    "https://wikitia.com/wiki/Dr._Connor_Robertson",
    "https://wikialpha.co/wiki/Dr._Connor_Robertson",
]

# The single sameAs array used by the Person node. Order matters a little:
# owned properties first, then profiles Connor controls, then third-party
# coverage -- consumers that truncate the list keep the strongest signals.
SAME_AS = OWNED_WEBSITES + list(SOCIAL_LINKS.values()) + PODCAST_PROFILES + PRESS_PROFILES

NAV_ITEMS = [
    ("About", "/about/"),
    ("Projects", "/projects/"),
    ("Speaker", "/speaker/"),
    ("Blog", "/blog/"),
    ("Books", "/books/"),
    ("Media Kit", "/media/"),
    ("Press & Media", "/press-media/"),
    ("FAQ", "/faq/"),
]

RESOURCE_HUBS = [
    ("Business Acquisitions & Scaling", "/blog/hub-business-acquisitions-scaling-dr-connor-robertson/"),
    ("Leadership & Legacy", "/blog/hub-leadership-legacy-dr-connor-robertson/"),
    ("Influence & Authority", "/blog/hub-influence-authority-dr-connor-robertson/"),
    ("Mindset & Systems", "/blog/hub-mindset-momentum-systems-dr-connor-robertson/"),
    ("Pittsburgh Business", "/blog/hub-pittsburgh-business-real-estate-dr-connor-robertson/"),
]

PILLAR_PAGES = [
    ("Business Acquisitions", "/business-acquisitions/"),
    ("AI Business Strategy", "/ai-business-strategy/"),
    ("Prospecting & Sales", "/prospecting-sales/"),
    ("Author Platform", "/author-platform/"),
]

# ââ Per-post SEO overrides ââââââââââââââââââââââââââââââââââââââââ
# Raw post titles run 58-75 chars before the brand suffix, so search engines
# truncate them. Each entry supplies a search-first title and description, a
# contextual link into the matching topic hub, and long-tail Q&A drawn from the
# post itself. The Q&A renders visibly on the page and as FAQPage schema.

POST_SEO = {
    "the-ai-agent-revolution-what-every-small-business-owner-needs-to-know-now": {
        "title": "AI Agents for Small Business: A Practical 2026 Guide",
        "desc": "What AI agents actually are, the three places they deliver the most leverage in a small business, and how to deploy your first one.",
        "hub": ("AI business strategy guide", "/ai-business-strategy/"),
        "faqs": [
            ("What is an AI agent, and how is it different from a chatbot?",
             "A chatbot answers questions you type into it. An AI agent is autonomous software you give a goal and a set of tools, and it works toward that goal across multiple steps without being prompted, monitoring your inbox, classifying email by urgency, drafting replies, routing requests to the right person, and flagging only the handful that need you."),
            ("Where do AI agents deliver the most value in a small business?",
             "Three areas consistently produce the most leverage: lead follow-up and prospect communication, content and publishing operations, and internal reporting that surfaces the few numbers you actually need to act on each morning."),
            ("How should a small business owner start using AI agents?",
             "Start with one workflow, the most painful repetitive task in the business, rather than automating everything at once. Treat the agent like a new team member with a defined role, clear guardrails, and regular review, not something you turn loose on autopilot."),
        ],
    },
    "the-age-of-the-ai-agent-why-entrepreneurs-who-wait-get-left-behind": {
        "title": "The Age of the AI Agent: Why Waiting Costs You",
        "desc": "AI agents compound with use. Why entrepreneurs deploying now build a lead that late starters spend the following year trying to close.",
        "hub": ("AI business strategy guide", "/ai-business-strategy/"),
        "faqs": [
            ("Why does deploying AI agents early actually matter?",
             "Agents improve with use: the more context they accumulate, the better their outputs become. A business that starts building agentic workflows early in the year has months of refined, context-rich automation by year end, while a business that starts late begins from zero."),
            ("What do entrepreneurs who succeed with AI agents do differently?",
             "They start with one workflow instead of everything at once, lead response and follow-up is the most common first choice because it is measurable and directly affects revenue. They document their processes first, since agents follow structured instructions rather than reading your mind. And they treat agents as infrastructure with roles and feedback loops, not a tool used sporadically."),
            ("Is AI still too expensive for a small business?",
             "That objection stopped holding roughly 18 months ago. Model costs have dropped more than 90% since early 2024, which puts capability that once required an enterprise budget within reach of a solo operator or a five-person team."),
        ],
    },
    "the-new-org-chart-leading-human-ai-teams-2026": {
        "title": "Leading Human-AI Teams: The New Org Chart for 2026",
        "desc": "AI agents now hold roles, not just features. How founders structure, lead, and set standards for blended human-AI teams in 2026.",
        "hub": ("AI business strategy guide", "/ai-business-strategy/"),
        "faqs": [
            ("What is a human-AI team?",
             "A team where human judgment is paired with AI agents that execute, monitor, and report. A well-configured agent can watch your client pipeline, identify who has gone cold, draft personalized follow-ups, send them on a schedule, and report back on what worked. That is a role, not a feature."),
            ("What does it mean to be an 'AI director' of your own business?",
             "Your job stops being to do everything and becomes to design the system, set the standards, and hold the outcomes: decide which functions get handed to agents, define what quality looks like for each, and protect the places where human judgment stays non-negotiable."),
            ("Why do some AI deployments produce mediocre results?",
             "Because the founder sets it up once and walks away. The ones getting transformational results manage agents the way a strong manager treats a good employee: clear expectations, regular feedback loops, and scope that expands as performance proves out."),
        ],
    },
    "why-2026-is-the-best-window-to-buy-a-business": {
        "title": "Why 2026 Is a Rare Window to Buy a Business",
        "desc": "Stabilised rates, open credit, creative deal structures, and retiring Boomer owners have opened a buyer's window for first-time acquirers.",
        "hub": ("business acquisitions guide", "/business-acquisitions/"),
        "faqs": [
            ("Why is 2026 a good year to buy a business?",
             "Interest rates have stabilised and credit markets are open, a meaningful cohort of Baby Boomer owners who spent three years waiting for a recovery are now ready to sell and retire, and creative deal structures are bridging the valuation gaps that would have killed deals 18 months ago."),
            ("How can you buy a business without a large amount of cash?",
             "Creative structures are back in use: seller financing, earn-outs, revenue-sharing arrangements, and equity rollovers. A well-structured seller-financed deal can put you inside a cash-flowing business for a fraction of what traditional financing would require upfront."),
            ("Can you use an SBA loan to buy a small business?",
             "The SBA 7(a) program remains one of the most underused tools in the small business acquisition playbook: a down payment as low as 10% on deals worth up to $5 million in total value, with active lenders and real appetite for qualified borrowers who have a clean financial profile and a target with demonstrated cash flow."),
        ],
    },
    "the-systems-playbook-how-to-stop-being-the-bottleneck-in-your-own-business": {
        "title": "Stop Being the Bottleneck: A Founder's Systems Playbook",
        "desc": "The three-layer framework, process infrastructure, decision architecture, talent leverage, that makes a business run without its owner.",
        "hub": ("mindset and systems resources", "/blog/hub-mindset-momentum-systems-dr-connor-robertson/"),
        "faqs": [
            ("How do you know if your business depends too much on you?",
             "Ask what happens if you go completely dark for two weeks. If deals stall, client relationships go quiet, and decisions pile up waiting on the one person who can make them, the business runs because of its owner rather than without them. That is the difference between building equity and building a trap."),
            ("Why do capable founders stay the bottleneck in their own business?",
             "The cause is psychological, not operational. Every early win came because you were personally involved, which trains the belief that your involvement is what makes things work. That belief is exactly right for the first phase of building and exactly wrong for every phase after it."),
            ("What are the three layers of an owner-independent business?",
             "Process infrastructure, the documentation and automation layer, plus decision architecture and talent leverage. Most businesses have fragments of each but have never built them as one complete, intentional system, and a workflow that exists only in the founder's head is institutional risk rather than a workflow."),
        ],
    },
    "your-name-is-your-best-business-asset": {
        "title": "Personal Branding for Entrepreneurs: Your Name as an Asset",
        "desc": "A personal brand is the reputation you build deliberately in one domain. The three returns: inbound deal flow, price authority, and talent.",
        "hub": ("author platform guide", "/author-platform/"),
        "faqs": [
            ("What is a personal brand, really?",
             "The reputation you deliberately cultivate in a specific domain with a specific audience over time. Your brand exists whether you manage it or not, every deal you close, every client conversation, every email builds a perception. The question is whether you are the one shaping it."),
            ("Is personal branding the same as self-promotion?",
             "No. Posting your morning routine, your airport meals, or vague inspiration about discipline is noise. A real personal brand is substantive, consistent visibility in one domain, aimed at a specific audience, sustained over years."),
            ("What is the business return on building a personal brand?",
             "Three returns compound: inbound deal flow, because people who already know your work start the first conversation evaluating fit rather than trust; price authority, because experts are not judged on price the way commodities are; and talent attraction."),
        ],
    },
    "why-every-entrepreneur-needs-to-think-like-a-media-company": {
        "title": "Why Entrepreneurs Should Think Like a Media Company",
        "desc": "Buying attention keeps getting more expensive. Why building an audience through publishing beats renting it, and how the trust compounds.",
        "hub": ("author platform guide", "/author-platform/"),
        "faqs": [
            ("What does it mean for a business to think like a media company?",
             "Instead of renting attention through advertising and cold outreach, you build an audience: publish consistently, provide genuine value, and let the audience come to you. When they need what you sell, you are already the first name in their head."),
            ("Why does content outperform advertising for small businesses?",
             "Traditional marketing is inherently adversarial, the prospect knows they are being sold to and their guard is up. Someone who has listened to your podcast for six months or read your newsletter for a year already trusts you before the sales conversation starts."),
            ("Do you have to publish on every platform to build a media presence?",
             "No. The cost of earning attention is low but consistency is what compounds: a well-written article can drive traffic for five years, and a steady presence in one or two formats you can actually sustain beats spreading yourself across all of them."),
        ],
    },
    "why-investors-are-quietly-moving-into-pittsburgh-real-estate-in-2026": {
        "title": "Pittsburgh Real Estate Investing: The 2026 Case",
        "desc": "Why quiet capital is moving into Pittsburgh: a $240K median price, top-tier price-to-rent ratios, and a $740M North Shore development pipeline.",
        "hub": ("Pittsburgh business and real estate resources", "/blog/hub-pittsburgh-business-real-estate-dr-connor-robertson/"),
        "faqs": [
            ("Is Pittsburgh a good market for real estate investors in 2026?",
             "Pittsburgh's median home price sits around $240,000 in early 2026 against a national median near $415,000, roughly a 41% discount, in a metro anchored by UPMC, Carnegie Mellon, Duquesne, and Pitt. Price-to-rent ratios rank among the most favorable in any major US metro, so cash flow is the base case and appreciation is the bonus."),
            ("What major real estate development is happening in Pittsburgh?",
             "Piatt Companies broke ground on the Esplanade, a $740 million, 15-acre mixed-use development on the North Shore waterfront in the Chateau neighborhood, including 750 housing units, retail, entertainment anchors, and a Transit Revitalization Investment District."),
            ("Why do out-of-state investors overlook Pittsburgh?",
             "Most capital maps to Phoenix, Nashville, and South Florida, with the bolder allocators looking at Raleigh or Columbus. Pittsburgh's reputation lags its economics, and that gap between perception and fundamentals is exactly the pricing inefficiency a small group of quiet buyers is working right now."),
        ],
    },
}

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
    ("Connor Robertson on AI Marketing Strategy", "https://www.tasteterminal.com/2026/04/16/connor-robertson-on-ai-marketing-strategy-how-connor-robertson-helps-entrepreneurs-build-audiences-and-close-more-deals/", "Taste Terminal"),
    ("Connor Robertson on Business Acquisitions", "https://fictiontalk.com/2026/04/16/connor-robertson-on-business-acquisitions-why-connor-robertson-says-buying-beats-building-for-most-entrepreneurs/", "Fiction Talk"),
    ("Connor Robertson on AI and Business Growth", "https://newsblaze.com/business/latest-business/connor-robertson-on-ai-and-business-growth-how-connor-robertson-helps-entrepreneurs-use-artificial-intelligence-to-outpace-the-competition_213548/", "NewsBlaze"),
    ("Connor Robertson on Prospecting Systems", "https://www.theroguemag.com/business/connor-robertson-on-prospecting-systems-how-connor-robertson-builds-a-predictable-pipeline-for-entrepreneurs/", "The Rogue Mag"),
    ("Connor Robertson on the Author Platform", "https://www.inentertainment.co.uk/connor-robertson-on-the-author-platform-how-connor-robertson-built-a-business-development-engine-through-publishing/", "InEntertainment"),
    ("Elixir Consulting Group Launches Business Automation Advisory Service", "https://finance.yahoo.com/sectors/technology/articles/elixir-consulting-group-launches-business-112900872.html", "Yahoo Finance"),
    ("Elixir Consulting Group Launches Business Automation Advisory Service for Small and Mid-Sized Business Owners", "https://www.theglobeandmail.com/investing/markets/markets-news/Newsfile/1681496/elixir-consulting-group-launches-business-automation-advisory-service-for-small-and-mid-sized-business-owners/", "The Globe and Mail"),
    ("Elixir Consulting Group Launches Business Automation Advisory Service for Small and Midsized Business Owners", "https://markets.businessinsider.com/news/stocks/elixir-consulting-group-launches-business-automation-advisory-service-for-small-and-midsized-business-owners-1036100299", "Business Insider"),
]

# `slug` is the stable anchor for each book: it is the id on the card, the
# fragment other pages deep-link to (/books/#buying-wealth), and the Book node's
# @id. Do not rename one without the others.
BOOKS = [
    {
        "slug": "buying-wealth",
        "title": "Buying Wealth",
        "desc": "A straightforward guide to ownership and practical wealth-building. Learn how to buy assets that produce cash flow, use leverage responsibly, and build disciplined systems for growth.",
        "retailers": [
            ("Google Play", "https://play.google.com/store/books/details/Dr_Connor_Robertson_Buying_Wealth?id=Dw2HEQAAQBAJ"),
            ("Official Site", "https://www.buyingwealthbook.com"),
        ],
    },
    {
        "slug": "the-7-minute-phone-call",
        "title": "The 7 Minute Phone Call",
        "desc": "Replace hesitation with action. Connect like a human being again. In seven minutes, you can build more trust than a dozen emails ever will.",
        "retailers": [
            ("Google Play", "https://play.google.com/store/books/details/Dr_Connor_Robertson_The_7_Minute_Phone_Call?id=9QyHEQAAQBAJ"),
        ],
    },
    {
        "slug": "creative-acquisitions",
        "title": "Creative Acquisitions: The Playbook for Modern Dealmakers",
        "desc": "A practical, operator focused guide for entrepreneurs who want to buy real businesses using flexible, creative, and durable acquisition strategies.",
        "retailers": [
            ("Barnes & Noble", "https://www.barnesandnoble.com/w/creative-acquisitions-by-dr-connor-robertson-connor-robertson/1148958050"),
            ("Kobo", "https://www.kobo.com/us/en/ebook/creative-acquisitions-by-dr-connor-robertson"),
        ],
    },
    {
        "slug": "built-to-run",
        "title": "Built to Run",
        "desc": "Build systems and processes that let your business operate without constant owner involvement. A framework for creating scalable, owner-independent operations.",
        "retailers": [
            ("Official Site", "https://builttorunbook.com"),
        ],
    },
    {
        "slug": "padsplit-playbook",
        "title": "PadSplit Playbook: Scaling Affordable Housing Through Shared Living",
        "desc": "A practical, experience driven guide for property owners, operators, and housing focused entrepreneurs who want to understand how PadSplit works in real life.",
        "retailers": [
            ("Google Play", "https://play.google.com/store/books/details/Dr_Connor_Robertson_Padsplit_Playbook_Scaling_Affo?id=9sSqEQAAQBAJ"),
            ("Barnes & Noble", "https://www.barnesandnoble.com/w/padsplit-playbook-by-dr-connor-robertson-connor-robertson/1149135521"),
            ("Kobo", "https://www.kobo.com/us/en/ebook/padsplit-playbook-by-dr-connor-robertson"),
        ],
    },
    {
        "slug": "buy-the-building-keep-the-profits",
        "title": "Buy The Building, Keep The Profits",
        "desc": "A clear and practical guide that helps business owners understand why the real money is not only in running a successful company but in owning the real estate that company occupies.",
        "retailers": [
            ("Google Play", "https://play.google.com/store/books/details/Dr_Connor_Robertson_Buy_the_Building_Keep_the_Prof?id=MRWfEQAAQBAJ"),
            ("Barnes & Noble", "https://www.barnesandnoble.com/w/buy-the-building-keep-the-profits-by-dr-connor-robertson-connor-robertson/1148885434"),
            ("Kobo", "https://www.kobo.com/us/en/ebook/buy-the-building-keep-the-profits-by-dr-connor-robertson"),
        ],
    },
]


# Ã¢ÂÂÃ¢ÂÂ CSS Ã¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂ

CSS = """
:root{--bg:#000;--bg2:#0a0a0a;--card:#111;--text:#fff;--text2:#b0b0b0;--muted:#888;--border:#222;--r:8px;--mw:1200px;--t:.3s ease}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'DM Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;font-size:16px}
a{color:var(--text);text-decoration:none;transition:opacity var(--t)}a:hover{opacity:.8}
img{max-width:100%;height:auto;display:block;background:var(--bg2)}
.ctn{max-width:var(--mw);margin:0 auto;padding:0 24px}

/* Header */
.hdr{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(0,0,0,.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}
.hdr-in{max-width:var(--mw);margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:72px}
.logo{font-size:18px;font-weight:700;letter-spacing:-.02em;white-space:nowrap}
.logo a{color:var(--text)}
.nav{display:flex;align-items:center;gap:28px;list-style:none}
.nav a{font-size:14px;font-weight:500;color:var(--text2);transition:color var(--t);min-height:44px;display:flex;align-items:center}
.nav a:hover{color:var(--text);opacity:1}
.nav-cta{display:inline-block;padding:10px 20px;background:var(--text);color:#000!important;border-radius:var(--r);font-size:14px;font-weight:600;transition:transform var(--t),box-shadow var(--t);min-height:44px;display:flex;align-items:center}
.nav-cta:hover{transform:translateY(-1px);box-shadow:0 4px 20px rgba(255,255,255,.15);opacity:1}
.mob-tog{display:none;background:0 0;border:none;color:var(--text);font-size:24px;cursor:pointer;padding:12px;min-width:44px;min-height:44px}
.has-dd{position:relative}
.dd{display:none;position:absolute;top:100%;left:0;background:#111;border:1px solid var(--border);border-radius:var(--r);padding:8px 0;min-width:240px;z-index:100}
.has-dd:hover .dd{display:block}
.dd a{display:block;padding:12px 20px;font-size:13px;color:var(--text2);min-height:44px;display:flex;align-items:center}
.dd a:hover{color:var(--text);background:rgba(255,255,255,.05)}

/* Hero */
.hero{position:relative;min-height:90vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px;overflow:hidden}
.hero-bg{position:absolute;inset:0;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#0a0a0a 100%);z-index:0}
.hero-bg::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(255,255,255,.03) 0%,transparent 70%);z-index:2}
.hero-ct{position:relative;z-index:3;max-width:800px;width:100%}
.hero h1{font-size:clamp(40px,6vw,72px);font-weight:700;letter-spacing:-.03em;margin-bottom:20px;line-height:1.1}
.hero .tag{font-size:clamp(16px,2vw,20px);color:var(--text2);margin-bottom:36px;line-height:1.6}
.hero-btn{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}
.hero-img{width:180px;height:180px;border-radius:50%;object-fit:cover;margin:0 auto 32px;border:3px solid rgba(255,255,255,.15);max-width:100%}
.hero-bg-img{position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;opacity:0.45;z-index:1;border-radius:0;border:none}
.btn-p{display:inline-flex;padding:14px 32px;background:var(--text);color:#000;border-radius:var(--r);font-weight:600;font-size:15px;transition:transform var(--t),box-shadow var(--t);min-height:44px;align-items:center}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(255,255,255,.15);opacity:1}
.btn-s{display:inline-flex;padding:14px 32px;background:rgba(0,0,0,.48);color:var(--text);border:1px solid rgba(255,255,255,.2);border-radius:var(--r);font-weight:600;font-size:15px;transition:background var(--t);min-height:44px;align-items:center}
.btn-s:hover{background:rgba(255,255,255,.1);opacity:1}

/* Featured */
.feat{padding:48px 0;text-align:center;border-bottom:1px solid var(--border)}
.feat h2{font-size:12px;text-transform:uppercase;letter-spacing:3px;color:var(--muted);margin-bottom:32px}
.feat-logos{display:flex;align-items:center;justify-content:center;opacity:.7;overflow:hidden;position:relative;width:100%}
.feat-logos-track{display:flex;gap:60px;animation:scroll-marquee 20s linear infinite;width:max-content}
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
.about-photo{text-align:center;margin-bottom:32px}.about-photo img{width:220px;height:220px;border-radius:50%;object-fit:cover;border:4px solid var(--border);max-width:100%}

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
.pag a,.pag span{display:inline-flex;padding:10px 16px;border:1px solid var(--border);border-radius:var(--r);font-size:14px;color:var(--text2);min-height:44px;min-width:44px;align-items:center;justify-content:center}
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
.bk-cta{display:inline-flex;padding:12px 28px;background:var(--text);color:#000;border-radius:var(--r);font-weight:600;font-size:14px;align-self:flex-start;margin-top:8px;transition:transform var(--t);min-height:44px;align-items:center}
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
.fg input,.fg select,.fg textarea{width:100%;padding:12px 16px;background:var(--card);border:1px solid var(--border);border-radius:15px;color:var(--text);font-family:inherit;font-size:15px;transition:border-color var(--t);-webkit-appearance:none;appearance:none}
.fg input:focus,.fg select:focus,.fg textarea:focus{outline:0;border-color:rgba(255,255,255,.3)}
.fg textarea{resize:vertical;min-height:120px}
.fr{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.fsub{display:inline-flex;padding:14px 40px;background:var(--text);color:#000;border:none;border-radius:15px;font-family:inherit;font-size:15px;font-weight:600;cursor:pointer;transition:transform var(--t);min-height:44px;align-items:center}
.fsub:hover{transform:translateY(-2px)}

/* Network Crosslinks */
.network-crosslinks{padding:80px 0;background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.network-crosslinks .eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:3px;color:var(--muted);display:block;margin-bottom:16px}
.network-crosslinks h2{font-size:clamp(28px,4vw,48px);font-weight:700;letter-spacing:-.02em;margin-bottom:48px;line-height:1.2}
.network-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:32px}
.network-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:32px;display:flex;flex-direction:column;justify-content:space-between;transition:transform var(--t),border-color var(--t)}
.network-card:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.15)}
.network-card .source-tag{font-size:11px;text-transform:uppercase;letter-spacing:2px;color:var(--muted);margin-bottom:12px;display:block}
.network-card h3{font-size:18px;font-weight:600;margin-bottom:12px;line-height:1.4}
.network-card h3 a{text-decoration:underline;text-underline-offset:3px}
.network-card p{color:var(--text2);font-size:14px;line-height:1.7;margin-bottom:16px;flex:1}

/* Scroll-triggered fade-in animation */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Breadcrumbs */
.breadcrumbs{border-bottom:1px solid var(--border);padding-top:84px;background:var(--bg)}
.breadcrumbs ol{max-width:var(--mw);margin:0 auto;padding:12px 24px;list-style:none;display:flex;flex-wrap:wrap;gap:8px;font-size:13px;color:var(--muted)}
.breadcrumbs li{display:flex;align-items:center;gap:8px}
.breadcrumbs li:not(:first-child)::before{content:"/";color:var(--border)}
.breadcrumbs a{color:var(--text2)}
.breadcrumbs a:hover{color:var(--text);opacity:1}
.breadcrumbs .bc-cur span{color:var(--text2)}
.breadcrumbs + .pg-hero{padding-top:48px}
.breadcrumbs + .post{padding-top:40px}
.breadcrumbs + .speaker-hero{padding-top:48px}
.post-faq-item{border:1px solid var(--border);border-radius:10px;padding:16px 20px;margin-bottom:12px;background:var(--card)}
.post-faq-item summary{cursor:pointer;font-weight:600;font-size:16px;line-height:1.5;list-style:none}
.post-faq-item summary::-webkit-details-marker{display:none}
.post-faq-item summary::after{content:"+";float:right;color:var(--muted);font-weight:400}
.post-faq-item[open] summary::after{content:"\\2212"}
.post-faq-item p{margin:12px 0 0;color:var(--text2);font-size:15px;line-height:1.7}
.link-list{list-style:none;padding:0;margin:8px 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:8px}
.link-list a{color:var(--text2);text-decoration:underline;text-underline-offset:3px;font-size:14px}
.link-list a:hover{color:var(--text);opacity:1}

/* Scrolling marquee for featured logos */
.feat-logos-track {
  display: flex;
  gap: 60px;
  animation: scroll-marquee 20s linear infinite;
  width: max-content;
}

@keyframes scroll-marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.feat-logos {
  overflow: hidden;
  position: relative;
}

/* Footer */
.ftr{background:var(--bg);border-top:1px solid var(--border);padding:64px 0 32px}
.ftr-top{display:grid;grid-template-columns:2fr 1fr 1fr;gap:48px;margin-bottom:48px}
.ftr-tag{color:var(--text2);font-size:15px;margin-top:12px;line-height:1.6}
.ftr-col h4{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;color:var(--muted)}
.ftr-col ul{list-style:none}.ftr-col li{margin-bottom:10px}
.ftr-col a{color:var(--text2);font-size:14px;min-height:44px;display:inline-flex;align-items:center}.ftr-col a:hover{color:var(--text)}
.ftr-btm{text-align:center;padding-top:32px;border-top:1px solid var(--border);color:var(--muted);font-size:13px}

/* Responsive: Tablet (768px and below) */
@media(max-width:768px){
.ctn{padding:0 16px}
.hdr-in{padding:0 16px}
.nav{display:none}
.mob-tog{display:block}
.nav.active{display:flex;flex-direction:column;position:absolute;top:72px;left:0;right:0;background:rgba(0,0,0,.98);padding:16px;gap:8px;border-bottom:1px solid var(--border);z-index:999}
.nav.active a{padding:16px 12px;min-height:48px;font-size:15px}
.hero{min-height:70vh;padding:100px 16px 60px}
.hero h1{font-size:clamp(28px,5vw,48px)}
.hero-img{width:140px;height:140px}
.hero-bg-img{object-position:center top}
.pg-hero{padding:120px 16px 40px}
.pg-hero h1{font-size:clamp(28px,4vw,42px)}
.ftr-top{grid-template-columns:1fr;gap:24px}
.stats{gap:24px;flex-direction:column}
.stat-n{font-size:36px}
.fr{grid-template-columns:1fr}
.bgrid{grid-template-columns:1fr}
.pills{grid-template-columns:1fr}
.post{padding:100px 16px 60px}
.post h1{font-size:clamp(24px,4vw,36px)}
.bcard-body{padding:20px 24px}
.dd{position:static;border:none;background:transparent;padding-left:16px}
.has-dd .dd{display:none}
.has-dd:hover .dd{display:none}
.agrid{grid-template-columns:1fr;gap:24px}
.pgrid{grid-template-columns:1fr}
.network-grid{grid-template-columns:1fr}
.feat{padding:32px 0}
.feat h2{margin-bottom:24px}
.quote{padding:60px 16px}
.quote-t{font-size:clamp(18px,4vw,28px)}
.sec{padding:60px 0}
.sec-t{font-size:clamp(24px,3vw,36px);margin-bottom:16px}
.sec-sub{font-size:15px;margin-bottom:32px}
}

/* Responsive: Mobile (480px and below) */
@media(max-width:480px){
.ctn{padding:0 12px}
.hdr-in{padding:0 12px;height:64px}
.logo{font-size:16px}
.hdr{top:0}
.nav.active{top:64px;padding:12px}
.nav.active a{padding:12px 8px;font-size:14px}
.mob-tog{font-size:20px;padding:10px}
.hero{min-height:60vh;padding:80px 12px 40px;text-align:center}
.hero h1{font-size:clamp(24px,5vw,38px);margin-bottom:16px}
.hero .tag{font-size:clamp(14px,2vw,16px);margin-bottom:24px}
.hero-img{width:120px;height:120px;margin:0 auto 20px}
.hero-bg-img{object-position:center top;opacity:0.4}
.hero-btn{flex-direction:column;width:100%;gap:12px}
.btn-p,.btn-s{width:100%;justify-content:center;padding:14px 20px}
.pg-hero{padding:100px 12px 30px}
.pg-hero h1{font-size:clamp(24px,4vw,36px);margin-bottom:12px}
.pg-hero p{font-size:15px}
.post{padding:80px 12px 40px}
.post h1{font-size:clamp(20px,4vw,28px)}
.post-feat{margin-bottom:24px}
.post .pm{font-size:12px;margin-bottom:24px;padding-bottom:16px}
.post .pb{font-size:15px}
.post .pb h2{font-size:22px;margin:32px 0 12px}
.post .pb h3{font-size:18px;margin:24px 0 8px}
.stat-n{font-size:32px}
.stat-l{font-size:12px}
.about-photo img{width:160px;height:160px}
.pill{padding:24px 20px}
.pill h3{font-size:18px}
.pill p{font-size:14px}
.bcard{border-radius:8px}
.bcard-img{height:160px}
.bcard-body{padding:16px 20px}
.bcard h3{font-size:16px}
.bcard .exc{font-size:13px}
.pag a,.pag span{padding:8px 12px;font-size:12px;min-height:40px;min-width:40px}
.acard{padding:24px}
.acard h3{font-size:18px}
.acard p{font-size:13px}
.tcard{padding:24px}
.tcard h3{font-size:16px}
.tcard p{font-size:13px}
.pcard{padding:24px}
.pcard h3{font-size:16px}
.pcard .src{font-size:12px}
.pcard .rl{font-size:12px}
.cform{padding-top:20px}
.fg{margin-bottom:16px}
.fg label{font-size:13px}
.fg input,.fg select,.fg textarea{padding:10px 12px;font-size:14px}
.fg textarea{min-height:100px}
.fr{grid-template-columns:1fr;gap:12px}
.fsub{padding:12px 24px;font-size:14px;width:100%;justify-content:center}
.quote{padding:40px 12px}
.quote-t{font-size:clamp(16px,3vw,22px);margin-bottom:16px}
.quote-a{font-size:13px}
.feat{padding:24px 0}
.feat h2{font-size:11px;margin-bottom:16px}
.feat-logos-track{gap:40px}
.feat-logos span{font-size:14px}
.feat-logos img{height:28px}
.sec{padding:40px 0}
.sec-t{font-size:clamp(20px,3vw,28px);margin-bottom:12px}
.sec-sub{font-size:14px;margin-bottom:24px}
.ftr{padding:40px 0 24px}
.ftr-top{gap:16px;margin-bottom:24px}
.ftr-col h4{font-size:12px;margin-bottom:12px}
.ftr-col a{font-size:13px}
.ftr-col li{margin-bottom:8px}
.ftr-btm{padding-top:16px;font-size:12px}
.dd{padding-left:0}
.agrid{gap:16px}
.pgrid{gap:16px}
.network-grid{gap:16px}
.network-card{padding:24px}
.network-card .source-tag{font-size:10px;margin-bottom:8px}
.network-card h3{font-size:16px;margin-bottom:8px}
.network-card p{font-size:13px}
.bkgrid{gap:24px}
.bk{padding:24px}
.bk h3{font-size:20px}
.bk p{font-size:14px}
.saud{gap:16px}
.topics{gap:16px}
}

/* Lead Magnet */
.lead-magnet{padding:80px 0;background:linear-gradient(135deg,#0d1117 0%,#161b22 50%,#0d1117 100%);border-top:1px solid var(--border);border-bottom:1px solid var(--border);text-align:center}
.lead-magnet h2{font-size:clamp(24px,3.5vw,40px);font-weight:700;letter-spacing:-.02em;margin-bottom:12px}
.lead-magnet .lm-sub{color:var(--text2);font-size:17px;max-width:600px;margin:0 auto 32px}
.lm-form{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;max-width:500px;margin:0 auto}
.lm-form input[type="email"]{flex:1;min-width:240px;padding:14px 20px;background:var(--card);border:1px solid var(--border);border-radius:var(--r);color:var(--text);font-size:15px;font-family:inherit}
.lm-form input[type="email"]:focus{outline:0;border-color:rgba(255,255,255,.3)}
.lm-form button{padding:14px 28px;background:var(--text);color:#000;border:none;border-radius:var(--r);font-weight:600;font-size:15px;cursor:pointer;font-family:inherit;transition:transform var(--t);white-space:nowrap}
.lm-form button:hover{transform:translateY(-2px)}
.lm-note{color:var(--muted);font-size:12px;margin-top:12px}

/* CTA Banner */
.cta-banner{padding:64px 0;text-align:center;background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.cta-banner h2{font-size:clamp(24px,3.5vw,40px);font-weight:700;letter-spacing:-.02em;margin-bottom:12px}
.cta-banner p{color:var(--text2);font-size:17px;max-width:600px;margin:0 auto 32px}
.cta-btns{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}

/* Podcast / As Heard On */
.podcast-section{padding:80px 0}
.podcast-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin-top:48px}
.pod-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:32px;text-align:center;transition:transform var(--t),border-color var(--t)}
.pod-card:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.15)}
.pod-card h3{font-size:18px;font-weight:600;margin-bottom:8px}
.pod-card p{color:var(--text2);font-size:14px;line-height:1.7}
.pod-card .pod-link{display:inline-flex;align-items:center;margin-top:16px;font-size:14px;font-weight:600;color:var(--text);gap:6px}

/* Speaker page enhancements */
.speaker-hero{padding:140px 24px 80px;text-align:center;background:linear-gradient(180deg,#000 0%,#0d1117 100%);position:relative;overflow:hidden}
.speaker-hero h1{font-size:clamp(36px,5vw,64px);font-weight:700;letter-spacing:-.03em;margin-bottom:20px;line-height:1.1}
.speaker-hero .sh-sub{font-size:clamp(16px,2vw,20px);color:var(--text2);max-width:700px;margin:0 auto 36px;line-height:1.6}
.speaker-stats{display:flex;gap:48px;justify-content:center;flex-wrap:wrap;margin:48px 0 0}
.speaker-stats .stat{text-align:center}
.topic-num{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:rgba(255,255,255,.08);border-radius:50%;font-size:14px;font-weight:700;margin-bottom:16px;color:var(--text2)}
.book-cta{display:inline-flex;padding:16px 40px;background:var(--text);color:#000;border-radius:var(--r);font-weight:700;font-size:16px;transition:transform var(--t),box-shadow var(--t);min-height:48px;align-items:center;text-transform:uppercase;letter-spacing:.5px}
.book-cta:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(255,255,255,.15);opacity:1}

/* About page credentials */
.cred-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;margin:48px 0}
.cred-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:28px;text-align:center}
.cred-card .cred-icon{font-size:32px;margin-bottom:12px}
.cred-card h3{font-size:16px;font-weight:600;margin-bottom:8px}
.cred-card p{color:var(--text2);font-size:13px;line-height:1.6}

/* Books showcase strip */
.books-strip{padding:80px 0;background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.books-strip h2{font-size:clamp(24px,3.5vw,40px);font-weight:700;letter-spacing:-.02em;margin-bottom:12px;text-align:center}
.books-strip .bs-sub{color:var(--text2);font-size:17px;text-align:center;max-width:600px;margin:0 auto 48px}
.books-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px}
.book-mini{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;text-align:center;transition:transform var(--t),border-color var(--t)}
.book-mini:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.15)}
.book-mini h3{font-size:16px;font-weight:600;margin-bottom:8px}
.book-mini p{color:var(--text2);font-size:13px;line-height:1.6;margin-bottom:12px}
.book-mini a{font-size:13px;font-weight:600;color:var(--text);text-decoration:underline;text-underline-offset:3px}
.bk-retailers{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.bk-retailer{display:inline-flex;padding:10px 20px;background:var(--text);color:#000;border-radius:var(--r);font-weight:600;font-size:14px;transition:transform var(--t),box-shadow var(--t);text-transform:uppercase;letter-spacing:.5px}
.bk-retailer:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(255,255,255,.15);opacity:1}
.bk-coming-soon{font-size:14px;color:var(--text2);font-style:italic;margin-top:16px;display:block}

@media(max-width:768px){
.lm-form{flex-direction:column;padding:0 16px}
.lm-form input[type="email"]{min-width:auto;width:100%}
.lm-form button{width:100%}
.cta-btns{flex-direction:column;align-items:center;padding:0 16px}
.cta-btns .btn-p,.cta-btns .btn-s{width:100%;max-width:320px;justify-content:center}
.speaker-hero{padding:120px 16px 60px}
.speaker-stats{gap:24px}
.podcast-grid{grid-template-columns:1fr}
.cred-grid{grid-template-columns:repeat(2,1fr)}
.books-row{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:480px){
.lead-magnet{padding:48px 0}
.lead-magnet h2{font-size:clamp(20px,4vw,28px)}
.lm-form{padding:0 12px}
.cta-banner{padding:40px 0}
.speaker-hero{padding:100px 12px 40px}
.speaker-stats{flex-direction:column;gap:16px}
.cred-grid{grid-template-columns:1fr}
.books-row{grid-template-columns:1fr}
.podcast-grid{gap:16px}
.pod-card{padding:24px}
}
"""

# Ã¢ÂÂÃ¢ÂÂ Template helpers Ã¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂ

FONT_LINK = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" media="print" onload="this.media=\'all\'"><noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap"></noscript>'

def esc(s):
    return html.escape(str(s))

def strip_tags(s):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '', s)
    return html.unescape(text).strip()

DESC_MAX = 155  # Google truncates meta descriptions around 155-160 chars
TITLE_MAX = 60  # Google truncates title tags around 580px / ~60 chars

def clip(text, limit=DESC_MAX):
    """Collapse whitespace and trim to a whole word within `limit` characters."""
    text = " ".join(strip_tags(str(text)).split())
    if len(text) <= limit:
        return text
    return text[:limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.-–—") + "…"


# ââ Sitewide entity graph âââââââââââââââââââââââââââââââââââââââââ
# One canonical Person and WebSite node, referenced by @id from every page,
# so search engines resolve a single entity instead of a dozen near-duplicates.

PERSON_ID = f"{SITE_URL}/#person"
WEBSITE_ID = f"{SITE_URL}/#website"
IMAGE_ID = f"{SITE_URL}/#headshot"

# Organizations Connor founded. Each becomes a first-class Organization node in
# the graph with its own @id, so `founder`, `worksFor` and `publisher` can point
# at one definition instead of repeating an inline stub in three places.
FOUNDED_ORGS = [
    {
        "slug": "elixir-consulting-group",
        "name": "Elixir Consulting Group",
        "url": "https://www.elixirconsultinggroup.com",
        "type": "Organization",
        "desc": "Business automation and acquisition advisory firm for small and mid-sized business owners, founded by Dr. Connor Robertson.",
        "primary": True,
    },
    {
        "slug": "the-pittsburgh-wire",
        "name": "The Pittsburgh Wire",
        "url": "https://www.thepittsburghwire.com",
        "type": "NewsMediaOrganization",
        "desc": "Pittsburgh business and real estate publication founded and published by Dr. Connor Robertson.",
    },
    {
        "slug": "the-prospecting-show",
        "name": "The Prospecting Show",
        "url": "https://www.prospectingshow.com",
        "type": "Organization",
        "desc": "Weekly podcast hosted by Dr. Connor Robertson interviewing entrepreneurs about how they built and scaled their businesses.",
    },
    {
        "slug": "the-grant-finder",
        "name": "The Grant Finder",
        "url": "https://thegrantfinder.com",
        "type": "Organization",
        "desc": "Grant discovery service helping small businesses and nonprofits find funding they qualify for.",
    },
    {
        "slug": "seymour-maison",
        "name": "Seymour Maison",
        "url": "https://www.seymourmaison.com",
        "type": "Organization",
        "desc": "Luxury apparel label founded by Dr. Connor Robertson.",
    },
]

# The org Connor is primarily identified with, used for Person.worksFor.
PRIMARY_ORG = next(o for o in FOUNDED_ORGS if o.get("primary"))


def org_id(slug):
    return f"{SITE_URL}/#{slug}"


def organization_nodes():
    """One Organization node per founded venture, each linked back to the Person."""
    nodes = []
    for o in FOUNDED_ORGS:
        nodes.append({
            "@type": o["type"],
            "@id": org_id(o["slug"]),
            "name": o["name"],
            "url": o["url"],
            "description": o["desc"],
            "founder": {"@id": PERSON_ID},
            "sameAs": [o["url"]],
        })
    return nodes

KNOWS_ABOUT = [
    "Business Acquisitions", "Mergers and Acquisitions", "AI Business Strategy",
    "Business Automation", "Prospecting", "Sales Systems", "Entrepreneurship",
    "Real Estate Investing", "Pittsburgh Business", "Author Platform",
    "Personal Branding", "Leadership", "Podcasting", "Philanthropy",
]


def site_graph_nodes():
    """The Person + Organization + WebSite nodes shared by every page."""
    person = {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Dr. Connor Robertson",
        "alternateName": "Connor Robertson",
        "url": f"{SITE_URL}/",
        "image": {
            "@type": "ImageObject",
            "@id": IMAGE_ID,
            "url": f"{SITE_URL}/images/dr-connor-robertson-headshot.jpg",
            "contentUrl": f"{SITE_URL}/images/dr-connor-robertson-headshot.jpg",
            "width": 1024,
            "height": 1024,
            "caption": "Dr. Connor Robertson",
        },
        "jobTitle": "Entrepreneur, Author, AI Strategist & Business Acquisition Expert",
        "description": "Dr. Connor Robertson is a Canadian-born entrepreneur, business strategist, author, podcast host, and philanthropist based in Pittsburgh, PA. Founder of Elixir Consulting Group, publisher of The Pittsburgh Wire, and host of The Prospecting Show.",
        "address": {"@type": "PostalAddress", "addressLocality": "Pittsburgh", "addressRegion": "PA", "addressCountry": "US"},
        "homeLocation": {"@type": "Place", "name": "Pittsburgh, Pennsylvania"},
        "sameAs": SAME_AS,
        "knowsAbout": KNOWS_ABOUT,
        "founder": [{"@id": org_id(o["slug"])} for o in FOUNDED_ORGS],
        "worksFor": {"@id": org_id(PRIMARY_ORG["slug"])},
        "memberOf": [
            {"@type": "Organization", "name": "Social Venture Partners"},
            {"@type": "Organization", "name": "Habitat for Humanity"},
        ],
        "mainEntityOfPage": {"@id": f"{SITE_URL}/about/#webpage"},
    }
    website = {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": f"{SITE_URL}/",
        "name": "Dr. Connor Robertson",
        "alternateName": "drconnorrobertson.com",
        "description": "Official site of Dr. Connor Robertson - Pittsburgh entrepreneur, author, AI strategist, and business acquisition expert.",
        "publisher": {"@id": PERSON_ID},
        "copyrightHolder": {"@id": PERSON_ID},
        "inLanguage": "en-US",
        "potentialAction": {
            "@type": "ReadAction",
            "target": [f"{SITE_URL}/blog/"],
        },
    }
    return [person] + organization_nodes() + [website]


def breadcrumb_node(crumbs, canonical):
    """BreadcrumbList node for the page graph. crumbs: [(label, href|None), ...]"""
    items = []
    for i, (label, href) in enumerate(crumbs, start=1):
        target = f"{SITE_URL}{href}" if href else f"{SITE_URL}{canonical}"
        items.append({"@type": "ListItem", "position": i, "name": strip_tags(label), "item": target})
    return {
        "@type": "BreadcrumbList",
        "@id": f"{SITE_URL}{canonical}#breadcrumb",
        "itemListElement": items,
    }

def nav_html():
    items = ""
    for label, href in NAV_ITEMS:
        items += f'<li><a href="{href}">{label}</a></li>'
    # Topics dropdown (pillar pages)
    tdd = "".join(f'<a href="{h}">{l}</a>' for l, h in PILLAR_PAGES)
    items += f'<li class="has-dd"><a href="/business-acquisitions/">Topics</a><div class="dd">{tdd}</div></li>'
    # Resources dropdown
    dd = "".join(f'<a href="{h}">{l}</a>' for l, h in RESOURCE_HUBS)
    items += f'<li class="has-dd"><a href="/blog/complete-resource-index-dr-connor-robertson/">Resources</a><div class="dd">{dd}</div></li>'
    items += '<li><a href="/contact/" class="nav-cta">Contact Connor</a></li>'
    return items

def header(title, desc="", canonical="/", extra="", og_image="", og_type="website",
           noindex=False, crumbs=None, page_type="WebPage", schema_nodes=None,
           page_extra=None, prev_url="", next_url=""):
    """Render <head> + site chrome.

    crumbs:       [(label, href|None), ...] -> BreadcrumbList in the page graph
    schema_nodes: extra JSON-LD nodes merged into the single @graph
    extra:        raw markup injected into <head> (kept for one-off cases)
    """
    if not desc:
        desc = "Dr. Connor Robertson is a Pittsburgh entrepreneur, author, AI strategist, and business acquisition expert. Founder of Elixir Consulting Group."
    desc = clip(desc)
    if len(title) > TITLE_MAX:
        print(f"    WARN: title {len(title)} chars (>{TITLE_MAX}) for {canonical}: {title}")
    can = f'<link rel="canonical" href="{SITE_URL}{canonical}">' if canonical else ""
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    og_img_tag = ""
    twitter_img_tag = ""
    if og_image:
        img_url = f"{SITE_URL}{og_image}" if og_image.startswith("/") else og_image
        og_img_tag = (f'<meta property="og:image" content="{img_url}">'
                      f'<meta property="og:image:secure_url" content="{img_url}">'
                      f'<meta property="og:image:alt" content="{esc(strip_tags(title))}">')
        twitter_img_tag = (f'<meta name="twitter:image" content="{img_url}">'
                           f'<meta name="twitter:image:alt" content="{esc(strip_tags(title))}">')
    pagination = ""
    if prev_url:
        pagination += f'<link rel="prev" href="{SITE_URL}{prev_url}">'
    if next_url:
        pagination += f'<link rel="next" href="{SITE_URL}{next_url}">'

    # Single JSON-LD graph: shared entities + this page + anything page-specific.
    page_node = {
        "@type": page_type,
        "@id": f"{SITE_URL}{canonical}#webpage",
        "url": f"{SITE_URL}{canonical}",
        "name": strip_tags(title),
        "description": desc,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": PERSON_ID},
        "inLanguage": "en-US",
    }
    if og_image:
        page_node["primaryImageOfPage"] = {
            "@type": "ImageObject",
            "url": f"{SITE_URL}{og_image}" if og_image.startswith("/") else og_image,
        }
    if page_extra:
        page_node.update(page_extra)
    nodes = site_graph_nodes()
    if crumbs:
        page_node["breadcrumb"] = {"@id": f"{SITE_URL}{canonical}#breadcrumb"}
        nodes.append(breadcrumb_node(crumbs, canonical))
    nodes.append(page_node)
    if schema_nodes:
        nodes.extend(schema_nodes)
    graph = json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False)
    graph_tag = "" if noindex else f'<script type="application/ld+json">{graph}</script>'

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
{twitter_img_tag}
<meta name="author" content="Dr. Connor Robertson">
<meta name="robots" content="{robots}">
{pagination}
<link rel="sitemap" type="application/xml" href="/sitemap.xml">{gsc}
<link rel="icon" type="image/jpeg" href="/images/dr-connor-robertson-headshot.jpg">
<link rel="apple-touch-icon" href="/images/dr-connor-robertson-headshot.jpg">
{FONT_LINK}
<style>{CSS}</style>
{graph_tag}
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
    pages = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in [("/","Home"),("/about/","About"),("/projects/","Projects"),("/speaker/","Speaker"),("/books/","Books"),("/blog/","Blog"),("/media/","Media Kit"),("/press-media/","Press & Media"),("/faq/","FAQ"),("/contact/","Contact")])
    ventures = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{u.replace("https://","").rstrip("/")}</a></li>' for u in OWNED_WEBSITES)
    return f"""
<footer class="ftr"><div class="ctn">
<div class="ftr-top">
<div><div class="logo" style="font-size:20px;margin-bottom:4px">Dr. Connor Robertson</div>
<p class="ftr-tag">Founder of <a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener" style="text-decoration:underline">Elixir Consulting Group</a>, <a href="https://thepittsburghwire.com" target="_blank" rel="noopener" style="text-decoration:underline">The Pittsburgh Wire</a>, <a href="https://www.prospectingshow.com" target="_blank" rel="noopener" style="text-decoration:underline">The Prospecting Show</a> &amp; <a href="https://thegrantfinder.com" target="_blank" rel="noopener" style="text-decoration:underline">The Grant Finder</a>.</p></div>
<div class="ftr-col"><h4>Pages</h4><ul>{pages}</ul></div>
<div class="ftr-col"><h4>Connect</h4><ul>{social}</ul></div>
</div>
<div class="ftr-btm">&copy; {datetime.now().year} Dr. Connor Robertson. All Rights Reserved.</div>
</div></footer>
<script>
(function(){{
  function reveal(){{
    var els=document.querySelectorAll('.fade-in');
    if(!('IntersectionObserver' in window)){{
      for(var i=0;i<els.length;i++){{els[i].classList.add('visible');}}
      return;
    }}
    var obs=new IntersectionObserver(function(entries){{
      entries.forEach(function(e){{
        if(e.isIntersecting){{e.target.classList.add('visible');obs.unobserve(e.target);}}
      }});
    }},{{rootMargin:'0px 0px -50px 0px',threshold:0.05}});
    els.forEach(function(el){{obs.observe(el);}});
  }}
  if(document.readyState==='loading'){{document.addEventListener('DOMContentLoaded',reveal);}}else{{reveal();}}
}})();
</script>
</body></html>"""


# Ã¢ÂÂÃ¢ÂÂ Page builders Ã¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂ

def breadcrumbs(trail):
    """Render visible breadcrumb nav. trail: list of (label, href). Last item is current page (no link)."""
    parts = []
    for i, (label, href) in enumerate(trail):
        if i == len(trail) - 1 or not href:
            parts.append(f'<li class="bc-cur" aria-current="page"><span>{esc(label)}</span></li>')
        else:
            parts.append(f'<li><a href="{href}">{esc(label)}</a></li>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="ctn"><ol>' + "".join(parts) + '</ol></div></nav>'


def related_posts_html(current_url, all_posts, limit=3):
    """Render a 'Related Posts' section showing up to `limit` other recent posts."""
    if not all_posts:
        return ""
    related = [rp for rp in all_posts if rp.get("relative_url") != current_url][:limit]
    if not related:
        return ""
    cards = ""
    for rp in related:
        try:
            dt = datetime.fromisoformat(rp["date"]).strftime("%B %d, %Y")
        except Exception:
            dt = ""
        ex = strip_tags(rp.get("excerpt", ""))
        if len(ex) > 120:
            ex = ex[:120].rsplit(" ", 1)[0] + "..."
        feat_img = ""
        if rp.get("featured_image"):
            local = downloaded_images.get(rp["featured_image"], "")
            if local:
                feat_img = f'<img src="{local}" alt="{esc(strip_tags(rp["title"]))}" class="bcard-img" width="400" height="225" loading="lazy">'
        cards += f'<a href="{rp["relative_url"]}" class="bcard">{feat_img}<div class="bcard-body"><h3>{rp["title"]}</h3><p class="exc">{esc(ex)}</p><span class="meta">{dt}</span></div></a>\n'
    return f"""<section class="sec related-posts"><div class="ctn">
<h2 class="sec-t">Related Posts</h2>
<div class="bgrid">{cards}</div>
</div></section>"""


def page_home():
    # Person + WebSite now live in the sitewide graph (see site_graph_nodes).
    # The home page adds only what is unique to it: the topic hubs as a site
    # navigation element, which helps search engines pick sitelinks.
    nav_schema = {
        "@type": "SiteNavigationElement",
        "@id": f"{SITE_URL}/#sitenav",
        "name": [label for label, _ in PILLAR_PAGES] + [label for label, _ in NAV_ITEMS],
        "url": [f"{SITE_URL}{href}" for _, href in PILLAR_PAGES] + [f"{SITE_URL}{href}" for _, href in NAV_ITEMS],
    }
    pillars = [
        ("Entrepreneur & Business Acquisition Expert", "Dr. Connor Robertson has founded four companies and helps business owners acquire, scale, and exit businesses through <a href=\"https://elixirconsultinggroup.com\" target=\"_blank\" rel=\"noopener\">Elixir Consulting Group</a>. His book <em>Creative Acquisitions</em> is the playbook for modern dealmakers."),
        ("Author & AI Strategist", "Six published books on acquisitions, prospecting, and wealth building. Connor also helps small businesses deploy AI to automate operations and outpace competitors. Browse all titles on <a href=\"/books/\">his books page</a>."),
        ("Podcast Host & Community Builder", "Host of <a href=\"https://www.prospectingshow.com\" target=\"_blank\" rel=\"noopener\">The Prospecting Show</a> with 350+ episodes and publisher of <a href=\"https://thepittsburghwire.com\" target=\"_blank\" rel=\"noopener\">The Pittsburgh Wire</a>. Connor also supports Social Venture Partners and Habitat for Humanity."),
    ]
    pcards = "".join(f'<div class="pill"><h3>{t}</h3><p>{d}</p></div>' for t, d in pillars)
    return header("Dr. Connor Robertson | Entrepreneur, Author & Speaker",
        "Pittsburgh entrepreneur, author and AI strategist Dr. Connor Robertson helps owners buy businesses, automate operations and build lasting wealth.",
        "/", og_image="/images/dr-connor-robertson-headshot.jpg",
        page_type="ProfilePage", schema_nodes=[nav_schema]) + f"""
<section class="hero"><div class="hero-bg"><img src="/images/dr-connor-robertson-headshot.jpg" alt="Dr. Connor Robertson - Entrepreneur, Author, and Business Strategist" width="1024" height="1024" loading="eager" class="hero-bg-img"></div><div class="hero-ct">
<h1>Dr. Connor Robertson</h1>
<p class="tag">Entrepreneur. Author. AI Strategist. Helping business owners acquire companies, automate operations, and build lasting wealth.</p>
<div class="hero-btn"><a href="/books/" class="btn-p">Browse My Books</a><a href="/speaker/" class="btn-s">Book Me to Speak</a></div>
<div style="background:var(--bg-card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:32px;transition:box-shadow .2s;">
<h3 style="font-size:22px;margin-bottom:8px;">Buying Wealth</h3>
<p style="color:var(--text-secondary,#6b7280);font-size:14px;line-height:1.7;margin-bottom:16px;">Dr. Robertson\'s book on building wealth through business acquisitions and real estate investing. A practical guide to creating lasting financial freedom.</p>
<a href="https://buyingwealthbook.com" target="_blank" rel="noopener" style="color:var(--accent,#2563eb);font-weight:600;font-size:14px;">Visit buyingwealthbook.com &rarr;</a>
</div>
</div></section>
<section class="feat"><div class="ctn">
<h2>As Featured On</h2>
<div class="feat-logos"><span>CXO Dispatch</span><span>C-Suite Brief</span><span>NY Wire</span><span>BLK News</span><span>Famous Times</span><span>Economic Insider</span><span>Taste Terminal</span><span>Fiction Talk</span><span>NewsBlaze</span><span>The Rogue Mag</span><span>InEntertainment</span><span>Yahoo Finance</span><span>The Globe and Mail</span><span>Business Insider</span></div>
</div></section>
<section class="sec"><div class="ctn">
<h2 class="sec-t">Dr. Connor Robertson is a Canadian-born entrepreneur, business strategist, author, podcast host, and philanthropist based in Pittsburgh.</h2>
<div class="pills">{pcards}</div>
</div></section>
<section class="quote"><div class="ctn">
<p class="quote-t">"Real success comes from creating impact that lasts longer than you do."</p>
<p class="quote-a"><strong>Dr. Connor Robertson</strong><br>Entrepreneur, Author, AI Strategist &amp; Business Acquisition Expert</p>
</div></section>

<section class="lead-magnet"><div class="ctn">
<h2>Free Guide: 5 Strategies to Acquire Your First Business</h2>
<p class="lm-sub">Connor's most-requested frameworks for finding, evaluating, and closing your first business acquisition, distilled into a free guide.</p>
<form class="lm-form" action="https://formspree.io/f/xdkobkzz" method="POST">
<input type="hidden" name="_subject" value="Lead Magnet Download Request">
<input type="hidden" name="source" value="homepage-lead-magnet">
<input type="email" name="email" placeholder="Enter your email address" required>
<button type="submit">Get the Free Guide</button>
</form>
<p class="lm-note">No spam. Unsubscribe anytime.</p>
</div></section>

<section class="cta-banner"><div class="ctn">
<h2>Ready to Take the Next Step?</h2>
<p>Explore Connor's books, book him for your next event, or work with Elixir Consulting to scale your business.</p>
<div class="cta-btns">
<a href="/books/" class="btn-p">Browse His Books</a>
<a href="/speaker/" class="btn-s">Book Connor to Speak</a>
<a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener" class="btn-s">Elixir Consulting</a>
</div>
</div></section>
""" + footer()


def page_about():
    # The Person entity is sitewide; /about/ is its mainEntityOfPage.
    faq_schema = {
        "@type": "FAQPage",
        "@id": f"{SITE_URL}/about/#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Who is Dr. Connor Robertson?",
             "acceptedAnswer": {"@type": "Answer", "text": "Dr. Connor Robertson is a Canadian-born entrepreneur, business strategist, author, podcast host, and philanthropist based in Pittsburgh, PA. He is the founder of Elixir Consulting Group, publisher of The Pittsburgh Wire, host of The Prospecting Show podcast, and creator of The Grant Finder."}},
            {"@type": "Question", "name": "What companies does Dr. Connor Robertson own?",
             "acceptedAnswer": {"@type": "Answer", "text": "Dr. Connor Robertson founded and operates Elixir Consulting Group (a business consulting firm), The Pittsburgh Wire (a Pittsburgh business news publication), The Prospecting Show (a business podcast on Spotify and Apple Podcasts), and The Grant Finder (a grant discovery platform)."}},
            {"@type": "Question", "name": "Where is Dr. Connor Robertson based?",
             "acceptedAnswer": {"@type": "Answer", "text": "Dr. Connor Robertson is based in Pittsburgh, Pennsylvania. He chose Pittsburgh for its strong business ecosystem, deep talent pool, and collaborative entrepreneurial community."}},
            {"@type": "Question", "name": "What is The Prospecting Show?",
             "acceptedAnswer": {"@type": "Answer", "text": "The Prospecting Show is a weekly business podcast hosted by Dr. Connor Robertson where he interviews entrepreneurs and small business owners about scaling their businesses. It is available on Spotify, Apple Podcasts, YouTube, and all major podcast platforms."}},
            {"@type": "Question", "name": "What books has Dr. Connor Robertson written?",
             "acceptedAnswer": {"@type": "Answer", "text": "Dr. Connor Robertson has authored six books including Buying Wealth, The 7 Minute Phone Call, Creative Acquisitions, Built to Run, PadSplit Playbook, and Buy The Building Keep The Profits. They are available on Google Play, Barnes & Noble, and Kobo."}},
            {"@type": "Question", "name": "How can I contact Dr. Connor Robertson?",
             "acceptedAnswer": {"@type": "Answer", "text": "You can reach Dr. Connor Robertson through the contact form on drconnorrobertson.com/contact/ for business inquiries, speaking engagements, press and media requests, and partnership opportunities."}},
        ]
    }
    return header("Who Is Dr. Connor Robertson? | Bio, Books & Podcast",
        "Who is Dr. Connor Robertson? Pittsburgh entrepreneur, author of six books, host of The Prospecting Show and founder of Elixir Consulting Group.",
        "/about/", og_image="/images/connor-about.jpg", page_type="AboutPage",
        crumbs=[("Home", "/"), ("About", None)],
        schema_nodes=[faq_schema]) + breadcrumbs([("Home", "/"), ("About", None)]) + """
<section class="pg-hero"><div class="ctn">
<h1>About Dr. Connor Robertson</h1>
<p>Entrepreneur. Author. AI Strategist. Business Acquisition Expert. Podcast Host. Founder of four companies based in Pittsburgh, PA.</p>
</div></section>
<section class="sec"><div class="ctn">
<div class="about-photo"><img src="/images/connor-hero.jpg" alt="Dr. Connor Robertson - Pittsburgh entrepreneur, author, AI strategist, and business acquisition expert" loading="lazy"></div>
<p class="sec-sub" style="max-width:900px">Dr. Connor Robertson is a Canadian-born entrepreneur, business strategist, author, and AI implementation expert based in Pittsburgh, PA. He has built four companies from the ground up, authored six books, hosted over 350 podcast episodes, and helped business owners across North America acquire companies, automate operations, and scale with purpose.</p>

<div class="cred-grid">
<div class="cred-card"><div class="cred-icon">&#9889;</div><h3>Entrepreneur</h3><p>Founded Elixir Consulting Group, The Pittsburgh Wire, The Prospecting Show, and The Grant Finder</p></div>
<div class="cred-card"><div class="cred-icon">&#9997;</div><h3>Author</h3><p>Six published books on acquisitions, wealth building, prospecting, and real estate strategy</p></div>
<div class="cred-card"><div class="cred-icon">&#129302;</div><h3>AI Strategist</h3><p>Helps small and mid-sized businesses deploy AI for automation, lead generation, and competitive advantage</p></div>
<div class="cred-card"><div class="cred-icon">&#127911;</div><h3>Podcast Host</h3><p>350+ episodes of The Prospecting Show featuring entrepreneurs and business operators</p></div>
</div>

<div class="stats">
<div class="stat"><div class="stat-n">6</div><div class="stat-l">Books Published</div></div>
<div class="stat"><div class="stat-n">4</div><div class="stat-l">Companies Founded</div></div>
<div class="stat"><div class="stat-n">350+</div><div class="stat-l">Podcast Episodes</div></div>
<div class="stat"><div class="stat-n">10K+</div><div class="stat-l">People Impacted</div></div>
</div>

<div class="agrid">
<div class="ablock"><h3>Business Acquisitions & Strategy</h3>
<p>Connor believes that buying an existing business is the fastest path to entrepreneurship. Through <a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener">Elixir Consulting Group</a>, he advises business owners on acquisitions, operational scaling, and exit strategies. His book <a href="https://www.barnesandnoble.com/w/creative-acquisitions-by-dr-connor-robertson-connor-robertson/1148958050" target="_blank" rel="noopener"><em>Creative Acquisitions</em></a> is the playbook for modern dealmakers. Browse all his books at <a href="/books/">his books page</a>.</p></div>
<div class="ablock"><h3>AI, Automation & Modern Growth</h3>
<p>Connor is at the forefront of helping small businesses adopt artificial intelligence. From automating client communications to building AI-powered lead generation systems, he shows owners how to do more with fewer resources. His approach is practical, not theoretical, focused on tools and workflows that produce ROI within weeks, not months.</p></div>
<div class="ablock"><h3>Media, Publishing & The Prospecting Show</h3>
<p>Connor built <a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a> into a leading local business publication and hosts <a href="https://www.prospectingshow.com" target="_blank" rel="noopener">The Prospecting Show</a>, a weekly podcast featuring entrepreneurs sharing real stories of scaling their businesses. He has authored six books including <em>Buying Wealth</em>, <em>The 7 Minute Phone Call</em>, and <em>Creative Acquisitions</em>, all available on <a href="/books/">his books page</a>.</p></div>
<div class="ablock"><h3>Philanthropy & Community Impact</h3>
<p>Connor's philanthropic work with Social Venture Partners and Habitat for Humanity has helped build over 150 homes and support 40+ global community branches. He believes that building businesses and building communities are inseparable, and that the best entrepreneurs create lasting value beyond the balance sheet.</p></div>
</div></div></section>

<section class="cta-banner"><div class="ctn">
<h2>Work With Connor</h2>
<p>Whether you want to acquire a business, scale your company with AI, or book Connor for your next event, start here.</p>
<div class="cta-btns">
<a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener" class="btn-p">Elixir Consulting</a>
<a href="/speaker/" class="btn-s">Book Connor to Speak</a>
<a href="/books/" class="btn-s">Browse His Books</a>
</div>
</div></section>
""" + footer()


def page_speaker():
    books_mini = ""
    for book in BOOKS:
        title, desc = book["title"], book["desc"]
        short_desc = desc[:80].rsplit(" ", 1)[0] + "..." if len(desc) > 80 else desc
        retailers = book["retailers"]
        if retailers:
            links = " ".join(f'<a href="{u}" target="_blank" rel="noopener" style="margin-right:8px;font-size:12px;font-weight:600;color:var(--text);text-decoration:underline;text-underline-offset:3px">{esc(s)}</a>' for s, u in retailers)
        else:
            links = '<span style="font-size:12px;color:var(--text2)">Coming Soon</span>'
        books_mini += f'<div class="book-mini"><h3>{esc(title)}</h3><p>{esc(short_desc)}</p><div>{links}</div></div>\n'
    speaking_topics = [
        "Buy the Business, Skip the Startup Phase",
        "AI as Your Unfair Advantage",
        "The 7-Minute Phone Call That Closes Deals",
        "Building Wealth Through Real Estate Ownership",
        "From Author to Authority: Publishing as a Business Development Engine",
        "Scaling with Systems, Not Just Hustle",
    ]
    speaking_service = {
        "@type": "Service",
        "@id": f"{SITE_URL}/speaker/#service",
        "name": "Keynote Speaking by Dr. Connor Robertson",
        "serviceType": "Keynote Speaking",
        "description": "Keynotes and workshops on business acquisitions, AI strategy, prospecting systems, and scaling companies, for conferences, summits, and corporate events.",
        "provider": {"@id": PERSON_ID},
        "areaServed": {"@type": "Country", "name": "United States"},
        "audience": {"@type": "Audience", "audienceType": "Entrepreneurs, founders, sales teams, and conference organizers"},
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Speaking Topics",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t}}
                for t in speaking_topics
            ],
        },
    }
    return header("Keynote Speaker Dr. Connor Robertson | Business & AI",
        "Book Dr. Connor Robertson to speak on business acquisitions, AI strategy and scaling. Keynotes for conferences, summits and corporate events.", "/speaker/",
        og_image="/images/connor-blazer.jpg",
        crumbs=[("Home", "/"), ("Speaker", None)],
        schema_nodes=[speaking_service]) + breadcrumbs([("Home", "/"), ("Speaker", None)]) + f"""
<section class="speaker-hero"><div class="ctn">
<div style="text-align:center;margin-bottom:2rem;"><img src="/images/connor-blazer.jpg" alt="Dr. Connor Robertson - Keynote Speaker on Business Acquisitions and AI Strategy" width="300" height="300" loading="eager" style="border-radius:50%;width:200px;height:200px;object-fit:cover;box-shadow:0 4px 20px rgba(0,0,0,0.15);"></div>
<h1>Dr. Connor Robertson: Keynote Speaker on Business Acquisitions, AI &amp; Entrepreneurship</h1>
<p class="sh-tag" style="font-size:1.05rem;color:var(--text2);margin-bottom:1rem">Your audience deserves more than motivation. Give them a playbook.</p>
<p class="sh-sub">Dr. Connor Robertson delivers high-energy keynotes packed with actionable frameworks on business acquisitions, AI-powered growth, and building companies that last. He has founded four companies, authored six books, and hosts The Prospecting Show podcast.</p>
<div class="hero-btn"><a href="#book-me" class="btn-p book-cta">Book Connor to Speak</a><a href="/books/" class="btn-s">Browse His Books</a></div>
<div class="speaker-stats">
<div class="stat"><div class="stat-n">6</div><div class="stat-l">Books Published</div></div>
<div class="stat"><div class="stat-n">4</div><div class="stat-l">Companies Founded</div></div>
<div class="stat"><div class="stat-n">350+</div><div class="stat-l">Podcast Episodes</div></div>
</div>
</div></section>

<section class="sec"><div class="ctn">
<h2 class="sec-t">Speaking Topics</h2>
<p class="sec-sub">Every talk is customized to your audience. These are Connor's most requested keynotes and workshop topics.</p>
<div class="topics">
<div class="tcard"><div class="topic-num">1</div><h3>Buy the Business, Skip the Startup Phase</h3><p>Why acquiring an existing company is the fastest path to entrepreneurship, and how to find, evaluate, and close your first deal using creative acquisition strategies. Based on his book <em>Creative Acquisitions</em>.</p></div>
<div class="tcard"><div class="topic-num">2</div><h3>AI as Your Unfair Advantage</h3><p>How small and mid-sized business owners can deploy AI to automate operations, generate leads, and outmaneuver competitors ten times their size. Real case studies, not theory.</p></div>
<div class="tcard"><div class="topic-num">3</div><h3>The 7-Minute Phone Call That Closes Deals</h3><p>The exact prospecting framework Connor used to build a pipeline worth millions. Your team will leave with a repeatable system they can use Monday morning. Based on his book <em>The 7 Minute Phone Call</em>.</p></div>
<div class="tcard"><div class="topic-num">4</div><h3>Building Wealth Through Real Estate Ownership</h3><p>Why every business owner should own the building their company operates from, and how to structure the deal. From Connor's book <em>Buy The Building, Keep The Profits</em>.</p></div>
<div class="tcard"><div class="topic-num">5</div><h3>From Author to Authority: Publishing as a Business Development Engine</h3><p>How writing a book (or five) builds credibility, generates inbound leads, and positions you as the go-to expert in your market. The playbook Connor used to establish his personal brand.</p></div>
<div class="tcard"><div class="topic-num">6</div><h3>Scaling with Systems, Not Just Hustle</h3><p>The operational frameworks, automation tools, and leadership principles that let founders step out of day-to-day firefighting and build businesses that run without them.</p></div>
</div></div></section>

<section class="sec sec-dk"><div class="ctn">
<h2 class="sec-t">Audiences Connor Connects With</h2>
<div class="saud">
<div class="acard"><h3>Entrepreneurs &amp; Founders</h3><p>From first-time buyers to seasoned operators looking to acquire their next company or scale what they have.</p></div>
<div class="acard"><h3>Corporate Teams &amp; Sales Organizations</h3><p>Actionable prospecting and pipeline-building frameworks your team can implement immediately.</p></div>
<div class="acard"><h3>Real Estate Investors &amp; Operators</h3><p>Strategies for building wealth through property ownership, creative deal structures, and portfolio scaling.</p></div>
<div class="acard"><h3>Conference &amp; Summit Organizers</h3><p>High-energy keynotes that leave audiences with real takeaways, not just inspiration, but implementation plans.</p></div>
</div></div></section>

<section class="podcast-section"><div class="ctn">
<h2 class="sec-t">As Heard On</h2>
<p class="sec-sub">Connor hosts The Prospecting Show and has been a featured guest on podcasts and media outlets reaching millions of listeners.</p>
<div class="podcast-grid">
<div class="pod-card"><h3>The Prospecting Show</h3><p>Connor's own weekly podcast, 350+ episodes interviewing entrepreneurs and small business owners about scaling their companies.</p><a href="https://www.prospectingshow.com" target="_blank" rel="noopener" class="pod-link">Listen Now &rarr;</a></div>
<div class="pod-card"><h3>Yahoo Finance</h3><p>Featured for the launch of Elixir Consulting Group's business automation advisory service.</p><a href="https://finance.yahoo.com/sectors/technology/articles/elixir-consulting-group-launches-business-112900872.html" target="_blank" rel="noopener" class="pod-link">Read More &rarr;</a></div>
<div class="pod-card"><h3>Business Insider</h3><p>Coverage of Elixir Consulting Group's advisory services for small and mid-sized business owners.</p><a href="https://markets.businessinsider.com/news/stocks/elixir-consulting-group-launches-business-automation-advisory-service-for-small-and-midsized-business-owners-1036100299" target="_blank" rel="noopener" class="pod-link">Read More &rarr;</a></div>
<div class="pod-card"><h3>The Globe and Mail</h3><p>National coverage of Connor's business consulting and automation advisory work.</p><a href="https://www.theglobeandmail.com/investing/markets/markets-news/Newsfile/1681496/elixir-consulting-group-launches-business-automation-advisory-service-for-small-and-mid-sized-business-owners/" target="_blank" rel="noopener" class="pod-link">Read More &rarr;</a></div>
</div>
</div></section>

<section class="lead-magnet"><div class="ctn">
<h2>Free Guide: 5 Strategies to Acquire Your First Business</h2>
<p class="lm-sub">The exact framework Connor teaches at live events, now available as a free download. Enter your email and get it instantly.</p>
<form class="lm-form" action="https://formspree.io/f/xdkobkzz" method="POST">
<input type="hidden" name="_subject" value="Lead Magnet Download Request">
<input type="hidden" name="source" value="speaker-page-lead-magnet">
<input type="email" name="email" placeholder="Enter your email address" required>
<button type="submit">Get the Free Guide</button>
</form>
<p class="lm-note">No spam. Unsubscribe anytime.</p>
</div></section>

<section class="books-strip"><div class="ctn">
<h2>Books by Dr. Connor Robertson</h2>
<p class="bs-sub">Six books on business acquisitions, wealth building, prospecting, and real estate strategy.</p>
<div class="books-row">{books_mini}</div>
<div style="text-align:center;margin-top:40px"><a href="/books/" class="btn-p">Browse All Books</a></div>
</div></section>

<section class="sec" id="book-me"><div class="ctn">
<h2 class="sec-t">Book Connor to Speak</h2>
<p class="sec-sub">Fill out the form below and Connor's team will follow up within 24 hours to discuss your event.</p>
<div class="cform">
<form action="https://formspree.io/f/xdkobkzz" method="POST">
<input type="hidden" name="_subject" value="Speaking Inquiry from drconnorrobertson.com">
<div class="fr"><div class="fg"><label>First Name</label><input type="text" name="first_name" required></div><div class="fg"><label>Last Name</label><input type="text" name="last_name" required></div></div>
<div class="fg"><label>Email</label><input type="email" name="email" required></div>
<div class="fg"><label>Organization / Company</label><input type="text" name="company" required></div>
<div class="fg"><label>Event Name</label><input type="text" name="event_name"></div>
<div class="fg"><label>Expected Audience Size</label><input type="number" name="event_size" min="0" placeholder="e.g. 200"></div>
<div class="fg"><label>Event Date (approximate is fine)</label><input type="date" name="event_date"></div>
<div class="fg"><label>Budget Range</label><select name="budget"><option value="">Select a range</option><option>Under $5,000</option><option>$5,000 - $10,000</option><option>$10,000 - $25,000</option><option>$25,000+</option></select></div>
<div class="fg"><label>Tell us about your event and what you are looking for</label><textarea name="speaking_request" rows="4" placeholder="Describe your event, audience, and any specific topics you would like Connor to cover..."></textarea></div>
<button type="submit" class="fsub">Submit Speaking Inquiry</button>
</form></div></div></section>
""" + footer()


def page_books():
    cards = ""
    book_schema_items = []
    for book in BOOKS:
        title, desc, retailers = book["title"], book["desc"], book["retailers"]
        slug = book["slug"]
        if retailers:
            retailer_links = "".join(f'<a href="{u}" target="_blank" rel="noopener" class="bk-retailer">{esc(s)}</a>' for s, u in retailers)
        else:
            retailer_links = '<span class="bk-coming-soon">Coming Soon</span>'
        # id= makes /books/#<slug> a real deep-link target for the pillar pages.
        cards += f'<div class="bk" id="{slug}"><h3>{esc(title)}</h3><p>{esc(desc)}</p><div class="bk-retailers">{retailer_links}</div></div>\n'
        offers = [{"@type": "Offer", "availability": "https://schema.org/InStock", "url": u, "seller": {"@type": "Organization", "name": s}} for s, u in retailers]
        book_schema_items.append({
            "@type": "Book",
            "@id": f"{SITE_URL}/books/#{slug}",
            "name": title,
            "url": f"{SITE_URL}/books/#{slug}",
            "author": {"@id": PERSON_ID},
            "publisher": {"@id": PERSON_ID},
            "description": desc,
            "inLanguage": "en",
            "bookFormat": "https://schema.org/EBook",
            "offers": offers,
        })
    book_list = {
        "@type": "ItemList",
        "@id": f"{SITE_URL}/books/#booklist",
        "name": "Books by Dr. Connor Robertson",
        "numberOfItems": len(book_schema_items),
        "itemListElement": [
            {"@type": "ListItem", "position": i, "item": b}
            for i, b in enumerate(book_schema_items, start=1)
        ],
    }
    return header("Books by Dr. Connor Robertson | Wealth & Acquisitions",
        "Books by Dr. Connor Robertson on wealth building, business acquisitions, real estate investing and entrepreneurship. Read the full list and buy online.",
        "/books/", og_image="/images/connor-book.jpg", page_type="CollectionPage",
        crumbs=[("Home", "/"), ("Books", None)],
        schema_nodes=[book_list]) + breadcrumbs([("Home", "/"), ("Books", None)]) + f"""
<section class="pg-hero"><div class="ctn">
<div style="text-align:center;margin-bottom:2rem;"><img src="/images/connor-book.jpg" alt="Dr. Connor Robertson - Author" width="300" height="300" loading="lazy" style="border-radius:12px;width:250px;height:250px;object-fit:cover;box-shadow:0 4px 20px rgba(0,0,0,0.15);"></div>
<h1>Books by Dr. Connor Robertson</h1><p>Practical guides on wealth building, real estate, and entrepreneurship by Dr. Connor Robertson.</p>
</div></section>
<section class="sec"><div class="ctn"><div class="bkgrid">{cards}</div>
<div style="text-align:center;margin-top:48px"><a href="/books/" class="btn-p">Browse All Books</a></div>
</div></section>

<section class="cta-banner"><div class="ctn">
<h2>Want Connor at Your Next Event?</h2>
<p>Connor delivers keynotes based on the frameworks from his books. Bring actionable strategies to your audience.</p>
<div class="cta-btns">
<a href="/speaker/" class="btn-p">Book Connor to Speak</a>
<a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener" class="btn-s">Work with Elixir Consulting</a>
</div>
</div></section>
""" + footer()


def page_press():
    cards = ""
    for title, url, source in PRESS_ARTICLES:
        cards += f'<div class="pcard"><div><h3>{esc(title)}</h3><p class="src">{esc(source)}</p></div><a href="{url}" target="_blank" rel="noopener" class="rl">Read &rarr;</a></div>\n'

    # One ItemList of externally published coverage. These articles live on other
    # domains, so they are listed as referenced works rather than declared as this
    # page's own NewsArticles (which would be invalid Article markup).
    press_list = {
        "@type": "ItemList",
        "@id": f"{SITE_URL}/press-media/#presslist",
        "name": "Press coverage of Dr. Connor Robertson",
        "numberOfItems": len(PRESS_ARTICLES),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "url": url,
                "item": {
                    "@type": "NewsArticle",
                    "@id": url,
                    "headline": title,
                    "url": url,
                    "publisher": {"@type": "Organization", "name": source},
                    "about": {"@id": PERSON_ID},
                    "mentions": {"@id": PERSON_ID},
                },
            }
            for i, (title, url, source) in enumerate(PRESS_ARTICLES, start=1)
        ],
    }

    return header("Dr. Connor Robertson in the Press | Media Features",
        "Press coverage of Dr. Connor Robertson in Yahoo Finance, The Globe and Mail, Business Insider, NY Wire, NewsBlaze, Economic Insider and more.",
        "/press-media/", og_image="/images/connor-press.jpg", page_type="CollectionPage",
        crumbs=[("Home", "/"), ("Press & Media", None)],
        schema_nodes=[press_list]) + breadcrumbs([("Home", "/"), ("Press & Media", None)]) + f"""
<section class="pg-hero"><div class="ctn">
<div style="text-align:center;margin-bottom:2rem;"><img src="/images/connor-press.jpg" alt="Dr. Connor Robertson - Press" width="300" height="300" loading="lazy" style="border-radius:50%;width:180px;height:180px;object-fit:cover;box-shadow:0 4px 20px rgba(0,0,0,0.15);"></div>
<h1>Press &amp; Media</h1><p>Dr. Connor Robertson's insights and features across leading publications.</p>
</div></section>
<section class="sec"><div class="ctn">
<div class="feat" style="padding:48px 0;margin-bottom:48px;border-bottom:none"><div class="feat-logos"><span>CXO Dispatch</span><span>C-Suite Brief</span><span>NY Wire</span><span>BLK News</span><span>Famous Times</span><span>Economic Insider</span><span>Taste Terminal</span><span>Fiction Talk</span><span>NewsBlaze</span><span>The Rogue Mag</span><span>InEntertainment</span><span>Yahoo Finance</span><span>The Globe and Mail</span><span>Business Insider</span></div></div>
<div class="pgrid">{cards}</div>
</div></section>
""" + footer()


def page_media():
    # Filenames must match what download_headshots() actually puts in dist/images/.
    photos = [
        ("dr-connor-robertson-headshot.jpg", "Dr. Connor Robertson professional headshot"),
        ("connor-headshot.jpg", "Dr. Connor Robertson professional portrait"),
        ("connor-blazer.jpg", "Dr. Connor Robertson in business blazer"),
        ("connor-hero.jpg", "Dr. Connor Robertson speaker portrait"),
        ("connor-casual.jpg", "Dr. Connor Robertson casual portrait"),
        ("connor-book.jpg", "Dr. Connor Robertson author photo"),
        ("connor-business.jpg", "Dr. Connor Robertson business strategist portrait"),
        ("connor-bold.jpg", "Dr. Connor Robertson editorial portrait"),
        ("connor-about.jpg", "Dr. Connor Robertson entrepreneur portrait"),
        ("connor-press.jpg", "Dr. Connor Robertson press portrait"),
    ]
    # Drop any photo that is not actually on disk, so the page never ships a 404.
    photos = [(f, a) for f, a in photos if (IMAGE_DIR / f).exists()]

    grid = ""
    image_items = []
    for i, (fname, alt) in enumerate(photos, start=1):
        grid += f'''<figure class="media-item" style="margin:0"><img src="/images/{fname}" alt="{alt}" width="400" height="400" loading="lazy" style="width:100%;height:auto;border-radius:8px;object-fit:cover;aspect-ratio:1;box-shadow:0 4px 16px rgba(0,0,0,0.1);"><figcaption style="margin-top:8px;font-size:13px;color:var(--smoke,#666);">{alt} &middot; <a href="/images/{fname}" download style="text-decoration:underline">Download</a></figcaption></figure>
'''
        image_items.append({
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "ImageObject",
                "@id": f"{SITE_URL}/media/#{fname}",
                "name": alt,
                "url": f"{SITE_URL}/images/{fname}",
                "contentUrl": f"{SITE_URL}/images/{fname}",
                "description": f"{alt} - available for editorial and media use with attribution.",
                "creator": {"@id": PERSON_ID},
                "copyrightHolder": {"@id": PERSON_ID},
                "creditText": "Dr. Connor Robertson",
                "acquireLicensePage": f"{SITE_URL}/media/",
            },
        })

    media_list = {
        "@type": "ItemList",
        "@id": f"{SITE_URL}/media/#photolist",
        "name": "Press photos of Dr. Connor Robertson",
        "numberOfItems": len(image_items),
        "itemListElement": image_items,
    }

    return header("Media Kit & Press Photos | Dr. Connor Robertson",
        "Download press photos of Dr. Connor Robertson for media coverage, event promotion, podcast features and editorial use. Free with attribution.",
        "/media/", og_image="/images/dr-connor-robertson-headshot.jpg", page_type="CollectionPage",
        crumbs=[("Home", "/"), ("Media Kit", None)],
        schema_nodes=[media_list]) + breadcrumbs([("Home", "/"), ("Media Kit", None)]) + f"""
<section class="pg-hero"><div class="ctn">
<h1>Media Kit &amp; Press Photos</h1>
<p>Professional photos of Dr. Connor Robertson available for journalists, event organizers, podcast hosts, and editorial teams. All images may be used for media coverage with attribution.</p>
</div></section>
<section class="sec"><div class="ctn">
<div style="background:var(--bg-card,#f8f8f8);border:1px solid var(--border,#e0e0e0);border-radius:12px;padding:24px 32px;margin-bottom:48px;">
<p style="font-size:15px;margin:0;"><strong>Download for media use:</strong> Use the download link under any photo, or right-click and choose "Save image as." Please credit "Dr. Connor Robertson." For high-resolution originals or specific requests, <a href="/contact/" style="color:var(--accent,#2563eb);text-decoration:underline;">contact Connor directly</a>.</p>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;">
{grid}
</div>
<style>@media(max-width:900px){{[style*="grid-template-columns:repeat(3"]{{grid-template-columns:repeat(2,1fr)!important;}}}}@media(max-width:600px){{[style*="grid-template-columns:repeat(3"]{{grid-template-columns:1fr!important;}}}}</style>
</div></section>
""" + footer()



def page_contact():
    contact_point = {
        "@type": "ContactPoint",
        "@id": f"{SITE_URL}/contact/#contactpoint",
        "contactType": "Business, speaking and press inquiries",
        "url": f"{SITE_URL}/contact/",
        "availableLanguage": ["English"],
        "areaServed": "US",
    }
    return header("Contact Dr. Connor Robertson | Speaking & Inquiries",
        "Contact Dr. Connor Robertson for business inquiries, speaking engagements, press and media requests, and partnership opportunities.",
        "/contact/", og_image="/images/connor-contact.jpg", page_type="ContactPage",
        crumbs=[("Home", "/"), ("Contact", None)],
        schema_nodes=[contact_point]) + breadcrumbs([("Home", "/"), ("Contact", None)]) + """
<section class="pg-hero"><div class="ctn">
<h1>Contact Dr. Connor Robertson</h1><p>Business inquiries, speaking engagements, press, partnerships, and more.</p>
</div></section>
<section class="sec"><div class="ctn">
<div class="contact-headshot fade-in"><img src="/images/connor-contact.jpg" alt="Dr. Connor Robertson - Contact" width="160" height="160" loading="lazy" decoding="async"></div>
<div class="cform">
<form action="https://formspree.io/f/xdkobkzz" method="POST">
<div class="fr"><div class="fg"><label for="cf-first">First Name *</label><input id="cf-first" type="text" name="first_name" autocomplete="given-name" required></div><div class="fg"><label for="cf-last">Last Name *</label><input id="cf-last" type="text" name="last_name" autocomplete="family-name" required></div></div>
<div class="fg"><label for="cf-email">Email *</label><input id="cf-email" type="email" name="email" autocomplete="email" required></div>
<div class="fg"><label for="cf-company">Company</label><input id="cf-company" type="text" name="company" autocomplete="organization"></div>
<div class="fg"><label for="cf-website">Website</label><input id="cf-website" type="url" name="website" autocomplete="url"></div>
<div class="fg"><label for="cf-phone">Phone</label><input id="cf-phone" type="tel" name="phone" autocomplete="tel"></div>
<div class="fg"><label for="cf-purpose">Purpose *</label><select id="cf-purpose" name="purpose" required><option value="">Select...</option><option>General Contact</option><option>Learn More About Connor</option><option>Book Connor For Event</option><option>Press &amp; Media Inquiry</option><option>Partnership</option><option>Other</option></select></div>
<div class="fg"><label for="cf-message">Message</label><textarea id="cf-message" name="message" rows="5"></textarea></div>
<button type="submit" class="fsub">Submit</button>
</form></div></div></section>
""" + footer()


def page_projects():
    ventures = [
        ("The Prospecting Show", "https://www.prospectingshow.com", "A weekly podcast interviewing entrepreneurs about how they built and scaled their businesses."),
        ("The Pittsburgh Wire", "https://thepittsburghwire.com", "An independent digital publication covering Pittsburgh business, real estate, and economic development."),
        ("Elixir Consulting Group", "https://elixirconsultinggroup.com", "Business automation and AI advisory for small and mid-sized business owners."),
        ("The Grant Finder", "https://thegrantfinder.com", "A grant discovery platform for nonprofits and small businesses."),
    ]
    venture_list = {
        "@type": "ItemList",
        "@id": f"{SITE_URL}/projects/#ventures",
        "name": "Ventures founded by Dr. Connor Robertson",
        "numberOfItems": len(ventures),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "item": {
                    "@type": "Organization",
                    "@id": url,
                    "name": name,
                    "url": url,
                    "description": desc,
                    "founder": {"@id": PERSON_ID},
                },
            }
            for i, (name, url, desc) in enumerate(ventures, start=1)
        ],
    }
    return header("Projects & Companies | Dr. Connor Robertson",
        "The companies and media brands founded by Dr. Connor Robertson: Elixir Consulting Group, The Pittsburgh Wire, The Prospecting Show and The Grant Finder.",
        "/projects/", og_image="/images/dr-connor-robertson-headshot.jpg", page_type="CollectionPage",
        crumbs=[("Home", "/"), ("Projects", None)],
        schema_nodes=[venture_list]) + breadcrumbs([("Home", "/"), ("Projects", None)]) + """
<section class="pg-hero"><div class="ctn">
<h1>Projects &amp; Companies</h1><p>The companies, media properties, and ventures I've built.</p>
</div></section>
<section class="sec"><div class="ctn">

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:32px;margin-bottom:48px;">

<div style="background:var(--bg-card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:32px;transition:box-shadow .2s;">
<h3 style="font-size:22px;margin-bottom:8px;">The Prospecting Show</h3>
<p style="color:var(--text-secondary,#6b7280);font-size:14px;line-height:1.7;margin-bottom:16px;">A weekly podcast interviewing entrepreneurs about how they built and scaled their businesses. 350+ episodes on Spotify, Apple Podcasts, YouTube, and all major platforms.</p>
<a href="https://prospectingshow.com" target="_blank" rel="noopener" style="color:var(--accent,#2563eb);font-weight:600;font-size:14px;">Visit prospectingshow.com &rarr;</a>
</div>

<div style="background:var(--bg-card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:32px;transition:box-shadow .2s;">
<h3 style="font-size:22px;margin-bottom:8px;">The Pittsburgh Wire</h3>
<p style="color:var(--text-secondary,#6b7280);font-size:14px;line-height:1.7;margin-bottom:16px;">An independent digital publication covering Pittsburgh business, real estate, economic development, and the people building the city. Published daily, Monday through Friday.</p>
<a href="https://thepittsburghwire.com" target="_blank" rel="noopener" style="color:var(--accent,#2563eb);font-weight:600;font-size:14px;">Visit thepittsburghwire.com &rarr;</a>
</div>

<div style="background:var(--bg-card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:32px;transition:box-shadow .2s;">
<h3 style="font-size:22px;margin-bottom:8px;">Elixir Consulting Group</h3>
<p style="color:var(--text-secondary,#6b7280);font-size:14px;line-height:1.7;margin-bottom:16px;">A consulting firm advising real estate investors, business owners, and high-income professionals on tax strategy, entity structuring, and accelerated depreciation.</p>
<a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener" style="color:var(--accent,#2563eb);font-weight:600;font-size:14px;">Visit elixirconsultinggroup.com &rarr;</a>
</div>

<div style="background:var(--bg-card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:32px;transition:box-shadow .2s;">
<h3 style="font-size:22px;margin-bottom:8px;">Books by Dr. Connor Robertson</h3>
<p style="color:var(--text-secondary,#6b7280);font-size:14px;line-height:1.7;margin-bottom:16px;">Multiple books on entrepreneurship, business acquisitions, and wealth building. Available on Amazon, Barnes &amp; Noble, Google Play, and Apple Books.</p>
<a href="/books/" style="color:var(--accent,#2563eb);font-weight:600;font-size:14px;">Browse all books &rarr;</a>
</div>

<div style="background:var(--bg-card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:32px;transition:box-shadow .2s;">
<h3 style="font-size:22px;margin-bottom:8px;">The Grant Finder</h3>
<p style="color:var(--text-secondary,#6b7280);font-size:14px;line-height:1.7;margin-bottom:16px;">A resource helping nonprofits and small businesses discover and access government grants, foundation funding, and alternative financing opportunities.</p>
<a href="https://thegrantfinder.org" target="_blank" rel="noopener" style="color:var(--accent,#2563eb);font-weight:600;font-size:14px;">Visit thegrantfinder.org &rarr;</a>
</div>

<div style="background:var(--bg-card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:32px;transition:box-shadow .2s;">
<h3 style="font-size:22px;margin-bottom:8px;">Swift Line Capital</h3>
<p style="color:var(--text-secondary,#6b7280);font-size:14px;line-height:1.7;margin-bottom:16px;">A lending platform connecting real estate investors with fast, flexible funding for fix-and-flip, bridge, DSCR, and ground-up construction loans.</p>
<a href="https://swiftline-portal.vercel.app" target="_blank" rel="noopener" style="color:var(--accent,#2563eb);font-weight:600;font-size:14px;">Visit Swift Line Capital &rarr;</a>
</div>

</div>
</div></section>
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
                feat_img = f'<img src="{local}" alt="{esc(strip_tags(p["title"]))}" class="bcard-img" width="400" height="225" loading="lazy">'
        cards += f'<a href="{p["relative_url"]}" class="bcard">{feat_img}<div class="bcard-body"><h3>{p["title"]}</h3><p class="exc">{esc(exc)}</p><span class="meta">{dt}</span><div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.75rem;padding-top:0.75rem;border-top:1px solid rgba(0,0,0,0.08);"><img src="/images/connor-blog-author.jpg" alt="Dr. Connor Robertson" width="28" height="28" loading="lazy" style="border-radius:50%;width:28px;height:28px;object-fit:cover;"><span style="font-size:0.8rem;color:#666;">Dr. Connor Robertson</span></div></div></a>\n'
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
    prev_url = "" if page_num == 1 else ("/blog/" if page_num == 2 else f"/blog/page/{page_num - 1}/")
    next_url = f"/blog/page/{page_num + 1}/" if page_num < total_pages else ""

    blog_node = {
        "@type": "Blog",
        "@id": f"{SITE_URL}/blog/#blog",
        "name": "The Dr. Connor Robertson Blog",
        "description": "Articles on business acquisitions, AI strategy, prospecting systems, and Pittsburgh business.",
        "url": f"{SITE_URL}/blog/",
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": PERSON_ID},
        "inLanguage": "en-US",
    }
    post_list = {
        "@type": "ItemList",
        "@id": f"{SITE_URL}{can}#postlist",
        "name": "Articles by Dr. Connor Robertson",
        "numberOfItems": len(batch),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": start + i,
                "url": f"{SITE_URL}{p['relative_url']}",
                "name": strip_tags(p["title"]),
            }
            for i, p in enumerate(batch, start=1)
        ],
    }
    return header(f"Dr. Connor Robertson Blog | Business & Pittsburgh{sfx}",
        "Articles by Dr. Connor Robertson on business acquisitions, AI strategy, prospecting systems, leadership and Pittsburgh business.",
        can, og_image="/images/dr-connor-robertson-headshot.jpg", page_type="CollectionPage",
        crumbs=[("Home", "/"), ("Blog", None)],
        schema_nodes=[blog_node, post_list],
        prev_url=prev_url, next_url=next_url) + breadcrumbs([("Home", "/"), ("Blog", None)]) + f"""
<section class="pg-hero"><div class="ctn"><h1>Blog, Leadership &amp; Entrepreneurship</h1>
<p>Practical writing on buying businesses, deploying AI, building a prospecting engine, and investing in Pittsburgh. Start with the <a href="/business-acquisitions/">business acquisitions guide</a>, the <a href="/ai-business-strategy/">AI business strategy guide</a>, the <a href="/prospecting-sales/">prospecting and sales guide</a>, or the <a href="/author-platform/">author platform guide</a>.</p></div></section>
<section class="sec"><div class="ctn"><div class="bgrid">{cards}</div>{pag}</div></section>
""" + footer()


def page_post(p, all_posts=None):
    try:
        dt = datetime.fromisoformat(p["date"]).strftime("%B %d, %Y")
    except:
        dt = ""
    seo = POST_SEO.get(p["slug"], {})
    exc = strip_tags(p.get("excerpt", ""))
    meta_desc = seo.get("desc") or clip(exc)

    # Featured image
    feat_img_html = ""
    og_image = ""
    if p.get("featured_image"):
        local = downloaded_images.get(p["featured_image"], p["featured_image"])
        feat_img_html = f'<img src="{local}" alt="{esc(strip_tags(p["title"]))}" class="post-feat" width="1200" height="675" loading="lazy">'
        og_image = local
    else:
        og_image = "/images/dr-connor-robertson-headshot.jpg"

    # Rewrite images in post content
    content = rewrite_image_urls(p["content"])

    # Repoint links that WordPress left aimed at hosts that no longer resolve
    global dead_links_rewritten
    content, n_dead = rewrite_dead_links(content)
    dead_links_rewritten += n_dead
    content = normalize_dashes(content)

    word_count = len(strip_tags(content).split())

    # Article schema, wired into the sitewide Person/WebSite graph by @id
    article_node = {
        "@type": "BlogPosting",
        "@id": f"{SITE_URL}{p['relative_url']}#article",
        "headline": clip(strip_tags(p["title"]), 110),
        "name": strip_tags(p["title"]),
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": PERSON_ID},
        "datePublished": p["date"],
        "dateModified": p["date"],
        "description": meta_desc,
        "wordCount": word_count,
        "inLanguage": "en-US",
        "isPartOf": {"@id": f"{SITE_URL}/blog/#blog"},
        "mainEntityOfPage": {"@id": f"{SITE_URL}{p['relative_url']}#webpage"},
        "keywords": [strip_tags(c) for c in p.get("categories", [])] or None,
    }
    if og_image:
        article_node["image"] = f"{SITE_URL}{og_image}" if og_image.startswith("/") else og_image
    article_node = {k: v for k, v in article_node.items() if v is not None}

    schema_nodes = [article_node]

    # Long-tail Q&A: rendered on the page and mirrored as FAQPage schema.
    faq_html = ""
    faqs = seo.get("faqs") or []
    if faqs:
        rows = "".join(
            f'<details class="post-faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
            for q, a in faqs
        )
        faq_html = f"""<section class="post-faq" style="margin-top:48px;padding-top:32px;border-top:1px solid var(--border)">
<h2 style="font-size:24px;font-weight:700;margin-bottom:16px">Frequently Asked Questions</h2>
{rows}
</section>"""
        schema_nodes.append({
            "@type": "FAQPage",
            "@id": f"{SITE_URL}{p['relative_url']}#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })

    # Contextual link into the matching topic hub.
    hub_html = ""
    if seo.get("hub"):
        hub_label, hub_href = seo["hub"]
        hub_html = (f'<p style="margin-top:32px;font-size:15px"><strong>Go deeper:</strong> '
                    f'read the full <a href="{hub_href}" style="text-decoration:underline">{esc(hub_label)}</a>.</p>')

    article_meta = (f'<meta property="article:published_time" content="{esc(p["date"])}">'
                    f'<meta property="article:modified_time" content="{esc(p["date"])}">'
                    f'<meta property="article:author" content="Dr. Connor Robertson">'
                    + "".join(f'<meta property="article:section" content="{esc(strip_tags(c))}">'
                              for c in p.get("categories", [])[:1]))

    # Title tag: prefer the hand-written SEO title, which is kept under the
    # ~60 char SERP limit. Raw post titles run long and get truncated.
    raw_title = p["title"]
    if seo.get("title"):
        page_title = seo["title"]
    elif "connor robertson" in raw_title.lower():
        page_title = f"{raw_title} | drconnorrobertson.com"
    else:
        page_title = f"{raw_title} | Dr. Connor Robertson"

    # Internal linking footer for every blog post
    internal_links = """<div style="margin-top:48px;padding:32px;background:var(--card);border:1px solid var(--border);border-radius:12px">
<h3 style="font-size:18px;font-weight:700;margin-bottom:16px">About the Author</h3>
<p style="color:var(--text2);font-size:14px;line-height:1.7;margin-bottom:16px"><a href="/about/" style="text-decoration:underline">Dr. Connor Robertson</a> is a Pittsburgh-based entrepreneur, author, and podcast host. He is the founder of <a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener">Elixir Consulting Group</a>, publisher of <a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a>, and host of <a href="https://www.prospectingshow.com" target="_blank" rel="noopener">The Prospecting Show</a>.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a href="/about/" class="btn-s" style="padding:8px 20px;font-size:13px">About Connor</a><a href="/books/" class="btn-s" style="padding:8px 20px;font-size:13px">Books</a><a href="/contact/" class="btn-s" style="padding:8px 20px;font-size:13px">Contact</a></div>
</div>"""

    crumb_trail = [("Home", "/"), ("Blog", "/blog/"), (strip_tags(p["title"]), None)]
    return header(page_title, meta_desc, p["relative_url"], extra=article_meta,
                  og_image=og_image, og_type="article", page_type="WebPage",
                  crumbs=crumb_trail, schema_nodes=schema_nodes) + breadcrumbs(crumb_trail) + f"""
<article class="post">
{feat_img_html}
<h1>{p["title"]}</h1>
<p class="pm"><time datetime="{esc(p["date"][:10])}">{dt}</time> &middot; <a href="/about/" style="color:var(--muted);text-decoration:underline">Dr. Connor Robertson</a></p>
<div class="pb">{content}</div>
{hub_html}
{faq_html}
{internal_links}
<div style="margin-top:24px;padding-top:24px;border-top:1px solid var(--border)"><a href="/blog/" style="font-size:14px;color:var(--muted)">&larr; Back to Blog</a></div>

<section class="author-bio" style="max-width:800px;margin:3rem auto;padding:2rem;background:#f8f9fa;border-radius:12px;display:flex;gap:1.5rem;align-items:center;"><img src="/images/connor-casual.jpg" alt="Dr. Connor Robertson" width="120" height="120" loading="lazy" style="border-radius:50%;width:120px;height:120px;object-fit:cover;flex-shrink:0;"><div><strong style="font-size:1.1rem;">Dr. Connor Robertson</strong><p style="margin:0.5rem 0 0;color:#555;line-height:1.6;">Entrepreneur, author, and podcast host based in Pittsburgh. Connor writes about business strategy, leadership, and building ventures that create lasting impact. <a href="/books/" style="color:#0066cc;text-decoration:underline;">Explore his published books</a>.</p></div></section>
</article>
""" + related_posts_html(p["relative_url"], all_posts) + footer()


# Ã¢ÂÂÃ¢ÂÂ File writers Ã¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂ

def write(path, content):
    full = DIST / path.lstrip("/")
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")

# lastmod for evergreen pages. Bump this when their copy is edited -- stamping
# every build with today's date trains crawlers to ignore the field entirely.
STATIC_LASTMOD = "2026-08-09"

SITEMAP_PRIORITY = {
    "/": ("1.0", "weekly"),
    "/about/": ("0.9", "monthly"),
    "/blog/": ("0.9", "weekly"),
    "/business-acquisitions/": ("0.8", "monthly"),
    "/ai-business-strategy/": ("0.8", "monthly"),
    "/prospecting-sales/": ("0.8", "monthly"),
    "/author-platform/": ("0.8", "monthly"),
    "/speaker/": ("0.8", "monthly"),
    "/books/": ("0.8", "monthly"),
    "/faq/": ("0.8", "monthly"),
    "/projects/": ("0.7", "monthly"),
    "/media/": ("0.7", "yearly"),
    "/press-media/": ("0.7", "monthly"),
    "/contact/": ("0.6", "yearly"),
    "/blog/complete-resource-index-dr-connor-robertson/": ("0.6", "weekly"),
}
SITEMAP_PRIORITY.update({href: ("0.7", "weekly") for _label, href in RESOURCE_HUBS})


def robots_txt():
    """Allow everything, and name the crawlers that matter explicitly.

    Bravebot is Brave Search's crawler, Brave has no URL-submission tool, so
    an unambiguous crawl permission plus the sitemap reference is the only
    lever a site owner actually has there.
    """
    named_bots = [
        "Googlebot", "Googlebot-Image", "Bingbot", "Bravebot", "DuckDuckBot",
        "Applebot", "YandexBot", "Slurp", "Twitterbot", "facebookexternalhit",
        "LinkedInBot", "OAI-SearchBot", "PerplexityBot",
    ]
    blocks = "\n\n".join(f"User-agent: {b}\nAllow: /" for b in named_bots)
    return (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"{blocks}\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )


def sitemap(posts):
    """Build the sitemap from the pages actually written to dist/.

    Scanning the output instead of a hand-maintained URL list means the sitemap
    can never drift out of sync with the site, and never lists a 404.
    """
    post_by_url = {p["relative_url"]: p for p in posts}
    urls = []
    for f in sorted(DIST.rglob("index.html")):
        rel = f.relative_to(DIST).parent
        loc = "/" if str(rel) == "." else f"/{rel.as_posix()}/"
        html_text = f.read_text(encoding="utf-8", errors="replace")
        if 'content="noindex' in html_text:
            continue
        p = post_by_url.get(loc)
        if p:
            lastmod, prio, freq = p["date"][:10], "0.6", "monthly"
        else:
            prio, freq = SITEMAP_PRIORITY.get(loc, ("0.6", "monthly"))
            lastmod = STATIC_LASTMOD
        # Surface the page's primary image so it is eligible for image search.
        img = ""
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html_text)
        if m:
            img = (f'\n    <image:image><image:loc>{esc(m.group(1))}</image:loc>'
                   f'<image:title>{esc(clip(strip_tags(re.search(r"<title>(.*?)</title>", html_text, re.S).group(1)), 90))}</image:title>'
                   f'</image:image>')
        urls.append(
            f"  <url><loc>{SITE_URL}{loc}</loc><lastmod>{lastmod}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{prio}</priority>{img}</url>"
        )
    body = "\n".join(urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        f"{body}\n</urlset>\n"
    )


# Ã¢ÂÂÃ¢ÂÂ Main Ã¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂÃ¢ÂÂ


# ── Pillar / Topic Hub Pages ──────────────────────────────────

def page_business_acquisitions():
    topic_page = {
        "@type": "TechArticle",
        "@id": f"{SITE_URL}/business-acquisitions/#guide",
        "headline": "Business Acquisitions",
        "name": "Business Acquisitions",
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": PERSON_ID},
        "about": {"@id": PERSON_ID},
        "inLanguage": "en-US",
        "mainEntityOfPage": {"@id": f"{SITE_URL}/business-acquisitions/#webpage"},
    }

    return header("Business Acquisitions Guide | Dr. Connor Robertson",
        "How to buy a business: deal sourcing, structures, due diligence, financing and valuation, from acquisition strategist Dr. Connor Robertson.",
        "/business-acquisitions/", og_image="/images/dr-connor-robertson-headshot.jpg",
        crumbs=[("Home", "/"), ("Business Acquisitions", None)],
        schema_nodes=[topic_page]) + breadcrumbs([("Home", "/"), ("Business Acquisitions", None)]) + """
<section class="pg-hero"><div class="ctn">
<h1>Business Acquisitions: The Complete Guide to Buying Businesses</h1>
<p>Master the frameworks, strategies, and systems that Dr. Connor Robertson uses to acquire businesses, from deal sourcing to integration and scale.</p>
</div></section>
<section class="sec"><div class="ctn">

<h2 class="fade-in">Why Buying Beats Building</h2>
<p class="fade-in">Most entrepreneurs face a critical decision early in their journey: should they build a business from scratch, or acquire an existing one? After years of both building and buying, the answer is clear, for most people, buying is the faster, lower-risk path to wealth and freedom.</p>
<p class="fade-in">When you acquire a business, you inherit proven revenue streams, existing customer relationships, established operational systems, and a team already in place. An existing business generating $1M in annual revenue might be purchased for 3-5x seller discretionary earnings. Compare that to the 5-10 years and significantly more capital required to build from zero, and the math speaks for itself.</p>
<p class="fade-in">The strategic advantages compound over time. Immediate cash flow means you can service acquisition debt from day one. Reduced risk means your capital is deployed against proven models rather than unvalidated ideas. An existing team reduces the hiring burden. Established customer relationships provide a foundation for growth rather than starting from an empty pipeline.</p>

<h2 class="fade-in">Deal Structures That Work</h2>
<p class="fade-in">Understanding deal structures is where most aspiring acquirers get stuck. The reality is that there are dozens of ways to structure a business purchase, and the best deals often combine multiple approaches to create win-win outcomes for both buyer and seller.</p>
<h3 class="fade-in">Asset Purchase vs. Stock Purchase</h3>
<p class="fade-in">In an asset purchase, you buy specific assets of the business, equipment, inventory, customer lists, intellectual property, without taking on the entity itself. This protects you from unknown liabilities and often provides better depreciation benefits. In a stock purchase, you buy the entity outright, including all assets and liabilities. Stock purchases are simpler but carry more risk.</p>
<h3 class="fade-in">Seller Financing</h3>
<p class="fade-in">Seller financing is one of the most powerful tools in creative acquisitions. The seller carries a note for a portion of the purchase price, typically 20-60%, creating alignment between buyer and seller. The seller gets a higher total price and ongoing income. The buyer gets favorable terms and reduced upfront capital requirements. Dr. Robertson covers this extensively in <a href="/books/#creative-acquisitions">Creative Acquisitions</a>.</p>
<h3 class="fade-in">Earnouts and Performance-Based Structures</h3>
<p class="fade-in">Earnouts bridge valuation gaps by tying a portion of the purchase price to future business performance. If the seller believes the business will grow, they accept an earnout because they expect to earn more total. If the buyer is uncertain about projections, they reduce risk by paying only when results materialize.</p>

<h2 class="fade-in">The Due Diligence Framework</h2>
<p class="fade-in">Due diligence separates successful acquirers from those who overpay for problems. A systematic approach ensures you uncover the real condition of the business before committing capital.</p>
<p class="fade-in"><strong>Financial Due Diligence:</strong> Verify revenue quality, examine customer concentration, analyze margins by product line, review accounts receivable aging, and confirm that reported earnings match actual cash flow. Look at three years of financials minimum.</p>
<p class="fade-in"><strong>Operational Due Diligence:</strong> Assess the team, systems, and processes that make the business run. How dependent is the business on the current owner? What happens if key employees leave? Are standard operating procedures documented?</p>
<p class="fade-in"><strong>Market Due Diligence:</strong> Evaluate the competitive landscape, market trends, customer satisfaction, and growth potential. Is the industry growing or declining? Are there regulatory risks on the horizon?</p>
<p class="fade-in"><strong>Legal Due Diligence:</strong> Review contracts, leases, intellectual property, pending litigation, compliance history, and employment agreements. Engage qualified legal counsel for this phase, it is not the place to cut corners.</p>

<h2 class="fade-in">Financing Your Acquisition</h2>
<p class="fade-in">Most business acquisitions do not require you to write a check for the full purchase price. Understanding financing options allows you to acquire larger businesses with less personal capital at risk.</p>
<p class="fade-in"><strong>SBA Loans:</strong> The Small Business Administration guarantees loans up to $5M for business acquisitions. SBA 7(a) loans typically require 10-20% down and offer 10-year terms. These are the most common financing vehicle for acquisitions under $5M.</p>
<p class="fade-in"><strong>Seller Financing:</strong> As mentioned above, seller notes reduce the amount of third-party financing needed and demonstrate the seller's confidence in the business's future.</p>
<p class="fade-in"><strong>Conventional Bank Loans:</strong> Traditional commercial loans may offer better rates than SBA loans for well-qualified buyers with strong collateral and industry experience.</p>
<p class="fade-in"><strong>Private Equity and Investor Capital:</strong> For larger deals, bringing in equity partners or investors can provide the capital needed while distributing risk.</p>

<h2 class="fade-in">Valuation Methods</h2>
<p class="fade-in">Business valuation is both art and science. Multiple approaches exist, and the best acquirers use several methods to triangulate fair value.</p>
<p class="fade-in"><strong>Multiple of SDE:</strong> Seller Discretionary Earnings multiplied by an industry-appropriate multiple (typically 2-4x for small businesses). This is the most common method for businesses under $5M in revenue.</p>
<p class="fade-in"><strong>Multiple of EBITDA:</strong> For larger businesses, EBITDA multiples (typically 4-8x) provide a more standardized valuation framework. Industry, growth rate, and risk profile determine where in the range a business falls.</p>
<p class="fade-in"><strong>Discounted Cash Flow:</strong> Projects future cash flows and discounts them to present value. More complex but accounts for growth trajectory and investment requirements.</p>
<p class="fade-in"><strong>Asset-Based Valuation:</strong> Values the business based on its tangible and intangible assets. Useful as a floor value or for asset-heavy businesses.</p>

<h2 class="fade-in">Your First Acquisition Roadmap</h2>
<p class="fade-in">Getting from idea to closed deal requires a systematic approach. Here is the framework Dr. Robertson recommends for first-time acquirers:</p>
<p class="fade-in"><strong>Phase 1, Define Your Criteria:</strong> What size business? What industry? What geographic area? What cash flow do you need? Getting clear on criteria prevents wasted time on wrong-fit opportunities.</p>
<p class="fade-in"><strong>Phase 2, Source Deals:</strong> Business brokers, online marketplaces, direct outreach to owners, your professional network, and industry events are all viable deal sources. The best deals are often found off-market through relationships and direct outreach.</p>
<p class="fade-in"><strong>Phase 3, Evaluate and Negotiate:</strong> Apply your due diligence framework, develop your valuation, and structure a deal that works for both parties. This is where the principles from <a href="/books/#creative-acquisitions">Creative Acquisitions</a> become critical.</p>
<p class="fade-in"><strong>Phase 4, Close and Integrate:</strong> Legal documentation, financing finalization, transition planning, and day-one operations. The first 90 days after closing determine long-term success.</p>
<p class="fade-in"><strong>Phase 5, Optimize and Scale:</strong> Apply systems thinking to improve operations, reduce owner dependency, and position for growth or additional acquisitions.</p>

<div class="quote fade-in" style="margin:48px 0">
<p class="quote-t">"The best time to buy a business was five years ago. The second best time is right now."</p>
<p class="quote-a"><strong>Dr. Connor Robertson</strong></p>
</div>

<h2 class="fade-in">Related Resources</h2>
<div class="pills fade-in" style="margin-top:24px">
<div class="pill"><h3><a href="/ai-business-strategy/">AI Business Strategy</a></h3><p>How to use AI to optimize operations after your acquisition.</p></div>
<div class="pill"><h3><a href="/prospecting-sales/">Prospecting & Sales</a></h3><p>Build the pipeline that feeds your acquisition deal flow.</p></div>
<div class="pill"><h3><a href="/author-platform/">Author Platform</a></h3><p>Establish authority that attracts off-market deal opportunities.</p></div>
<div class="pill"><h3><a href="/books/#creative-acquisitions">Creative Acquisitions (Book)</a></h3><p>The complete playbook for modern dealmakers.</p></div>
<div class="pill"><h3><a href="/books/#buying-wealth">Buying Wealth (Book)</a></h3><p>A practical guide to building wealth through ownership.</p></div>
</div>

<div style="margin-top:48px;padding:32px;background:var(--card);border-radius:var(--r);text-align:center" class="fade-in">
<h3>Ready to Make Your First Acquisition?</h3>
<p style="margin:16px 0;color:var(--text2)">Dr. Connor Robertson helps entrepreneurs acquire businesses through proven frameworks and hands-on guidance.</p>
<a href="/contact/" class="btn-p" style="display:inline-block;margin-top:12px">Contact Connor</a>
</div>

</div></section>
""" + footer()


def page_ai_business_strategy():
    topic_page = {
        "@type": "TechArticle",
        "@id": f"{SITE_URL}/ai-business-strategy/#guide",
        "headline": "AI Business Strategy",
        "name": "AI Business Strategy",
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": PERSON_ID},
        "about": {"@id": PERSON_ID},
        "inLanguage": "en-US",
        "mainEntityOfPage": {"@id": f"{SITE_URL}/ai-business-strategy/#webpage"},
    }

    return header("AI Business Strategy Guide | Dr. Connor Robertson",
        "How to deploy AI across marketing, operations and sales for real competitive advantage, without the hype. A practical guide for business owners.",
        "/ai-business-strategy/", og_image="/images/dr-connor-robertson-headshot.jpg",
        crumbs=[("Home", "/"), ("AI Business Strategy", None)],
        schema_nodes=[topic_page]) + breadcrumbs([("Home", "/"), ("AI Business Strategy", None)]) + """
<section class="pg-hero"><div class="ctn">
<h1>AI Business Strategy: How Entrepreneurs Use AI for Competitive Advantage</h1>
<p>Practical frameworks for deploying artificial intelligence across marketing, operations, and sales, without the hype.</p>
</div></section>
<section class="sec"><div class="ctn">

<h2 class="fade-in">The Strategic Imperative</h2>
<p class="fade-in">Artificial intelligence is not a future consideration, it is a present-day competitive weapon. Entrepreneurs who deploy AI strategically today are building advantages that compound over time, while those who wait find themselves playing catch-up against competitors who move faster, respond quicker, and operate more efficiently.</p>
<p class="fade-in">The opportunity is not about replacing humans with machines. It is about augmenting human decision-making, automating repetitive workflows, and creating systems that scale without proportional increases in headcount or cost. The businesses that win in 2026 and beyond will be those that treat AI as infrastructure, not as a novelty.</p>

<h2 class="fade-in">AI for Marketing Automation</h2>
<p class="fade-in">Marketing is where most businesses see their first AI wins. The combination of content generation, audience targeting, and performance optimization creates immediate ROI for businesses of any size.</p>
<p class="fade-in"><strong>Content Systems:</strong> AI enables entrepreneurs to produce high-quality content at 10x the volume of manual creation. Blog posts, social media content, email sequences, video scripts, and advertising copy can all be generated, refined, and optimized using AI tools. The key is building systems, not just using tools occasionally, but creating repeatable workflows that produce consistent output.</p>
<p class="fade-in"><strong>Audience Intelligence:</strong> AI analyzes customer behavior patterns, identifies high-value segments, predicts churn, and personalizes messaging at scale. What previously required a team of data analysts can now be accomplished with properly configured AI systems.</p>
<p class="fade-in"><strong>Performance Optimization:</strong> AI continuously tests headlines, images, copy variants, and audience segments to maximize conversion rates. The compounding effect of daily optimization creates significant advantages over competitors who optimize monthly or quarterly.</p>

<h2 class="fade-in">AI for Operations</h2>
<p class="fade-in">Operational efficiency is where AI delivers its most dramatic long-term impact. Every repetitive process in your business is a candidate for AI augmentation or full automation.</p>
<p class="fade-in"><strong>Workflow Automation:</strong> Invoice processing, data entry, scheduling, inventory management, customer onboarding, and reporting can all be automated using AI agents. The goal is removing yourself and your team from low-value repetitive tasks so you can focus on high-value strategic work.</p>
<p class="fade-in"><strong>Decision Support:</strong> AI systems can analyze complex data sets, identify patterns, flag anomalies, and recommend actions. Financial forecasting, demand planning, pricing optimization, and resource allocation all benefit from AI-powered analysis.</p>
<p class="fade-in"><strong>Quality Control:</strong> AI monitors outputs, detects errors, ensures consistency, and maintains standards across your operation. This is particularly valuable as you scale, maintaining quality becomes harder with growth, and AI provides the monitoring layer that catches issues before they reach customers.</p>
<p class="fade-in">Dr. Robertson's book <a href="/books/#built-to-run">Built to Run</a> provides frameworks for building systems that operate without constant owner involvement, AI accelerates this vision dramatically.</p>

<h2 class="fade-in">AI for Sales Intelligence</h2>
<p class="fade-in">Sales teams equipped with AI outperform those without it by significant margins. The advantage comes from better targeting, faster research, and more personalized outreach at scale.</p>
<p class="fade-in"><strong>Prospect Research:</strong> AI can research prospects, identify pain points, map organizational structures, and surface trigger events in minutes rather than hours. This intelligence makes every sales conversation more relevant and valuable.</p>
<p class="fade-in"><strong>Outreach Personalization:</strong> Generic outreach fails. AI enables personalization at scale, crafting messages that reference specific details about the prospect, their company, and their challenges. Combined with the methodology from <a href="/books/#the-7-minute-phone-call">The 7 Minute Phone Call</a>, AI-powered research makes every call more productive.</p>
<p class="fade-in"><strong>Pipeline Analytics:</strong> AI predicts which deals will close, identifies stalled opportunities, recommends next actions, and helps sales teams prioritize their time on the highest-probability opportunities.</p>

<h2 class="fade-in">Implementation Roadmap</h2>
<p class="fade-in">Successful AI implementation follows a predictable pattern. Rushing to deploy complex systems without foundation leads to failure. Here is the phased approach that works:</p>
<p class="fade-in"><strong>Phase 1, Audit and Prioritize:</strong> Map every process in your business. Identify which are repetitive, rule-based, and high-volume. These are your AI candidates. Prioritize by potential impact and implementation difficulty.</p>
<p class="fade-in"><strong>Phase 2, Quick Wins:</strong> Start with high-impact, low-complexity implementations. Content generation, email automation, and basic workflow automation typically deliver fastest ROI and build organizational confidence in AI.</p>
<p class="fade-in"><strong>Phase 3, Core Systems:</strong> Build AI into your core operational workflows. This is where you move from using AI tools to having AI-powered systems that run continuously. CRM automation, financial analysis, customer service, and reporting infrastructure.</p>
<p class="fade-in"><strong>Phase 4, Competitive Moat:</strong> Deploy AI in ways that create sustainable advantages, proprietary data, custom models, unique workflows, and integrated systems that competitors cannot easily replicate.</p>

<h2 class="fade-in">Avoiding Common Mistakes</h2>
<p class="fade-in">The biggest mistake entrepreneurs make with AI is treating it as a magic bullet rather than a tool that requires strategy, implementation, and iteration. Other common failures include deploying AI without clear success metrics, automating broken processes (which just creates broken automation faster), and failing to invest in the human oversight that keeps AI systems on track.</p>
<p class="fade-in">AI works best when paired with clear business objectives, defined processes, and competent human oversight. It amplifies what is already working, it does not fix what is fundamentally broken.</p>

<div class="quote fade-in" style="margin:48px 0">
<p class="quote-t">"AI does not replace strategy. It accelerates it. The entrepreneurs who win are those who know what to build, AI just helps them build it faster."</p>
<p class="quote-a"><strong>Dr. Connor Robertson</strong></p>
</div>

<h2 class="fade-in">Related Resources</h2>
<div class="pills fade-in" style="margin-top:24px">
<div class="pill"><h3><a href="/business-acquisitions/">Business Acquisitions</a></h3><p>Apply AI to optimize acquired businesses from day one.</p></div>
<div class="pill"><h3><a href="/prospecting-sales/">Prospecting & Sales</a></h3><p>AI-powered prospecting systems that fill your pipeline.</p></div>
<div class="pill"><h3><a href="/author-platform/">Author Platform</a></h3><p>Use AI to scale content creation and audience building.</p></div>
<div class="pill"><h3><a href="/books/#built-to-run">Built to Run (Book)</a></h3><p>Build systems and processes that run without you.</p></div>
</div>

<div style="margin-top:48px;padding:32px;background:var(--card);border-radius:var(--r);text-align:center" class="fade-in">
<h3>Want to Deploy AI in Your Business?</h3>
<p style="margin:16px 0;color:var(--text2)">Dr. Connor Robertson helps entrepreneurs build AI-powered systems that create real competitive advantage.</p>
<a href="/contact/" class="btn-p" style="display:inline-block;margin-top:12px">Contact Connor</a>
</div>

</div></section>
""" + footer()


def page_prospecting_sales():
    topic_page = {
        "@type": "TechArticle",
        "@id": f"{SITE_URL}/prospecting-sales/#guide",
        "headline": "Prospecting & Sales",
        "name": "Prospecting & Sales",
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": PERSON_ID},
        "about": {"@id": PERSON_ID},
        "inLanguage": "en-US",
        "mainEntityOfPage": {"@id": f"{SITE_URL}/prospecting-sales/#webpage"},
    }

    return header("Prospecting & Sales Guide | Dr. Connor Robertson",
        "Build a predictable sales pipeline: The 7 Minute Phone Call method, outbound systems, pipeline architecture and closing frameworks.",
        "/prospecting-sales/", og_image="/images/dr-connor-robertson-headshot.jpg",
        crumbs=[("Home", "/"), ("Prospecting & Sales", None)],
        schema_nodes=[topic_page]) + breadcrumbs([("Home", "/"), ("Prospecting & Sales", None)]) + """
<section class="pg-hero"><div class="ctn">
<h1>Prospecting & Sales: Building Predictable Revenue Pipelines</h1>
<p>The systems, scripts, and strategies that generate consistent deal flow, anchored by The 7 Minute Phone Call methodology.</p>
</div></section>
<section class="sec"><div class="ctn">

<h2 class="fade-in">The Foundation: Why Prospecting Matters More Than Anything</h2>
<p class="fade-in">Every business problem is a pipeline problem in disguise. Revenue shortfalls, inconsistent months, over-reliance on referrals, and growth plateaus all trace back to the same root cause, insufficient prospecting activity. The businesses that thrive are those with predictable, repeatable systems for generating new conversations with qualified prospects.</p>
<p class="fade-in">Most entrepreneurs avoid prospecting because it feels uncomfortable. Cold outreach, follow-up sequences, and phone calls push people outside their comfort zones. But comfort and growth do not coexist. The entrepreneurs who build the most valuable businesses are those who master the discipline of consistent daily outreach.</p>

<h2 class="fade-in">The 7 Minute Phone Call Methodology</h2>
<p class="fade-in">At the heart of Dr. Robertson's prospecting philosophy is a simple truth: seven minutes on the phone builds more trust than a dozen emails ever will. The human voice carries nuance, warmth, and authenticity that no written communication can replicate.</p>
<p class="fade-in"><strong>The Framework:</strong> Every effective prospecting call follows a structure. Open with context (why you are calling and how you found them). Establish relevance (demonstrate you understand their world). Ask a diagnostic question (uncover a pain point or opportunity). Offer value (share an insight or resource). Close with a clear next step (schedule a deeper conversation or send specific information).</p>
<p class="fade-in"><strong>Seven Minutes, Not Sixty:</strong> Brevity signals respect for the prospect's time. A concise, focused conversation creates curiosity and momentum. Long calls exhaust attention and reduce the likelihood of a second conversation. Get in, deliver value, and get out with a next step.</p>
<p class="fade-in"><strong>Preparation Matters:</strong> The best seven-minute calls are preceded by five minutes of research. Know who you are calling, what they do, what challenges they likely face, and what specific value you can offer. This preparation transforms cold calls into warm, relevant conversations.</p>
<p class="fade-in">The complete methodology is detailed in <a href="/books/#the-7-minute-phone-call">The 7 Minute Phone Call</a>.</p>

<h2 class="fade-in">Outbound Prospecting Systems</h2>
<p class="fade-in">Individual effort does not scale. Systems do. Building an outbound prospecting machine requires defined processes, consistent execution, and measurement at every stage.</p>
<p class="fade-in"><strong>List Building:</strong> Your prospect list is your most valuable sales asset. Build targeted lists using LinkedIn, industry databases, event attendee lists, and your existing network. Quality matters more than quantity, 100 well-researched prospects outperform 1,000 random contacts.</p>
<p class="fade-in"><strong>Multi-Channel Sequencing:</strong> The most effective outreach combines phone calls, emails, LinkedIn messages, and social engagement into coordinated sequences. A typical sequence might include a LinkedIn connection request on day 1, a phone call on day 3, a value-add email on day 5, and a follow-up call on day 8.</p>
<p class="fade-in"><strong>Cadence and Consistency:</strong> Daily prospecting activity is non-negotiable. Set a minimum daily standard, whether that is 25 calls, 50 emails, or a combination, and hold yourself accountable to it without exception. Consistency compounds over time in ways that burst-and-rest approaches never can.</p>

<h2 class="fade-in">Pipeline Architecture</h2>
<p class="fade-in">A well-designed pipeline gives you visibility, predictability, and control over your revenue trajectory. Without pipeline discipline, growth becomes random rather than intentional.</p>
<p class="fade-in"><strong>Stage Definition:</strong> Define clear stages that prospects move through. A typical B2B pipeline includes: Lead Identified, Initial Contact Made, Discovery Completed, Proposal Delivered, Negotiation, and Closed. Each stage should have clear entry criteria and required actions.</p>
<p class="fade-in"><strong>Conversion Metrics:</strong> Track conversion rates between each stage. If you know that 100 calls produce 20 conversations, 20 conversations produce 8 meetings, and 8 meetings produce 2 clients, you have a formula. Need 4 clients this month? Make 200 calls.</p>
<p class="fade-in"><strong>Pipeline Velocity:</strong> Monitor how quickly prospects move through stages. Stalled deals indicate either poor qualification or insufficient follow-up. Both are solvable with better process.</p>

<h2 class="fade-in">Closing Frameworks</h2>
<p class="fade-in">Closing is not a single event, it is the natural conclusion of a well-executed sales process. If you have qualified properly, understood the prospect's needs, and demonstrated clear value, closing becomes a formality rather than a battle.</p>
<p class="fade-in"><strong>Assumptive Progression:</strong> At each stage, assume the next step rather than asking permission for it. Instead of "Would you like to schedule a follow-up?", try "I will send over some times for next Tuesday, does morning or afternoon work better?"</p>
<p class="fade-in"><strong>Objection as Information:</strong> Objections are not rejection, they are requests for more information or reassurance. When a prospect objects, they are telling you exactly what they need to hear before saying yes. Listen, acknowledge, and address specifically.</p>
<p class="fade-in"><strong>The Walk-Away:</strong> Willingness to walk away from a deal is paradoxically one of the most powerful closing tools. When a prospect senses desperation, trust erodes. When they sense that you are selective about who you work with, desire increases.</p>

<h2 class="fade-in">CRM and Technology</h2>
<p class="fade-in">Your CRM is the operating system of your sales process. It should track every interaction, automate follow-up reminders, provide pipeline visibility, and generate the metrics you need to optimize performance. Choose a CRM that your team will actually use, the best system in the world is worthless if it sits empty.</p>

<div class="quote fade-in" style="margin:48px 0">
<p class="quote-t">"Sales is not about convincing people to buy things they do not want. It is about connecting people with solutions to problems they already have."</p>
<p class="quote-a"><strong>Dr. Connor Robertson</strong></p>
</div>

<h2 class="fade-in">Related Resources</h2>
<div class="pills fade-in" style="margin-top:24px">
<div class="pill"><h3><a href="/business-acquisitions/">Business Acquisitions</a></h3><p>Use prospecting skills to source off-market deals.</p></div>
<div class="pill"><h3><a href="/ai-business-strategy/">AI Business Strategy</a></h3><p>Deploy AI to supercharge your prospecting systems.</p></div>
<div class="pill"><h3><a href="/author-platform/">Author Platform</a></h3><p>Build inbound authority that warms up cold prospects.</p></div>
<div class="pill"><h3><a href="/books/#the-7-minute-phone-call">The 7 Minute Phone Call (Book)</a></h3><p>The complete prospecting methodology in detail.</p></div>
</div>

<div style="margin-top:48px;padding:32px;background:var(--card);border-radius:var(--r);text-align:center" class="fade-in">
<h3>Ready to Build Your Pipeline?</h3>
<p style="margin:16px 0;color:var(--text2)">Dr. Connor Robertson teaches entrepreneurs how to build prospecting systems that generate predictable revenue.</p>
<a href="/contact/" class="btn-p" style="display:inline-block;margin-top:12px">Contact Connor</a>
</div>

</div></section>
""" + footer()


def page_author_platform():
    topic_page = {
        "@type": "TechArticle",
        "@id": f"{SITE_URL}/author-platform/#guide",
        "headline": "Author Platform",
        "name": "Author Platform",
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": PERSON_ID},
        "about": {"@id": PERSON_ID},
        "inLanguage": "en-US",
        "mainEntityOfPage": {"@id": f"{SITE_URL}/author-platform/#webpage"},
    }

    return header("Author Platform Guide | Dr. Connor Robertson",
        "How publishing builds authority: book strategy, content repurposing, personal branding, and turning an author platform into business development.",
        "/author-platform/", og_image="/images/dr-connor-robertson-headshot.jpg",
        crumbs=[("Home", "/"), ("Author Platform", None)],
        schema_nodes=[topic_page]) + breadcrumbs([("Home", "/"), ("Author Platform", None)]) + """
<section class="pg-hero"><div class="ctn">
<h1>Author Platform: Building Authority Through Publishing</h1>
<p>How writing books and creating content builds the authority, trust, and visibility that drives real business results.</p>
</div></section>
<section class="sec"><div class="ctn">

<h2 class="fade-in">Why Authors Win</h2>
<p class="fade-in">In a world saturated with content, a published book remains the single most powerful credibility asset an entrepreneur can create. A book signals depth of expertise, commitment to your craft, and willingness to share knowledge publicly. It positions you as the authority in your space, not just another voice competing for attention.</p>
<p class="fade-in">But the real power of authorship extends far beyond credibility. A book is a business development engine. It opens doors to speaking engagements, podcast appearances, media coverage, partnerships, and client relationships that would otherwise take years to build. Every copy in circulation is a salesperson working on your behalf, 24 hours a day.</p>
<p class="fade-in">Dr. Robertson has published multiple books, including <a href="/books/#buying-wealth">Buying Wealth</a>, <a href="/books/#creative-acquisitions">Creative Acquisitions</a>, <a href="/books/#the-7-minute-phone-call">The 7 Minute Phone Call</a>, and <a href="/books/#built-to-run">Built to Run</a>, each serving as a pillar of his broader business development strategy.</p>

<h2 class="fade-in">Book Writing Strategy</h2>
<p class="fade-in">Writing a book does not require genius or years of isolation. It requires a system. The most effective approach is to write from experience rather than research alone, your unique perspective and real-world results are what readers cannot find anywhere else.</p>
<p class="fade-in"><strong>Start With the Transformation:</strong> Every great book promises a specific transformation. What will the reader be able to do, think, or achieve after reading that they could not before? Define this clearly before writing a single chapter.</p>
<p class="fade-in"><strong>Structure Around Problems:</strong> Each chapter should address a specific problem your audience faces and provide a clear framework for solving it. This makes the book immediately actionable rather than merely theoretical.</p>
<p class="fade-in"><strong>Write in Sprints:</strong> Aim for 1,000-2,000 words per writing session. A 40,000-word book requires only 20-40 focused sessions. Most entrepreneurs can complete a first draft in 60-90 days with consistent daily writing habits.</p>
<p class="fade-in"><strong>Edit Ruthlessly:</strong> First drafts are for getting ideas down. Editing is where the book becomes great. Cut everything that does not directly serve the reader's transformation. Clarity beats cleverness every time.</p>

<h2 class="fade-in">Content Repurposing</h2>
<p class="fade-in">A single book contains hundreds of pieces of derivative content. Strategic repurposing multiplies your reach without multiplying your effort.</p>
<p class="fade-in"><strong>Blog Posts:</strong> Each chapter becomes 2-5 blog posts exploring specific concepts in more detail. These posts drive organic search traffic back to your book and author platform.</p>
<p class="fade-in"><strong>Social Media:</strong> Key quotes, frameworks, and insights become daily social content across LinkedIn, Twitter, Instagram, and other platforms. A single book provides 6-12 months of daily content.</p>
<p class="fade-in"><strong>Podcast Episodes:</strong> Each chapter is a potential podcast episode topic. Whether on your own show or as a guest, book content provides endless conversation material.</p>
<p class="fade-in"><strong>Email Sequences:</strong> Book excerpts and expanded chapters become nurture sequences that build relationships with your audience over time.</p>
<p class="fade-in"><strong>Speaking Material:</strong> Book frameworks translate directly into keynote presentations, workshop content, and training materials.</p>

<h2 class="fade-in">Personal Branding and Visibility</h2>
<p class="fade-in">Your author platform is the hub that connects all your content, presence, and credibility into a cohesive brand that people trust and remember.</p>
<p class="fade-in"><strong>Multi-Platform Presence:</strong> Show up consistently across the platforms where your audience spends time. LinkedIn for professional audiences, YouTube for long-form education, podcasts for commuters, and social media for daily engagement. Consistency across platforms creates an omnipresent feeling that builds familiarity and trust.</p>
<p class="fade-in"><strong>Thought Leadership:</strong> Share perspectives that challenge conventional thinking in your industry. Agree-with-everyone content is forgettable. Distinct points of view attract the right people and repel the wrong ones, both outcomes serve you.</p>
<p class="fade-in"><strong>Media and PR:</strong> Published authors attract media attention naturally. Proactive outreach to podcasts, publications, and industry events accelerates visibility. Each appearance reinforces your authority and introduces you to new audiences.</p>

<h2 class="fade-in">Publishing as Business Development</h2>
<p class="fade-in">The most successful author-entrepreneurs treat their books not as profit centers (though they can be) but as business development tools that generate far more value through indirect channels.</p>
<p class="fade-in"><strong>Authority Positioning:</strong> When a prospect is choosing between you and a competitor, being a published author on the topic immediately differentiates you. Books create a perception of expertise that no amount of social media posts can replicate.</p>
<p class="fade-in"><strong>Inbound Lead Generation:</strong> Books attract readers who self-identify as your ideal clients. A reader who finishes your book and reaches out is pre-sold on your philosophy and approach, they are not comparing you against five competitors.</p>
<p class="fade-in"><strong>Strategic Gifting:</strong> Sending your book to prospects, partners, and referral sources is a low-cost, high-impact business development tactic. A book is not junk mail, it sits on shelves, gets read, and creates ongoing impressions.</p>
<p class="fade-in"><strong>Speaking and Events:</strong> Books open doors to speaking engagements where you address rooms full of potential clients, partners, and collaborators. Every stage appearance compounds your visibility and authority.</p>

<h2 class="fade-in">Building Your Platform</h2>
<p class="fade-in">An author platform is not built overnight. It is built through consistent action over months and years. But the compound returns make the investment worthwhile many times over.</p>
<p class="fade-in"><strong>Start Today:</strong> You do not need a finished book to start building your platform. Begin sharing your expertise through blog posts, social content, and conversations. The book crystallizes what you are already teaching.</p>
<p class="fade-in"><strong>Be Consistent:</strong> Publish on a regular schedule. Daily social content, weekly blog posts, monthly podcast episodes, whatever cadence you choose, maintain it without exception. Consistency builds audience trust and algorithmic favor.</p>
<p class="fade-in"><strong>Invest in Quality:</strong> Professional covers, quality editing, and polished production signal that you take your work seriously. First impressions matter, do not undermine strong content with weak presentation.</p>

<div class="quote fade-in" style="margin:48px 0">
<p class="quote-t">"A book is not just something you write. It is something that works for you, opening doors, building trust, and creating opportunities, long after you have finished writing it."</p>
<p class="quote-a"><strong>Dr. Connor Robertson</strong></p>
</div>

<h2 class="fade-in">Related Resources</h2>
<div class="pills fade-in" style="margin-top:24px">
<div class="pill"><h3><a href="/business-acquisitions/">Business Acquisitions</a></h3><p>Books position you as the expert acquirers want to work with.</p></div>
<div class="pill"><h3><a href="/ai-business-strategy/">AI Business Strategy</a></h3><p>Use AI to accelerate content creation and distribution.</p></div>
<div class="pill"><h3><a href="/prospecting-sales/">Prospecting & Sales</a></h3><p>Combine authorship with outbound for unstoppable deal flow.</p></div>
<div class="pill"><h3><a href="/books/">All Books by Dr. Connor Robertson</a></h3><p>Browse the complete library of published works.</p></div>
</div>

<div style="margin-top:48px;padding:32px;background:var(--card);border-radius:var(--r);text-align:center" class="fade-in">
<h3>Ready to Build Your Author Platform?</h3>
<p style="margin:16px 0;color:var(--text2)">Dr. Connor Robertson helps entrepreneurs leverage publishing as a business development strategy.</p>
<a href="/contact/" class="btn-p" style="display:inline-block;margin-top:12px">Contact Connor</a>
</div>

</div></section>
""" + footer()


def page_faq():
    faqs = [
        ("Who is Dr. Connor Robertson?",
         "Dr. Connor Robertson is an entrepreneur, author, podcast host, and business strategist based in Pittsburgh, Pennsylvania. He is the founder of multiple companies including Elixir Consulting Group, The Prospecting Show, The Pittsburgh Wire, The Grant Finder, and Seymour Maison. Connor is widely recognized for his expertise in business acquisitions, real estate investing, and helping business owners scale through strategic advisory services. He has authored six books on business strategy and wealth building, and his podcast, The Prospecting Show, has featured over 178 episodes with top entrepreneurs and business leaders."),
        ("What companies does Dr. Connor Robertson own?",
         "Dr. Connor Robertson is the founder and owner of several successful companies across diverse industries. These include Elixir Consulting Group, a strategic business advisory firm helping owners with growth, acquisitions, and operational excellence; The Prospecting Show, a top-rated weekly podcast interviewing entrepreneurs about building and scaling businesses; The Pittsburgh Wire, a digital media publication covering Pittsburgh business, real estate, and development news; The Grant Finder, a platform connecting organizations with grant funding opportunities; and Seymour Maison, a luxury t-shirt brand offering premium essentials through a waitlist-only model. He also manages an active real estate investment portfolio."),
        ("What books has Dr. Connor Robertson written?",
         "Dr. Connor Robertson has authored six books focused on business strategy, acquisitions, and wealth building. His published works include Buying Wealth, which teaches readers how to build wealth through asset acquisition; Creative Acquisitions, a guide to innovative deal structures for purchasing businesses; The 7 Minute Phone Call, a framework for effective prospecting conversations; PadSplit Playbook, a comprehensive guide to co-living real estate investing; Buy The Building Keep The Profits, which covers strategies for business owners to acquire their commercial properties; and Built to Run, a playbook for building businesses with systems that operate independently of the founder."),
        ("Where is Dr. Connor Robertson based?",
         "Dr. Connor Robertson is based in Pittsburgh, Pennsylvania. Pittsburgh serves as the headquarters for his companies and ventures, and he is an active participant in the Pittsburgh business community. His publication, The Pittsburgh Wire, reflects his deep connection to the city by covering local business, real estate, and development news. Connor frequently speaks at events and conferences in the Pittsburgh area and throughout the United States."),
        ("What is The Prospecting Show?",
         "The Prospecting Show is a weekly podcast hosted by Dr. Connor Robertson that features in-depth interviews with entrepreneurs, business owners, and industry leaders about building and scaling successful businesses. With over 178 episodes, the show covers topics including sales strategy, business acquisitions, real estate investing, leadership, and operational excellence. The Prospecting Show is available on all major podcast platforms including Spotify, Apple Podcasts, and YouTube. It has become a go-to resource for entrepreneurs looking for practical, actionable advice on business growth."),
        ("What is Elixir Consulting Group?",
         "Elixir Consulting Group is a strategic advisory firm founded by Dr. Connor Robertson. The firm specializes in helping business owners achieve growth through acquisitions, partnerships, and operational improvement. Elixir Consulting Group works with entrepreneurs and companies across a range of industries, providing guidance on deal structuring, scaling operations, improving profitability, and building sustainable business systems. Based in Pittsburgh, Pennsylvania, the firm reflects Connor's hands-on approach to business strategy and his belief that disciplined systems and smart acquisitions are the foundation of long-term success."),
        ("What is Dr. Connor Robertson known for?",
         "Dr. Connor Robertson is known for his expertise in entrepreneurship, business acquisitions, real estate investing, podcasting, and authoring practical business guides. He has built a reputation as a trusted voice in the business community through his podcast The Prospecting Show, his six published books, and his work as founder of Elixir Consulting Group. Connor is recognized for his hands-on, results-oriented approach to helping business owners grow through strategic acquisitions and operational excellence. He is also known for his contributions to the Pittsburgh business community through The Pittsburgh Wire and his active involvement in local entrepreneurship."),
        ("How can I contact Dr. Connor Robertson?",
         "You can contact Dr. Connor Robertson through his official website at drconnorrobertson.com/contact/, where you will find a contact form for business inquiries, speaking engagements, press and media requests, and partnership opportunities. Connor is also active on LinkedIn, where he regularly shares insights on entrepreneurship and business strategy. For press and media inquiries, you can visit his media kit page at drconnorrobertson.com/media/ for downloadable resources and contact information."),
        ("What is The Pittsburgh Wire?",
         "The Pittsburgh Wire is a digital media publication founded by Dr. Connor Robertson that covers Pittsburgh business, real estate, and development news. The publication focuses on positive stories of growth, investment, and innovation in the Pittsburgh region, highlighting new businesses, real estate developments, and economic progress across the city and surrounding areas. The Pittsburgh Wire has become a trusted source for anyone interested in the Pittsburgh business landscape and the city's ongoing economic development."),
        ("What is Seymour Maison?",
         "Seymour Maison is a luxury t-shirt brand founded by Dr. Connor Robertson that offers premium essentials through a waitlist-only model. Established in 1993, Seymour Maison focuses on exceptional quality, craftsmanship, and understated elegance. The brand sources premium materials and emphasizes limited production runs to maintain exclusivity and quality. Seymour Maison represents Connor's commitment to building brands that prioritize excellence and long-term value over mass-market appeal."),
    ]

    faq_schema_items = []
    faq_html_items = ""
    for q, a in faqs:
        faq_schema_items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
        faq_html_items += f"""
      <div class="faq-item fade-in">
        <h2 class="faq-q">{esc(q)}</h2>
        <div class="faq-a"><p>{esc(a)}</p></div>
      </div>"""

    # The Person entity comes from the sitewide graph; only the FAQ is page-specific.

    extra_head = """<style>
.faq-item{{background:#fff;border:1px solid #e8e8e8;border-radius:12px;padding:32px;margin-bottom:20px;transition:box-shadow .3s}}
.faq-item:hover{{box-shadow:0 4px 20px rgba(0,0,0,.08)}}
.faq-q{{font-size:1.25rem;margin:0 0 12px;color:#1a1a2e;line-height:1.4}}
.faq-a p{{margin:0;color:#555;line-height:1.7;font-size:1.05rem}}
.faq-intro{{max-width:720px;margin:0 auto 40px;text-align:center;color:#555;font-size:1.1rem;line-height:1.7}}
</style>"""

    return header(
        "FAQ | Dr. Connor Robertson: Companies, Books & Podcast",
        "Answers to the most common questions about Dr. Connor Robertson: his companies, his six books, The Prospecting Show, and how to get in touch.",
        "/faq/",
        extra=extra_head,
        og_image="/images/connor-hero.jpg",
        page_type="FAQPage",
        crumbs=[("Home", "/"), ("FAQ", None)],
        page_extra={"mainEntity": faq_schema_items},
    ) + breadcrumbs([("Home", "/"), ("FAQ", None)]) + f"""
<section class="pg-hero"><div class="ctn">
<h1>Frequently Asked Questions</h1>
<p>Common questions about Dr. Connor Robertson, his companies, books, and ventures.</p>
</div></section>

<section class="sec"><div class="ctn">
<p class="faq-intro">Dr. Connor Robertson is a Pittsburgh-based entrepreneur, author, podcast host, and business strategist. Below you will find answers to the most frequently asked questions about Connor, his companies, and his work.</p>
{faq_html_items}

<div style="text-align:center;margin-top:48px" class="fade-in">
<h2 style="margin-bottom:16px">Have Another Question?</h2>
<p style="color:#555;margin-bottom:24px">Get in touch with Dr. Connor Robertson for business inquiries, speaking engagements, or media requests.</p>
<a href="/contact/" class="btn-p">Contact Connor</a>
</div>
</div></section>
""" + footer()


# ── Resource Hub Pages ──────────────────────────────────

# Short intro copy for each resource hub, keyed by URL.
RESOURCE_HUB_INTROS = {
    "/blog/hub-business-acquisitions-scaling-dr-connor-robertson/":
        "Frameworks, playbooks, and field notes on buying businesses, structuring creative deals, and scaling what you acquire. Start with the pillar guides below, then dive into the latest articles.",
    "/blog/hub-leadership-legacy-dr-connor-robertson/":
        "Lessons on leading teams, building durable companies, and creating impact that outlasts you. Curated guides and articles from Dr. Connor Robertson on leadership and legacy.",
    "/blog/hub-influence-authority-dr-connor-robertson/":
        "How to build authority through publishing, media, and a strong personal brand. Explore the author-platform playbook and related articles on growing your influence.",
    "/blog/hub-mindset-momentum-systems-dr-connor-robertson/":
        "Mindset, momentum, and the operating systems that let founders step out of the day-to-day. Strategy guides and practical articles for building businesses that run without you.",
    "/blog/hub-pittsburgh-business-real-estate-dr-connor-robertson/":
        "Coverage of Pittsburgh business, real estate, and economic development, plus Dr. Connor Robertson's broader writing on ownership and local entrepreneurship.",
}

# Unique title + description per hub. Without these all five hubs shipped the
# same boilerplate description, which reads as duplicate content.
HUB_SEO = {
    "/blog/hub-business-acquisitions-scaling-dr-connor-robertson/": {
        "title": "Business Acquisitions & Scaling Resources",
        "desc": "Frameworks and field notes on buying businesses, structuring creative deals, financing acquisitions, and scaling what you buy.",
    },
    "/blog/hub-leadership-legacy-dr-connor-robertson/": {
        "title": "Leadership & Legacy Resources | Dr. Connor Robertson",
        "desc": "Guides on leading teams, building durable companies, and creating impact that outlasts you, from entrepreneur Dr. Connor Robertson.",
    },
    "/blog/hub-influence-authority-dr-connor-robertson/": {
        "title": "Influence & Authority Resources | Dr. Connor Robertson",
        "desc": "How to build authority through publishing, media, and a deliberate personal brand. The author-platform playbook and related articles.",
    },
    "/blog/hub-mindset-momentum-systems-dr-connor-robertson/": {
        "title": "Mindset & Business Systems Resources",
        "desc": "Mindset, momentum, and the operating systems that let founders step out of the day-to-day and build a business that runs without them.",
    },
    "/blog/hub-pittsburgh-business-real-estate-dr-connor-robertson/": {
        "title": "Pittsburgh Business & Real Estate Resources",
        "desc": "Pittsburgh business, real estate, and economic development coverage, plus writing on local ownership and entrepreneurship in the region.",
    },
}


def page_resource_hub(label, href, posts):
    intro = RESOURCE_HUB_INTROS.get(href, f"A curated collection of guides and articles from Dr. Connor Robertson on {label}.")
    seo = HUB_SEO.get(href, {})
    title = seo.get("title") or f"{label} | Dr. Connor Robertson"
    desc = seo.get("desc") or clip(intro)

    hub_list = {
        "@type": "ItemList",
        "@id": f"{SITE_URL}{href}#itemlist",
        "numberOfItems": len(posts[:6]),
        "itemListElement": [
            {"@type": "ListItem", "position": i,
             "url": f"{SITE_URL}{p['relative_url']}", "name": strip_tags(p["title"])}
            for i, p in enumerate(posts[:6], start=1)
        ],
    }

    pillar_cards = "".join(
        f'<div class="pill"><h3><a href="{h}">{l}</a></h3><p>In-depth pillar guide from Dr. Connor Robertson.</p></div>'
        for l, h in PILLAR_PAGES
    )

    # Recent articles grid
    art_cards = ""
    for p in posts[:6]:
        try:
            dt = datetime.fromisoformat(p["date"]).strftime("%B %d, %Y")
        except Exception:
            dt = ""
        ex = strip_tags(p.get("excerpt", ""))
        if len(ex) > 140:
            ex = ex[:140].rsplit(" ", 1)[0] + "..."
        feat_img = ""
        if p.get("featured_image"):
            local = downloaded_images.get(p["featured_image"], "")
            if local:
                feat_img = f'<img src="{local}" alt="{esc(strip_tags(p["title"]))}" class="bcard-img" width="400" height="225" loading="lazy">'
        art_cards += f'<a href="{p["relative_url"]}" class="bcard">{feat_img}<div class="bcard-body"><h3>{p["title"]}</h3><p class="exc">{esc(ex)}</p><span class="meta">{dt}</span></div></a>\n'

    return header(title, desc, href, og_image="/images/dr-connor-robertson-headshot.jpg",
                  page_type="CollectionPage",
                  crumbs=[("Home", "/"), ("Blog", "/blog/"), (label, None)],
                  page_extra={"mainEntity": hub_list}) + breadcrumbs([
        ("Home", "/"), ("Blog", "/blog/"), (label, None)
    ]) + f"""
<section class="pg-hero"><div class="ctn">
<h1>{esc(label)}</h1><p>{esc(intro)}</p>
</div></section>
<section class="sec"><div class="ctn">
<h2 class="sec-t">Pillar Guides</h2>
<div class="pills">{pillar_cards}</div>
</div></section>
<section class="sec sec-dk"><div class="ctn">
<h2 class="sec-t">Latest Articles</h2>
<div class="bgrid">{art_cards}</div>
<div style="text-align:center;margin-top:40px"><a href="/blog/" class="btn-p">View All Articles</a></div>
</div></section>
""" + footer()


def page_resource_index(posts):
    href = "/blog/complete-resource-index-dr-connor-robertson/"
    title = "Complete Resource Index | Dr. Connor Robertson"
    desc = "Every page and article by Dr. Connor Robertson in one index: topic hubs, pillar guides on acquisitions, AI, prospecting and publishing."

    hubs = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in RESOURCE_HUBS)
    pillars = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in PILLAR_PAGES)
    main_pages = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in [
        ("About", "/about/"), ("Projects", "/projects/"), ("Speaker", "/speaker/"),
        ("Books", "/books/"), ("Media Kit", "/media/"), ("Press & Media", "/press-media/"),
        ("Blog", "/blog/"), ("Contact", "/contact/"),
    ])
    articles = "".join(f'<li><a href="{p["relative_url"]}">{p["title"]}</a></li>' for p in posts)

    return header(title, desc, href, og_image="/images/dr-connor-robertson-headshot.jpg",
                  page_type="CollectionPage",
                  crumbs=[("Home", "/"), ("Blog", "/blog/"), ("Complete Resource Index", None)]) + breadcrumbs([
        ("Home", "/"), ("Blog", "/blog/"), ("Complete Resource Index", None)
    ]) + f"""
<section class="pg-hero"><div class="ctn">
<h1>Complete Resource Index</h1><p>Everything published by Dr. Connor Robertson in one place, topic hubs, pillar guides, key pages, and every article.</p>
</div></section>
<section class="sec"><div class="ctn">
<div class="ablock"><h2>Resource Hubs</h2><ul class="link-list">{hubs}</ul></div>
<div class="ablock"><h2>Pillar Guides</h2><ul class="link-list">{pillars}</ul></div>
<div class="ablock"><h2>Key Pages</h2><ul class="link-list">{main_pages}</ul></div>
<div class="ablock"><h2>All Articles</h2><ul class="link-list">{articles}</ul></div>
</div></section>
""" + footer()


def main():
    no_fetch = "--no-fetch" in sys.argv

    print("=" * 60)
    print("Building drconnorrobertson.com static site")
    print("=" * 60)

    # Fetch posts - load manual_posts.json and merge with WP API/cache posts
    MANUAL_POSTS_FILE = BASE_DIR / "manual_posts.json"
    manual_posts = []
    if MANUAL_POSTS_FILE.exists():
        print("\n[1/8] Loading posts from manual_posts.json + WP API/cache...")
        with open(MANUAL_POSTS_FILE) as f:
            manual_posts = json.load(f)
        print(f"  Loaded {len(manual_posts)} manual posts")
    else:
        print("\n[1/8] Fetching posts...")

    # Also load WP API posts or cache to merge with manual posts
    wp_posts = []
    if no_fetch and CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            wp_posts = json.load(f)
        print(f"  Loaded {len(wp_posts)} posts from cache")
    elif not no_fetch:
        try:
            wp_posts = fetch_all_posts()
            print(f"  Fetched {len(wp_posts)} posts from WP API")
            with open(CACHE_FILE, "w") as f:
                json.dump(wp_posts, f)
            print("  Cached to posts_cache.json")
        except Exception as e:
            print(f"  Could not fetch from WP API: {e}")
            if CACHE_FILE.exists():
                with open(CACHE_FILE) as f:
                    wp_posts = json.load(f)
                print(f"  Fell back to {len(wp_posts)} cached posts")

    # Merge: manual posts take precedence over WP posts (by slug)
    manual_slugs = {p["slug"] for p in manual_posts}
    posts = list(manual_posts)
    for wp in wp_posts:
        if wp["slug"] not in manual_slugs:
            posts.append(wp)
    print(f"  Total posts after merge: {len(posts)} ({len(manual_posts)} manual + {len(posts) - len(manual_posts)} from WP/cache)")

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    print(f"  Sorted {len(posts)} posts by date (newest first)")

    # Remove duplicate posts (slugs ending in -2, -3, etc.)
    before_dedup = len(posts)
    seen_titles = {}
    deduped_posts = []
    for p in posts:
        title_key = p["title"].lower().strip()
        slug = p["slug"]
        # If we already saw this title, keep the original (without -2 suffix)
        if title_key in seen_titles:
            if re.match(r'.*-\d+$', slug):
                print(f"  Removing duplicate: {slug}")
                continue  # Skip the -2/-3 version
            else:
                # This is the original, remove the previously stored one if it was the -2
                prev_slug = seen_titles[title_key]["slug"]
                if re.match(r'.*-\d+$', prev_slug):
                    deduped_posts = [dp for dp in deduped_posts if dp["slug"] != prev_slug]
                    print(f"  Removing duplicate: {prev_slug}")
        seen_titles[title_key] = p
        deduped_posts.append(p)
    posts = deduped_posts
    if before_dedup != len(posts):
        print(f"  Removed {before_dedup - len(posts)} duplicate posts ({before_dedup} -> {len(posts)})")
        # Update cache with deduped posts
        with open(CACHE_FILE, "w") as f:
            json.dump(posts, f)

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

    # Download headshot images from Google Drive
    print("\n[3.5/8] Downloading headshot images from Google Drive...")
    download_headshots()

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

    # Image verification: check for any remaining WordPress URLs in content
    print("\n[4b/8] Verifying image integrity...")
    wp_url_remaining = 0
    missing_featured = 0
    for p in posts:
        content = p.get("content", "")
        # Check for any unrewritten WP image URLs
        wp_refs = re.findall(r'(?:src|srcset)=["\']([^"\']*(?:drconnorrobertson\.com|wp-content/uploads)[^"\']*)["\']', content)
        for ref in wp_refs:
            # Check if this URL was successfully downloaded
            for part in ref.split(","):
                url = part.strip().split()[0]
                if url not in downloaded_images and (WP_DOMAIN in url or "wp-content/uploads" in url):
                    wp_url_remaining += 1
                    if wp_url_remaining <= 5:
                        print(f"    WARN: Un-downloaded image in {p['slug']}: {url[:80]}")
        # Check featured images
        if p.get("featured_image") and p["featured_image"] not in downloaded_images:
            missing_featured += 1
            if missing_featured <= 5:
                print(f"    WARN: Missing featured image for {p['slug']}: {p['featured_image'][:80]}")
    # Verify headshot exists
    headshot = DIST / "images" / "connor-hero.jpg"
    if not headshot.exists():
        print("    WARN: About page headshot missing! Will need manual upload.")
    else:
        print(f"    OK: Headshot found ({headshot.stat().st_size:,} bytes)")
    print(f"  Image verification: {wp_url_remaining} un-downloaded WP refs, {missing_featured} missing featured images")
    print(f"  Total unique images on disk: {len(list(IMAGE_DIR.rglob('*')))}")

    # Static pages
    print("\n[5/8] Generating static pages...")
    write("index.html", page_home())
    write("about/index.html", page_about())
    write("projects/index.html", page_projects())
    write("speaker/index.html", page_speaker())
    write("books/index.html", page_books())
    write("press-media/index.html", page_press())
    write("media/index.html", page_media())
    write("contact/index.html", page_contact())
    write("faq/index.html", page_faq())
    # Pillar/Topic Hub pages
    write("business-acquisitions/index.html", page_business_acquisitions())
    write("ai-business-strategy/index.html", page_ai_business_strategy())
    write("prospecting-sales/index.html", page_prospecting_sales())
    write("author-platform/index.html", page_author_platform())
    # Resource hub pages (linked from nav on every page)
    for label, href in RESOURCE_HUBS:
        write(f"{href.strip('/')}/index.html", page_resource_hub(label, href, posts))
    write("blog/complete-resource-index-dr-connor-robertson/index.html", page_resource_index(posts))
    print(f"  {12 + len(RESOURCE_HUBS) + 1} static pages generated (4 pillar pages + FAQ, {len(RESOURCE_HUBS)} resource hubs, 1 resource index)")

    # Blog posts
    print(f"\n[6/8] Generating {len(posts)} blog post pages...")
    for i, p in enumerate(posts):
        rel = p["relative_url"].strip("/")
        if rel:
            write(f"{rel}/index.html", page_post(p, posts))
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{len(posts)}...")
    print(f"  {len(posts)} post pages generated")
    print(f"  {dead_links_rewritten} dead outbound links repointed at live hosts")

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
    write("robots.txt", robots_txt())
    write(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)
    write("404.html", header("Page Not Found | Dr. Connor Robertson", "", "", noindex=True) + """
<section class="pg-hero" style="min-height:60vh;display:flex;align-items:center"><div class="ctn" style="text-align:center">
<h1>404 &ndash; Page Not Found</h1><p style="margin-top:16px">The page you're looking for doesn't exist. Try one of these instead:</p>
<ul style="list-style:none;padding:0;margin:24px 0;display:flex;gap:20px;flex-wrap:wrap;justify-content:center">
<li><a href="/about/" style="text-decoration:underline">About Connor</a></li>
<li><a href="/blog/" style="text-decoration:underline">Blog</a></li>
<li><a href="/books/" style="text-decoration:underline">Books</a></li>
<li><a href="/speaker/" style="text-decoration:underline">Speaking</a></li>
<li><a href="/contact/" style="text-decoration:underline">Contact</a></li>
</ul>
<a href="/" class="btn-p" style="margin-top:8px;display:inline-block">Go Home</a>
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
