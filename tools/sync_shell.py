#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copia los bloques compartidos de index.html al resto de las páginas.

    python3 tools/sync_shell.py

La cabecera, el pie, el sprite del logo y la sección de contacto son los mismos
en todas las páginas. Duplicarlos a mano en seis archivos es garantía de que
tarde o temprano dos páginas tengan menús distintos, así que viven en un solo
sitio —index.html, el francés, que sigue siendo la fuente— y desde ahí se
copian.

En index.html cada bloque va entre marcas:

    <!-- shell:header -->  ...  <!-- /shell:header -->

y en las demás páginas van las mismas marcas con lo que sea adentro: este
script reemplaza el contenido entre marcas. Al copiar ajusta lo que depende de
dónde está la página:

- las rutas a recursos y a otras páginas, que en index.html son relativas a la
  raíz, reciben tantos ../ como haga falta;
- un enlace que apunte a la propia página se convierte en ancla (#servicios),
  para que no recargue;
- un ancla a una sección que esa página no tiene (#faq desde la landing) se
  convierte en enlace a la home más el ancla;
- el selector de idioma apunta a la misma página en el otro idioma, no a la
  home del otro idioma;
- en una landing con una sola audiencia el formulario pierde el selector
  Entreprise / Particulier y queda fijo en la que corresponde.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import PAGES, src_of, prefix_of

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCKS = ("sprite", "header", "contact", "footer")
# Landings con una sola audiencia: el formulario no pregunta por el perfil,
# ya lo sabe. El valor sigue viajando en un campo oculto, asi que el backend
# recibe exactamente lo mismo que desde la home.
PROFIL = {"entreprises": "entreprise", "particuliers": "particulier"}
ASSETS = ("assets/", "favicon.ico", "favicon.svg", "apple-touch-icon.png", "site.webmanifest")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|data:|//)")


def block(doc, name):
    m = re.search(r"<!-- shell:%s -->(.*?)<!-- /shell:%s -->" % (name, name), doc, re.S)
    return m.group(1) if m else None


def page_ids(doc):
    return set(re.findall(r'\bid="([^"]+)"', doc))


def site_path(d):
    return (d + "/") if d else ""


def rewrite(html, page_dir, ids):
    """Adapta un bloque de la home a una página que vive en page_dir."""
    pre = prefix_of(page_dir)
    mine = site_path(page_dir)

    if pre:
        for a in ('href="', 'src="', 'poster="'):
            for asset in ASSETS:
                html = html.replace(a + asset, a + pre + asset)

    def on_href(m):
        url = m.group(1)
        if EXTERNAL.match(url) or url.startswith(pre) and pre:
            return m.group(0)
        if url == "#":
            # Enlace todavia sin destino: se deja como esta.
            return m.group(0)
        if url.startswith("#"):
            # Ancla: si la seccion esta en esta pagina se queda; si no, va a la home.
            return m.group(0) if url[1:] in ids else 'href="%s%s"' % (pre, url)
        target, _, frag = url.partition("#")
        if target in ("./", ""):
            target = ""
        if target == mine:
            # Enlace a uno mismo: ancla, para no recargar la pagina.
            return 'href="#%s"' % frag if frag else 'href="#top"'
        return 'href="%s%s"' % (pre, url)

    # Las rutas de recursos ya llevan el prefijo, asi que no vuelven a entrar.
    html = re.sub(r'href="([^"]*)"', on_href, html)
    return html


def lock_profil(html, page_dir):
    """Quita el selector de perfil en las landings de una sola audiencia."""
    p = PROFIL.get(page_dir)
    if not p:
        return html
    html = re.sub(r'(<form[^>]*\sid="ctForm"[^>]*\sdata-profil=")[^"]*(")',
                  r"\g<1>%s\g<2>" % p, html)
    # El <input type=hidden> no crea fila en la grilla del formulario: la hoja
    # de estilos del navegador ya le pone display:none.
    rep = ('<!-- Perfil fijo: esta landing tiene una sola audiencia, asi que el\n'
           '           selector no decide nada. Lo pone tools/sync_shell.py a partir\n'
           '           del bloque shell:contact de index.html; no se edita a mano. -->\n'
           '      <input type="hidden" name="profil" value="%s">' % p)
    html = re.sub(r'<div class="seg" role="radiogroup".*?</div>', rep, html, flags=re.S)
    return html


def lang_nav(html, page_dir):
    """Reescribe los selectores de idioma para que apunten a ESTA página."""
    # Este script solo toca las paginas en frances, asi que el frances siempre
    # es la pagina misma. Los otros dos idiomas son la MISMA pagina bajo /en/ o
    # /es/, no la home de ese idioma.
    pre = prefix_of(page_dir)
    mine = site_path(page_dir)
    hrefs = {"fr": "./", "en": pre + "en/" + mine, "es": pre + "es/" + mine}

    def build(cls, indent):
        out = ['<nav class="%s" aria-label="Langue">' % cls]
        for c, label in (("fr", "FR"), ("en", "EN"), ("es", "ES")):
            cur = ' aria-current="true"' if c == "fr" else ""
            out.append('%s  <a href="%s" hreflang="%s"%s>%s</a>' % (indent, hrefs[c], c, cur, label))
        out.append(indent + "</nav>")
        return "\n".join(out)

    INDENT = {"lang": "      ", "lang lang-mob": "        ", "lang lang-ft": "        "}
    return re.sub(r'<nav class="(lang(?: lang-(?:ft|mob))?)" aria-label="Langue">.*?</nav>',
                  lambda m: build(m.group(1), INDENT.get(m.group(1), "      ")),
                  html, flags=re.S)


def main():
    home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    src = {}
    for name in BLOCKS:
        b = block(home, name)
        if b is None:
            sys.exit("index.html no tiene el bloque shell:%s" % name)
        src[name] = b

    for page in PAGES:
        d = page["dir"]
        if not d:
            continue
        path = os.path.join(ROOT, src_of(d))
        if not os.path.exists(path):
            print("  %-28s (todavía no existe, se salta)" % src_of(d))
            continue
        doc = open(path, encoding="utf-8").read()
        # Los id de los bloques compartidos cuentan como propios de la pagina:
        # el sprite del logo llega con el shell, y sin esto el <use href="#..."> del
        # logo se reescribiria como si apuntara a otra pagina.
        ids = page_ids(doc) | set().union(*(page_ids(b) for b in src.values()))
        done = []
        for name in BLOCKS:
            pat = re.compile(r"(<!-- shell:%s -->).*?(<!-- /shell:%s -->)" % (name, name), re.S)
            if not pat.search(doc):
                continue
            new = rewrite(src[name], d, ids)
            if name in ("header", "footer") and d:
                # En la home el logo es un ancla al principio de la pagina; en
                # una pagina interior tiene que VOLVER a la home, que es lo que
                # todo el mundo espera al hacer clic en el logo.
                new = new.replace('<a href="#top" class="brand"',
                                  '<a href="%s" class="brand"' % (prefix_of(d) or "./"))
            if name in ("header", "footer"):
                new = lang_nav(new, d)
            if name == "contact":
                new = lock_profil(new, d)
            doc = pat.sub(lambda m: m.group(1) + new.replace("\\", "\\\\") + m.group(2), doc, count=1)
            done.append(name)
        open(path, "w", encoding="utf-8").write(doc)
        print("  %-28s %s" % (src_of(d), ", ".join(done) or "sin marcas"))

    print("\nListo. Después de esto hay que correr build.py para regenerar en/ y es/.")


if __name__ == "__main__":
    sys.exit(main())
