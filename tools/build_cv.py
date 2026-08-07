#!/usr/bin/env python3
"""Genera el CV de Andrés Pérez Coronado en HTML y PDF, en español e inglés.

Toda la información vive en CV = {...} más abajo: para actualizar el CV se edita
esa estructura y se vuelve a correr el script. No hay que tocar el HTML.

    python3 tools/build_cv.py

Produce, en la raíz del repositorio:
    cv-andres-perez-coronado-es.html / .pdf
    cv-andres-perez-coronado-en.html / .pdf

El PDF se imprime con Chrome en modo headless, que ya viene instalado en macOS
y respeta @page y las reglas de salto de página. Si Chrome no está, el script
deja igual los HTML y avisa.
"""

from __future__ import annotations

import html
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "cv-andres-perez-coronado"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome",
    "chromium",
]

# --------------------------------------------------------------------------
# Contenido del CV
# --------------------------------------------------------------------------

CV = {
    "es": {
        "lang": "es",
        "title": "CV — Andrés Pérez Coronado",
        "name": "Andrés Pérez Coronado",
        "role": "PhD · Founder & AI/ML Architect, FastAnalytics S.A.S.",
        "contact": [
            ("Correo", "hola@fastanalytics.co", "mailto:hola@fastanalytics.co"),
            ("Sitio", "andrego50.github.io/AndresPerezCoronado", "https://andrego50.github.io/AndresPerezCoronado"),
            ("LinkedIn", "andres-perez-coronado", "https://www.linkedin.com/in/andres-perez-coronado-63792618/"),
            ("Ubicación", "Colombia", None),
        ],
        "profile_heading": "Perfil",
        "profile": (
            "Más de 20 años en analítica de seguridad ciudadana. Lideré equipos de más de 80 "
            "analistas en la Policía Nacional de Colombia, donde diseñé y desplegué los modelos "
            "matemáticos que sustentaron las principales estrategias de seguridad del país. "
            "Trabajo en la intersección poco frecuentada entre el modelamiento riguroso y la "
            "operación real: modelos que no se quedan en un informe, sino que cambian cómo se "
            "patrulla. Hoy dirijo FastAnalytics S.A.S., desde donde llevo inteligencia artificial "
            "espaciotemporal a gobiernos y empresas de la región."
        ),
        "sections": [
            {
                "heading": "Educación",
                "items": [
                    ("2025", "PhD en Ingeniería Matemática", "Universidad EAFIT",
                     "Modelamiento matemático aplicado a fenómenos espaciotemporales."),
                    ("", "MSc en Management", "IAE — Université Grenoble Alpes",
                     "Formación en gestión y estrategia, complementaria al perfil técnico."),
                    ("", "Humphrey Fellow", "University of Minnesota",
                     "Programa Fulbright-Humphrey para líderes con potencial de impacto en políticas públicas."),
                    ("", "Fulbright Scholar", "",
                     "Beca Fulbright para estudios de posgrado en Estados Unidos."),
                ],
            },
            {
                "heading": "Experiencia",
                "items": [
                    ("2024 — hoy", "Founder & AI/ML Architect", "FastAnalytics S.A.S.",
                     "Fundé la empresa para llevar modelos de IA espaciotemporal a gobiernos y "
                     "empresas de la región. Dirijo el diseño de los modelos y de los productos "
                     "que los ponen en manos de quien decide."),
                    ("20+ años", "Analítica de seguridad ciudadana", "Policía Nacional de Colombia",
                     "Lideré equipos de más de 80 analistas. Diseñé y desplegué los modelos "
                     "matemáticos que sustentaron las estrategias nacionales de seguridad, y "
                     "acompañé su implementación hasta el nivel operativo."),
                ],
            },
            {
                "heading": "Resultados destacados",
                "items": [
                    ("2024", "Modelo Multicrimen", "Desplegado a escala nacional",
                     "Modelo predictivo multidelito que cruza patrones espaciotemporales de varios "
                     "delitos a la vez. Resultados: −17,8 % hurto, −25,9 % hurto residencial, "
                     "−13 % masacres; 7 de 11 delitos reducidos en Bogotá; 28.243 denuncias de "
                     "hurto menos."),
                    ("2021", "Modelo Cuadrantes Outliers", "Desplegado a escala nacional",
                     "Modelo espaciotemporal de detección de valores atípicos para anticipar "
                     "concentraciones de homicidios por cuadrante. Sustentó la estrategia del "
                     "diciembre más seguro de Colombia en 19 años: −17 % homicidios a nivel "
                     "nacional, −33 % en Bogotá, 772 municipios sin homicidios."),
                ],
            },
            {
                "heading": "Publicaciones",
                "items": [
                    ("2024", "Analítica de datos para la seguridad ciudadana", "Editorial Logos",
                     "Coautor de todos los capítulos. Modelos matemáticos para la anticipación de "
                     "respuestas orientadas a la convivencia."),
                    ("2021", "Policía para el Desarrollo Humano", "Grupo Editorial Ibáñez",
                     "Marco para la seguridad ciudadana en Latinoamérica que mide el resultado en "
                     "desarrollo humano y no solo en conteo de delitos."),
                    ("", "Artículos académicos", "7+ publicaciones",
                     "Modelamiento espaciotemporal aplicado a dengue, hurto e inteligencia "
                     "colectiva. Listado completo en Academia.edu."),
                ],
            },
            {
                "heading": "Conferencias",
                "items": [
                    ("2026", "IACP Technology Conference", "Ponente",
                     "«Finding the Missing Links: Using AI to Map and Disrupt Transnational Crime "
                     "Networks»."),
                    ("2025", "Universidad del Rosario", "Sesión con concejales de Cundinamarca",
                     "Presentación y prueba en vivo de TavoDebate: 527 consultas, 73 enmiendas y "
                     "votación artículo por artículo."),
                ],
            },
            {
                "heading": "Productos diseñados",
                "items": [
                    ("", "GabyVigía", "En producción",
                     "Sistema de decisión predictiva bajo el ciclo Vigilar · Predecir · Decidir, "
                     "con 5 capas de inteligencia integradas."),
                    ("", "TavoDebate", "En producción",
                     "Plataforma de sesiones legislativas con 10 asesores de IA especializados "
                     "trabajando en paralelo."),
                    ("", "AlejoSeguro", "En producción",
                     "Bot de Telegram para recolectar percepciones georreferenciadas de seguridad "
                     "ciudadana en tiempo real."),
                    ("", "AlejoGeo", "En desarrollo",
                     "Plataforma de inteligencia espaciotemporal multimodal con bases de datos "
                     "vectoriales y chat sobre el entorno."),
                ],
            },
        ],
        "languages_heading": "Idiomas",
        "languages": "Español · Inglés · Francés",
        "footer": "Andrés Pérez Coronado · hola@fastanalytics.co",
    },
    "en": {
        "lang": "en",
        "title": "CV — Andrés Pérez Coronado",
        "name": "Andrés Pérez Coronado",
        "role": "PhD · Founder & AI/ML Architect, FastAnalytics S.A.S.",
        "contact": [
            ("Email", "hola@fastanalytics.co", "mailto:hola@fastanalytics.co"),
            ("Website", "andrego50.github.io/AndresPerezCoronado", "https://andrego50.github.io/AndresPerezCoronado"),
            ("LinkedIn", "andres-perez-coronado", "https://www.linkedin.com/in/andres-perez-coronado-63792618/"),
            ("Location", "Colombia", None),
        ],
        "profile_heading": "Profile",
        "profile": (
            "More than 20 years in citizen-security analytics. I led teams of over 80 analysts at "
            "the Colombian National Police, where I designed and deployed the mathematical models "
            "underpinning the country's main security strategies. I work at the rarely occupied "
            "intersection of rigorous modeling and real operations: models that do not stop at a "
            "report, but change how officers patrol. Today I run FastAnalytics S.A.S., bringing "
            "spatiotemporal artificial intelligence to governments and companies across the region."
        ),
        "sections": [
            {
                "heading": "Education",
                "items": [
                    ("2025", "PhD in Mathematical Engineering", "Universidad EAFIT",
                     "Mathematical modeling applied to spatiotemporal phenomena."),
                    ("", "MSc in Management", "IAE — Université Grenoble Alpes",
                     "Management and strategy training, complementing the technical profile."),
                    ("", "Humphrey Fellow", "University of Minnesota",
                     "Fulbright-Humphrey program for leaders with the potential to shape public policy."),
                    ("", "Fulbright Scholar", "",
                     "Fulbright scholarship for graduate studies in the United States."),
                ],
            },
            {
                "heading": "Experience",
                "items": [
                    ("2024 — present", "Founder & AI/ML Architect", "FastAnalytics S.A.S.",
                     "I founded the company to bring spatiotemporal AI models to governments and "
                     "companies across the region. I lead the design of both the models and the "
                     "products that put them in the hands of decision-makers."),
                    ("20+ years", "Citizen-security analytics", "Colombian National Police",
                     "I led teams of more than 80 analysts. I designed and deployed the "
                     "mathematical models behind national security strategies, and supported their "
                     "implementation down to the operational level."),
                ],
            },
            {
                "heading": "Selected results",
                "items": [
                    ("2024", "Multicrime model", "Deployed nationally",
                     "Multi-offense predictive model cross-referencing spatiotemporal patterns of "
                     "several crime types at once. Results: −17.8% theft, −25.9% residential "
                     "burglary, −13% massacres; 7 of 11 crime categories reduced in Bogotá; 28,243 "
                     "fewer theft reports."),
                    ("2021", "Outlier Quadrants model", "Deployed nationally",
                     "Spatiotemporal outlier-detection model anticipating homicide concentrations "
                     "by quadrant. It underpinned the strategy behind Colombia's safest December "
                     "in 19 years: −17% homicides nationally, −33% in Bogotá, 772 municipalities "
                     "with zero homicides."),
                ],
            },
            {
                "heading": "Publications",
                "items": [
                    ("2024", "Analítica de datos para la seguridad ciudadana", "Editorial Logos",
                     "Co-author of every chapter. Mathematical models for anticipating responses "
                     "oriented to civic coexistence."),
                    ("2021", "Policía para el Desarrollo Humano", "Grupo Editorial Ibáñez",
                     "A framework for citizen security in Latin America that measures results in "
                     "human development, not merely in crime counts."),
                    ("", "Academic papers", "7+ publications",
                     "Spatiotemporal modeling applied to dengue, theft, and collective "
                     "intelligence. Full listing on Academia.edu."),
                ],
            },
            {
                "heading": "Speaking",
                "items": [
                    ("2026", "IACP Technology Conference", "Speaker",
                     "“Finding the Missing Links: Using AI to Map and Disrupt Transnational "
                     "Crime Networks”."),
                    ("2025", "Universidad del Rosario", "Session with council members of Cundinamarca",
                     "Presentation and live test of TavoDebate: 527 queries, 73 amendments, and "
                     "article-by-article voting."),
                ],
            },
            {
                "heading": "Products designed",
                "items": [
                    ("", "GabyVigía", "In production",
                     "Predictive decision system built on the Watch · Predict · Decide cycle, with "
                     "5 integrated intelligence layers."),
                    ("", "TavoDebate", "In production",
                     "Legislative-session platform with 10 specialized AI advisors working in "
                     "parallel."),
                    ("", "AlejoSeguro", "In production",
                     "Telegram bot collecting georeferenced citizen-security perceptions in real "
                     "time."),
                    ("", "AlejoGeo", "In development",
                     "Multimodal spatiotemporal intelligence platform with vector databases and a "
                     "chat interface over your surroundings."),
                ],
            },
        ],
        "languages_heading": "Languages",
        "languages": "Spanish · English · French",
        "footer": "Andrés Pérez Coronado · hola@fastanalytics.co",
    },
}

