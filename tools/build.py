# -*- coding: utf-8 -*-
"""Z.R. Tool Inc. — static site generator.

Usage:  python3 tools/build.py
Writes finished pages into ./public (the Cloudflare Pages output folder).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data import (SITE, PRODUCTS, MACHINES, MACHINES_INTRO, PARTS, FAQS,
                  INDUSTRIES, HT_NOTE, APPLICATIONS)

ROOT = os.path.join(os.path.dirname(__file__), "..", "public")
D = SITE["domain"]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def jsonld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False) + "</script>")


def breadcrumb_ld(items):
    return jsonld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name,
             "item": D + url}
            for i, (name, url) in enumerate(items)
        ],
    })


def crumbs_html(items):
    lis = []
    for i, (name, url) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            lis.append(f'<li><a href="{url}">{esc(name)}</a></li>')
    return ('<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>'
            + "".join(lis) + "</ol></nav>")


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": D + "/#organization",
    "name": SITE["name"],
    "alternateName": "ZR Tool",
    "url": D + "/",
    "logo": D + "/assets/img/zr-badge-512.png",
    "foundingDate": SITE["founded"],
    "email": SITE["email"],
    "telephone": "+1-905-836-0590",
    "description": ("Manufacturer of steel strapping tools, sealless "
                    "combination tools, strapping machines and replacement "
                    "parts for all major brands. Newmarket, Ontario, since 1978."),
    "address": {
        "@type": "PostalAddress",
        "streetAddress": SITE["address"]["street"],
        "addressLocality": SITE["address"]["city"],
        "addressRegion": SITE["address"]["region"],
        "postalCode": SITE["address"]["postal"],
        "addressCountry": SITE["address"]["country"],
    },
    "contactPoint": [{
        "@type": "ContactPoint",
        "telephone": "+1-905-836-0590",
        "contactType": "sales",
        "email": SITE["email"],
        "areaServed": "Worldwide",
        "availableLanguage": "English",
    }],
}


BADGE_INLINE = """<svg viewBox="379.4 0 400.6 361.3" aria-hidden="true" focusable="false"><circle fill="#FE0000" cx="579.5" cy="160.1" r="160.1"/><rect fill="#FFFFFF" x="482" y="62.6" width="195.1" height="195.1" transform="translate(56.5 456.7) rotate(-45)"/><g fill="#000"><path transform="translate(494.3,110.9)" d="M0,0 H76 V22 L33,72 H76 V94 H0 V72 L43,22 H0 Z"/><path transform="translate(584.3,110.9)" fill-rule="evenodd" d="M0,0 H54 C72,0 80,10 80,30 C80,46 72,56 56,60 L80,94 H52 L32,62 H22 V94 H0 Z M22,22 H52 C57,22 58,25 58,30 C58,35 57,38 52,38 H22 Z"/></g><path fill="#000" d="M752.6,176.1c-8.1,88.5-82.5,157.8-173,157.8s-165-69.3-173-157.8h-27.4c2.5,31.2,12,60.3,27,85.9l10.9-6.4c6.2,10.4,13.5,20.1,21.5,29.1l-10.9,7.2c17.2,19.8,38.1,36.2,61.7,48l1.4-2.2,5.3-9.6c14.4,7,29.9,12.3,46.1,15.5,0,.2,0,.4-.1.6l-1.1,12.4v.9c0,0,0,0,0,0,12.5,2.4,25.4,3.7,38.7,3.7s21.3-.9,31.6-2.5c0,0,0,0,0,0v-1.3c-.1,0-.9-12.2-.9-12.2,0-.3,0-.5,0-.8,16.9-2.9,33-8,48-15,.3.4.6.8.9,1.2l6.1,9.5,1,1.5c23.2-11.1,44-26.6,61.3-45.3,0,0,0,0,0,0l-1.1-1-8.4-7.4c-.5-.4-1-.7-1.5-1.1,8.9-9.6,16.8-20.1,23.6-31.4.6.2,1.3.4,1.9.6l8.5,5.8,1.9,1.1s0,0,0,0c15.3-25.8,25.1-55.3,27.6-86.8h-27.4Z"/></svg>"""

BADGE_REV = BADGE_INLINE.replace(
    '<path fill="#000" d="M752.6', '<path fill="#F7F5F0" d="M752.6')

DOC_ICON = ('<svg class="ic" viewBox="0 0 16 16" aria-hidden="true">'
            '<path fill="currentColor" d="M3 0h7l3 3v13H3V0zm7 1v3h3M5 8h6v1H5'
            'V8zm0 3h6v1H5v-1z"/></svg>')


NAV_ITEMS = [
    ("Tools", "/products/"),
    ("Machines", "/machines/"),
    ("Parts", "/parts/"),
    ("Services", "/services/"),
    ("Support", "/support/"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
]


def shell(*, path, title, desc, body, extra_head="", current=None,
          og_type="website"):
    canonical = D + path
    nav = "".join(
        f'<li><a href="{url}"'
        + (' aria-current="page"' if current == url else "")
        + f'>{label}</a></li>'
        for label, url in NAV_ITEMS
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#1F2328">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{D}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{D}/assets/img/og-image.png">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/oswald-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibmplexsans-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/main.css">
{extra_head}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="Z.R. Tool Inc. — home">
      {BADGE_INLINE}
      <span class="word">Z.R. Tool<small>Quality Strapping · Since 1978</small></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Primary">
      <ul>
        {nav}
        <li class="header-cta"><a class="btn btn-red btn-sm" href="/contact/" style="border-bottom:none">Request Quote</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="hazard" aria-hidden="true"></div>
  <div class="wrap top">
    <div>
      <div class="badge">{BADGE_REV}</div>
      <p style="font-family:var(--f-display);font-weight:700;font-size:1.4rem;text-transform:uppercase;line-height:1">Z.R. Tool Inc.</p>
      <p class="tagline">— {SITE['tagline']} —</p>
    </div>
    <div>
      <h4>Products</h4>
      <ul>
        <li><a href="/products/manual-sealless-tools/">Manual Sealless Tools</a></li>
        <li><a href="/products/pneumatic-sealless-tools/">Pneumatic Sealless Tools</a></li>
        <li><a href="/machines/">Strapping Machines</a></li>
        <li><a href="/parts/">Replacement Parts</a></li>
      </ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul>
        <li><a href="/about/">About ZR Tool</a></li>
        <li><a href="/services/">Services</a></li>
        <li><a href="/support/">Support &amp; Downloads</a></li>
        <li><a href="/distributors/">Distributors</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <address>
        {SITE['address']['street']}<br>
        {SITE['address']['city']}, {SITE['address']['region']} {SITE['address']['postal']} · {SITE['address']['country_name']}<br>
        <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a><br>
        <a href="mailto:{SITE['email']}">{SITE['email']}</a>
      </address>
    </div>
  </div>
  <div class="wrap legal">
    <span>© Z.R. Tool Inc. · All rights reserved</span>
    <span>Products shown are patented or have patents pending</span>
    <span class="doc">ZRTOOL.COM · EST. 1978 · NEWMARKET, ONTARIO</span>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def write(path, html):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def sec_head(eyebrow, title, lede=None, dark=False):
    out = [f'<div class="sec-head"><p class="eyebrow">{eyebrow}</p>']
    out.append(f'<h2>{title}<span class="dot">.</span></h2>')
    out.append('<hr class="rulepair">')
    if lede:
        out.append(f'<p class="lede mt-2">{lede}</p>')
    out.append("</div>")
    return "".join(out)


def prod_art(model, small=False, note="Product photography in production"):
    cls = "prod-art small" if small else "prod-art"
    return (f'<div class="{cls}" role="img" aria-label="{model} — product '
            f'photo placeholder"><p class="label"><span class="model">{model}'
            f'</span>{note}</p></div>')


def doc_button(kind, prod):
    """Placeholder-aware document link. kind: 'trade-sheet' | 'manual'."""
    if kind == "trade-sheet":
        url = f"/downloads/trade-sheets/zr-{prod['slug']}-trade-sheet.pdf"
        label = "Trade sheet"
        subj = f"Trade sheet request — {prod['model']}"
    else:
        url = f"/downloads/manuals/zr-{prod['slug']}-operation-manual.pdf"
        label = "Operation manual"
        subj = f"Operation manual request — {prod['model']}"
    mail = (f"mailto:{SITE['email']}?subject=" + subj.replace(" ", "%20")
            .replace("—", "%E2%80%94"))
    return (f'<a class="doc-pending" data-doc="{url}" href="{mail}">'
            f'{DOC_ICON}<span>{label}</span>'
            f'<span class="st">Request by email</span></a>')


def cta_band(title="Ready to talk strapping", text=None, primary=("Request a quote", "/contact/"),
             secondary=("Call " + SITE["phone_display"], "tel:" + SITE["phone_tel"])):
    text = text or ("You identify the need. We engineer the solution. "
                    "Same shop in Newmarket since 1978.")
    return f"""<section class="cta-band">
  <div class="wrap">
    <div>
      <h2>{title}<span class="dot">.</span></h2>
      <p>{text}</p>
    </div>
    <div class="btns">
      <a class="btn btn-ink" href="{primary[1]}">{primary[0]}</a>
      <a class="btn" href="{secondary[1]}">{secondary[0]}</a>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------

