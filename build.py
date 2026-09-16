"""Ensambla las páginas del sitio (beta) a partir de src/pages/*.html y src/partials/.

Uso:  python build.py
Cada página en src/pages empieza con una línea de metadatos:
  <!-- title: ... | desc: ... | nav: casos -->
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
PARTIALS = SRC / "partials"
PAGES = SRC / "pages"

head = (PARTIALS / "head.html").read_text(encoding="utf-8")
mapa = (PARTIALS / "mapa.svg").read_text(encoding="utf-8") if (PARTIALS / "mapa.svg").exists() else ""
header = (PARTIALS / "header.html").read_text(encoding="utf-8")
footer = (PARTIALS / "footer.html").read_text(encoding="utf-8")

META_RE = re.compile(r"^\s*<!--\s*(.*?)\s*-->", re.S)


def parse_meta(text):
    m = META_RE.match(text)
    if not m:
        raise SystemExit("Falta la línea de metadatos")
    meta = {}
    for part in m.group(1).split("|"):
        k, _, v = part.partition(":")
        meta[k.strip()] = v.strip()
    return meta, text[m.end():].lstrip("\n")


def mark_current(html, nav):
    if not nav:
        return html
    # Enlaces: aria-current="page". Ítem con menú: clase is-current.
    html = html.replace(f'data-nav="{nav}"', f'data-nav="{nav}" aria-current="page"', 1)
    html = html.replace(
        f'class="nav__item nav__item--menu" data-nav="{nav}"',
        f'class="nav__item nav__item--menu is-current" data-nav="{nav}"',
    )
    return html


for page in sorted(PAGES.glob("*.html")):
    meta, body = parse_meta(page.read_text(encoding="utf-8"))
    out = (
        head.replace("{{TITLE}}", meta["title"]).replace("{{DESC}}", meta.get("desc", ""))
        + mark_current(header, meta.get("nav"))
        + body.replace("{{MAPA}}", mapa)
        + footer
    )
    (ROOT / page.name).write_text(out, encoding="utf-8")
    print("ok ", page.name)
