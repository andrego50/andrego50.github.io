#!/usr/bin/env python3
"""Reescribe el dominio del sitio en todos los archivos que lo llevan absoluto.

El scaffold nació apuntando a andres-perez-coronado.fastanalytics.co y esa URL
está incrustada en canonical, og:url, hreflang, JSON-LD, sitemap.xml, robots.txt
y llms.txt. Este script la cambia de golpe y, si el destino es un dominio de
github.io, borra además el archivo CNAME (que es justamente lo que forzaría a
GitHub Pages a seguir sirviendo en el dominio viejo).

    python3 tools/set_domain.py andresperezcoronado.github.io
    python3 tools/set_domain.py andresperezcoronado.com   # dominio propio

Es idempotente y se puede correr las veces que haga falta.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Cualquier host que el sitio haya usado antes. Se añaden aquí según se migre.
KNOWN_HOSTS = [
    "andres-perez-coronado.fastanalytics.co",
    "andresperezcoronado.github.io",
    "andrego50.github.io",
]

TARGETS = [
    "*.html",
    "blog/*.html",
    "sitemap.xml",
    "robots.txt",
    "llms.txt",
    "css/*.css",
    "tools/build_cv.py",
    "README.md",
]

# Hosts que sirven por HTTPS pero NO admiten CNAME propio: si el sitio va a uno
# de estos, el archivo CNAME debe desaparecer del repositorio.
GITHUB_IO_SUFFIX = ".github.io"


def collect_files() -> list[Path]:
    seen: dict[Path, None] = {}
    for pattern in TARGETS:
        for path in sorted(ROOT.glob(pattern)):
            if path.is_file():
                seen[path] = None
    return list(seen)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2

    new_host = argv[1].strip().rstrip("/")
    if new_host.startswith("http"):
        print("Pasa solo el host, sin esquema (p. ej. andresperezcoronado.github.io)")
        return 2

    old_hosts = [h for h in KNOWN_HOSTS if h != new_host]
    changed = 0

    for path in collect_files():
        text = original = path.read_text(encoding="utf-8")
        for old in old_hosts:
            text = text.replace(old, new_host)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"  actualizado  {path.relative_to(ROOT)}")

    cname = ROOT / "CNAME"
    if new_host.endswith(GITHUB_IO_SUFFIX):
        if cname.exists():
            cname.unlink()
            print("  eliminado    CNAME  (GitHub Pages servirá en el dominio por defecto)")
    else:
        cname.write_text(new_host + "\n", encoding="utf-8")
        print(f"  escrito      CNAME -> {new_host}")

    print(f"\n{changed} archivos actualizados. Dominio: https://{new_host}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