def build_home():
    tiles = f"""
    <div class="grid grid-4">
      <div class="tile"><span class="num">01 / TOOLS — MANUAL</span>
        <h3>Manual Sealless Tools</h3>
        <p>Eight tools that tension, seal and cut with no metal seals — including the world's only manual sealless tools for 1 1/4" strap.</p>
        <a class="goto" href="/products/manual-sealless-tools/">View the line →</a></div>
      <div class="tile"><span class="num">02 / TOOLS — PNEUMATIC</span>
        <h3>Pneumatic Sealless Tools</h3>
        <p>Two-button, air-powered strapping for production volume. Up to 2,900 lbs of tension on 1 1/4" strap.</p>
        <a class="goto" href="/products/pneumatic-sealless-tools/">View the line →</a></div>
      <div class="tile"><span class="num">03 / MACHINERY</span>
        <h3>Strapping Machines</h3>
        <p>Sealless and seal-type machines from 5/8" to 1 1/4", hydraulic or pneumatic — plus conversion kits and heads.</p>
        <a class="goto" href="/machines/">View machinery →</a></div>
      <div class="tile"><span class="num">04 / PARTS</span>
        <h3>Replacement Parts</h3>
        <p>Feedwheels, grippers, knives, punches and dies for all major brands — or machined from your sample.</p>
        <a class="goto" href="/parts/">View parts →</a></div>
    </div>"""

    finder_buttons = "".join(
        f'<a class="btn" href="/products/?width={w}">{lbl}</a>'
        for w, lbl in [("13", '1/2" · 13 mm'), ("16", '5/8" · 16 mm'),
                       ("19", '3/4" · 19 mm'), ("32", '1 1/4" · 32 mm')])

    why = """
    <div class="grid grid-3">
      <div class="card"><span class="mono-tag">Nº 01 — Patented</span>
        <h3>The Joint Does the Talking</h3>
        <p>Patented sealless designs with better joint efficiency and 30–50% less operator effort than comparable tools. Numerous patents awarded over four decades of doing one thing right.</p></div>
      <div class="card"><span class="mono-tag">Nº 02 — Exclusive</span>
        <h3>Z-Lock Reverse Locking</h3>
        <p>The only manual tools available with a reverse locking system. The joint holds in either direction — added protection for loads that shift, settle or ride rough.</p></div>
      <div class="card"><span class="mono-tag">Nº 03 — Only One</span>
        <h3>1 1/4" Without Air or Power</h3>
        <p>The ZL90 and TE90 are the world's only manual sealless combination tools for 1 1/4" (32 mm) steel strapping. Nobody else makes them. We do.</p></div>
      <div class="card"><span class="mono-tag">Nº 04 — Fewer Parts</span>
        <h3>Half the Parts to Fail</h3>
        <p>Our tools carry the fewest components in their class — comparable tools have roughly twice as many. Fewer parts, easier operation, less time on the bench.</p></div>
      <div class="card"><span class="mono-tag">Nº 05 — Serviceable</span>
        <h3>Minutes, Not Hours</h3>
        <p>Feedwheel, gripper, knife, punch or die: each replaces in a few minutes. Tools built to be maintained in your shop, not shipped away.</p></div>
      <div class="card"><span class="mono-tag">Nº 06 — All Brands</span>
        <h3>Parts for Everyone's Equipment</h3>
        <p>We manufacture replacement parts and assemblies for all major brands of strapping machinery and tools — and we can work from a sample.</p></div>
    </div>"""

    industries = "".join(
        f'<div class="card"><h3 style="font-size:1.05rem">{t}</h3>'
        f'<p>{d}</p></div>' for t, d in INDUSTRIES)

    body = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow">Steel Strapping Equipment · Manufacturer</p>
      <h1>Strapping tools built to outlast the job<span class="dot">.</span></h1>
      <p class="lede">Z.R. Tool designs and manufactures sealless combination tools, steel strapping machines and replacement parts for all major brands — engineered and built in Newmarket, Ontario since 1978.</p>
      <div class="cta-row">
        <a class="btn btn-red" href="/products/">Browse tools</a>
        <a class="btn" href="/contact/">Request a quote</a>
      </div>
      <p class="tagline since">— {SITE['tagline']} —</p>
    </div>
    <div class="badge-art">{BADGE_INLINE}</div>
  </div>
  <div class="hazard" aria-hidden="true"></div>
</section>

<section class="truststrip" aria-label="Company facts">
  <div class="wrap">
    <div class="cell"><p class="k">Since 1978</p><p class="v">Same specialty · Same shop</p></div>
    <div class="cell"><p class="k">Patented</p><p class="v">Numerous patents awarded</p></div>
    <div class="cell"><p class="k">1 1/4" Sealless</p><p class="v">World's only manual tools</p></div>
    <div class="cell"><p class="k">All Brands</p><p class="v">Replacement parts made here</p></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("The catalog", "Tools, machines &amp; parts", "Everything below is designed, machined, assembled and tested in-house. If it wears the ZR name, it was built here.")}
    {tiles}
  </div>
