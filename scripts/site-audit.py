from pathlib import Path
import re

pages = [
    "index.html",
    "support.html",
    "privacy.html",
    "terms.html",
    "delete-account.html",
]

required_checks = {
    "viewport": 'name="viewport"',
    "theme-color": 'name="theme-color"',
    "favicon": 'rel="icon"',
    "description": 'name="description"',
    "robots": 'name="robots"',
    "Open Graph": 'property="og:title"',
    "Twitter": 'name="twitter:card"',
    "stylesheet": 'assets/css/styles.css',
    "main.js": 'assets/js/main.js',
}

errors = []
titles = {}

for filename in pages:
    path = Path(filename)

    if not path.exists():
        errors.append(f"{filename}: archivo no existe")
        continue

    html = path.read_text(encoding="utf-8")

    print(f"\nREVISANDO: {filename}")

    for label, needle in required_checks.items():
        if needle in html:
            print(f"  OK  {label}")
        else:
            print(f"  FALTA  {label}")
            errors.append(f"{filename}: falta {label}")

    match = re.search(r"<title>(.*?)</title>", html, re.S)

    if match:
        title = " ".join(match.group(1).split())
        titles[filename] = title
        print(f"  OK  title: {title}")
    else:
        errors.append(f"{filename}: falta <title>")
        print("  FALTA title")

    if "<main" not in html:
        errors.append(f"{filename}: falta <main>")

    if "<footer" not in html:
        errors.append(f"{filename}: falta <footer>")

    if "</html>" not in html:
        errors.append(f"{filename}: falta cierre </html>")

print("\n" + "=" * 60)

duplicate_titles = {}

for filename, title in titles.items():
    duplicate_titles.setdefault(title, []).append(filename)

for title, files in duplicate_titles.items():
    if len(files) > 1:
        errors.append(
            f"Título duplicado '{title}' en: {', '.join(files)}"
        )

if errors:
    print("AUDITORÍA CON OBSERVACIONES:\n")

    for error in errors:
        print("-", error)

else:
    print("AUDITORÍA OK")
    print("Las 5 páginas cumplen la estructura técnica básica.")
