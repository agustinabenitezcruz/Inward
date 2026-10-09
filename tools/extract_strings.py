#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae de TODAS las páginas en francés los textos traducibles y escribe content/strings.csv
con las columnas key, fr, en, es. Las columnas en y es quedan vacías: las llena
la clienta. Si el CSV ya existe, conserva lo que esté traducido y sólo agrega
las claves nuevas, así se puede volver a correr cada vez que cambie el francés.

    python3 tools/extract_strings.py
"""
import csv, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import PAGES, src_of

OUT = os.path.join(ROOT, "content", "strings.csv")

# Etiquetas cuyo contenido nunca se traduce
SKIP_TAGS = ("script", "style", "svg", "symbol", "title")
# Atributos traducibles
ATTRS = ("alt", "placeholder", "title", "aria-label")

# Textos que no se traducen: nombres propios, marcas, siglas
LITERAL = {
    "INWARD", "FR", "EN", "ES", "RGPD", "CGV", "Passeport Talent", "Menu",
    "Delfina Benitez Cruz", "Marina Biedma", "Google", "Trustpilot", "Calendly",
    "Typeform", "Beytours", "Biondi", "Mouve", "Superprof", "Prolenser",
    "De Altura", "Las Praderas", "Bey tours, DMC Europe", "O2Switch", "+XX",
}


def clean(t):
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def translatable(t):
    if not t or t in LITERAL:
        return False
    if not re.search(r"[A-Za-zÀ-ÿ]{2}", t):     # sin letras: cifras, símbolos, flechas
        return False
    if re.fullmatch(r"[\d\s%+.,/·-]+", t):
        return False
    return True


def make_key(text, used):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())[:44].strip("-") or "txt"
    key, n = slug, 2
    while key in used:
        key, n = "%s-%d" % (slug, n), n + 1
    used.add(key)
    return key


def extract(src):
    # Fuera del contenido lo que no se traduce
    body = src
    for tag in SKIP_TAGS:
        body = re.sub(r"<%s\b.*?</%s>" % (tag, tag), " ", body, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)

    found, used = [], set()

    # <title> y <meta name/property=...content>
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    if m:
        found.append(("meta-title", clean(m.group(1))))
        used.add("meta-title")
    for name, key in (("description", "meta-description"),
                      ("og:title", "meta-og-title"),
                      ("og:description", "meta-og-description")):
        m = re.search(r'<meta\s+(?:name|property)="%s"\s+content="([^"]*)"' % re.escape(name), src)
        if m and translatable(clean(m.group(1))):
            found.append((key, clean(m.group(1))))
            used.add(key)

    # Atributos traducibles
    for attr in ATTRS:
        for m in re.finditer(r'\b%s="([^"]+)"' % attr, body):
            t = clean(m.group(1))
            if translatable(t) and t not in [x[1] for x in found]:
                found.append((make_key(t, used), t))

    # Nodos de texto
    for m in re.finditer(r">([^<>]+)<", body):
        t = clean(m.group(1))
        if translatable(t) and t not in [x[1] for x in found]:
            found.append((make_key(t, used), t))

    return found


def main():
    # Un solo CSV para todo el sitio: la cabecera, el pie y el formulario son
    # los mismos en todas las páginas, y un texto repetido tiene que traducirse
    # una vez, no seis. Las claves se reparten por página pero el texto manda.
    rows, seen = [], set()
    for page in PAGES:
        path = os.path.join(ROOT, src_of(page["dir"]))
        if not os.path.exists(path):
            continue
        for key, fr in extract(open(path, encoding="utf-8").read()):
            if fr in seen:
                continue
            seen.add(fr)
            rows.append((key, fr))

    previous = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                previous[r["fr"]] = (r.get("en", ""), r.get("es", ""))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    kept = 0
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "fr", "en", "es"])
        for key, fr in rows:
            en, es = previous.get(fr, ("", ""))
            if en or es:
                kept += 1
            w.writerow([key, fr, en, es])

    print("%d textos escritos en content/strings.csv" % len(rows))
    if kept:
        print("%d traducciones existentes conservadas" % kept)
    print("Las columnas en y es vacías se completan y después se corre build.py")


if __name__ == "__main__":
    sys.exit(main())