</section>

<section class="section section-white">
  <div class="wrap">
    {sec_head("Find your tool", "Start with your strap")}
    <p class="lede mb-3">Pick the strap width you run and we'll show every tool that handles it — manual and pneumatic, standard and Z-Lock.</p>
    <div class="doc-row">{finder_buttons}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Why ZR", "Trust, not talk", "Four decades of shipping to the same customers. The catalog earns respect the way the tools do — by holding up over time.")}
    {why}
  </div>
</section>

<section class="section section-ink">
  <div class="wrap">
    {sec_head("Capabilities", "Design. Build. Rebuild.")}
    <div class="split">
      <div>
        <p class="lede">Full in-house engineering and manufacturing: CAD/CAM design, CNC machining, assembly and final testing to our own uncompromising standard.</p>
        <p class="mt-2" style="color:var(--steel)">From redesigning heads and sealing systems to seal-type ↔ sealless conversions and full special-application machinery — we have done it all, worldwide.</p>
        <div class="cta-row mt-3"><a class="btn btn-ghost-light" href="/services/">Explore services</a></div>
      </div>
      <div class="grid" style="gap:.75rem">
        <div class="card" style="background:transparent;border-color:rgba(247,245,240,.2)"><h3 style="color:var(--paper);font-size:1rem">Design</h3><p style="color:var(--steel)">Concept to final product with in-house designers and draftspeople.</p></div>
        <div class="card" style="background:transparent;border-color:rgba(247,245,240,.2)"><h3 style="color:var(--paper);font-size:1rem">Manufacturing</h3><p style="color:var(--steel)">CNC and conventional machining by skilled toolmakers.</p></div>
        <div class="card" style="background:transparent;border-color:rgba(247,245,240,.2)"><h3 style="color:var(--paper);font-size:1rem">Assembly &amp; Testing</h3><p style="color:var(--steel)">Every unit assembled and final-tested before it ships.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Industries", "Where our strapping goes to work")}
    <div class="grid grid-3">{industries}</div>
  </div>
</section>

{cta_band()}
"""
    ld = [
        jsonld({**ORG_LD}),
        jsonld({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "url": D + "/",
            "name": SITE["name"],
            "publisher": {"@id": D + "/#organization"},
        }),
    ]
    write("/index.html", shell(
        path="/",
        title="Steel Strapping Tools & Machines | Z.R. Tool Inc.",
        desc=("Manufacturer of sealless steel strapping tools, machines and "
              "replacement parts for all major brands. Patented designs, "
              "built in Newmarket, Ontario since 1978."),
        body=body, extra_head="".join(ld), current=None))


# ---------------------------------------------------------------------------
# PRODUCTS INDEX (+ filter)
# ---------------------------------------------------------------------------

def product_card(p):
    chips = []
    if p.get("world_only"):
        chips.append('<span class="chip chip-red">Only one of its kind</span>')
    if p["zlock"]:
        chips.append('<span class="chip">Z-Lock</span>')
    if p["stainless"]:
        chips.append('<span class="chip">Stainless-capable</span>')
    if p["windlass"]:
        chips.append('<span class="chip">Windlass tension</span>')
    power_lbl = "Manual" if p["category"] == "manual" else "Pneumatic"
    return f"""<article class="card" data-widths="{' '.join(p['widths'])}" data-power="{p['category']}">
  <span class="mono-tag">{power_lbl} · Sealless combination</span>
  <h3><a href="/products/{p['slug']}/">{p['model']}</a></h3>
  <p>{esc(p['summary'])}</p>
  <div class="doc-row" style="gap:.35rem">{''.join(chips)}</div>
  <p class="spec-line">{esc(p['range_line'])}</p>
</article>"""


def build_products_index():
    cards = "".join(product_card(p) for p in PRODUCTS)
    filterbar = """
<div class="filterbar" id="tool-filter">
  <div class="group">
    <span class="group-label" id="fl-width">Strap width</span>
    <div class="opts" role="group" aria-labelledby="fl-width">
      <button class="fbtn" data-group="width" data-value="all" aria-pressed="true">All</button>
      <button class="fbtn" data-group="width" data-value="13" aria-pressed="false">1/2" · 13 mm</button>
      <button class="fbtn" data-group="width" data-value="16" aria-pressed="false">5/8" · 16 mm</button>
      <button class="fbtn" data-group="width" data-value="19" aria-pressed="false">3/4" · 19 mm</button>
      <button class="fbtn" data-group="width" data-value="32" aria-pressed="false">1 1/4" · 32 mm</button>
    </div>
  </div>
  <div class="group">
    <span class="group-label" id="fl-power">Operation</span>
    <div class="opts" role="group" aria-labelledby="fl-power">
      <button class="fbtn" data-group="power" data-value="all" aria-pressed="true">All</button>
      <button class="fbtn" data-group="power" data-value="manual" aria-pressed="false">Manual</button>
      <button class="fbtn" data-group="power" data-value="pneumatic" aria-pressed="false">Pneumatic</button>
    </div>
  </div>
  <span class="filter-count" id="filter-count" aria-live="polite"></span>
</div>"""

    crumbs = [("Home", "/"), ("Tools", "/products/")]
    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Product catalog</p>
  <h1>Sealless combination tools<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">Eleven tools. One patented joint. Every ZR combination tool tensions, seals and cuts high-tensile steel strapping — up to 156,000 psi (1,100 N/mm²) — with no metal seals to buy, stock or load.</p>
</div></section>
<section class="section-tight"><div class="wrap">
  {filterbar}
  <h2 class="mb-2" style="font-size:1.4rem">Manual tools</h2>
  <div class="grid grid-3 mb-3">{''.join(product_card(p) for p in PRODUCTS if p['category']=='manual')}</div>
  <h2 class="mb-2" style="font-size:1.4rem">Pneumatic tools</h2>
  <div class="grid grid-3">{''.join(product_card(p) for p in PRODUCTS if p['category']=='pneumatic')}</div>
</div></section>
{cta_band("Not sure which tool fits", "Tell us your strap size, load and volume. We'll point you at the right tool — and only the right tool.")}
"""
    ld = [
        breadcrumb_ld(crumbs),
        jsonld({
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "ZR Tool sealless combination tools",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "url": f"{D}/products/{p['slug']}/", "name": p["name"]}
                for i, p in enumerate(PRODUCTS)
            ],
        }),
    ]
    write("/products/index.html", shell(
        path="/products/",
        title="Sealless Steel Strapping Tools | Z.R. Tool Inc.",
        desc=("The complete ZR line: 8 manual and 3 pneumatic sealless "
              "combination tools for steel strapping from 1/2\" to 1 1/4\". "
              "Filter by strap size and operation."),
        body=body, extra_head="".join(ld), current="/products/"))
    _ = cards  # cards rendered per-section above