# --------------------------------------------------------------------------
# Plantilla
# --------------------------------------------------------------------------

STYLE = """
@page { size: A4; margin: 14mm 15mm; }

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
  font-size: 9.6pt;
  line-height: 1.5;
  color: #1A1A2E;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

a { color: #006D6D; text-decoration: none; }

header { border-bottom: 2.5pt solid #006D6D; padding-bottom: 9pt; margin-bottom: 14pt; }

h1 { font-size: 21pt; font-weight: 800; letter-spacing: -0.02em; line-height: 1.1; }

.role { font-size: 10.5pt; font-weight: 600; color: #006D6D; margin-top: 3pt; }

.contact { margin-top: 8pt; font-size: 8.6pt; color: #4A4A6A; }
.contact span { margin-right: 14pt; white-space: nowrap; }
.contact b { color: #8888A0; font-weight: 600; }

section { margin-bottom: 13pt; }

h2 {
  font-size: 8.4pt;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #006D6D;
  padding-bottom: 3pt;
  margin-bottom: 8pt;
  border-bottom: 0.6pt solid #E5E7EB;
}

.profile { text-align: justify; color: #33334D; }

/* Cada entrada: año a la izquierda, contenido a la derecha. break-inside evita
   que una entrada quede partida entre dos páginas. */
.item {
  display: grid;
  grid-template-columns: 62pt 1fr;
  gap: 10pt;
  margin-bottom: 8pt;
  break-inside: avoid;
  page-break-inside: avoid;
}

.item:last-child { margin-bottom: 0; }

.item-when { font-size: 8.4pt; font-weight: 700; color: #006D6D; padding-top: 1pt; }

.item-title { font-size: 10pt; font-weight: 700; }

.item-where { font-size: 8.8pt; font-weight: 600; color: #8888A0; margin-bottom: 2pt; }

.item-desc { color: #4A4A6A; }

.langs { font-weight: 600; }

footer {
  margin-top: 14pt;
  padding-top: 7pt;
  border-top: 0.6pt solid #E5E7EB;
  font-size: 8pt;
  color: #8888A0;
  text-align: center;
}
"""

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>{style}</style>
</head>
<body>
<header>
  <h1>{name}</h1>
  <div class="role">{role}</div>
  <div class="contact">{contact}</div>
