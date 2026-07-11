# -*- coding: utf-8 -*-
"""QA suite for the generated site."""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(__file__), "..", "public")
issues = []


class Check(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.imgs_no_alt = []
        self.h1 = 0
        self.title = ""
        self.desc = ""
        self.in_title = False
        self.scripts_ld = []
        self.in_ld = False
        self.ld_buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img" and not a.get("alt"):
            self.imgs_no_alt.append(a.get("src", "?"))
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_ld = True
            self.ld_buf = ""
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append(a.get("href"))
        if tag == "script" and a.get("src"):
            self.links.append(a["src"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_ld:
            self.in_ld = False
            self.scripts_ld.append(self.ld_buf)

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_ld:
            self.ld_buf += data


pages = []
for dirpath, _, files in os.walk(ROOT):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(dirpath, f))

all_titles = {}
for page in sorted(pages):
    rel = "/" + os.path.relpath(page, ROOT).replace(os.sep, "/")
    with open(page, encoding="utf-8") as fh:
        html = fh.read()
    c = Check()
    c.feed(html)

    # h1 count
    if c.h1 != 1:
        issues.append(f"{rel}: {c.h1} <h1> tags")
    # title/desc lengths
    t = c.title.strip()
    if not (10 < len(t) <= 65):
        issues.append(f"{rel}: title length {len(t)} — {t!r}")
    if t in all_titles:
        issues.append(f"{rel}: duplicate title with {all_titles[t]}")
    all_titles[t] = rel
    if not (50 <= len(c.desc) <= 165):
        issues.append(f"{rel}: meta description length {len(c.desc)}")
    # imgs
    for src in c.imgs_no_alt:
        issues.append(f"{rel}: img missing alt — {src}")
    # JSON-LD validity
    for ld in c.scripts_ld:
        try:
            json.loads(ld)
        except Exception as e:
            issues.append(f"{rel}: invalid JSON-LD — {e}")
    # internal links resolve
    for href in c.links:
        if not href:
            continue
        if href.startswith(("http", "mailto:", "tel:", "#", "javascript")):
            continue
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        fs = os.path.join(ROOT, target.lstrip("/"))
        ok = (os.path.isfile(fs)
              or os.path.isfile(os.path.join(fs, "index.html")))
        # downloads are intentional placeholders (data-doc handled in JS)
        if not ok and not target.startswith("/downloads/"):
            issues.append(f"{rel}: broken internal link {href}")

# catalog completeness vs original site
required = ["MS25", "MS31", "ZL25", "ZL31", "ZL90", "TF25", "TE31", "TE90",
            "PS25", "PS31", "PS90"]
with open(os.path.join(ROOT, "products", "index.html"), encoding="utf-8") as fh:
    cat = fh.read()
for m in required:
    if m not in cat:
        issues.append(f"catalog missing model {m}")
    if not os.path.isfile(os.path.join(ROOT, "products", m.lower(),
                                       "index.html")):
        issues.append(f"missing product page for {m}")

machine_ids = ["sealless-58", "sealless-34", "sealless-114",
               "sealless-114-lock", "sealtype-58", "sealtype-34",
               "sealtype-114"]
with open(os.path.join(ROOT, "machines", "index.html"), encoding="utf-8") as fh:
    mach = fh.read()
for mid in machine_ids:
    if f'id="{mid}"' not in mach:
        issues.append(f"machines page missing anchor {mid}")

parts_ids = ["feedwheels", "grippers", "knives", "miscellaneous"]
with open(os.path.join(ROOT, "parts", "index.html"), encoding="utf-8") as fh:
    parts = fh.read()
for pid in parts_ids:
    if f'id="{pid}"' not in parts:
        issues.append(f"parts page missing anchor {pid}")

print(f"pages checked: {len(pages)}")
if issues:
    print(f"ISSUES ({len(issues)}):")
    for i in issues:
        print(" -", i)
    sys.exit(1)
print("all checks passed ✓")