# ---------------------------------------------------------------------------
# CATEGORY PAGES
# ---------------------------------------------------------------------------

def build_category(cat, path, title, h1, desc, lede, extra):
    items = [p for p in PRODUCTS if p["category"] == cat]
    crumbs = [("Home", "/"), ("Tools", "/products/"), (h1, path)]
    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">{'Manual line' if cat=='manual' else 'Pneumatic line'}</p>
  <h1>{h1}<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">{lede}</p>
</div></section>
<section class="section-tight"><div class="wrap">
  <div class="grid grid-3">{''.join(product_card(p) for p in items)}</div>
  <div class="callout mt-4"><p class="k">▸ Good to know</p><p>{extra}</p></div>
</div></section>
{cta_band()}
"""
    ld = [
        breadcrumb_ld(crumbs),
        jsonld({
            "@context": "https://schema.org", "@type": "ItemList",
            "name": h1,
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "url": f"{D}/products/{p['slug']}/", "name": p["name"]}
                for i, p in enumerate(items)
            ],
        }),
    ]
    write(path + "index.html", shell(
        path=path, title=title, desc=desc, body=body,
        extra_head="".join(ld), current="/products/"))


# ---------------------------------------------------------------------------
# PRODUCT PAGES
# ---------------------------------------------------------------------------

def build_product(p):
    path = f"/products/{p['slug']}/"
    cat_name = ("Manual Sealless Tools" if p["category"] == "manual"
                else "Pneumatic Sealless Tools")
    cat_url = ("/products/manual-sealless-tools/" if p["category"] == "manual"
               else "/products/pneumatic-sealless-tools/")
    crumbs = [("Home", "/"), ("Tools", "/products/"),
              (cat_name, cat_url), (p["model"], path)]

    chips = [f'<span class="chip">{p["kind"]}</span>']
    if p.get("world_only"):
        chips.insert(0, '<span class="chip chip-red">Only one of its kind</span>')

    feats = "".join(
        f"<li><strong>{t}.</strong> {d}</li>" for t, d in p["features"])

    variants_rows = "".join(
        f"<tr><th scope='row'>{m}</th><td>{w}</td><td>{t}</td></tr>"
        for m, w, t in p["variants"])
    vnote = (f'<p class="small mt-1">{esc(p["variant_note"])}</p>'
             if p.get("variant_note") else "")

    phys_rows = "".join(
        f"<tr><th scope='row'>{k}</th><td>{v}</td></tr>"
        for k, v in p["physical"])
    pneumo_rows = "".join(
        f"<tr><th scope='row'>{k}</th><td>{v}</td></tr>"
        for k, v in p.get("pneumo", []))
    pneumo_table = (f"""<table class="spec-table mt-3">
      <caption>Performance</caption>
      <tbody>{pneumo_rows}</tbody></table>""" if pneumo_rows else "")

    world = (f'<div class="callout mb-3"><p class="k">▸ One of one</p>'
             f'<p>{esc(p["world_only"])}</p></div>'
             if p.get("world_only") else "")

    related = [x for x in PRODUCTS if x["slug"] != p["slug"]
               and (set(x["widths"]) & set(p["widths"]))][:3]
    related_html = "".join(product_card(x) for x in related)

    desc_html = "".join(f"<p class='mt-2'>{esc(t)}</p>" for t in p["desc"])

    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap prod-top">
  <div>
    <p class="eyebrow">{'Manual' if p['category']=='manual' else 'Pneumatic'} sealless combination tool</p>
    <h1>{p['model']}<span class="dot">.</span></h1>
    <div class="prod-meta">{''.join(chips)}</div>
    <p class="lede">{esc(p['summary'])}</p>
    {desc_html}
    <p class="mt-2 small">{HT_NOTE}</p>
    <div class="cta-row mt-3" style="display:flex;gap:.9rem;flex-wrap:wrap">
      <a class="btn btn-red" href="/contact/?product={p['model']}">Request a quote</a>
      <a class="btn" href="tel:{SITE['phone_tel']}">Call {SITE['phone_display']}</a>
    </div>
  </div>
  <div>
    {prod_art(p['model'])}
    <div class="doc-row mt-2">
      {doc_button('trade-sheet', p)}
      {doc_button('manual', p) if p['has_manual'] else ''}
    </div>
    <p class="small mt-1">Documents marked “request by email” are being prepared for the new site — we'll send the PDF directly, usually the same business day.</p>
  </div>
</div></section>

<section class="section-tight section-white"><div class="wrap">
  {world}
  {sec_head("Why this tool", "Built the ZR way")}
  <ul class="featlist">{feats}</ul>
</div></section>

<section class="section-tight"><div class="wrap">
  {sec_head("Specifications", "The numbers")}
  <div class="split" style="align-items:start">
    <div class="spec-wrap">
      <table class="spec-table">
        <caption>Models &amp; strap range</caption>
        <thead><tr><th scope="col">Model</th><th scope="col">Strap width</th><th scope="col">Strap thickness</th></tr></thead>
        <tbody>{variants_rows}</tbody>
      </table>
      {vnote}
    </div>
    <div>
      <table class="spec-table">
        <caption>Physical</caption>
        <tbody>{phys_rows}</tbody>
      </table>
      {pneumo_table}
    </div>
  </div>
  <p class="small mt-3">Applications: {APPLICATIONS}.</p>
</div></section>

<section class="section-tight section-white"><div class="wrap">
  {sec_head("Related", "Tools that run the same strap")}
  <div class="grid grid-3">{related_html}</div>
</div></section>

{cta_band(f"Put the {p['model']} to work",
          "Test and compare — price, value, quality and durability. We're confident where you'll land.")}
"""

    props = []
    for m, w, t in p["variants"]:
        props.append({"@type": "PropertyValue",
                      "name": f"{m} strap width", "value": w})
        props.append({"@type": "PropertyValue",
                      "name": f"{m} strap thickness", "value": t})
    for k, v in p["physical"] + p.get("pneumo", []):
        props.append({"@type": "PropertyValue", "name": k, "value": v})

    product_ld = jsonld({
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["name"],
        "model": p["model"],
        "sku": p["model"],
        "url": D + path,
        "image": D + "/assets/img/og-image.png",
        "description": p["summary"],
        "category": ("Manual sealless combination tools"
                     if p["category"] == "manual"
                     else "Pneumatic sealless combination tools"),
        "brand": {"@type": "Brand", "name": "ZR Tool"},
        "manufacturer": {"@id": D + "/#organization"},
        "countryOfOrigin": "CA",
        "additionalProperty": props,
    })

    title = f"{p['model']} {('Manual' if p['category']=='manual' else 'Pneumatic')} Sealless Strapping Tool | ZR Tool"
    meta = (f"{p['model']} {'manual' if p['category']=='manual' else 'pneumatic'} "
            f"sealless combination tool for steel strapping, "
            f"{p['range_line']}. Full specs and documentation from the "
            f"manufacturer — Z.R. Tool Inc.")
    if len(meta) > 160:
        meta = (f"{p['model']} {'manual' if p['category']=='manual' else 'pneumatic'} "
                f"sealless combination tool for high-tensile steel strapping. "
                f"Full specs and documentation from the manufacturer — "
                f"Z.R. Tool Inc.")
    write(path + "index.html", shell(
        path=path, title=title, desc=meta, body=body,
        extra_head=breadcrumb_ld(crumbs) + product_ld,
        current="/products/", og_type="product"))


