# SEO Portfolio Audit V1 (2026-11-21)

Scope: 73 public repos under drconnorrobertson, shallow cloned and scanned statically (about 50k HTML pages). 10 private repos were not scanned (need add_repo). Live rankings, indexation and Core Web Vitals were not measured (no Search Console or live crawl in this session).

## Baseline
Strong. Nearly every site has titles, descriptions, canonicals, one H1, robots.txt, sitemap.xml and llms.txt. The gaps below are the remaining upside.

## Priority 1: Fix first (largest ranking impact)
1. Sitemaps that omit most pages (pages found vs URLs in sitemap):
   - ae-tax-real-estate 589 vs 9
   - ae-tax-business-owners 581 vs 62
   - ae-tax-case-studies 526 vs 62
   - ae-tax-reviews 555 vs 86
   - swift-line-capital 131 vs 36
   - pittsburgh-business-directory 129 vs 39
   - christinanortman / marksimonsen 20 vs 13
2. No sitemap at all: short-term-rental-vendors (5,952 pages), craft-collective-sample (760), str-market-guide (104), padsplit-playbook (25), bnbacceleratorreviews-site (66, robots has no Sitemap line), mrocek-quote-app, BNB-Underwriting, bnb-accelerator-* mini sites (7 pages each).
3. No robots.txt: short-term-rental-vendors, str-market-guide, padsplit-playbook, the three bnb-accelerator-* mini sites, BNB-Underwriting, connorrobertson-redirect.
4. Duplicate content: the AE Tax satellite sites ship each page twice (root path and /public/ path, same title). Pick one, 301 or canonical the other. Also 130 to 178 duplicate titles per site on ae-tax-reviews, ae-tax-case-studies, ae-tax-business-owners.
5. short-term-rental-vendors: 54% of sampled pages are thin (under 300 words), 99% lack Open Graph tags, and vendor titles and descriptions run over length. Biggest thin-content risk in the portfolio.

## Priority 2: Structured data and snippets
- Missing JSON-LD: bnbacceleratorreviews-site 98%, theprospectingshow 100%, builttorunbook 100%, vitality-chiropractic 87%, connor-robertson-press 80%, estes-associates-website 75%, ae-tax-real-estate 49%, ae-tax-business-owners 41%, centurion-tax-strategist 45%, grant-finder 46%.
- Missing Open Graph and Twitter cards: ae-tax-* satellites 58 to 85%, estes-and-associates 99%, vitality-chiropractic 93%, bnbacceleratorreviews-site 98%, mike-zara-injury 83%, short-term-rental-vendors 99%.
- FAQPage schema absent on pages that already have question headings (ae-tax-* hubs, pittsburghwire, craft-collective-sample). Add FAQPage or HowTo where the page truly answers the questions.
- Long titles (over 65 chars) and descriptions (over 160) truncate in results: ae-tax-*, pittsburghwire /best/ pages, craft-collective-sample posts, vitality-chiropractic.
- Add dateModified to Article schema and lastmod to sitemaps that lack it: builttorunbook, centurion-tax-strategist, lumascapes-pgh, theprospectingshow have none; mike-zara-*, investinshorttermrentals-site, shorttermrentalforsale-site, connor-robertson-books and elixir-consulting-group have it on a minority of URLs.

## Priority 3: Page quality and internal links
- Thin pages: jack-wilder-music 73%, nickkorom 71%, infinitystim 40%, vitality-chiropractic 37%, estes-and-associates 38%, bnb-accelerator mini sites 42 to 85%, pittsburghwire 11% (programmatic /best/ pages with no schema).
- Programmatic pages with under 5 internal links (pittsburghwire guides, ae-tax-reviews blog posts): add related-article and hub links.
- Image alt text is missing on craft-collective-sample (286 of 639 images) and connor-robertson-books (14 of 45). Most other sites show 0 missing alt in the sample. Many sites have thousands of images without width and height or loading="lazy" (ae-tax-advisors-static 3,458, elixir-consulting-group 3,049, restoration-growth-partners 1,511). That costs LCP and CLS.
- Missing canonical: elixirconsultinggroup (100%), thegrantfinder (83%), mrocek-quote-app, connorrobertson-blog 33%, stratum-cost-segregation 6%.
- Missing H1: stratum-cost-segregation 5%, BNB-Underwriting 50%.

## Priority 4: AI search (GEO) and entity signals
- llms.txt missing on: estes-associates-website, estes-and-associates, centurion-tax-strategist, craft-collective-sample, mike-zara-*, matchonemedical, vitality-chiropractic, pittsburgh-business-directory, venoussystems, theprospectingshow, builttorunbook, buy-the-building-book, lumascapes-pgh, restoration-growth-partners, investinshorttermrentals-site, shorttermrentalforsale-site, swift-line-capital.
- robots.txt on all but two sites has no explicit rules for GPTBot, ClaudeBot, PerplexityBot or Google-Extended. Add explicit Allow rules so the intent is unambiguous.
- Cross-link the book sites, wiki sites and personal sites with Person and Organization sameAs schema pointing at one canonical entity.

## Empty or non-site repos
bnbacceleratorreviews and theshorttermrentalblog (1 non-HTML file), cargan-quoting, drconnorrobertson (profile README), rgp-funnel, swiftline-portal (no HTML at root, likely app or build output).

## Suggested order of execution
1. Regenerate sitemaps and robots for the Priority 1 repos (scriptable, low risk).
2. Resolve the /public/ duplicate paths on the four AE satellite sites.
3. Bulk add OG, JSON-LD, FAQ schema and trimmed titles through each site's generator (build.py style) rather than by hand.
4. Add llms.txt and AI crawler rules everywhere.
5. Image attributes and thin-page expansion.

## Not covered
Live indexation, rankings, backlinks, Core Web Vitals, broken external links, and the 10 private repos. Connecting Search Console or Ahrefs (blocked by the proxy this session) would let the next version prioritize by real traffic.