</header>

<section>
  <h2>{profile_heading}</h2>
  <p class="profile">{profile}</p>
</section>

{sections}

<section>
  <h2>{languages_heading}</h2>
  <p class="langs">{languages}</p>
</section>

<footer>{footer}</footer>
</body>
</html>
"""


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def render_contact(entries) -> str:
    parts = []
    for label, value, href in entries:
        shown = f'<a href="{href}">{esc(value)}</a>' if href else esc(value)
        parts.append(f"<span><b>{esc(label)}</b> {shown}</span>")
    return "".join(parts)


def render_sections(sections) -> str:
    out = []
    for section in sections:
        items = []
        for when, title, where, desc in section["items"]:
            where_html = f'<div class="item-where">{esc(where)}</div>' if where else ""
            items.append(
                '<div class="item">'
                f'<div class="item-when">{esc(when)}</div>'
                "<div>"
                f'<div class="item-title">{esc(title)}</div>'
                f"{where_html}"
                f'<div class="item-desc">{esc(desc)}</div>'
                "</div>"
                "</div>"
            )
        out.append(
            f'<section>\n  <h2>{esc(section["heading"])}</h2>\n  ' + "\n  ".join(items) + "\n</section>"
        )
    return "\n\n".join(out)


def build_html(data: dict) -> str:
    return PAGE.format(
        lang=data["lang"],
        title=esc(data["title"]),
        style=STYLE,
        name=esc(data["name"]),
        role=esc(data["role"]),
        contact=render_contact(data["contact"]),
        profile_heading=esc(data["profile_heading"]),
        profile=esc(data["profile"]),
        sections=render_sections(data["sections"]),
        languages_heading=esc(data["languages_heading"]),
        languages=esc(data["languages"]),
        footer=esc(data["footer"]),
    )


def find_chrome() -> str | None:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    return None


def to_pdf(chrome: str, html_path: Path, pdf_path: Path) -> None:
    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        check=True,
        capture_output=True,
    )


def main() -> int:
    chrome = find_chrome()
    if chrome is None:
        print("Chrome no encontrado: genero solo los HTML.", file=sys.stderr)

    for lang, data in CV.items():
        html_path = ROOT / f"{SLUG}-{lang}.html"
        html_path.write_text(build_html(data), encoding="utf-8")
        print(f"HTML  {html_path.relative_to(ROOT)}")

        if chrome:
            pdf_path = ROOT / f"{SLUG}-{lang}.pdf"
            to_pdf(chrome, html_path, pdf_path)
            size_kb = pdf_path.stat().st_size / 1024
            print(f"PDF   {pdf_path.relative_to(ROOT)}  ({size_kb:.0f} KB)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
