# SEO Portfolio Audit V2 (2026-11-21)

Supersedes SEO_PORTFOLIO_AUDIT_V1.md. Adds the Codex exclusion list and what was changed.

## Codex exclusion (not touched)
Any repo with codex/* branches (30 repos) was treated as under active Codex work and left alone, plus repos pushed within the last day and repos rebuilt by generator scripts (edits would be overwritten).
Excluded with codex branches: ae-tax-advisors-static, ae-tax-business-owners, ae-tax-case-studies, ae-tax-real-estate, ae-tax-reviews, bnb-accelerator-site, bnbacceleratorreviews-site, BNB-Underwriting, built-to-run-book, ccorptaxbook, connor-robertson-books, cost-seg-book, craft-collective-sample, elixir-consulting-group, grant-finder, investinshorttermrentals-site, lumascapes-pgh, mybnbdesign, partnershiptaxbook, pittsburgh-business-directory, pittsburghwire, restoration-growth-partners, seymour-maison, short-term-rental-vendors, shorttermrentalforsale-site, stratum-cost-segregation, the-prospecting-show, therealestatetaxbook, thescorptaxbook, 7-minute-phone-call-book.
Excluded as generated or very recently pushed: book sites with scripts/ builders, wiki sites, nickkorom, christinanortman, marksimonsen, bnb-accelerator mini sites, str-market-guide, padsplit-playbook, vitality-chiropractic (canonical points at github.io, needs an owner decision).

## Changed (branch claude/technical-seo-v1-20261121, additive only, not merged)
swift-line-capital (sitemap +95 URLs, OG on 14 pages, llms.txt), estes-and-associates (OG on 212 pages, llms.txt), estes-associates-website, mike-zara-injury, mike-zara-business-law, matchonemedical, venoussystems, theprospectingshow, builttorunbook, thegrantfinder (canonical + OG on 5 pages), infinitystim, jack-wilder-music, connor-robertson-press, connor-robertson-speaker, connorrobertson-blog.
Each got only what was missing: Open Graph and Twitter tags, canonical, sitemap entries, llms.txt, AI crawler rules in robots.txt (skipped when robots.txt has Disallow rules).

## Still open
All Priority 1 items on Codex repos (sitemap gaps on the AE Tax satellites, /public/ duplicates, short-term-rental-vendors thin pages) need a coordination decision with whoever runs Codex.
JSON-LD and og:image were not auto-generated (need per-site facts and images).
mike-zara-injury canonicals use a vercel.app host; the real domain should be confirmed.
