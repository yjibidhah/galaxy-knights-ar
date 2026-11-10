# مجرة الفرسان — موقع أبطال الكرة فرسان المجرة بالعربية

A fast Arabic RTL fan site for **Inazuma Eleven GO Galaxy / أبطال الكرة: فرسان المجرة**, built with plain HTML, CSS, JavaScript and a Python 3 standard-library static-site generator.

This is an independent fan project, not an official website. No anime footage is distributed here. The original illustrations are made specifically for this site.

## Features

- 16 generated pages: homepage, 43-episode viewing tracker, 3 character profiles, 4 Arabic articles, quiz, About, Contact, Privacy, 404 and index pages
- Responsive, accessible Arabic layout for phones and desktop
- Eight-question quiz and local-only viewing progress
- Searchable character directory and articles
- Unique metadata per page, JSON-LD, Open Graph tags, robots.txt, conditional canonical tags and sitemap
- No registration, behavioral tracking or advertising SDKs
- Original CSS, SVG artwork and favicon
- Zero paid API dependencies

## Deploy with Cloudflare Pages

1. In Cloudflare, open **Workers & Pages → Create application → Pages → Connect to Git**.
2. Authorize and select **yjibidhah/galaxy-knights-ar**.
3. Production branch: **main**.
4. Framework preset: **None**.
5. Build command: **python3 build.py**.
6. Build output directory: **public**.
7. Save and deploy. Cloudflare assigns a real \`*.pages.dev\` site address.

Cloudflare builds the \`public/\` folder automatically; generated HTML is not committed to this repository.

## After the first deployment

In the Cloudflare Pages project, add a production environment variable:

\`SITE_URL=https://YOUR-REAL-PROJECT.pages.dev\`

Use the real address assigned by Cloudflare. Redeploy. The builder then adds \`public/sitemap.xml\`, canonical URLs, and full Open Graph URLs.

Submit the verified site to Google Search Console. Indexing and first-page rankings are **not guaranteed**.

## Local testing

\`\`\`bash
python3 build.py
python3 -m http.server 8000 -d public
\`\`\`

Open http://localhost:8000 . No npm packages needed.

To verify the full site and its links, use the included GitHub Actions validation workflow.

## Project files

- \`build.py\`: site source content, templates, SEO, and page generation
- \`assets/styles.css\`: responsive design
- \`assets/app.js\`: episode tracker, quiz, navigation and search
- \`assets/hero.svg\`: original football-in-space illustration
- \`assets/favicon.svg\`: original vector icon

## Before monetization

The site can attract children. Do not add behavioral profiling, personalized advertisements, external chat tools, or data collection until the necessary child-directed advertising and privacy safeguards are reviewed and implemented.

The site is not affiliated with Level-5, the anime's rights holders or distributors. All anime names and trademarks belong to their owners.

## Social links

Actual YouTube and Facebook URLs have **not yet been provided**; no social links were invented.
