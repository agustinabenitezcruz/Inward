# INWARD — Home (paleta secundaria)

Rediseño de inwardpro.com. Esta es la **home en francés** con la **paleta secundaria
del brand book** (verde agua, amarillo, lila) con el **violeta oscuro de la
primaria** como acento, sobre fondo blanco. Es la combinación que eligió la
clienta.

Abrir `index.html` directamente en el navegador ya funciona: no hay build, no hay
dependencias, no hay npm. Es HTML, CSS y un JS de 3 kB.

**Una salvedad:** abriendo con `file://`, los enlaces de idioma que apuntan a una
carpeta (`../`, `en/`) caen en el listado de directorios en vez de servir el
`index.html`. No es un error del código, es cómo funciona `file://`. Para probar
la navegación entre idiomas, levantá un servidor:

```bash
python3 -m http.server 8000     # y abrí http://localhost:8000
```

---

## Estructura

```
DESIGN.md                  Sistema de diseño en texto plano, para agentes de IA
.claude/skills/            Skills de diseño instaladas en el proyecto
index.html                 Home FR. Es la FUENTE: se edita a mano
en/index.html              Home EN. GENERADA, no editar a mano
es/index.html              Home ES. GENERADA, no editar a mano
build.py                   Genera en/ y es/ desde index.html + el CSV
tools/extract_strings.py   Vuelca los textos de index.html al CSV
content/strings.csv        Los 179 textos, columnas key / fr / en / es
favicon.svg                Isotipo blanco sobre cuadrado de acento de marca
favicon.ico                16 / 32 / 48 px, para navegadores viejos
apple-touch-icon.png       180x180, iOS
site.webmanifest           Nombre, colores e iconos de la app
assets/
  css/styles.css           Todo el diseño. Los tokens están arriba del todo, en :root
  js/main.js               Reveal on scroll, filas B2C, rail de secciones, panel de notas
  img/*.webp               Fotos del shooting, optimizadas
  img/*.jpg                Las mismas en JPG (respaldo y para previsualizar en Finder)
  img/hero-video-poster.webp  Primer fotograma del video, poster del hero
  img/logo/                Logo listo para web (ver abajo)
  img/clients/             Los 7 logos de clientes, normalizados
  video/hero.webm|.mp4     Video de fondo del hero
  Videos/                  Material bruto del rodaje. No se publica
  SVG/                     Los 20 SVG originales del brand book. No tocar: son la fuente
```

## Skills y DESIGN.md

En el proyecto hay dos cosas distintas, aunque las dos vengan de GitHub.

**`.claude/skills/`** son skills de verdad, instaladas con
`npx skills add Leonxlnx/taste-skill`. Son instrucciones que Claude Code carga
solo cuando la tarea las pide:

| Skill | Para qué |
|---|---|
| `design-taste-frontend` | Anti-slop para landings. Dials de variance/motion/density, patrones prohibidos, checklist de pre-vuelo |
| `redesign-existing-projects` | Protocolo de rediseño: auditar antes de tocar, qué se preserva, qué se jubila |
| `brandkit` | Trabajo con manuales de marca |

Están instaladas a nivel proyecto, así que sólo aplican acá. Para actualizarlas:
`npx skills update`.

