# Crawford Consultancy — Website

Static marketing site for **Crawford Consultancy** (HR, payroll and admin support, Falkirk & Central Scotland). Live at [crawfordconsultancy.co.uk](https://crawfordconsultancy.co.uk).

## Current setup (April 2026)

| Item | Detail |
|------|--------|
| Stack | Plain HTML + CSS per page (no bundler or framework) |
| Fonts | Google Fonts: Playfair Display, DM Sans |
| Repo | GitHub (`Crawford1982/crawfordconsultancy`), default branch `master` |
| Domain | `CNAME` sets `crawfordconsultancy.co.uk` for GitHub Pages |

Each page is self-contained: shared look and feel is duplicated in `<style>` blocks (intentionally simple hosting with no build step).

## Site map (main routes)

| Path | Purpose |
|------|---------|
| `/` | Homepage |
| `/pricing/` | HR pricing (Starter Pack, ongoing support, pay-as-you-go) |
| `/about/` | About |
| `/contact/` | Contact / Book a call |
| `/insights/` | Blog / insights index |
| `/hr-payroll-people-support/` | HR & payroll services |
| `/admin-pa-support/` | Admin & PA services |
| `/hr-consultant-falkirk/` | Local SEO hub + areas served |
| `/privacy/` | Privacy policy |

Additional **location/service** landing pages include Stirling, Grangemouth, payroll Falkirk/Stirling, plus dated **insights articles** under their own URLs (see `sitemap.xml`).

## Editing the site

1. **Navigation** — Primary nav and footers are **manual copies** on each HTML file. When adding or renaming a top-level page, update every page that includes the nav (grep for `nav-links` or `href="/pricing/"` patterns to find them).

2. **New page** — Copy a similar existing page (e.g. `about/index.html`), change content, `<title>`, meta description, canonical URL, and add the folder + `index.html`.

3. **SEO** — After adding or removing a public URL, edit **`sitemap.xml`** (and verify internal links).

4. **Apache hosting** — If deploying to Apache, **`/.htaccess`** sets directory indexes, disables directory listings, and cache headers for HTML vs static assets.

## Assets

| File | Role |
|------|------|
| `favicon.svg` | Favicon |
| `og-image.svg` | Open Graph / Twitter preview image |
| `404.html` | Not found page |
| `robots.txt` | Crawl rules + sitemap location |

## Local preview

Open `index.html` in a browser, or from the project root:

```bash
npx serve .
```

(or any static file server).

## Licence / content

Site content is for Crawford Consultancy. Technical configuration in this repo is maintained for deployment only.
