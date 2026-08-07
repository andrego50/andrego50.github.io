# andres-perez-coronado

Sitio personal de Andrés Pérez Coronado — trayectoria, portafolio de proyectos y blog. Se publica en `andrego50.github.io/AndresPerezCoronado`.

Repositorio independiente del sitio de FastAnalytics S.A.S. (`web_site_fastanalytics`), pero forkeado del mismo stack: HTML/CSS/JS plano, sin build, desplegado en GitHub Pages.

## Estructura

- `index.html`, `trayectoria.html`, `portafolio.html` — páginas principales.
- `blog/` — `index.html` (lista de posts), `_template.html` (plantilla para nuevos posts, no enlazada), y un archivo `.html` por post.
- `css/styles.css` — copia verbatim del sistema visual de FastAnalytics. `css/site.css` — componentes propios de este sitio (timeline, blog, etc.).
- `js/main.js` — fork de FastAnalytics con soporte para títulos por página (`window.PAGE_TITLES`).

## Publicar un nuevo post de blog

1. Duplica `blog/_template.html` con un nombre de archivo nuevo (el slug del post).
2. Reemplaza todos los `__TOKEN__` por el contenido real.
3. Añade una tarjeta en `blog/index.html` enlazando al nuevo archivo.
4. Añade una entrada `<url>` en `sitemap.xml`.

## Deploy

1. `git init` y commit (ya hecho en la preparación inicial).
2. Crear el repo en GitHub y hacer push.
3. Activar GitHub Pages (rama `main`, carpeta raíz) — detecta el `CNAME` automáticamente.
4. En el DNS de `fastanalytics.co`, crear un registro `CNAME`: host `andres-perez-coronado` → `<usuario-github>.github.io.`
5. Esperar propagación y activar "Enforce HTTPS" en la configuración de Pages.
