#!/usr/bin/env python3
"""Inserta Publicaciones y Speaker en los menús de navegación y pie de página.

El scaffold traía 5 enlaces (Inicio, Trayectoria, Portafolio, Blog, Contacto) en
el nav y 4 en el footer, repetidos literalmente en cada página. Este script añade
las dos páginas nuevas justo después de su vecino lógico —Publicaciones tras
Trayectoria, Speaker tras Portafolio— respetando el prefijo relativo de cada
archivo (los del blog necesitan «../»).

Es idempotente: si el enlace ya está, no lo duplica.

    python3 tools/add_nav_links.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# archivo -> prefijo relativo hacia la raíz del sitio
PAGES = {
    "index.html": "",
    "trayectoria.html": "",
    "portafolio.html": "",
    "blog/index.html": "../",
    "blog/bienvenida.html": "../",
    "blog/_template.html": "../",
}

# (ancla tras la que se inserta, archivo nuevo, textos es/en/fr)
INSERTIONS = [
    ("trayectoria.html", "publicaciones.html", "Publicaciones", "Publications", "Publications"),
    ("portafolio.html", "speaker.html", "Speaker", "Speaking", "Conférences"),
]


def build_li(prefix: str, href: str, es: str, en: str, fr: str, indent: str) -> str:
    return (
        f'{indent}<li><a href="{prefix}{href}" '
        f'data-es="{es}" data-en="{en}" data-fr="{fr}">{es}</a></li>'
    )


def process(path: Path, prefix: str) -> int:
    text = path.read_text(encoding="utf-8")
    added = 0

    for anchor, href, es, en, fr in INSERTIONS:
        if f'href="{prefix}{href}"' in text:
            continue  # ya está

        # Cada <li> del ancla: puede aparecer en el nav y en el footer.
        pattern = re.compile(
            r'^([ \t]*)<li><a href="' + re.escape(prefix + anchor) + r'"[^>]*>.*?</a></li>$',
            re.MULTILINE,
        )

        def repl(m: re.Match) -> str:
            nonlocal added
            added += 1
            return m.group(0) + "\n" + build_li(prefix, href, es, en, fr, m.group(1))

        text = pattern.sub(repl, text)

    if added:
        path.write_text(text, encoding="utf-8")
    return added


def main() -> int:
    total = 0
    for rel, prefix in PAGES.items():
        path = ROOT / rel
        if not path.exists():
            print(f"  falta {rel}")
            continue
        n = process(path, prefix)
        total += n
        print(f"  {rel}: {n} enlaces añadidos")
    print(f"total: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
