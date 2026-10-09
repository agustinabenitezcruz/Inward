# -*- coding: utf-8 -*-
"""Las páginas del sitio, en un solo lugar.

`dir` es la ruta de la página respecto de la raíz del sitio, sin barra final.
La home es "". De acá salen tanto la profundidad (cuántos ../ hay que poner
delante de los recursos) como las rutas del selector de idioma, así que build.py
y tools/sync_shell.py leen los dos esta lista y no pueden discrepar.

`noindex: True` marca una página que existe —tiene URL, enlaces y JSON-LD— pero
que todavía no tiene su texto: lleva <meta name="robots" content="noindex"> en
el HTML y NO entra en el sitemap. Una página vacía indexada hace más daño que
no existir. Cuando llegue el texto se quita el meta y se borra la bandera.
"""

PAGES = [
    {"dir": "",             "title": "Home"},
    {"dir": "entreprises",  "title": "Landing Entreprises"},
    {"dir": "particuliers", "title": "Landing Particuliers"},
    {"dir": "blog",         "title": "Blog"},
    {"dir": "blog/changement-de-statut-salarie-entrepreneur",
     "title": "Article : changement de statut", "noindex": True},
    {"dir": "blog/delais-prefecture-carte-de-sejour-2026",
     "title": "Article : délais préfecture 2026", "noindex": True},
    {"dir": "videos",       "title": "Vidéos"},
    {"dir": "videos/presentation-inward-palais-garnier",
     "title": "Vidéo : INWARD devant le Palais Garnier"},
    # Pendientes: qui-sommes-nous, mentions-legales
]

# Prioridad y frecuencia del sitemap. No son una orden para Google, son una
# pista; se escriben igual porque no cuestan nada y dejan el criterio escrito.
SITEMAP = {
    "":             (1.0, "weekly"),
    "entreprises":  (0.9, "monthly"),
    "particuliers": (0.9, "monthly"),
    "blog":         (0.8, "weekly"),
    "videos":       (0.5, "monthly"),
}
SITEMAP_DEFAULT = (0.6, "monthly")


def src_of(d):
    """Archivo fuente en francés de una página."""
    return (d + "/index.html") if d else "index.html"


def depth_of(d):
    return len([s for s in d.split("/") if s])


def prefix_of(d):
    """Lo que hay que anteponer a una ruta relativa a la raíz."""
    return "../" * depth_of(d)


def indexable(page):
    return not page.get("noindex")


def sitemap_hint(d):
    return SITEMAP.get(d, SITEMAP_DEFAULT)
