# -*- coding: utf-8 -*-
"""Z.R. Tool Inc. — site content data.

Every product, spec and category migrated from the original zrtool.com
catalog (verified July 2026), rewritten to the ZR Tool Brand Standard
voice: plainspoken, earned, warm, steady.
"""

SITE = {
    "name": "Z.R. Tool Inc.",
    "short": "ZR Tool",
    "domain": "https://www.zrtool.com",
    "tagline": "Quality Strapping · Since 1978",
    "phone_display": "(905) 836-0590",
    "phone_tel": "+19058360590",
    "email": "info@zrtool.com",
    "email_support": "support@zrtool.com",
    "address": {
        "street": "1190 Stellar Drive",
        "city": "Newmarket",
        "region": "ON",
        "postal": "L3Y 7B7",
        "country": "CA",
        "country_name": "Canada",
    },
    "founded": "1978",
    "build_date": "2026-07-10",
}

# ---------------------------------------------------------------------------
# Shared copy blocks
# ---------------------------------------------------------------------------

HT_NOTE = ("Designed for high-tensile steel strapping up to 156,000 psi "
           "(1,100 N/mm²). Runs regular-duty strap too — with durability to spare.")

FEATURES_MANUAL = [
    ("Patented sealless joint", "A joint system like no other. Better seal-joint "
     "efficiency with 30–50% less operator effort than comparable tools."),
    ("Fewest parts in its class", "Comparable tools carry roughly twice as many "
     "components. Fewer parts means easier operation, less maintenance, fewer repairs."),
    ("Minutes to service", "Feedwheel, gripper, knife, punch or die — each swaps "
     "out in a few minutes with basic hand tools."),
    ("All-steel construction", "Every part manufactured and treated for long "
     "service life under real shop conditions."),
    ("Built for North American strap", "Designed around North American-grade "
     "steel strapping. Performs even better on European-grade strap."),
    ("Proven against every major brand", "In identical application testing, "
     "outperforms and outlasts the other major tools in its category."),
]

FEATURES_PNEUMATIC = [
    ("Two-button operation", "Two buttons control the entire cycle — tensioning, "
     "sealing and cutting."),
    ("Patented sealless joint", "Much improved seal-joint efficiency compared "
     "with other tools in its category."),
    ("Easy strap access", "The sealing-mechanism assembly is designed so strap "
     "loads in without a fight."),
    ("Light for its class", "Lightweight and easily maneuverable compared with "
     "other pneumatic combination tools."),
    ("Fewest parts in its class", "Less maintenance and repair than tools "
     "carrying twice the component count."),
    ("Minutes to service", "Feedwheel, gripper, knife, punch or die replace in "
     "a few minutes."),
]

ZLOCK = ("Z-Lock reverse locking", "Our exclusive Z-Lock system protects the "
         "sealless connection against loosening or unlocking in either "
         "direction — built for the most demanding loads.")

APPLICATIONS = ("concrete products, crates, lumber, metal products and "
                "palletized loads — anything unitized with steel strapping")

# ---------------------------------------------------------------------------
# Tools — the complete line
#   widths tokens: 13, 16, 19, 32 (mm)  ·  power: manual | pneumatic
# ---------------------------------------------------------------------------

