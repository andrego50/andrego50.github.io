#!/usr/bin/env python3
"""Reescribe la URL base del sitio en todos los archivos que la llevan absoluta.

La URL base está incrustada en canonical, og:url, hreflang, JSON-LD,
sitemap.xml, robots.txt y llms.txt. Este script la cambia de golpe.

Acepta base con o sin ruta, porque GitHub Pages sirve distinto según cómo se
llame el repo:

    # sitio de usuario (repo llamado igual que la cuenta) -> raíz
    python3 tools/set_domain.py andresperezcoronado.github.io

    # sitio de proyecto (cualquier otro nombre de repo) -> subruta
    python3 tools/set_domain.py andrego50.github.io/AndresPerezCoronado

    # dominio propio
    python3 tools/set_domain.py andresperezcoronado.com

Los enlaces relativos del sitio (href="trayectoria.html") funcionan igual en
ambos casos, así que solo hay que tocar los absolutos.

Del archivo CNAME se encarga solo: lo borra si el destino es github.io (donde
no aplica) y lo escribe si es un dominio propio.

Es idempotente: correrlo dos veces con la misma base no duplica la ruta.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Cualquier base que el sitio haya usado. Se añaden aquí según se migre.
KNOWN_BASES = [
    "andres-perez-coronado.fastanalytics.co",
    "andrego50.github.io/AndresPerezCoronado",
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

SENTINEL = "\x00BASE\x00"


def collect_files() -> list[Path]:
    seen: dict[Path, None] = {}
    for pattern in TARGETS:
        for path in sorted(ROOT.glob(pattern)):
            if path.is_file():
                seen[path] = None
    return list(seen)


def rewrite(text: str, new_base: str) -> str:
    """Sustituye cualquier base conocida por la nueva.

    La base nueva se aparca en un centinela antes de sustituir, porque si no
    una base vieja que sea prefijo de la nueva (andrego50.github.io dentro de
    andrego50.github.io/AndresPerezCoronado) volvería a expandirse en cada
    pasada y la ruta se duplicaría.
    """
    text = text.replace(new_base, SENTINEL)

    # De más larga a más corta: así "host/ruta" gana sobre "host" a secas.
    for old in sorted(KNOWN_BASES, key=len, reverse=True):
        if old == new_base:
            continue
        text = text.replace(old, SENTINEL)

    return text.replace(SENTINEL, new_base)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2

    new_base = argv[1].strip().strip("/")
    if new_base.startswith("http"):
        print("Pasa solo la base, sin esquema (p. ej. andrego50.github.io/AndresPerezCoronado)")
        return 2

    host = new_base.split("/")[0]
    changed = 0

    for path in collect_files():
        original = path.read_text(encoding="utf-8")
        text = rewrite(original, new_base)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"  actualizado  {path.relative_to(ROOT)}")

    cname = ROOT / "CNAME"
    if host.endswith(".github.io"):
        if cname.exists():
            cname.unlink()
            print("  eliminado    CNAME  (no aplica en github.io)")
    else:
        cname.write_text(host + "\n", encoding="utf-8")
        print(f"  escrito      CNAME -> {host}")

    print(f"\n{changed} archivos actualizados. Sitio: https://{new_base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
