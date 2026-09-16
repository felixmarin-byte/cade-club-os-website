from pathlib import Path
from datetime import date
import os
import sys

base_url = os.getenv("BASE_URL", "").rstrip("/")

if not base_url.startswith(("https://", "http://")):
    print("ERROR: Define BASE_URL con la URL pública del sitio.")
    print("Ejemplo:")
    print("BASE_URL=https://ejemplo.com python3 scripts/generate-sitemap.py")
    sys.exit(1)

pages = [
    ("index.html", "1.0"),
    ("support.html", "0.7"),
    ("privacy.html", "0.5"),
    ("terms.html", "0.5"),
    ("delete-account.html", "0.5"),
]

today = date.today().isoformat()

urls = []

for filename, priority in pages:
    if not Path(filename).exists():
        print(f"ADVERTENCIA: no existe {filename}")
        continue

    if filename == "index.html":
        loc = f"{base_url}/"
    else:
        loc = f"{base_url}/{filename}"

    urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>""")

xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""

Path("sitemap.xml").write_text(xml, encoding="utf-8")

print(f"OK: sitemap.xml generado con {len(urls)} páginas")
print(f"URL base: {base_url}")
