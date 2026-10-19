"""Builds the delivery website: runs the analyses, writes dist/data.json and inlines it into the HTML template.

Usage (from submissions/rafael): .venv/bin/python solution/site/build_site.py
Outputs: solution/site/dist/index.html (standalone page) and dist/site.html (fragment for hosts that add their own <head>).
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from social_insights import data, site_export  # noqa: E402

TEMPLATE = HERE / "template.html"
DIST = HERE / "dist"
PLACEHOLDER = "/*__SITE_DATA__*/null"
DOCUMENT = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head>
<body>
{body}
</body>
</html>
"""


def render(payload_json: str, template: str) -> str:
    if PLACEHOLDER not in template:
        raise ValueError(f"template has no {PLACEHOLDER} placeholder")
    return template.replace(PLACEHOLDER, payload_json)


def main() -> None:
    start = time.time()
    payload_json = site_export.to_json(site_export.build_payload(data.load_posts()))
    fragment = render(payload_json, TEMPLATE.read_text(encoding="utf-8"))
    DIST.mkdir(exist_ok=True)
    (DIST / "data.json").write_text(payload_json, encoding="utf-8")
    (DIST / "site.html").write_text(fragment, encoding="utf-8")
    (DIST / "index.html").write_text(DOCUMENT.format(body=fragment), encoding="utf-8")
    print(f"Site gerado em {DIST / 'index.html'} ({len(fragment) / 1024:.0f} KB, {time.time() - start:.0f} s)")


if __name__ == "__main__":
    main()