# ---------------------------------------------------------------------------
# MACHINES
# ---------------------------------------------------------------------------

def build_machines():
    crumbs = [("Home", "/"), ("Strapping Machines", "/machines/")]

    def machine_cards(group):
        cards = []
        for it in MACHINES[group]["items"]:
            note = (f'<p class="small" style="color:#8a5f14">{it["note"]}</p>'
                    if it.get("note") else "")
            cards.append(f"""<article class="card anchor-offset" id="{it['id']}">
  <span class="mono-tag">{MACHINES[group]['title']}</span>
  <h3 style="position:static">{it['label']}</h3>
  {prod_art(it['label'], small=True, note='Machine photography in production')}
  <p class="spec-line" style="border-top:0;padding-top:0">{it['spec']}</p>
  {note}
</article>""")
        return "".join(cards)

    intro = "".join(f"<p class='lede mt-2'>{t}</p>" for t in MACHINES_INTRO)
    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Machinery</p>
  <h1>Steel strapping machines<span class="dot">.</span></h1>
  <hr class="rulepair">
  {intro}
</div></section>

<section class="section-tight"><div class="wrap">
  {sec_head("Sealless", MACHINES['sealless']['title'], MACHINES['sealless']['blurb'])}
  <div class="grid grid-2">{machine_cards('sealless')}</div>
</div></section>

<section class="section-tight section-white"><div class="wrap">
  {sec_head("Seal-type", MACHINES['sealtype']['title'], MACHINES['sealtype']['blurb'])}
  <div class="grid grid-3">{machine_cards('sealtype')}</div>
</div></section>

<section class="section-tight"><div class="wrap">
  {sec_head("Beyond the standard line", "Heads, conversions &amp; custom builds")}
  <div class="grid grid-3">
    <div class="card"><h3>Strapping heads</h3><p>New heads, and redesign or rebuild of your existing heads — restored to spec and returned to service.</p></div>
    <div class="card"><h3>Conversion kits</h3><p>Move existing machinery between seal-type and sealless operation without replacing the machine.</p></div>
    <div class="card"><h3>Special application machinery</h3><p>Hydraulic or pneumatic, engineered around your product. Some of the most innovative strapping projects worldwide started as a conversation here.</p></div>
  </div>
  <div class="callout mt-4"><p class="k">▸ How machine quotes work</p>
  <p>Machinery is specified to your line: strap size, package, cycle rate, and plant utilities. Send us those four things and we'll come back with a recommendation and quote — no configurator guesswork.</p></div>
</div></section>

{cta_band("Spec a machine", "Tell us your strap size, package and cycle rate. We'll engineer from there.")}
"""
    ld = [
        breadcrumb_ld(crumbs),
        jsonld({
            "@context": "https://schema.org", "@type": "ItemList",
            "name": "ZR Tool steel strapping machines",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "name": it["label"],
                 "url": f"{D}/machines/#{it['id']}"}
                for i, it in enumerate(
                    MACHINES["sealless"]["items"] + MACHINES["sealtype"]["items"])
            ],
        }),
    ]
    write("/machines/index.html", shell(
        path="/machines/",
        title="Steel Strapping Machines & Heads | Z.R. Tool Inc.",
        desc=("Sealless and seal-type steel strapping machines, 5/8\" to "
              "1 1/4\", hydraulic or pneumatic. Conversion kits, heads and "
              "custom machinery — built since 1978."),
        body=body, extra_head="".join(ld), current="/machines/"))


# ---------------------------------------------------------------------------
# PARTS
# ---------------------------------------------------------------------------

def build_parts():
    crumbs = [("Home", "/"), ("Replacement Parts", "/parts/")]
    cards = "".join(f"""<article class="card anchor-offset" id="{c['id']}">
  <span class="mono-tag">Parts · {c['title']}</span>
  <h3 style="position:static">{c['title']}</h3>
  <p>{c['desc']}</p>
</article>""" for c in PARTS)

    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Replacement parts</p>
  <h1>Parts for all major brands<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">Z.R. Tool manufactures replacement parts and assemblies for all major brands of strapping machinery, equipment and tools — not just our own. If we don't already make it, send a sample: we'll manufacture it, or improve it to suit your application.</p>
</div></section>

<section class="section-tight"><div class="wrap">
  <div class="grid grid-2">{cards}</div>
</div></section>

<section class="section-tight section-white"><div class="wrap">
  {sec_head("Ordering", "Three ways to get the right part")}
  <div class="grid grid-3">
    <div class="card"><span class="mono-tag">Option 1</span><h3 style="font-size:1.05rem">By ZR part number</h3><p>Every ZR operation manual carries a full parts list with positions and part numbers. Quote the number and we'll take it from there.</p></div>
    <div class="card"><span class="mono-tag">Option 2</span><h3 style="font-size:1.05rem">By make &amp; model</h3><p>Running another brand? Give us the equipment make, model and the part you need — we manufacture for all major brands.</p></div>
    <div class="card"><span class="mono-tag">Option 3</span><h3 style="font-size:1.05rem">From a sample</h3><p>No number, no drawing, no problem. Ship us the worn part and we'll reverse-engineer it — or improve it while we're at it.</p></div>
  </div>
  <div class="callout mt-4"><p class="k">▸ A word on genuine parts</p>
  <p>ZR tools are designed for high-tensile strapping, and every part is manufactured or treated for those conditions. Parts from unauthorized sources will affect performance — and can cause injury. Use genuine ZR replacement parts.</p></div>
</div></section>

{cta_band("Order a part", "Part number, make &amp; model, or a sample in a box — whatever you have, we can work with it.")}
"""
    write("/parts/index.html", shell(
        path="/parts/",
        title="Strapping Tool & Machine Replacement Parts | ZR Tool",
        desc=("Feedwheels, grippers, knives, punches and dies for all major "
              "brands of strapping tools and machinery. Custom parts "
              "machined from your sample by Z.R. Tool."),
        body=body, extra_head=breadcrumb_ld(crumbs), current="/parts/"))


# ---------------------------------------------------------------------------
# SERVICES
# ---------------------------------------------------------------------------

def build_services():
    crumbs = [("Home", "/"), ("Services", "/services/")]
    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Capabilities</p>
  <h1>Design. Build. Rebuild<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">Full in-house services, product or project. We respond to the specific packaging needs of a wide range of industries, and an experienced staff member is always on hand to talk through what you need.</p>
</div></section>

