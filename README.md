# Dr. Connor Robertson website

Static Python-generated website deployed through Vercel from this GitHub repository.

## Build

```sh
python3 build.py --no-fetch
node scripts/optimize-media.mjs dist
node scripts/buyer-intent-release.cjs dist
```

Python 3 and Node.js are required. No third-party build dependencies are needed. Vercel uses the build command and output directory in `vercel.json`.

## AI implementation library

`ai_implementation.py` owns 18 original implementation playbooks, three collection pages, the library landing page, templates, and a browser-only ROI calculator. The module uses the existing page chrome, canonical origin, breadcrumbs, and author identity from `build.py`. The sitemap discovers generated pages automatically. The library is linked from the global navigation, AI strategy pillar, and `llms.txt`.

The calculator estimates capacity value, not guaranteed cash savings. Inputs stay in the browser; review and rework are included. Playbook scenarios are explicitly illustrative and make no client-results claims.

See `AI_CONTENT_MAP.md` for URL ownership. Preserve the existing 60 task workflows when adding implementation content.

## Release verification — October 24, 2026

- Full production build pipeline passed.
- All 24 new pages checked for internal link targets, canonical URLs, one H1, valid JSON-LD, and sitemap inclusion.
- Calculator checked against an independently computed example, negative ROI, zero volume, and nonfinite input.
- Browser inspection confirmed the library layout and calculator rendering.

Push the reviewed commit to the connected production branch. Verify the Vercel deployment status and public library URL before reporting it live.

## Industry and discovery expansion

`ai_growth.py` renders eight industry operating plans, six architecture decision guides, their two hubs, a sixteen-term glossary, the complete guide directory, and a readiness planner. Editorial content lives in `content/ai-industries.json` and `content/ai-decisions.json`. The directory combines all 60 task workflows, 18 implementation playbooks, and 14 new guides. Existing URLs retain their original intent.

The directory filters server-rendered cards in the browser. The readiness planner generates concrete missing-prerequisite actions using DOM text nodes, without collecting or transmitting form inputs. Neither tool requires a service or API key.

Run release checks after the complete build pipeline:

```sh
python3 scripts/verify-ai-library.py
node scripts/verify-ai-tools.cjs
```

The checks cover 43 implementation pages, 92 unique guide URLs, canonical metadata, sitemap inclusion, structured data, internal links and fragments, directory search/category/reset behavior, and readiness checklist states. Search performance could not be measured during this release because GSC Wizard required an active subscription. No ranking gains are claimed.
