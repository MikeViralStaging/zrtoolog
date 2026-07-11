# Z.R. Tool Inc. — Website

New zrtool.com, built to the ZR Tool Brand Standard (DOC ZR-BG-02, Edition 02).
Static, fast, dependency-free — designed for **Cloudflare Pages**.

```
zrtool/
├── public/            ← DEPLOY THIS FOLDER (Cloudflare Pages output dir)
│   ├── index.html
│   ├── products/      ← catalog + 11 product pages (MS/ZL/TF/TE/PS series)
│   ├── machines/      ← 7 machine categories + heads/conversions/custom
│   ├── parts/         ← feedwheels · grippers · knives · punches & dies
│   ├── services/  support/  about/  distributors/  contact/
│   ├── downloads/     ← drop manual & trade-sheet PDFs here (see READMEs)
│   ├── assets/        ← css · js · self-hosted fonts · logo · og image
│   ├── _redirects     ← 301s for every legacy /html/*.html URL
│   ├── _headers       ← security + cache headers
│   ├── sitemap.xml  robots.txt  404.html
└── tools/
    ├── data.py        ← ALL site content lives here (products, specs, FAQ…)
    ├── build.py       ← regenerates every page:  python3 tools/build.py
    └── qa.py          ← link/SEO/schema checks:  python3 tools/qa.py
```

## Deploy to Cloudflare Pages

**Option A — drag & drop (fastest):**
Cloudflare dashboard → Workers & Pages → Create → Pages →
*Upload assets* → drag the **contents of `public/`** → Deploy.
Then add the custom domain `www.zrtool.com` (and apex redirect) under
*Custom domains*.

**Option B — Git (recommended long-term):**
Push this whole folder to a repo → Pages → *Connect to Git* →
Build command: `python3 tools/build.py` · Output directory: `public`.
Every push rebuilds and deploys automatically.

## Adding the product manuals (the placeholders)

Every product page and the Support page already show a button per
document. Until the PDF exists it reads **“Request by email”** and opens
a pre-addressed email. The moment you upload a PDF with the matching
filename into `public/downloads/manuals/` or
`public/downloads/trade-sheets/` and deploy, **the button switches itself
to a live download** — the page script checks for the file. Exact
filenames are listed in the `README.txt` inside each downloads folder
(pattern: `zr-ms25-operation-manual.pdf`, `zr-ms25-trade-sheet.pdf`).

## Replacing the photo placeholders

Product/machine images currently use branded technical placeholders
(dark steel panels per the imagery direction, §09 of the brand standard).
When photography is ready, add images and swap the `prod_art(...)` calls
in `tools/build.py` for `<img>` tags — or ask your developer to; it's a
one-line change per product. Shoot to the brand standard: industrial
surfaces, natural side-light, never staged, never stock.

## Editing content

All copy, specs and products live in **`tools/data.py`** — plain Python
lists and strings, clearly labeled. Edit, then run:

```
python3 tools/build.py   # regenerate the site
python3 tools/qa.py      # verify links, titles, schema
```

No build step is required just to deploy — `public/` is always the
finished site.

## Upgrading the forms (optional)

The quote and distributor forms work with zero backend today: submitting
opens the visitor's email client pre-filled to info@zrtool.com. For
silent in-page submission later, add a Cloudflare **Pages Function**
(e.g. `functions/api/quote.js` that emails via MailChannels) and point
the forms at it — the markup already has clean `name` attributes.
Add Cloudflare **Turnstile** for spam protection at the same time.

## SEO — what's built in

- Unique titles & meta descriptions on every page (length-checked)
- Canonical URLs, Open Graph + Twitter cards, custom share image
- JSON-LD structured data: Organization, WebSite, Product (per tool,
  with full spec properties), ItemList, BreadcrumbList, FAQPage,
  ContactPage
- `sitemap.xml` + `robots.txt`
- **301 redirects for every legacy URL** (`/html/MS25.html` →
  `/products/ms25/` etc.) so 25 years of inbound links keep working
- Semantic HTML, one `<h1>` per page, breadcrumbs, skip-link,
  keyboard focus styles, `prefers-reduced-motion` support
- Self-hosted subset WOFF2 fonts (~150 KB total), preloaded criticals,
  no third-party requests at all, immutable asset caching
- Content-Security-Policy and security headers via `_headers`

## After launch checklist

1. Verify the domain in **Google Search Console** and **Bing Webmaster
   Tools**; submit `https://www.zrtool.com/sitemap.xml`.
2. Create/claim the **Google Business Profile** for 1190 Stellar Drive
   and keep the name/address/phone identical to the site footer.
3. Watch Search Console → *Pages* for the legacy `/html/…` URLs being
   reassigned to the new pages (the 301s handle this automatically).
4. Upload manual/trade-sheet PDFs as they're finalized.
5. Replace photo placeholders with real product photography.
