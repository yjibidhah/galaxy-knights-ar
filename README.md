# مجرة الفرسان | Galaxy Knights Arabic fan site

موقع عربي مستقل لمحبي **أبطال الكرة: فرسان المجرة / Inazuma Eleven GO Galaxy**.

A fast, mobile-first, right-to-left fan website, built as **static HTML, CSS, JavaScript, and a Python 3 standard-library site generator**. It does not require npm, a database, paid hosting, or a backend.

## What's included

- Fully responsive Arabic homepage and accessible navigation
- 43 numbered episodes (Japanese original), with a filter and local-only watch progress
- Character directory and profile pages for بيان، حيان، عقاب
- Four original Arabic articles and an article index
- Eight-question interactive quiz with local scores and optional sharing
- About, Contact, Privacy and custom 404 pages
- Original SVG illustrations, favicon, social card image
- SEO titles, descriptions, Open Graph tags, semantic navigation, JSON-LD, optional canonical URLs and sitemap, `robots.txt`
- Cloudflare security headers
- No copied anime episodes or unlicensed promotional artwork
- No accounts, visitor analytics, or ad scripts in the initial version

## 1. Deploy on GitHub + Cloudflare Pages

1. Go to **https://github.com/new** and create a repository named `galaxy-knights-ar` under your own GitHub account. Keep your existing `sixradar` and `adsnap-ai` repositories untouched.
2. Extract the provided ZIP to a folder, then upload its **contents**, not the ZIP itself, to the new repository. Or open a terminal in that folder and use:

   ```bash
   git init
   git add .
   git commit -m "Launch Arabic Galaxy Knights fan site"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/galaxy-knights-ar.git
   git push -u origin main
   ```

3. In **Cloudflare → Workers & Pages → Create → Pages → Connect to Git**, choose the new repository.
4. Set **Production branch** to `main`, **Build command** to `python3 build.py`, and **Build output directory** to `public` (without a leading `/`).
5. Deploy. Cloudflare provides your actual `*.pages.dev` URL; availability of a particular name is not guaranteed.

The `public/` folder is pre-generated, so you can preview the static pages even without running the build script.

## 2. Enable sitemap and canonical tags after the first deployment

Once Cloudflare gives you the **real** address (e.g. `https://YOUR-ACTUAL-PROJECT.pages.dev`), go to your project's **Settings → Environment variables** and add:

`SITE_URL` = `https://YOUR-ACTUAL-PROJECT.pages.dev`

Set it for **Production** and redeploy (or push a commit). The next `python3 build.py` run generates a valid `public/sitemap.xml`, announces it in `robots.txt`, and adds canonical and full social-media image URLs. **Never leave an invented/incorrect site URL here.**

Visit your live `/sitemap.xml` and then submit it in **Google Search Console**. Request indexing for the homepage and valuable article pages. This helps discovery but does not guarantee ranking or indexation.

## 3. Add your YouTube and Facebook links

Edit `assets/site-config.js`:

```js
window.GALAXY_SOCIAL = {
  youtube: 'https://www.youtube.com/@YOUR_CHANNEL',
  facebook: 'https://www.facebook.com/YOUR_PAGE'
};
```

The site only shows those social links if they are set to a valid HTTPS address. **Use your real URLs, not the examples.** Commit the change to GitHub; Cloudflare rebuilds it automatically.

## 4. Update content / styling

- Text and pages: `build.py`. Run `python3 build.py` and commit the changes.
- Design: `assets/styles.css`
- Interactive tools: `assets/app.js`
- Original vector assets: `assets/hero.svg`, `assets/favicon.svg`
- Shared OG image: `assets/og-cover.png`
- Output: `public/` (generated automatically)

To preview locally:

```bash
python3 build.py
python3 -m http.server 8000 --directory public
```

Then open `http://localhost:8000`.

The optional `make_social_image.py` recreates the OG card; it requires Pillow and CairoSVG and local Arabic font availability. **Not required** for building or deploying the website. Font files are not included.

## SEO and publication checklist

- [ ] Confirm the exact project URL, set `SITE_URL`, and redeploy
- [ ] Submit `https://YOUR_SITE/sitemap.xml` to Google Search Console
- [ ] Add your real YouTube and Facebook profile links
- [ ] Verify the Arabic character-name spellings against your own dubbed reference
- [ ] Add distinctive original articles and community content regularly
- [ ] Replace any artwork only with images you own or have permission to use
- [ ] Verify mobile appearance and usability on a real phone
- [ ] Before advertising, review all applicable child-privacy, COPPA, GDPR, Google publisher, and consent requirements
- [ ] Update the Privacy page if analytics, forms, or advertising are introduced

### Child-friendly design and ads

The intended audience includes young children. **Google ads are not yet configured.** If the site is considered child-directed under applicable law, Google requires proper child-directed treatment and does **not** allow interest-based targeting on child-directed pages or users known to be under 13. Carefully check local laws and updated policies before placing any ad code. A first-page Google rank cannot be promised.

## Rights and attribution

This is a **non-official fan-made informational website**. *Inazuma Eleven*, *Inazuma Eleven GO*, *Inazuma Eleven GO Galaxy*, and the characters are the property of their respective rights holders. The site does not host, distribute, or embed unauthorized episodes and does not copy character art. Descriptive Arabic fan content is editorial.

Factual background and season count checked with publicly accessible sources:
- https://animecca.jp/en/works/inazumairebungogyarakushi
- https://en.wikipedia.org/wiki/Inazuma_Eleven_GO:_Galaxy_(TV_series)
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://support.google.com/publisherpolicies/answer/10436800
- https://developers.cloudflare.com/pages/framework-guides/deploy-anything/