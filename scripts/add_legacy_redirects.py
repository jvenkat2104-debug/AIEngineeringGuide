"""Keep old project-site reading URLs working after migration to the account root."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dist" / "site"
ORIGIN = "https://jvenkat2104-debug.github.io/"

pages = list(SITE.rglob("*.html"))
count = 0
for page in pages:
    relative = page.relative_to(SITE)
    if relative.parts[0] == "AIEngineeringGuide" or relative.name == "404.html":
        continue
    path = relative.as_posix()
    if path.endswith("index.html"):
        path = path[:-len("index.html")]
    url = ORIGIN + path
    alias = SITE / "AIEngineeringGuide" / relative
    assert alias.resolve().is_relative_to(SITE.resolve())
    alias.parent.mkdir(parents=True, exist_ok=True)
    alias.write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex">'
        f'<link rel="canonical" href="{escape(url, quote=True)}">'
        f'<meta http-equiv="refresh" content="0;url={escape(url, quote=True)}">'
        '<title>This guide has moved</title>'
        f'<script>location.replace({json.dumps(url)} + location.search + location.hash);</script>'
        '<body><p>This page has moved. '
        f'<a href="{escape(url, quote=True)}">Continue to the engineering guide</a>.</p></body></html>',
        encoding="utf-8",
    )
    count += 1
print(f"Created {count} compatibility pages for former /AIEngineeringGuide/ URLs")