PRODUCTS = [
    # ------------------------- MANUAL -------------------------
    {
        "slug": "ms25", "model": "MS25",
        "name": "MS25 Manual Sealless Combination Tool",
        "category": "manual",
        "kind": "Manual sealless combination tool",
        "range_line": '1/2" × .015" (13 mm × 0.38 mm) to 3/4" × .025" (19 mm × 0.635 mm)',
        "widths": ["13", "16", "19"],
        "zlock": False, "stainless": False, "windlass": False, "hightension": False,
        "summary": "The workhorse. One tool that tensions, seals and cuts high-tensile steel strapping from 1/2\" to 3/4\" — with no metal seals to buy, stock or load.",
        "desc": [
            "The MS25 is where most operations start with ZR. It pulls the strap tight, punches its own interlocking sealless joint, and cuts the tail — one tool, one motion, no seals.",
            "The patented joint design delivers better seal-joint efficiency while asking 30–50% less effort from the operator than comparable tools. And because the MS25 carries the fewest parts in its class, there is simply less in it to maintain, adjust or replace.",
        ],
        "features": FEATURES_MANUAL,
        "variants": [
            ("MS25-1", '1/2" (13 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
            ("MS25-2", '5/8" (16 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
            ("MS25-3", '3/4" (19 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
        ],
        "physical": [
            ("Weight", "9.4 lbs (4.25 kg)"),
            ("Base length", '4.2" (105 mm)'),
            ("Base width", '2.4" (60 mm)'),
            ("Height", '4.2" (105 mm)'),
        ],
        "has_manual": True,
    },
    {
        "slug": "ms31", "model": "MS31",
        "name": "MS31 Manual Sealless Combination Tool",
        "category": "manual",
        "kind": "Manual sealless combination tool",
        "range_line": '3/4" × .025" (19 mm × 0.635 mm) to 3/4" × .031" (19 mm × 0.80 mm)',
        "widths": ["19"],
        "zlock": False, "stainless": False, "windlass": False, "hightension": False,
        "summary": "The MS25's heavier-gauge sibling. Same patented sealless joint, tuned for 3/4\" strap up to .031\" thick.",
        "desc": [
            "When the load calls for thicker 3/4\" strap, the MS31 picks up where the MS25 leaves off — handling gauges from .025\" through .031\" high-tensile without changing how your crew works.",
            "It shares the MS series DNA: a patented sealless joint with 30–50% less operator effort, the fewest parts in its category, and wear items that swap out in minutes.",
        ],
        "features": FEATURES_MANUAL,
        "variants": [
            ("MS31-1", '3/4" (19 mm)', '.025" – .031" (0.635 – 0.80 mm)'),
        ],
        "physical": [
            ("Weight", "9.8 lbs (4.4 kg)"),
            ("Base length", '4.2" (105 mm)'),
            ("Base width", '2.4" (60 mm)'),
            ("Height", '4.2" (105 mm)'),
        ],
        "has_manual": True,
    },
    {
        "slug": "zl25", "model": "ZL25",
        "name": "ZL25 Manual Sealless Combination Tool with Z-Lock",
        "category": "manual",
        "kind": "Manual sealless combination tool · Z-Lock",
        "range_line": '1/2" × .015" (13 mm × 0.38 mm) to 3/4" × .025" (19 mm × 0.635 mm)',
        "widths": ["13", "16", "19"],
        "zlock": True, "stainless": False, "windlass": False, "hightension": False,
        "summary": "Everything the MS25 does, plus our exclusive Z-Lock reverse locking system — the joint holds in either direction, even on demanding loads.",
        "desc": [
            "The ZL25 is the only manual tool of its kind with an easy-to-use reverse locking system. Our exclusive Z-Lock protects the sealless connection against loosening or unlocking in either direction — added insurance for loads that shift, settle or ride rough.",
            "Underneath the lock is the same proven platform: a patented sealless joint, 30–50% less effort, the fewest parts in its category, and service in minutes.",
        ],
        "features": [ZLOCK] + FEATURES_MANUAL,
        "variants": [
            ("ZL25-1", '1/2" (13 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
            ("ZL25-2", '5/8" (16 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
            ("ZL25-3", '3/4" (19 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
        ],
        "physical": [
            ("Weight", "10.6 lbs (4.8 kg)"),
            ("Base length", '4.2" (105 mm)'),
            ("Base width", '2.4" (60 mm)'),
            ("Height", '4.2" (105 mm)'),
        ],
        "has_manual": True,
    },
    {
        "slug": "zl31", "model": "ZL31",
        "name": "ZL31 Manual Sealless Combination Tool with Z-Lock",
        "category": "manual",
        "kind": "Manual sealless combination tool · Z-Lock",
        "range_line": '3/4" × .025" (19 mm × 0.635 mm) to 3/4" × .031" (19 mm × 0.80 mm)',
        "widths": ["19"],
        "zlock": True, "stainless": False, "windlass": False, "hightension": False,
        "summary": "Z-Lock security for heavier 3/4\" strap. The reverse locking joint that will not walk loose — up to .031\" high-tensile.",
        "desc": [
            "The ZL31 brings Z-Lock reverse locking to heavier 3/4\" applications. The joint resists loosening in either direction, so what you strap stays strapped — through handling, transport and everything between.",
            "It runs .025\" to .031\" high-tensile steel strapping on the same low-effort, low-maintenance platform as the rest of the ZL line.",
        ],
        "features": [ZLOCK] + FEATURES_MANUAL,
        "variants": [
            ("ZL31-1", '3/4" (19 mm)', '.025" – .031" (0.635 – 0.80 mm)'),
        ],
        "physical": [
            ("Weight", "11.0 lbs (5.0 kg)"),
            ("Base length", '4.2" (105 mm)'),
            ("Base width", '2.4" (60 mm)'),
            ("Height", '4.2" (105 mm)'),
        ],
        "has_manual": True,
    },
    {
        "slug": "zl90", "model": "ZL90",
        "name": "ZL90 Manual Sealless Combination Tool — 1 1/4\"",
        "category": "manual",
        "kind": "Manual sealless combination tool · Z-Lock · 1 1/4\"",
        "range_line": '1 1/4" × .025" (32 mm × 0.635 mm) to 1 1/4" × .031" (32 mm × 0.80 mm)',
        "widths": ["32"],
        "zlock": True, "stainless": False, "windlass": False, "hightension": False,
        "world_only": "The world's only manual sealless combination tool for 1 1/4\" (32 mm) steel strapping.",
        "summary": "The world's only manual sealless combination tool for 1 1/4\" (32 mm) steel strapping — with Z-Lock reverse locking as standard.",
        "desc": [
            "For decades, sealless joints on 1 1/4\" strap meant powered equipment. The ZL90 changed that: it remains the only manual sealless combination tool available anywhere for 32 mm steel strapping. If you strap heavy loads away from air and power, this is the tool that makes it possible.",
            "Z-Lock reverse locking comes standard, protecting the joint in either direction. The patented design keeps effort minimal for a tool in this class, and wear parts replace in minutes.",
        ],
        "features": [ZLOCK] + FEATURES_MANUAL,
        "variants": [
            ("ZL90-1", '1 1/4" (32 mm)', '.025" – .031" (0.635 – 0.80 mm)'),
        ],
        "physical": [
            ("Weight", "13.4 lbs (6.0 kg)"),
            ("Base length", '4.9" (125 mm)'),
            ("Base width", '2.8" (70 mm)'),
            ("Height", '4.4" (110 mm)'),
        ],
        "has_manual": True,
    },
    {
        "slug": "tf25", "model": "TF25",
        "name": "TF25 High-Tension Sealless Tool — Steel & Stainless",
        "category": "manual",
        "kind": "High-tension sealless combination tool · Z-Lock · Stainless-capable",
        "range_line": 'Steel: 1/2" × .015" to 3/4" × .025" · Stainless: 1/2" × .015" to 3/4" × .032"',
        "widths": ["13", "16", "19"],
        "zlock": True, "stainless": True, "windlass": False, "hightension": True,
        "world_only": "The only manual combination tool built specifically for high-tension requirements.",
        "summary": "Built for high-tension work and awkward loads — small, round or irregular packages — in both high-tensile and stainless steel strapping.",
        "desc": [
            "The TF25 is the only manual combination tool designed specifically for high-tension requirements. Where standard tools run out of pull, the TF25 keeps going — on flat loads, and on the small, round and irregular packages other combination tools struggle to reach.",
            "It handles high-tensile steel strapping from 1/2\" to 3/4\", and stainless steel strapping up to 3/4\" × .032\" — a rare capability in a manual tool. Z-Lock reverse locking is standard, and the patented joint takes 40–60% less effort than tools in a similar category.",
        ],
        "features": [
            ("High-tension by design", "Purpose-built for high-tension applications, "
             "including small, round and irregular packages."),
            ("Stainless-capable", 'Runs stainless steel strapping from 1/2" × .015" '
             '(13 mm × 0.38 mm) up to 3/4" × .032" (19 mm × 0.82 mm).'),
            ZLOCK,
            ("40–60% less effort", "The patented joint design cuts operator effort "
             "dramatically versus tools in a similar category."),
        ] + FEATURES_MANUAL[1:5],
        "variants": [
            ("TF25-1", '1/2" (13 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
            ("TF25-2", '5/8" (16 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
            ("TF25-3", '3/4" (19 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
        ],
        "variant_note": 'Stainless steel strapping: .015" – .032" (0.38 – 0.82 mm) across widths.',
        "physical": [
            ("Weight", "11.0 lbs (5.0 kg)"),
            ("Base length", '3.0" (75 mm)'),
            ("Base width", '2.2" (55 mm)'),
            ("Height", '4.2" (105 mm)'),
        ],
        "has_manual": False,
    },
    {
        "slug": "te31", "model": "TE31",
        "name": "TE31 Windlass-Tension Sealless Combination Tool",
        "category": "manual",
        "kind": "Drum / windlass sealless combination tool · Z-Lock",
        "range_line": '3/4" × .025" (19 mm × 0.635 mm) to 3/4" × .031" (19 mm × 0.80 mm)',
        "widths": ["19"],
        "zlock": True, "stainless": False, "windlass": True, "hightension": True,
        "world_only": "The only combination tool with a drum / windlass tensioning system.",
        "summary": "Drum / windlass tensioning for heavy-duty pull on 3/4\" strap — the only combination tool of its kind, with Z-Lock standard.",
        "desc": [
            "The TE31 is the only combination tool available with a drum / windlass tensioning system. The windlass winds strap onto a drum for serious, controlled tension — the kind heavy-duty applications and small, round or irregular packages demand.",
            "It runs 3/4\" high-tensile strap from .025\" to .031\", locks every joint with Z-Lock, and takes 40–60% less effort than tools in a similar category.",
        ],
        "features": [
            ("Drum / windlass tensioning", "Winds strap onto a drum for heavy-duty, "
             "controlled tension — ideal for compressible and irregular loads."),
            ZLOCK,
            ("40–60% less effort", "The patented joint design cuts operator effort "
             "dramatically versus tools in a similar category."),
        ] + FEATURES_MANUAL[1:5],
        "variants": [
            ("TE31-1", '3/4" (19 mm)', '.025" – .031" (0.635 – 0.80 mm)'),
        ],
        "physical": [
            ("Weight", "10.8 lbs (4.9 kg)"),
            ("Base length", '3.5" (90 mm)'),
            ("Base width", '2.2" (55 mm)'),
            ("Height", '4.2" (105 mm)'),
        ],
        "has_manual": False,
    },
    {
        "slug": "te90", "model": "TE90",
        "name": "TE90 Windlass-Tension Sealless Tool — 1 1/4\"",
        "category": "manual",
        "kind": "Drum / windlass sealless combination tool · Z-Lock · 1 1/4\"",
        "range_line": '1 1/4" × .025" (32 mm × 0.635 mm) to 1 1/4" × .031" (32 mm × 0.80 mm)',
        "widths": ["32"],
        "zlock": True, "stainless": False, "windlass": True, "hightension": True,
        "world_only": "The only combination tool for 1 1/4\" strap with drum / windlass tensioning.",
        "summary": "The heaviest pull in the manual line: drum / windlass tensioning on 1 1/4\" strap, with Z-Lock reverse locking standard.",
        "desc": [
            "The TE90 pairs the widest strap in the manual line — 1 1/4\" (32 mm) — with a drum / windlass tensioning system built for heavy-duty pull. It is the only combination tool of its kind, anywhere.",
            "Like every ZL and TE tool, it ships with Z-Lock reverse locking, holds joints in either direction, and keeps effort minimal for a tool in this class. Small, round and irregular packages are exactly what it was designed around.",
        ],
        "features": [
            ("Drum / windlass tensioning", "Winds strap onto a drum for heavy-duty, "
             "controlled tension on the largest loads."),
            ("Only one of its kind", 'The only combination tool for 1 1/4" (32 mm) '
             "steel strapping with windlass tensioning."),
            ZLOCK,
        ] + FEATURES_MANUAL[1:5],
        "variants": [
            ("TE90-1", '1 1/4" (32 mm)', '.025" – .031" (0.635 – 0.80 mm)'),
        ],
        "physical": [
            ("Weight", "13.3 lbs (6.0 kg)"),
            ("Base length", '4.2" (105 mm)'),
            ("Base width", '2.6" (65 mm)'),
            ("Height", '4.4" (110 mm)'),
        ],
        "has_manual": False,
    },
    # ------------------------- PNEUMATIC -------------------------
    {
        "slug": "ps25", "model": "PS25",
        "name": "PS25 Pneumatic Sealless Combination Tool",
        "category": "pneumatic",
        "kind": "Pneumatic sealless combination tool",
        "range_line": '1/2" × .015" (13 mm × 0.38 mm) to 3/4" × .025" (19 mm × 0.635 mm)',
        "widths": ["13", "16", "19"],
        "zlock": False, "stainless": False, "windlass": False, "hightension": False,
        "summary": "Air-powered speed for production strapping. Two buttons run the whole cycle — tension, seal, cut — up to 1,800 lbs of pull.",
        "desc": [
            "When volume matters, the PS25 turns strapping into a two-button job: one to tension, one to seal and cut. Rapid, repeatable, reliable — cycle after cycle.",
            "It pulls up to 1,800 lbs (8,000 N) of tension on 65 psi shop air, stays light and maneuverable for its class, and forms the same patented sealless joint the manual line is known for.",
        ],
        "features": FEATURES_PNEUMATIC,
        "variants": [
            ("PS25-1", '1/2" (13 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
            ("PS25-2", '5/8" (16 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
            ("PS25-3", '3/4" (19 mm)', '.015" – .025" (0.38 – 0.635 mm)'),
        ],
        "physical": [
            ("Weight", "25.0 lbs (11.3 kg)"),
            ("Base length", '4.5" (115 mm)'),
            ("Base width", '3.0" (75 mm)'),
            ("Height", '9.8" (250 mm)'),
        ],
        "pneumo": [
            ("Max tension", "1,800 lbs (8,000 N)"),
            ("Working air pressure", "65 psi (4.5 bar)"),
        ],
        "has_manual": False,
    },
    {
        "slug": "ps31", "model": "PS31",
        "name": "PS31 Pneumatic Sealless Combination Tool",
        "category": "pneumatic",
        "kind": "Pneumatic sealless combination tool",
        "range_line": '3/4" × .025" (19 mm × 0.635 mm) to 3/4" × .031" (19 mm × 0.80 mm)',
        "widths": ["19"],
        "zlock": False, "stainless": False, "windlass": False, "hightension": False,
        "summary": "Heavier-gauge pneumatic strapping on 3/4\" strap — 2,100 lbs of tension from the same two-button cycle.",
        "desc": [
            "The PS31 takes the two-button pneumatic cycle up a gauge: 3/4\" high-tensile strap from .025\" through .031\", with up to 2,100 lbs (9,500 N) of tension on standard 65 psi shop air.",
            "Fewest parts in its class, minutes to service, and the patented ZR sealless joint on every cycle.",
        ],
        "features": FEATURES_PNEUMATIC,
        "variants": [
            ("PS31-1", '3/4" (19 mm)', '.025" – .031" (0.635 – 0.80 mm)'),
        ],
        "physical": [
            ("Weight", "26.2 lbs (11.9 kg)"),
            ("Base length", '4.5" (115 mm)'),
            ("Base width", '3.0" (75 mm)'),
            ("Height", '9.8" (250 mm)'),
        ],
        "pneumo": [
            ("Max tension", "2,100 lbs (9,500 N)"),
            ("Working air pressure", "65 psi (4.5 bar)"),
        ],
        "has_manual": False,
    },
    {
        "slug": "ps90", "model": "PS90",
        "name": "PS90 Pneumatic Sealless Combination Tool — 1 1/4\"",
        "category": "pneumatic",
        "kind": "Pneumatic sealless combination tool · 1 1/4\"",
        "range_line": '1 1/4" × .025" (32 mm × 0.635 mm) to 1 1/4" × .031" (32 mm × 0.80 mm)',
        "widths": ["32"],
        "zlock": False, "stainless": False, "windlass": False, "hightension": False,
        "summary": "The big pull: 2,900 lbs of tension on 1 1/4\" strap. Two buttons, one sealless joint, built for the heaviest packages.",
        "desc": [
            "The PS90 is the top of the pneumatic line — 1 1/4\" (32 mm) high-tensile strap, up to 2,900 lbs (13,000 N) of tension at 80 psi, and the same two-button simplicity as its smaller siblings.",
            "For steel, lumber, concrete and the heaviest palletized loads, it delivers production-rate strapping with the fewest parts in its class and service measured in minutes, not hours.",
        ],
        "features": FEATURES_PNEUMATIC,
        "variants": [
            ("PS90-1", '1 1/4" (32 mm)', '.025" – .031" (0.635 – 0.80 mm)'),
        ],
        "physical": [
            ("Weight", "30.5 lbs (13.8 kg)"),
            ("Base length", '5.3" (135 mm)'),
            ("Base width", '3.5" (90 mm)'),
            ("Height", '10.3" (260 mm)'),
        ],
        "pneumo": [
            ("Max tension", "2,900 lbs (13,000 N)"),
            ("Working air pressure", "80 psi (5.5 bar)"),
        ],
        "has_manual": False,
    },
]

# ---------------------------------------------------------------------------
# Strapping machines — categories as manufactured
# ---------------------------------------------------------------------------

MACHINES_INTRO = [
    "Rugged, reliable, proven. ZR strapping machines have become an industry "
    "benchmark for dependability, availability and value.",
    "We manufacture a full line of steel strapping machines for sealless and "
    "seal-type applications, in hydraulic or pneumatic versions — all designed "
    "for high-tensile and regular-duty steel strapping. Conversion kits move "
    "existing equipment between seal-type and sealless operation.",
]

MACHINES = {
    "sealless": {
        "title": "Sealless Machines",
        "blurb": "No seals to buy, stock or load. The machine forms the joint "
                 "directly in the strap — the ZR specialty since the beginning.",
        "items": [
            {"id": "sealless-58", "label": '5/8" Sealless',
             "spec": '5/8" × .015" – .031" H.T. (16 mm × 0.38 – 0.80 mm)'},
            {"id": "sealless-34", "label": '3/4" Sealless',
             "spec": '3/4" × .015" – .031" H.T. (19 mm × 0.38 – 0.80 mm)'},
            {"id": "sealless-114", "label": '1 1/4" Sealless',
             "spec": '1 1/4" × .025" – .044" H.T. (32 mm × 0.635 – 1.12 mm)'},
            {"id": "sealless-114-lock", "label": '1 1/4" Sealless · Lock',
             "spec": '1 1/4" × .025" – .044" H.T. (32 mm × 0.635 – 1.12 mm)',
             "note": "Equipped with reverse locking system."},
        ],
    },
    "sealtype": {
        "title": "Seal-Type Machines",
        "blurb": "Conventional seal-joint machinery, built to the same standard "
                 "— for operations and specifications that call for seals.",
        "items": [
            {"id": "sealtype-58", "label": '5/8" Seal-Type',
             "spec": '5/8" × .015" – .031" H.T. (16 mm × 0.38 – 0.80 mm)'},
            {"id": "sealtype-34", "label": '3/4" Seal-Type',
             "spec": '3/4" × .015" – .031" H.T. (19 mm × 0.38 – 0.80 mm)'},
            {"id": "sealtype-114", "label": '1 1/4" Seal-Type',
             "spec": '1 1/4" × .025" – .035" H.T. (32 mm × 0.635 – 0.90 mm)'},
        ],
    },
}

# ---------------------------------------------------------------------------
# Replacement parts
# ---------------------------------------------------------------------------

PARTS = [
    {"id": "feedwheels", "title": "Feedwheels",
     "desc": "Precision-ground feedwheels for ZR tools and all major brands of "
             "strapping tools and machinery. The part that pulls the tension — "
             "machined and treated to grip strap cycle after cycle."},
    {"id": "grippers", "title": "Grippers",
     "desc": "Grippers that hold strap firm under full tension. Manufactured "
             "from durable tool steel and treated for high-tensile service."},
    {"id": "knives", "title": "Knives",
     "desc": "Cut-off knives that stay sharp through high-tensile strap. "
             "Available for ZR equipment and all major competitive brands."},
    {"id": "miscellaneous", "title": "Punches, Dies & More",
     "desc": "Punches, dies, strap stops, shafts, springs, cams and complete "
             "assemblies — the full range of wear and service parts, plus "
             "anything we can reverse-engineer from your sample."},
]

# ---------------------------------------------------------------------------
# FAQ (support page — used for FAQPage structured data too)
# ---------------------------------------------------------------------------

FAQS = [
    ("What is a sealless joint?",
     "A sealless combination tool tensions the strap, then punches a set of "
     "interlocking keys directly into the two strap layers — no separate metal "
     "seal required. You stop buying, stocking and loading seals, and you "
     "remove an interruption from every cycle. ZR's patented joint designs "
     "deliver high joint efficiency with 30–50% less operator effort than "
     "comparable tools (40–60% on our TF and TE series)."),
    ("What is the Z-Lock reverse locking system?",
     "Z-Lock is ZR's exclusive reverse locking feature, standard on ZL, TF and "
     "TE series tools and available on 1 1/4\" sealless machines. It protects "
     "the sealless connection against loosening or unlocking in either "
     "direction — extra security for loads that shift or settle in transit."),
    ("Which tool fits my strap size?",
     "Match the tool series to your strap width and gauge: MS25 / ZL25 / TF25 / "
     "PS25 cover 1/2\" to 3/4\" strap up to .025\"; MS31 / ZL31 / TE31 / PS31 "
     "cover 3/4\" strap from .025\" to .031\"; and ZL90 / TE90 / PS90 cover "
     "1 1/4\" strap from .025\" to .031\". Every product page lists exact "
     "specifications, or use the strap-size filter on the products page."),
    ("Do you really make the only manual sealless tools for 1 1/4\" strapping?",
     "Yes. The ZL90 and TE90 are the only manual sealless combination tools "
     "available anywhere for 1 1/4\" (32 mm) steel strapping. If you strap "
     "heavy loads where air or power is not practical, they are the tools "
     "that make it possible."),
    ("Can I strap stainless steel?",
     "The TF25 is designed for it — it runs stainless steel strapping from "
     "1/2\" × .015\" up to 3/4\" × .032\", in addition to standard "
     "high-tensile steel strap."),
    ("Do your replacement parts fit other brands of equipment?",
     "Yes. We manufacture replacement parts and assemblies for all major "
     "brands of strapping machinery, equipment and tools — feedwheels, "
     "grippers, knives, punches, dies and more. We can also manufacture a "
     "part from your sample, or improve a part to suit your application."),
    ("What strapping grades do ZR tools handle?",
     "Every tool in the line is designed for high-tensile steel strapping up "
     "to 156,000 psi (1,100 N/mm²), and all may be used with regular-duty "
     "strapping — where the same construction simply delivers longer life."),
    ("How do I get an operation manual or trade sheet?",
     "Trade sheets and operation manuals are collected on the Support & "
     "Downloads page. Documents still being prepared for the new site can be "
     "requested by email and we will send the PDF directly — usually the "
     "same business day."),
]

INDUSTRIES = [
    ("Steel & metals", "Coils, sheet, tube, bar and fabricated product."),
    ("Lumber & building products", "Dimensional lumber, panels, engineered wood."),
    ("Concrete products", "Block, brick, pavers and precast units."),
    ("Crating & export packing", "Crates, cases and mixed heavy freight."),
    ("Palletized goods", "Unitized loads across general manufacturing."),
    ("Distribution & logistics", "Load securement for rail, road and sea."),
]
