#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las versiones en inglés y español de TODAS las páginas a partir de sus
originales en francés (que son la fuente) y de content/strings.csv.

    python3 build.py

Salida, para cada página de tools/pages.py:
    en/<pagina>/index.html
    es/<pagina>/index.html

Los originales en francés no se tocan nunca: son los que se editan a mano.
Cuando cambie el francés, correr antes tools/extract_strings.py (y despues tools/stamp.py) para que el CSV
recoja los textos nuevos.

Una página cuyo idioma no esté completo se marca con noindex y muestra una
franja de aviso, para que nadie la confunda con una página terminada y para que
Google no la indexe a medio traducir.
"""
import csv, datetime, html, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from pages import PAGES, src_of, depth_of, prefix_of, indexable, sitemap_hint

CSV = os.path.join(ROOT, "content", "strings.csv")
DOMAIN = "https://inwardpro.com"

LANGS = {
    "en": {"dir": "en", "locale": "en_US", "label": "English",
           "notice": "Translation in progress. This page still shows the French text where the English is missing."},
    "es": {"dir": "es", "locale": "es_ES", "label": "Español",
           "notice": "Traducción en curso. Esta página muestra el texto en francés donde falta el español."},
}
ATTRS = ("alt", "placeholder", "title", "aria-label")
PROTECTED = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>|<!--.*?-->", re.S | re.I)


def load_strings():
    if not os.path.exists(CSV):
        sys.exit("Falta content/strings.csv. Corré antes: python3 tools/extract_strings.py")
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    if not rows:
        sys.exit("content/strings.csv está vacío.")
    return rows


def protected_spans(doc):
    return [(m.start(), m.end()) for m in PROTECTED.finditer(doc)]


def inside(pos, spans):
    return any(a <= pos < b for a, b in spans)


def norm(t):
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def translate(doc, mapping):
    """Sustituye sólo en nodos de texto y en atributos traducibles."""
    spans = protected_spans(doc)
    hits = [0]

    def swap(text):
        key = norm(text)
        if key in mapping and mapping[key]:
            lead = text[:len(text) - len(text.lstrip())]
            tail = text[len(text.rstrip()):]
            hits[0] += 1
            return lead + html.escape(mapping[key], quote=False) + tail
        return text

    def on_text(m):
        if inside(m.start(), spans):
            return m.group(0)
        return ">" + swap(m.group(1)) + "<"

    doc = re.sub(r">([^<>]+)<", on_text, doc)

    for attr in ATTRS + ("content",):
        def on_attr(m, attr=attr):
            if inside(m.start(), spans):
                return m.group(0)
            val = norm(m.group(1))
            if val in mapping and mapping[val]:
                return '%s="%s"' % (attr, html.escape(mapping[val], quote=True))
            return m.group(0)
        doc = re.sub(r'\b%s="([^"]+)"' % attr, on_attr, doc)

    m = re.search(r"<title>(.*?)</title>", doc, re.S)
    if m and norm(m.group(1)) in mapping and mapping[norm(m.group(1))]:
        doc = doc[:m.start(1)] + html.escape(mapping[norm(m.group(1))], quote=False) + doc[m.end(1):]

    return doc, hits[0]


def rewrite_paths(doc):
    """La versión traducida vive un nivel más abajo que el original.

    No importa a qué profundidad esté la página: /en/ está un nivel por debajo
    de la raíz y /en/entreprises/ un nivel por debajo de /entreprises/, así que
    en los dos casos alcanza con anteponer UN ../ a lo que ya hubiera.
    data-api y api/ entran por el endpoint de las opiniones: sin ellos /en/ y
    /es/ pedian en/api/avis.php, que no existe (404)."""
    return re.sub(r'\b(href|src|poster|data-api)="((?:\.\./)*)(assets/|api/|favicon\.svg|favicon\.ico|apple-touch-icon\.png|site\.webmanifest)',
                  lambda m: '%s="../%s%s' % (m.group(1), m.group(2), m.group(3)), doc)


def rewrite_head(doc, code, cfg, page_dir):
    """canonical y og:url apuntan a esta página en este idioma."""
    here = "%s/%s" % (DOMAIN, (page_dir + "/") if page_dir else "")
    there = "%s/%s/%s" % (DOMAIN, cfg["dir"], (page_dir + "/") if page_dir else "")
    doc = doc.replace('<html lang="fr">', '<html lang="%s">' % code, 1)
    doc = doc.replace('<link rel="canonical" href="%s">' % here,
                      '<link rel="canonical" href="%s">' % there)
    doc = doc.replace('<meta property="og:locale" content="fr_FR">',
                      '<meta property="og:locale" content="%s">' % cfg["locale"])
    doc = doc.replace('<meta property="og:url" content="%s">' % here,
                      '<meta property="og:url" content="%s">' % there)
    doc = doc.replace('"url": "%s/",' % DOMAIN, '"url": "%s/%s/",' % (DOMAIN, cfg["dir"]))
    return doc


def rewrite_lang_nav(doc, code, page_dir):
    """Rutas relativas correctas y aria-current en el idioma de la pagina.
    Hay tres selectores: el del header, el del menu desplegable y el del pie.
    Se reescriben los tres; si alguno quedara sin tocar, /es/ enlazaria a
    /es/en/ y el idioma activo se marcaria en la pagina equivocada.
    Los tres apuntan a ESTA pagina en el otro idioma, no a la home."""
    up = "../" * (depth_of(page_dir) + 1)
    mine = (page_dir + "/") if page_dir else ""
    hrefs = {"fr": up + mine, "en": up + "en/" + mine, "es": up + "es/" + mine}
    hrefs[code] = "./"

    def build(cls, indent):
        out = ['<nav class="%s" aria-label="Langue">' % cls]
        for c, label in (("fr", "FR"), ("en", "EN"), ("es", "ES")):
            cur = ' aria-current="true"' if c == code else ""
            out.append('%s  <a href="%s" hreflang="%s"%s>%s</a>' % (indent, hrefs[c], c, cur, label))
        out.append(indent + "</nav>")
        return "\n".join(out)

    INDENT = {"lang": "      ", "lang lang-mob": "        ", "lang lang-ft": "        "}

    def swap(m):
        cls = m.group(1)
        return build(cls, INDENT.get(cls, "      "))

    doc, n = re.subn(r'<nav class="(lang(?: lang-(?:ft|mob))?)" aria-label="Langue">.*?</nav>',
                     swap, doc, flags=re.S)
    if n != 3:
        sys.exit("Se esperaban 3 selectores de idioma en index.html, se encontraron %d" % n)
    return doc


def add_notice(doc, cfg, missing):
    """Aviso fijo abajo a la izquierda: no empuja el layout ni tapa la barra fija."""
    doc = doc.replace("<title>", '<meta name="robots" content="noindex, follow">\n<title>', 1)
    banner = (
        '<p style="position:fixed;left:16px;bottom:16px;z-index:80;margin:0;'
        'max-width:min(340px,calc(100vw - 32px));padding:.6rem .85rem;border-radius:12px;'
        'background:#ebff76;color:#101010;box-shadow:0 8px 24px -10px rgba(16,16,16,.45);'
        'font:500 .74rem/1.45 Jost,system-ui,sans-serif">%s (%d)</p>\n'
        % (html.escape(cfg["notice"]), missing)
    )
    return doc.replace("<body>\n", "<body>\n" + banner, 1)


def write_sitemap(ready):
    """sitemap.xml con las tres versiones de cada pagina indexable.

    Reglas, y las tres importan:
    - una pagina marcada noindex en tools/pages.py no entra: pedirle a Google
      que rastree una URL que le prohibe indexar es contradictorio;
    - una traduccion incompleta tampoco, porque build.py le pone noindex;
    - cada URL declara sus alternativas con xhtml:link, que es como se le dice
      a Google que /en/ y /es/ son la misma pagina en otro idioma y no
      contenido duplicado. Sin eso el hreflang del <head> vale la mitad.
    """
    today = datetime.date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- Generado por build.py. No editar a mano. -->',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in PAGES:
        d = page["dir"]
        if not indexable(page):
            continue
        langs = ["fr"] + [c for c in LANGS if ready.get((d, c))]
        tail = (d + "/") if d else ""
        url_of = lambda c: "%s/%s%s" % (DOMAIN, "" if c == "fr" else LANGS[c]["dir"] + "/", tail)
        prio, freq = sitemap_hint(d)
        for c in langs:
            out.append("  <url>")
            out.append("    <loc>%s</loc>" % url_of(c))
            out.append("    <lastmod>%s</lastmod>" % today)
            out.append("    <changefreq>%s</changefreq>" % freq)
            out.append("    <priority>%.1f</priority>" % prio)
            for alt in langs:
                out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (alt, url_of(alt)))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % url_of("fr"))
            out.append("  </url>")
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    n = sum(1 for line in out if line.strip().startswith("<loc>"))
    print("sitemap.xml: %d URL" % n)


def main():
    rows = load_strings()
    print("%d textos en el CSV\n" % len(rows))

    ready = {}
    for page in PAGES:
        d = page["dir"]
        path = os.path.join(ROOT, src_of(d))
        if not os.path.exists(path):
            print("  %-24s (todavía no existe, se salta)" % src_of(d))
            continue
        src = open(path, encoding="utf-8").read()

        for code, cfg in LANGS.items():  # noqa: E501
            mapping = {r["fr"]: (r.get(code) or "").strip() for r in rows}
            missing = sum(1 for v in mapping.values() if not v)

            doc, replaced = translate(src, mapping)
            doc = rewrite_paths(doc)
            doc = rewrite_head(doc, code, cfg, d)
            doc = rewrite_lang_nav(doc, code, d)
            if missing:
                doc = add_notice(doc, cfg, missing)

            out_dir = os.path.join(ROOT, cfg["dir"], d) if d else os.path.join(ROOT, cfg["dir"])
            os.makedirs(out_dir, exist_ok=True)
            out = os.path.join(out_dir, "index.html")
            open(out, "w", encoding="utf-8").write(doc)

            ready[(d, code)] = not missing
            state = "completa" if not missing else "%d sin traducir, noindex" % missing
            print("  %-26s ->  %d sustituidos, %s"
                  % (os.path.relpath(out, ROOT), replaced, state))
        print("")

    write_sitemap(ready)

    print("Listo. Los originales en francés no se modificaron.")


if __name__ == "__main__":
    sys.exit(main())