<section class="section-tight"><div class="wrap grid" style="gap:1.5rem">
  <article class="card"><span class="mono-tag">§ 01 — Design</span>
    <h3>Engineering &amp; Design</h3>
    <p>Our in-house designers and draftspeople work in current CAD/CAM software, carrying projects from concept through to final product. From the redesign of tools and sealing systems to entirely new strapping machinery, consultants are on hand to define the requirement before a single chip is cut.</p></article>
  <article class="card"><span class="mono-tag">§ 02 — Manufacturing</span>
    <h3>Precision Manufacturing</h3>
    <p>A fully equipped facility running computerized CNC alongside conventional machinery handles both streamlined assembly runs and custom precision work. Everything is manufactured in-house by skilled toolmakers, to one rigid company standard.</p></article>
  <article class="card"><span class="mono-tag">§ 03 — Assembly &amp; Testing</span>
    <h3>Assembly &amp; Final Testing</h3>
    <p>Every unit is assembled and final-tested to ZR's uncompromising standard before it ships. We've been part of some of the most innovative projects in the industry worldwide — head redesigns and rebuilds, seal-type to sealless conversions, and full special-application machinery.</p></article>
</div></section>

<section class="section-tight section-white"><div class="wrap">
  {sec_head("Consulting", "You identify the need. We engineer the solution.")}
  <p class="lede">Our consulting and custom design services help you determine the requirement itself — not just fill an order. We work for long-term, responsible partnerships, which is why customers from our first decade are still customers now.</p>
  <p class="mt-2 small">For technical support on any ZR product or service: <a href="mailto:{SITE['email_support']}">{SITE['email_support']}</a></p>
</div></section>

{cta_band("Start a project", "Rebuild, conversion or clean-sheet design — the first conversation costs nothing.")}
"""
    write("/services/index.html", shell(
        path="/services/",
        title="Design, Manufacturing & Rebuilds | Z.R. Tool Inc.",
        desc=("In-house CAD/CAM design, CNC manufacturing, assembly and "
              "testing. Head rebuilds, sealless conversions and custom "
              "strapping machinery from Z.R. Tool."),
        body=body, extra_head=breadcrumb_ld(crumbs), current="/services/"))


# ---------------------------------------------------------------------------
# SUPPORT & DOWNLOADS
# ---------------------------------------------------------------------------

def build_support():
    crumbs = [("Home", "/"), ("Support & Downloads", "/support/")]
    rows = []
    for p in PRODUCTS:
        manual_cell = (doc_button("manual", p) if p["has_manual"]
                       else doc_button("manual", p))
        rows.append(f"""<tr>
  <td class="model-cell"><a href="/products/{p['slug']}/" style="text-decoration:none;color:inherit">{p['model']}</a></td>
  <td class="cat-cell">{'Manual' if p['category']=='manual' else 'Pneumatic'}</td>
  <td>{doc_button('trade-sheet', p)}</td>
  <td>{manual_cell}</td>
</tr>""")

    faq_html = "".join(
        f"""<details><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>"""
        for q, a in FAQS)

    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Support</p>
  <h1>Manuals, trade sheets &amp; answers<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">Every document for every tool, in one place. PDFs still being prepared for the new site show as “request by email” — send the request and we'll reply with the document directly, usually the same business day. As each PDF is uploaded, its download button switches on automatically.</p>
</div></section>

<section class="section-tight"><div class="wrap">
  {sec_head("Downloads", "Documentation by model")}
  <div class="spec-wrap">
  <table class="dl-table">
    <thead><tr><th scope="col">Model</th><th scope="col">Type</th><th scope="col">Trade sheet</th><th scope="col">Operation manual</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  </div>
</div></section>

<section class="section-tight section-white"><div class="wrap">
  {sec_head("Safety", "Before you run any strapping tool")}
  <ul class="featlist">
    <li><strong>Read the operation manual first.</strong> The whole thing — before the tool touches strap. Failure to follow the instructions can result in severe injury.</li>
    <li><strong>Wear safety glasses and face protection</strong> whenever operating a strapping tool. Tensioned steel strap stores real energy.</li>
    <li><strong>Wear protective gloves</strong> when handling strapping. Cut strap edges are sharp.</li>
    <li><strong>Use genuine replacement parts from an authorized dealer.</strong> ZR tools are built for high-tensile conditions; other parts will affect performance and may cause injury.</li>
  </ul>
</div></section>

<section class="section-tight"><div class="wrap">
  {sec_head("FAQ", "Straight answers")}
  <div class="faq">{faq_html}</div>
  <p class="small mt-3">Something we didn't cover? Technical support: <a href="mailto:{SITE['email_support']}">{SITE['email_support']}</a> · General: <a href="mailto:{SITE['email']}">{SITE['email']}</a> · <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p>
</div></section>

{cta_band("Need a hand", "Real people who built the tools answer the support line.")}
"""
    faq_ld = jsonld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQS
        ],
    })
    write("/support/index.html", shell(
        path="/support/",
        title="Manuals, Trade Sheets & Support | Z.R. Tool Inc.",
        desc=("Operation manuals and trade sheets for every ZR strapping "
              "tool, plus safety guidance and answers on sealless joints, "
              "Z-Lock and parts compatibility."),
        body=body, extra_head=breadcrumb_ld(crumbs) + faq_ld,
        current="/support/"))


# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------

def build_about():
    crumbs = [("Home", "/"), ("About", "/about/")]
    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Company profile</p>
  <h1>Since 1978. Still building<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">Z.R. Tool Inc. has engineered package strapping equipment since 1978. Same specialty. Same shop in Newmarket, Ontario. Same standard: the work has to outlast the conditions it's built for.</p>
</div></section>

<section class="section-tight"><div class="wrap split" style="align-items:start">
  <div>
    <p>Z.R. Tool Inc. is a division of Z.R. Tool and Machinery Company, a privately held company founded in 1978. In the decades since, we've become one of the leading package strapping equipment manufacturers in the world — designing and manufacturing sealless combination tools, strapping machinery, strapping heads, and replacement parts and assemblies for all major brands.</p>
    <p class="mt-2">Our objective has never changed: design the products the industry actually demands. We bring real innovation to a field that has seen little change, and through continued research and technical development we've been awarded numerous patents for it — including the joint designs, the Z-Lock reverse locking system, and the world's only manual sealless combination tools for 1 1/4" steel strapping.</p>
    <p class="mt-2">We are experts who understand the interests of the strapping industry. Our consulting and custom design services help clients determine their requirements — and we work for long-term, responsible partnerships, not one-time orders.</p>
  </div>
  <div class="grid" style="gap:1rem">
    <div class="card"><span class="mono-tag">Nº 01 — Earned</span><h3 style="font-size:1.1rem">Trust, not talk</h3><p>Four decades of shipping to the same customers. The catalog earns respect the way the tools do — by holding up over time.</p></div>
    <div class="card"><span class="mono-tag">Nº 02 — Crafted</span><h3 style="font-size:1.1rem">Hand-finished. Machine-precise.</h3><p>CNC accuracy, toolmaker judgment. Everything under the ZR name is made in-house, to one standard.</p></div>
    <div class="card"><span class="mono-tag">Nº 03 — Steady</span><h3 style="font-size:1.1rem">Same tone in good years and bad</h3><p>Plainspoken, specific, built on decades of doing one thing right rather than many things noisily.</p></div>
  </div>
