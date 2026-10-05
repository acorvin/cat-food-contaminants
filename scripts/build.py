#!/usr/bin/env python3
"""Build docs/index.html, docs/study.html and docs/poster.html (the overview) from the templates in src/ and data/cat-food-contaminants.csv.

Run from the repository root:  python3 scripts/build.py
Edit the templates in src/, not the files in docs/, or the next build overwrites them.
"""
import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "cat-food-contaminants.csv"
PAGES = [
    (ROOT / "src" / "page.template.html", ROOT / "docs" / "index.html"),
    (ROOT / "src" / "study.template.html", ROOT / "docs" / "study.html"),
    (ROOT / "src" / "poster.template.html", ROOT / "docs" / "poster.html"),
]
SOURCE_CODES = {"R", "W", "P", "C", "N"}


def load():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["value"] = float(r["value"])
        if r["value"].is_integer():
            r["value"] = int(r["value"])
        codes = set(r["sources"].split(";"))
        if not codes <= SOURCE_CODES:
            sys.exit(f"Unknown source code in row {r['block']}/{r['item']}: {codes - SOURCE_CODES}")
    return rows


def check(rows):
    """Consistency checks on the figures themselves."""
    def pick(block, **kw):
        out = [r for r in rows if r["block"] == block and all(r[k] == v for k, v in kw.items())]
        if len(out) != 1:
            sys.exit(f"Expected one row for {block} {kw}, found {len(out)}")
        return out[0]["value"]

    # Format counts add up to the number of products.
    fmt = [r["value"] for r in rows if r["block"] == "sample" and r["group"] == "Format"]
    total = pick("sample", item="Products tested")
    assert sum(fmt) == total == 100, f"format counts {fmt} do not sum to {total}"

    # Detection counts are products out of 100.
    per_item = {}
    for r in rows:
        if r["block"] == "detection":
            per_item[r["item"]] = per_item.get(r["item"], 0) + r["value"]
    assert all(0 <= v <= total for v in per_item.values()), per_item

    # The poultry and fish shares, their gap and their ratio agree with each other.
    poultry = pick("standard", group="Poultry products")
    fish = pick("standard", group="Fish and seafood products")
    gap = pick("standard", group="Gap between poultry and fish and seafood")
    ratio = pick("standard", group="Poultry vs fish and seafood likelihood")
    assert round(poultry - fish, 1) == gap, (poultry, fish, gap)
    assert round(poultry / fish, 1) == ratio, (poultry, fish, ratio)

    # Acrylamide: 4 measurable plus 24 trace is 28 products.
    assert per_item["Acrylamide"] == 28, per_item["Acrylamide"]
    print("data checks passed:", len(rows), "rows")


def build(rows):
    marker = "/*__DATA__*/null"
    payload = json.dumps(rows, ensure_ascii=False)
    for template_path, out in PAGES:
        template = template_path.read_text(encoding="utf-8")
        if marker not in template:
            sys.exit(f"Data marker missing from {template_path.name}")
        html = template.replace(marker, payload)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("wrote", out.relative_to(ROOT), f"({len(html):,} bytes)")
    data_dir = PAGES[0][1].parent / "data"
    data_dir.mkdir(exist_ok=True)
    shutil.copyfile(CSV_PATH, data_dir / CSV_PATH.name)


if __name__ == "__main__":
    data = load()
    check(data)
    build(data)