**`DESIGN.md`** no es una skill. Es el formato de
[awesome-design-md](https://github.com/voltagent/awesome-design-md): un
documento en texto plano con el sistema de diseño, que cualquier agente lee
para generar UI consistente. El de la raíz describe el sistema de INWARD:
tokens, escalas, componentes, reglas de movimiento y una lista de qué hacer y
qué no.

Sirve para que la próxima sesión, con Claude Code o con lo que sea, no vuelva a
inventar un segundo acento ni a meter tres tarjetas iguales en fila. Si cambiás
el sistema en `styles.css`, actualizá `DESIGN.md`.

## Los tres idiomas

Son **tres páginas estáticas** con su propia URL, no un switch en JavaScript.
Cada una tiene su `canonical`, su `hreflang` y su meta description, que es lo
que hace falta para que Google indexe las tres. El selector del header son
enlaces reales, no botones.

El francés es la fuente y se edita a mano. El inglés y el español se generan:

```bash
python3 tools/extract_strings.py   # index.html -> content/strings.csv
# la clienta completa las columnas en y es del CSV
python3 build.py                   # CSV -> en/index.html y es/index.html
```

`content/strings.csv` se abre en Excel o Numbers. Tiene cuatro columnas:
`key`, `fr`, `en`, `es`. Sólo hay que llenar las dos últimas. `extract_strings.py`
se puede volver a correr cada vez que cambie el francés: conserva lo que ya
esté traducido y agrega sólo las claves nuevas.

**Mientras falte texto**, `build.py` deja el francés en su lugar, marca la página
con `noindex, follow` y muestra un aviso fijo abajo a la izquierda. Así nadie
confunde una página a medio traducir con una terminada, y Google no la indexa
en ese estado. Cuando el CSV esté completo, el aviso y el `noindex` desaparecen
solos.

`build.py` también se encarga de: reescribir las rutas de los recursos a
`../assets/`, poner el `lang` correcto en el `<html>`, ajustar `canonical`,
`og:url`, `og:locale` y la URL del JSON-LD, y marcar el idioma activo en el
selector. Sólo usa la librería estándar de Python, no hay que instalar nada.

Es una consultora de inmigración: el vocabulario legal en inglés y español lo
tiene que escribir o revisar la clienta. Por eso el CSV va vacío en vez de con
una traducción automática.

## Logo

Los originales del brand book están en `assets/SVG/`. De ahí saqué dos versiones
recortadas para web, en `assets/img/logo/`:

| Archivo | Qué es |
|---|---|
| `inward-logo-horizontal.svg` | Isologotipo horizontal, viewBox ajustado al contenido |
| `inward-isotipo.svg` | Solo el isotipo, monocromo con `currentColor` |
| `favicon-192.png` / `favicon-512.png` | Para el manifest |

En `index.html` el logo va **inline**, como sprite `<symbol>` justo después de
`<body>`, y se usa con `<use href="#lg-inward">` y `<use href="#lg-iso">`.
Así se dibuja una sola vez, no hace requests extra y hereda el color del CSS.

**Es bicolor por tokens:** el isotipo toma `--accent` y el mot-symbole toma `--text`.
Si cambiamos de paleta, el logo se recolorea solo. No hay ningún hex del logo
escrito a mano en el CSS.

El isotipo también reemplazó los hexágonos que yo había dibujado a ojo antes de
tener los archivos: aparece como marca de agua en el bento, como viñeta en la
lista de valores y en el rail de secciones. 13 usos, todos vía `<use>`.

## Video del hero

El hero es una banda a todo el ancho con video de fondo. El material bruto es
`assets/Videos/VIDEO HOME.mov` (39 MB, 1920x1080, 45 s).

Recorté **del segundo 0,3 al 20,0**, casi 20 segundos. Son dos actos que ya
venían montados en el bruto: el Palais Garnier con las fundadoras caminando
(hasta el segundo 8,7) y la llegada a la oficina, con las dos sentándose a
trabajar frente al ventanal. El corte entre ambos ya existe en el material,
no lo agregué yo.

De ahí salieron dos archivos, ambos sin audio y a 1440 px de ancho:

| Archivo | Códec | Peso |
|---|---|---|
| `assets/video/hero.webm` | VP9, crf 36 | 2,6 MB |
| `assets/video/hero.mp4` | H.264, crf 29, faststart | 2,1 MB |

Bajé de 1600 a 1440 px de ancho para que el video, al pasar de 9 a 20 segundos,
casi no engordara. Detrás del velo y a esa escala no se nota.

El webm lo usan Chrome y Firefox, el mp4 es para Safari. El `poster` es
`assets/img/hero-video-poster.webp`, así que si el video tarda o falla se ve
un fotograma en su lugar en vez de un rectángulo negro.

Para regenerarlos con otro tramo, cambiá `-ss` y `-t`:

```bash
ffmpeg -ss 0.3 -t 8.7 -i "assets/Videos/VIDEO HOME.mov" -an \
  -c:v libvpx-vp9 -crf 34 -b:v 0 -row-mt 1 -cpu-used 4 -pix_fmt yuv420p \
  -vf "scale=1600:-2" -g 120 assets/video/hero.webm -y

ffmpeg -ss 0.3 -t 8.7 -i "assets/Videos/VIDEO HOME.mov" -an \
  -c:v libx264 -crf 27 -preset slow -profile:v high -pix_fmt yuv420p \
  -vf "scale=1600:-2" -g 120 -movflags +faststart assets/video/hero.mp4 -y
```

**El loop corta.** El plano final (las dos sentadas trabajando) no enlaza con
el primero (la calle), así que cada 20 s hay un salto. A 20 segundos molesta
mucho menos que a 9, pero sigue estando. Si quieren eliminarlo del todo hace
falta un plano rodado pensado para loopear.

Después del segundo 23 el bruto se queda en el mismo plano fijo de las dos
tecleando, así que alargarlo más no aporta.

El video se pausa solo si el sistema pide `prefers-reduced-motion: reduce`;
en ese caso queda el poster.

**La barra de navegación es transparente sobre el video** y se vuelve blanca
al scrollear. El cambio lo dispara un `IntersectionObserver` sobre una
sentinela, no un listener de scroll. Sobre el video la barra redefine sus
propios tokens (`--text`, `--accent`) en blanco, así que el logo y los links
se adaptan solos. También se vuelve blanca al abrir un mega menú, porque si no
el panel quedaría con texto blanco sobre blanco.

## Logos de clientes

Los 7 originales están en `assets/Logos clientes/`. Los procesados, en
`assets/img/clients/`. A cada uno le quité el fondo blanco, lo recorté al
contenido y lo escalé a una altura calculada según su proporción: un
mot-symbole ancho va a 26 px y una marca compacta a 41 px, si no la fila
queda descompensada. Cada `<img>` lleva su propio `width`/`height`; los
archivos están a 2x para retina. Los 7 juntos pesan 60 kB.

`mouve.` venía como texto blanco sobre un cuadro verde. Le invertí la
luminancia para tener el logo en verde oscuro sobre transparente, así no
queda un rectángulo entre logos sin fondo.

En la página van en gris al reposo y a color al pasar el cursor: siete marcas
muy distintas entre sí se leen como una sola fila.

## Cambiar colores

Todo el color de la página vive en el bloque `:root` de `assets/css/styles.css`.
Son 29 variables. Ningún componente tiene un color escrito a mano, así que cambiar
la paleta entera es cambiar ese bloque y nada más.

| Variable | Valor | Rol |
|---|---|---|
| `--ground` | `#ffffff` | Fondo de la página |
| `--surface` / `--surface-2` | `#f4f3ff` / `#e7e5ff` | Bandas y bloques suaves |
| `--text` | `#101010` | NEGRO del brand book |
| `--accent` | `#202045` | VIOLETA OSCURO. Acento único: títulos de acento, links, labels |
| `--fill` / `--fill-ink` | `#202045` / `#ffffff` | Relleno de los CTA |
| `--tint-1` | `#55ffd2` | VERDE AGUA. Celda tintada del bento |
| `--tint-2` | `#ebff76` | AMARILLO. Segunda celda tintada |
| `--deep` | `#202045` | Bandas plenas (confianza y contacto) |

La versión con la **paleta primaria** (violeta oscuro, violeta claro, vert digital)
usa exactamente el mismo CSS con otro bloque `:root`. Si la clienta la elige,
se sustituyen esas variables.

## Sistema de formas

Rectángulos con esquinas redondeadas. Una sola escala, en `:root`:

| Variable | Valor | Dónde |
|---|---|---|
| `--r` | 18 px | Media, celdas del bento, tarjetas. Clase utilitaria `.rounded` |
| `--r-band` | 28 px | Esquinas superiores de la banda que se desliza sobre el hero |
| `--r-sm` | 10 px | Campos de formulario |
| — | pill | Botones y el selector de idioma |

No hay ningún otro radio en la página. Si agregás un componente, usá `.rounded`
o una de esas variables; no escribas un `border-radius` suelto.

## Tipografías

Ahora mismo carga **Outfit** y **Jost** desde Google Fonts como sustitutos de
**Figerona** (titulares) y **Walkway** (textos).

Para producción:

1. Conseguir los `.woff2` reales y ponerlos en `assets/fonts/`
2. Declarar `@font-face` con `font-display: swap` al principio de `styles.css`
3. Cambiar `--font-display` y `--font-body` en `:root`
4. Borrar el `<link>` de Google Fonts del `index.html` (obligatorio en Francia:
   cargar Google Fonts desde el CDN transfiere IPs a EE. UU. y la CNIL lo ha
   sancionado; con las fuentes auto-hospedadas el problema desaparece)

**Ojo con la licencia:** Figerona (Drizy Studio) es *free for personal use*.
Para un sitio comercial hay que comprar licencia o cambiar la tipografía de titulares.

## Animaciones

Todas están motivadas y ninguna usa un listener de scroll:

- Hero: las líneas del H1 suben con reveal por clip, escalonadas 90 ms
- Hero sticky: las bandas siguientes se deslizan por encima con el chaflán abierto.
  La salida y el paneo de la foto van con `animation-timeline: scroll()`,
  fuera del hilo principal
- Mega menú: panel a ancho completo, 200 ms ease-out, ítems escalonados 40 ms
- Filas B2C: se abren y cambian la foto de vista previa con crossfade + blur
- Botones: `scale(0.97)` en `:active`, 160 ms
- Rail de hexágonos: sección activa vía IntersectionObserver

Todo cae a estático con `prefers-reduced-motion: reduce`.

## Antes de publicar en O2Switch

- [ ] Auto-hospedar las tipografías y quitar el `<link>` de Google Fonts
- [ ] Reemplazar el dominio en `canonical`, `hreflang` y `og:url` si no es inwardpro.com
      (en `index.html` y en la constante `DOMAIN` de `build.py`)
- [ ] Completar `content/strings.csv` y correr `build.py` para las versiones EN y ES
- [ ] Producir la imagen de compartir `assets/img/og-inward.jpg` (1200x630)
- [ ] Revisar en pantalla real que el favicon se lea a 16 px en la pestaña
- [ ] Completar el JSON-LD con dirección, teléfono y valoración **reales**
- [ ] `sitemap.xml` y `robots.txt`
- [ ] Páginas legales: mentions légales, politique de confidentialité (RGPD), CGV
- [ ] Activar compresión gzip/brotli y cache de estáticos en el `.htaccess` de cPanel
- [ ] Quitar las clases `.todo` cuando llegue el contenido definitivo

## Avis Google (sección "Avis Google")

La sección **no trae ninguna opinión escrita a mano**. Los datos salen de
`api/avis.php`, que consulta la Places API de Google **desde el servidor**.

### Por qué un PHP y no un widget

- La clave de la API **no puede ir en el navegador**: quien mire el código
  fuente la usa y la factura queda a nombre de la clienta. Con el PHP la clave
  vive en el servidor y el navegador sólo habla con `inwardpro.com`.
- Los widgets de terceros (Elfsight, Trustindex y compañía) cargan un script
  externo que perfila al visitante. En Francia ese es exactamente el problema
  que ya nos obliga a auto-hospedar las tipografías. Acá **no se carga nada de
  terceros**, salvo la foto de perfil de cada autor, que Google exige mostrar.

### Puesta en marcha

1. Conseguir el **place ID** de la ficha Google Business de INWARD:
   https://developers.google.com/maps/documentation/places/web-service/place-id
2. En Google Cloud Console, crear un proyecto, activar **Places API (New)** y
   generar una clave. Restringirla **por IP del servidor**, no por dominio: la
   llamada la hace O2Switch, no el navegador.
3. `cp api/config.example.php api/config.php` y completar `place_id` y
   `api_key`. **`config.php` no se versiona** y el `.htaccess` de `api/` ya lo
   bloquea para accesos web.
4. Verificar en `https://inwardpro.com/api/avis.php`: tiene que devolver JSON.
   `{"error":"not_configured"}` significa que falta el paso 3.

### Límites que conviene saber antes de prometer nada

- **La API devuelve como máximo 5 opiniones.** No hay forma de traer más por la
  vía oficial. Se muestran las 5 más recientes.
- **Google prohíbe cachear el contenido de las opiniones** más allá de lo
  necesario para rendimiento. Por eso el TTL es de 1 hora y no de una semana.
  El place ID sí se puede guardar indefinidamente, es la única excepción
  explícita de la política.
- **Atribución obligatoria**: nombre y foto del autor, fecha relativa, enlace a
  la opinión original y mención a Google. Todo eso ya está en el maquetado; no
  se puede quitar sin violar los términos.
- **La ley francesa exige mostrar la fecha de la visita.** Hoy se muestra la
  fecha relativa que devuelve la API. Si la clienta publica avis también por
  otra vía, conviene revisarlo con quien lleve el tema legal.
- La API se factura por consulta. Con TTL de 1 hora son unas 720 consultas al
  mes, que entra de sobra en el crédito gratuito mensual de Google.

## Contenido que falta (marcado en la página)

El panel "Notes de maquette" ya no existe: se quitó del HTML, del CSS y del JS.
Lo que sigue faltando queda marcado en la página con subrayado punteado
(clase `.todo`), y la lista viva es esta:

1. Licencia y archivos de Figerona / Walkway
2. Nota real de Google / Trustpilot (la de 4,9 / 5 del brief sin verificar)
3. Texto de "Qui sommes-nous": relato, año de creación, tamaño del equipo
4. Coordenadas públicas: dos teléfonos y un email. El brand book dice
   `inwardimmigration.com` y un teléfono incompleto; el sitio es `inwardpro.com`
5. Tercer artículo del blog
6. Las seis respuestas de la FAQ (la primera está en lorem ipsum)
7. Place ID de la ficha Google Business y clave de Places API, para los avis

Resueltos: video del hero y logos de clientes.

Nada de esto está inventado en el código.

## Próximas páginas

La home usa las secciones que pide el brief. Faltan por hacer las landings de
servicio (5 B2B + 4 B2C), Qui sommes-nous, el blog, contacto y las legales.

Cuando esas páginas existan, hay que extender `build.py` para que recorra una
lista de páginas en vez de sólo `index.html`. La lógica ya está toda escrita,
es cambiar una constante por un bucle.


## Páginas y flujo de trabajo

Las páginas están en `tools/pages.py`. Hoy: la home (`index.html`) y la landing
de empresas (`entreprises/index.html`). Cada una en francés es la fuente; el
inglés y el español se generan.

Los bloques compartidos (logo, cabecera, contacto, pie) viven **sólo en
index.html**, entre marcas `<!-- shell:… -->`, y se copian al resto con
`tools/sync_shell.py`. No los edites en las otras páginas: el script los pisa.

Después de tocar cualquier texto en francés:

```bash
python3 tools/sync_shell.py        # propaga cabecera, pie, contacto y logo
python3 tools/extract_strings.py   # recoge los textos nuevos en el CSV
python3 build.py                   # regenera en/ y es/
```

Para agregar una página: crearla en su carpeta con las marcas `<!-- shell:… -->`
vacías, sumarla a `tools/pages.py` y correr los tres comandos.

## Avis Google

La page n'appelle jamais Google directement : elle appelle `api/avis.php`, qui
parle à l'API Places côté serveur. Aucun script tiers, aucun cookie, aucune
session — ce qui est aussi ce qui évite le problème CNIL sur un site français.

Trois niveaux, dans cet ordre :

1. cache local encore valide → servi sans appel réseau ;
2. appel à l'API Places → avis filtrés (note ≥ 4, texte non vide), les plus
   récents d'abord, mis en cache ;
3. Google injoignable ou rien de configuré → `content/avis.json`, des avis
   réels recopiés à la main.

### Mise en route, une seule fois

1. Console Google Cloud → nouveau projet → activer **Places API (New)**.
2. Créer une clé API et la restreindre : par **adresse IP** (celle du serveur
   O2Switch, pas le domaine — l'appel part du serveur) et par API (Places).
3. Récupérer le place ID : `python3 tools/place_id.py LA_CLE`. Le script
   cherche la fiche et affiche son ID. La bonne fiche est celle du CID
   **1377371409426816352**.
4. Copier `api/config.example.php` en `api/config.php` et y coller les deux
   valeurs.

Ensuite plus rien à faire : les avis se rafraîchissent tout seuls.

Coût : avec un cache d'une heure, le site appelle Google environ 24 fois par
jour (~720 par mois), largement dans le palier gratuit mensuel de Google Maps
Platform. Une carte bancaire reste exigée à la création du compte.

Deux limites à connaître : l'API renvoie **5 avis au maximum** par fiche, et la
politique Places **interdit** de conserver le contenu des avis au-delà de ce
qu'exige la performance — donc pas d'archive locale qui grossirait avec le
temps. Le place ID, lui, peut être conservé sans limite.

## Publicar en O2Switch

    python3 tools/sync_shell.py
    python3 tools/extract_strings.py
    python3 build.py
    python3 tools/stamp.py
    python3 tools/dist.py

`tools/dist.py` arma `dist/`: la copia que se sube al servidor. Lleva solo lo
que el navegador necesita, con HTML, CSS y JS sin comentarios. No se versiona
(está en `.gitignore`). Los logos originales de clientes y de INWARD están en
`_fuentes/` y tampoco se publican.