</div></section>

<section class="section-tight section-ink"><div class="wrap">
  {sec_head("The record", "What four decades looks like")}
  <div class="grid grid-4">
    <div class="cell"><p class="k" style="font-family:var(--f-display);font-weight:700;font-size:2rem;color:var(--paper)">1978</p><p class="v mono" style="color:var(--steel);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase">Founded · Ontario, Canada</p></div>
    <div class="cell"><p class="k" style="font-family:var(--f-display);font-weight:700;font-size:2rem;color:var(--paper)">Numerous</p><p class="v mono" style="color:var(--steel);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase">Patents awarded</p></div>
    <div class="cell"><p class="k" style="font-family:var(--f-display);font-weight:700;font-size:2rem;color:var(--paper)">11 Tools</p><p class="v mono" style="color:var(--steel);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase">Manual &amp; pneumatic line</p></div>
    <div class="cell"><p class="k" style="font-family:var(--f-display);font-weight:700;font-size:2rem;color:var(--paper)">Worldwide</p><p class="v mono" style="color:var(--steel);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase">Projects &amp; distribution</p></div>
  </div>
</div></section>

{cta_band("Work with the source", "Talk directly with the people who design and build the equipment.")}
"""
    write("/about/index.html", shell(
        path="/about/",
        title="About Z.R. Tool Inc. — Since 1978 | Newmarket, Ontario",
        desc=("Z.R. Tool Inc. has designed and manufactured steel strapping "
              "tools, machines and parts in Newmarket, Ontario since 1978. "
              "Patented sealless designs, built in-house."),
        body=body, extra_head=breadcrumb_ld(crumbs), current="/about/"))


# ---------------------------------------------------------------------------
# DISTRIBUTORS
# ---------------------------------------------------------------------------

def build_distributors():
    crumbs = [("Home", "/"), ("Distributors", "/distributors/")]
    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Distribution</p>
  <h1>Carry the line<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">ZR products are sold worldwide through packaging distributors who want equipment their customers keep — tools that outlast, parts that fit, and a manufacturer who answers the phone. If that's how you do business, let's talk.</p>
</div></section>

<section class="section-tight"><div class="wrap split" style="align-items:start">
  <div>
    <h2 style="font-size:1.5rem">Why distributors stay<span class="dot">.</span></h2>
    <ul class="featlist mt-2">
      <li><strong>Products nobody else has.</strong> The world's only manual sealless tools for 1 1/4" strap, and the only manual tools with reverse locking.</li>
      <li><strong>A parts business built in.</strong> We manufacture replacement parts for all major brands — every competitive tool in your territory is an opportunity.</li>
      <li><strong>Factory-direct support.</strong> Design, technical and service support from the people who build the equipment.</li>
      <li><strong>Long-term partnerships.</strong> We work for responsible, long-term relationships — the same way we've kept customers since 1978.</li>
    </ul>
  </div>
  <div>
    <form class="card" data-mailto="{SITE['email']}" data-subject="Distributor inquiry" novalidate>
      <h3 style="font-size:1.15rem">Distributor inquiry</h3>
      <div class="form-grid mt-2">
        <div class="field"><label for="d-name">Name <span class="req">*</span></label><input id="d-name" name="name" data-label="Name" required autocomplete="name"></div>
        <div class="field"><label for="d-pos">Position</label><input id="d-pos" name="position" data-label="Position" autocomplete="organization-title"></div>
        <div class="field full"><label for="d-co">Company name <span class="req">*</span></label><input id="d-co" name="company" data-label="Company" required autocomplete="organization"></div>
        <div class="field full"><label for="d-addr">Address <span class="req">*</span></label><input id="d-addr" name="address" data-label="Address" required autocomplete="street-address"></div>
        <div class="field"><label for="d-city">City <span class="req">*</span></label><input id="d-city" name="city" data-label="City" required autocomplete="address-level2"></div>
        <div class="field"><label for="d-state">State / Province <span class="req">*</span></label><input id="d-state" name="state" data-label="State/Province" required autocomplete="address-level1"></div>
        <div class="field"><label for="d-zip">ZIP / Postal code <span class="req">*</span></label><input id="d-zip" name="postal" data-label="Postal code" required autocomplete="postal-code"></div>
        <div class="field"><label for="d-country">Country <span class="req">*</span></label><input id="d-country" name="country" data-label="Country" required autocomplete="country-name"></div>
        <div class="field"><label for="d-email">Email <span class="req">*</span></label><input id="d-email" type="email" name="email" data-label="Email" required autocomplete="email"></div>
        <div class="field"><label for="d-phone">Telephone <span class="req">*</span></label><input id="d-phone" type="tel" name="phone" data-label="Telephone" required autocomplete="tel"></div>
        <div class="field full"><label for="d-url">Website</label><input id="d-url" type="url" name="website" data-label="Website" autocomplete="url" placeholder="https://"></div>
        <div class="field full"><label for="d-msg">Message</label><textarea id="d-msg" name="message" data-label="Message" placeholder="Territory, lines carried, and what you're looking for."></textarea></div>
      </div>
      <p class="form-status" role="status" aria-live="polite"></p>
      <div class="mt-2"><button class="btn btn-red" type="submit">Send inquiry</button></div>
      <p class="form-note mt-1">Submitting opens a pre-filled email to {SITE['email']} — nothing is stored on this site.</p>
    </form>
  </div>
</div></section>

{cta_band("Prefer to talk first", "Call and ask for distribution. We'll tell you plainly whether the territory works.")}
"""
    write("/distributors/index.html", shell(
        path="/distributors/",
        title="Become a Distributor | Z.R. Tool Inc.",
        desc=("Distribute ZR strapping tools, machines and parts. Exclusive "
              "products, factory-direct support and a replacement-parts "
              "business for all major brands. Inquire today."),
        body=body, extra_head=breadcrumb_ld(crumbs), current=None))


# ---------------------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------------------

