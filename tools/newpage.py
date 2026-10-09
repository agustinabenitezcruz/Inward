#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Esqueleto de una página nueva.

    python3 tools/newpage.py <dir> --title ... --desc ...

Escribe el <head> completo y el cuerpo con las marcas shell:* vacías; el
contenido lo copia después tools/sync_shell.py. No sobreescribe una página que
ya exista: si el archivo está, no hace nada.

Esto existe para que ninguna página nueva nazca sin canonical, sin hreflang,
sin og: y sin JSON-LD. Los seis archivos del sitio tienen que tener la misma
cabeza y a mano eso no se sostiene.
"""
import argparse, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://inwardpro.com"

HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#202045">

<link rel="icon" href="{p}favicon.ico" sizes="32x32">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">

<link rel="canonical" href="{dom}/{d}/">
<link rel="alternate" hreflang="fr" href="{dom}/{d}/">
<link rel="alternate" hreflang="en" href="{dom}/en/{d}/">
<link rel="alternate" hreflang="es" href="{dom}/es/{d}/">
<link rel="alternate" hreflang="x-default" href="{dom}/{d}/">

<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="INWARD">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{dom}/{d}/">
<meta property="og:image" content="{dom}/assets/img/og-inward-partage.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300..600&family=Jost:wght@300..600&display=swap">
<link rel="stylesheet" href="{p}assets/css/styles.css">

<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

<!-- Los bloques marcados shell:* no se editan aca: salen de index.html y los
     copia tools/sync_shell.py. -->
<!-- shell:sprite --><!-- /shell:sprite -->
<!-- shell:header --><!-- /shell:header -->

<div id="top"></div>

{body}

<!-- shell:contact --><!-- /shell:contact -->
<!-- shell:footer --><!-- /shell:footer -->

<nav class="rail" aria-label="Sections de la page">
{rail}
</nav>

<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
"""


def write(d, title, desc, jsonld, body, rail, ogtype="website", noindex=False):
    path = os.path.join(ROOT, d, "index.html")
    if os.path.exists(path):
        print("  %-52s ya existe, no se toca" % (d + "/index.html"))
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    p = "../" * len([s for s in d.split("/") if s])
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else ""
    open(path, "w", encoding="utf-8").write(HEAD.format(
        robots=robots, title=title, desc=desc, p=p, dom=DOMAIN, d=d,
        ogtype=ogtype, jsonld=jsonld.strip(), body=body.strip(), rail=rail.strip()))
    print("  %-52s creada" % (d + "/index.html"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--title", required=True)
    ap.add_argument("--desc", required=True)
    a = ap.parse_args()
    write(a.dir, a.title, a.desc, "{}", "", '  <a href="#top" aria-label="Haut de page"><span></span></a>')