def build_contact():
    crumbs = [("Home", "/"), ("Contact", "/contact/")]
    options = "".join(
        f'<option value="{p["model"]}">{p["model"]} — {p["kind"]}</option>'
        for p in PRODUCTS)
    maps_q = ("https://www.google.com/maps/search/?api=1&query="
              "1190+Stellar+Drive+Newmarket+ON+L3Y+7B7")
    body = f"""
{crumbs_html(crumbs)}
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Contact</p>
  <h1>Request a quote<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">Tell us what you strap and how much of it. A real person replies — usually the same business day.</p>
</div></section>

<section class="section-tight"><div class="wrap split" style="align-items:start">
  <div>
    <form class="card" data-mailto="{SITE['email']}" data-subject="Quote request" novalidate>
      <h3 style="font-size:1.15rem">Quote request</h3>
      <div class="form-grid mt-2">
        <div class="field"><label for="q-name">Name <span class="req">*</span></label><input id="q-name" name="name" data-label="Name" required autocomplete="name"></div>
        <div class="field"><label for="q-co">Company <span class="req">*</span></label><input id="q-co" name="company" data-label="Company" required autocomplete="organization"></div>
        <div class="field"><label for="q-email">Email <span class="req">*</span></label><input id="q-email" type="email" name="email" data-label="Email" required autocomplete="email"></div>
        <div class="field"><label for="q-phone">Telephone</label><input id="q-phone" type="tel" name="phone" data-label="Telephone" autocomplete="tel"></div>
        <div class="field full"><label for="q-product">Product of interest</label>
          <select id="q-product" name="product" data-label="Product">
            <option value="">— Select (optional) —</option>
            {options}
            <option value="Strapping machine">Strapping machine</option>
            <option value="Replacement parts">Replacement parts</option>
            <option value="Custom / other">Custom / other</option>
          </select></div>
        <div class="field full"><label for="q-msg">What are you strapping? <span class="req">*</span></label>
          <textarea id="q-msg" name="message" data-label="Details" required placeholder="Strap size and grade, package type, volume per day — whatever you know."></textarea></div>
      </div>
      <p class="form-status" role="status" aria-live="polite"></p>
      <div class="mt-2"><button class="btn btn-red" type="submit">Send request</button></div>
      <p class="form-note mt-1">Submitting opens a pre-filled email to {SITE['email']} — nothing is stored on this site.</p>
    </form>
  </div>
  <div>
    <div class="card">
      <span class="mono-tag">Head office &amp; manufacturing</span>
      <h3 style="font-size:1.2rem">Z.R. Tool Inc.</h3>
      <address style="font-style:normal;line-height:1.9">
        {SITE['address']['street']}<br>
        {SITE['address']['city']}, {SITE['address']['region']} {SITE['address']['postal']}<br>
        {SITE['address']['country_name']}
      </address>
      <p class="spec-line">Tel <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a><br>
      Sales <a href="mailto:{SITE['email']}">{SITE['email']}</a><br>
      Support <a href="mailto:{SITE['email_support']}">{SITE['email_support']}</a></p>
      <div class="mt-2"><a class="btn btn-sm" href="{maps_q}" rel="noopener" target="_blank">Get directions ↗</a></div>
    </div>
    <div class="callout mt-3"><p class="k">▸ Distributors</p>
      <p>Interested in carrying the line? Use the <a href="/distributors/">distributor inquiry form</a> instead — it asks the right questions.</p></div>
  </div>
</div></section>
"""
    contact_ld = jsonld({
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "url": D + "/contact/",
        "name": "Contact Z.R. Tool Inc.",
        "about": {"@id": D + "/#organization"},
    })
    write("/contact/index.html", shell(
        path="/contact/",
        title="Contact & Request a Quote | Z.R. Tool Inc.",
        desc=("Request a quote for ZR strapping tools, machines and parts. "
              "Z.R. Tool Inc., 1190 Stellar Drive, Newmarket ON. "
              "(905) 836-0590 · info@zrtool.com"),
        body=body, extra_head=breadcrumb_ld(crumbs) + contact_ld,
        current="/contact/"))


# ---------------------------------------------------------------------------
# 404
# ---------------------------------------------------------------------------

def build_404():
    body = f"""
<section class="section"><div class="wrap">
  <p class="eyebrow">Error 404</p>
  <h1>That page isn't on the rack<span class="dot">.</span></h1>
  <hr class="rulepair">
  <p class="lede mt-2">The address may have changed when we rebuilt the site. Everything still exists — try one of these.</p>
  <div class="cta-row mt-3" style="display:flex;gap:.9rem;flex-wrap:wrap">
    <a class="btn btn-red" href="/products/">Browse tools</a>
    <a class="btn" href="/support/">Support &amp; downloads</a>
    <a class="btn" href="/">Home</a>
  </div>
</div></section>
"""
    html = shell(path="/404.html",
                 title="Page not found | Z.R. Tool Inc.",
                 desc=("The page you were looking for has moved with the site "
                       "rebuild — use the links here to find it."),
                 body=body)
    html = html.replace('<meta name="robots" content="index, follow, '
                        'max-image-preview:large">',
                        '<meta name="robots" content="noindex">')
    write("/404.html", html)


# ---------------------------------------------------------------------------
# sitemap & robots
# ---------------------------------------------------------------------------

def build_sitemap():
    urls = (["/", "/products/", "/products/manual-sealless-tools/",
             "/products/pneumatic-sealless-tools/"]
            + [f"/products/{p['slug']}/" for p in PRODUCTS]
            + ["/machines/", "/parts/", "/services/", "/support/",
               "/about/", "/distributors/", "/contact/"])
    entries = "".join(
        f"<url><loc>{D}{u}</loc><lastmod>{SITE['build_date']}</lastmod>"
        f"<changefreq>{'weekly' if u=='/' else 'monthly'}</changefreq>"
        f"</url>" for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           + entries + "</urlset>\n")
    write("/sitemap.xml", xml)
    write("/robots.txt",
          "User-agent: *\nAllow: /\n\nSitemap: " + D + "/sitemap.xml\n")


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    build_home()
    build_products_index()
    build_category(
        "manual", "/products/manual-sealless-tools/",
        "Manual Sealless Combination Tools | Z.R. Tool Inc.",
        "Manual sealless tools",
        ("Eight manual sealless combination tools for steel strapping — "
         "MS, ZL, TF and TE series, 1/2\" to 1 1/4\". The finest available "
         "in the industry, made by ZR Tool."),
        ("We consider these the finest tools available in the industry — "
         "compare them with any others and the differences show up "
         "immediately. Patented joints, 30–50% less effort, the fewest parts "
         "in their class, and the world's only manual sealless tools with "
         "reverse locking and for 1 1/4\" strap."),
        ("Every manual tool runs high-tensile steel strapping up to 156,000 "
         "psi (1,100 N/mm²) and can run regular-duty strap for even longer "
         "life. Feedwheel, gripper, knife, punch or die all replace in "
         "minutes.")),
    build_category(
        "pneumatic", "/products/pneumatic-sealless-tools/",
        "Pneumatic Sealless Strapping Tools | Z.R. Tool Inc.",
        "Pneumatic sealless tools",
        ("PS25, PS31 and PS90 pneumatic sealless combination tools — "
         "two-button tension, seal and cut for steel strapping from 1/2\" "
         "to 1 1/4\", up to 2,900 lbs of tension."),
        ("Production speed without seals. Two buttons control the entire "
         "cycle — tensioning, sealing and cutting — on the same patented "
         "sealless joint the manual line is known for. Light for their "
         "class, easy to load, minutes to service."),
        ("PS-series tools run on standard shop air — 65 psi for the PS25 and "
         "PS31, 80 psi for the PS90 — and are designed for the rapid, "
         "reliable strapping of concrete, crates, lumber, metal and "
         "palletized products.")),
    for prod in PRODUCTS:
        build_product(prod)
    build_machines()
    build_parts()
    build_services()
    build_support()
    build_about()
    build_distributors()
    build_contact()
    build_404()
    build_sitemap()
    print("\nSite build complete.")
