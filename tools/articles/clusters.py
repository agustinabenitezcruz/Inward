# -*- coding: utf-8 -*-
"""Blog por clusters tematicos (carpeta "Cluster thematique" de la clienta).
Cada cluster = un articulo pilar + satelites. Lee clusters.json (generado por
parse_clusters.py desde los .docx) y escribe:
  - cada articulo (los que reescriben un articulo viejo van en SU URL de
    siempre, en la raiz; los nuevos en /ressources/<slug>/), solo en frances;
  - la pagina /ressources/ (categorias = clusters) y las 3 tarjetas de la home.
"""
import sys, os, json, re, html, datetime, shutil
sys.path.insert(0, 'tools')
from newpage import write

DOM = "https://www.inwardpro.com"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = {a["file"]: a for a in json.load(open(os.path.join(HERE, "clusters.json"), encoding="utf-8"))}
TODAY = datetime.date.today().isoformat()

CLUSTERS = [("embaucher", "Embaucher un salarié étranger"),
            ("passeport-talent", "Passeport Talent"),
            ("vvt", "Visa vacances-travail")]
IMG = {
 "equipe-multiculturelle-reunion-travail": (874, 1200, "Équipe multiculturelle en réunion de travail autour d'une table"),
 "equipe-internationale-bureau-adaptation-culturelle": (1400, 788, "Équipe internationale travaillant ensemble dans un bureau"),
 "collegues-echange-ordinateur-bureau": (1400, 934, "Collègues échangeant autour d'un ordinateur dans un bureau"),
 "visa-passeport-talent-chercheurs-laboratoire": (800, 1066, "Deux chercheurs travaillant avec des tubes à essai dans un laboratoire"),
 "signature-documents-autorisation-de-travail": (1400, 934, "Signature de documents de travail sur une table de réunion"),
 "visa-pvt-voyage": (800, 1066, "Voyageuse avec son sac à dos regardant le paysage"),
 "visa-pvt-sacre-coeur-montmartre": (800, 1066, "Rue de Montmartre avec le Sacré-Cœur au fond"),
 "consultante-inward-entretien-salarie-etranger": (1400, 933, "Consultante INWARD en entretien avec un salarié étranger autour d'une table"),
}
# Categorias del blog (definidas por la clienta, 26/11/2026). Son distintas de
# los clusters: el cluster es el "dossier" de cada articulo (pilar + satelites,
# se ve dentro del articulo) y la categoria es el filtro de /ressources/.
# Las categorias sin articulos no se muestran; el CSS ya las filtra todas, asi
# que basta asignar un articulo para que la pastilla aparezca.
CATS = [("etude-de-cas", "Étude de cas"),
        ("travail", "Travail en France"),
        ("famille", "Immigration familiale"),
        ("etudier", "Étudier en France"),
        ("tourisme", "Tourisme"),
        ("embaucher", "Embaucher un salarié de nationalité étrangère")]
CAT_DE = {  # url del articulo -> categorias (separadas por espacio)
 "avantages-dembaucher-un-salarie-etranger": "embaucher",
 "adaptation-culturelle-travailleurs-etrangers": "embaucher",
 "cout-pour-recruter-un-salarie-etranger": "embaucher",
 "ressources/visa-talent-france-conditions-demarches": "travail",
 "ressources/passeport-talent-salarie-qualifie-carte-bleue-europeenne": "travail",
 "ressources/visa-vacances-travail-france": "tourisme",
 "comment-faire-un-chengement-de-statut-apres-un-visa-vvt": "travail",
 "embaucher-salarie-vvt": "embaucher",
}
CAT_N = dict(CATS)
# (archivo, cluster, rol, url, imagen, fecha de publicacion)
ARTS = [
 ("Embaucher un salarié étranger/Pilar_.docx", "embaucher", "pilier", "avantages-dembaucher-un-salarie-etranger", "equipe-multiculturelle-reunion-travail", "2023-08-31"),
 ("Embaucher un salarié étranger/Satelite 1.docx", "embaucher", "satellite", "adaptation-culturelle-travailleurs-etrangers", "equipe-internationale-bureau-adaptation-culturelle", "2023-08-31"),
 ("Embaucher un salarié étranger/Satellite 2.docx", "embaucher", "satellite", "cout-pour-recruter-un-salarie-etranger", "collegues-echange-ordinateur-bureau", "2023-08-31"),
 ("Passeport Talent/PILIER Brief Guide visa Talent 2026.docx", "passeport-talent", "pilier", "ressources/visa-talent-france-conditions-demarches", "visa-passeport-talent-chercheurs-laboratoire", "2026-10-21"),
 ("Passeport Talent/Article satellite 2 Passeport-Talent-salarie-qualifie-ou-Carte-Bleue-Europeenne-2026.docx", "passeport-talent", "satellite", "ressources/passeport-talent-salarie-qualifie-carte-bleue-europeenne", "signature-documents-autorisation-de-travail", "2026-11-16"),
 ("vvt/Pilar.docx", "vvt", "pilier", "ressources/visa-vacances-travail-france", "visa-pvt-voyage", TODAY),
 ("vvt/satelite 1.docx", "vvt", "satellite", "comment-faire-un-chengement-de-statut-apres-un-visa-vvt", "visa-pvt-sacre-coeur-montmartre", "2023-12-14"),
 ("vvt/Satellite 2.docx", "vvt", "satellite", "embaucher-salarie-vvt", "consultante-inward-entretien-salarie-etranger", "2023-12-14"),
]
URL_MAP = {  # URLs que aparecen en los textos -> pagina actual
 "limportance-de-ladaptation-culturelle-pour-les-travailleurs-etrangers": "adaptation-culturelle-travailleurs-etrangers",
 "tout-savoir-sur-la-vtt-visa-vacances-travail": "ressources/visa-vacances-travail-france",
 "passeport-talent-salarie-qualifie": "ressources/passeport-talent-salarie-qualifie-carte-bleue-europeenne",
}
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def fdate(s):
    d = datetime.date.fromisoformat(s[:10]); return "%d %s %d" % (d.day, MOIS[d.month-1], d.year)
def plain(h): return html.unescape(re.sub(r"<[^>]+>", "", h)).strip()

def link_fix(h, pre):
    def own(m):
        path = m.group(1).strip("/")
        path = URL_MAP.get(path, path)
        return 'href="%s%s"' % (pre, (path + "/") if path else "")
    h = re.sub(r'href="https?://(?:www\.)?inwardpro\.com/?([^"#?]*)"', own, h)
    h = re.sub(r'href="(https?://[^"]+)"', r'href="\1" target="_blank" rel="noopener"', h)
    return h

QA_SVG = '<svg class="qa-mk" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M3 5.25L7 9.25l4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def render(blocks, pre):
    out, faqs = [], []
    for b in blocks:
        t = b["t"]
        if t in ("h2", "h3", "p"):
            out.append("    <%s>%s</%s>" % (t, link_fix(b["h"], pre), t))
        elif t == "ul":
            out.append("    <ul>\n%s\n    </ul>" % "\n".join("      <li>%s</li>" % link_fix(i, pre) for i in b["items"]))
        elif t == "box":
            inner = link_fix(b["h"], pre)
            if "<li>" in inner and "<ul>" not in inner:
                inner = re.sub(r"((?:<li>.*?</li>)+)", r"<ul>\1</ul>", inner)
            if not inner.startswith("<"): inner = "<p>%s</p>" % inner
            out.append('    <aside class="art-box"><p class="art-box-t">%s</p>%s</aside>' % (b["title"], inner))
        elif t == "table":
            rows = b["rows"]
            head = "".join("<th>%s</th>" % c for c in rows[0])
            body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows[1:])
            out.append('    <div class="art-table"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (head, body))
        elif t == "faq" and b["qa"]:
            out.append("    <h2>Questions fréquentes</h2>")
            qs = []
            for k, (q, a) in enumerate(b["qa"]):
                faqs.append((plain(q), plain(a)))
                qs.append('''      <details class="qa" name="faq">
        <summary>
          <span class="qa-n">%02d</span>
          <span class="qa-q">%s</span>
          %s
        </summary>
        <div class="qa-a">%s</div>
      </details>''' % (k + 1, q, QA_SVG, link_fix(a, pre).replace("<p>", '<p class="body-2">')))
            out.append('    <div class="faq-list art-faq">\n%s\n    </div>' % "\n".join(qs))
        elif t == "refs" and b["items"]:
            lis = []
            for label, url in b["items"]:
                if url:
                    lis.append('<li><a href="%s">%s</a></li>' % (html.escape(url), label))
                else:
                    lis.append("<li>%s</li>" % label)
            out.append('    <h2>Sources</h2>\n    <ul class="art-refs">\n      %s\n    </ul>' % link_fix("\n      ".join(lis), pre))
    return "\n".join(out), faqs

def words(blocks):
    t = " ".join(plain(json.dumps(b, ensure_ascii=False)) for b in blocks)
    return len(t.split())

cards = []
for f, cl, role, url, img, pub in ARTS:
    a = DATA[f]; m = a["meta"]
    depth = len(url.split("/")); pre = "../" * depth
    h1 = html.unescape(m["h1"]).strip()
    title = html.unescape(m.get("title", h1)).strip()
    desc = html.unescape(m.get("desc", "")).strip()
    U = "%s/%s/" % (DOM, url)
    w, h, alt = IMG[img]
    clname = dict(CLUSTERS)[cl]
    rm = re.search(r"(\d+)", m.get("read", ""))
    mins = int(rm.group(1)) if rm else max(3, round(words(a["blocks"]) / 220))
    body, faqs = render(a["blocks"], pre)
    # mismo cluster: enlaces cruzados (pilar <-> satelites)
    sib = [x for x in ARTS if x[1] == cl and x[3] != url]
    rel = "\n".join('      <li><a href="%s%s/">%s</a>%s</li>' % (pre, x[3], html.escape(html.unescape(DATA[x[0]]["meta"]["h1"]).strip(), quote=False),
                    ' <span class="art-role">Guide complet</span>' if x[2] == "pilier" else "") for x in sib)
    mod = TODAY
    graph = [
        {"@type": "BlogPosting", "@id": U + "#article", "headline": h1, "description": desc, "url": U,
         "inLanguage": "fr", "datePublished": pub, "dateModified": mod, "articleSection": clname,
         "isPartOf": {"@id": DOM + "/ressources/#blog"}, "publisher": {"@id": DOM + "/#organization"},
         "author": {"@id": DOM + "/#organization"}, "image": DOM + "/assets/img/%s.webp" % img,
         "mainEntityOfPage": U},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": DOM + "/"},
            {"@type": "ListItem", "position": 2, "name": "Ressources", "item": DOM + "/ressources/"},
            {"@type": "ListItem", "position": 3, "name": h1, "item": U}]}]
    if faqs:
        graph.append({"@type": "FAQPage", "@id": U + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faqs]})
    jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    dates = "Publié le %s" % fdate(pub) + ("" if pub == mod else " · Mis à jour le %s" % fdate(mod))
    page = '''<!-- Articulo del cluster "%s" (%s). Generado con tools/articles/clusters.py
     a partir del .docx de la clienta: no editar a mano. -->
<article class="band pg-head art-page">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane">
      <a href="%s">Accueil</a> <span aria-hidden="true">/</span>
      <a href="%sressources/">Ressources</a> <span aria-hidden="true">/</span>
      <span aria-current="page">%s</span>
    </nav>
    <p class="label">%s</p>
    <h1>%s</h1>
    <p class="lead">%s</p>
    <p class="art-date">%s · Lecture %d min</p>
  </div>
</article>

<section class="band sec" id="texte">
  <div class="wrap art-body art-old">
    <figure class="art-fig rounded">
      <img src="%sassets/img/%s.webp" width="%d" height="%d" alt="%s" decoding="async">
    </figure>
%s
    <nav class="art-cluster" aria-label="Dans le même dossier">
      <p class="art-cluster-t">Dans le même dossier : %s</p>
      <ul>
%s
      </ul>
    </nav>
    <p class="art-back"><a href="%sressources/">&lsaquo; Tous les articles</a></p>
  </div>
</section>''' % (clname, role, pre or "./", pre, html.escape(h1, quote=False), clname, html.escape(h1, quote=False), html.escape(desc, quote=False), dates, mins, pre, img, w, h, alt, body, clname, rel, pre)
    shutil.rmtree(url, ignore_errors=True)
    write(url, html.escape(title, quote=True).replace("&#x27;", "'"), html.escape(desc, quote=True).replace("&#x27;", "'"), jsonld, page,
          '  <a href="#top" aria-label="Haut de page"><span></span></a>', ogtype="article")
    p = os.path.join(url, "index.html"); t = open(p, encoding="utf-8").read()
    t = re.sub(r'<link rel="alternate" hreflang="(en|es)"[^>]*>\n', "", t)
    t = t.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="article">\n<meta property="article:published_time" content="%s">\n<meta property="article:modified_time" content="%s">' % (pub, mod))
    open(p, "w", encoding="utf-8").write(t)
    cards.append(dict(url=url, cl=cl, clname=clname, role=role, h1=h1, desc=desc, img=(img + ".webp", w, h, alt), mins=mins, pub=pub))

json.dump(cards, open(os.path.join(HERE, "cluster_cards.json"), "w"), ensure_ascii=False, indent=1)

def card(c, i, pre, cats=True):
    f, w, h, alt = c["img"]
    cs = CAT_DE[c["url"]]
    dc = ' data-cat="%s"' % cs if cats else ""
    kd = CAT_N[cs.split()[0]] + (" · Guide complet" if c["role"] == "pilier" else "")
    return '''      <article class="art art-ov%d rounded rv"%s>
        <figure class="art-ph"><img src="%sassets/img/%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></figure>
        <div class="art-b">
          <span class="kd">%s</span>
          <h3><a class="art-lnk" href="%s%s/">%s</a></h3>
          <p class="body-2">%s</p>
          <span class="rd-meta">Lecture %d min <span class="arw">&rsaquo;</span></span>
        </div>
      </article>''' % (i % 3 + 1, dc, pre, f, w, h, alt, kd, pre, c["url"], html.escape(c["h1"], quote=False), html.escape(c["desc"], quote=False), c["mins"])

# /ressources/: categorias de la clienta (solo las que tienen articulos),
# articulos ordenados por cluster (pilar primero)
p = "ressources/index.html"; s = open(p, encoding="utf-8").read()
def ncat(k): return sum(1 for c in cards if k in CAT_DE[c["url"]].split())
USADAS = [(k, n) for k, n in CATS if ncat(k)]
nav = '      <ul>\n        <li><a href="#articles">Tous les articles <span class="cats-n">%d</span></a></li>\n%s\n      </ul>' % (
    len(cards), "\n".join('        <li><a href="#cat-%s">%s <span class="cats-n">%d</span></a></li>' % (k, n, ncat(k)) for k, n in USADAS))
s = re.sub(r'      <ul>\n        <li><a href="#articles">.*?\n      </ul>', lambda m: nav, s, count=1, flags=re.S)
spans = "\n".join('    <span class="cat-t" id="cat-%s"></span>' % k for k, _ in USADAS)
s = re.sub(r'(    <span class="cat-t" id="cat-[^"]+"></span>\n)+', spans + "\n", s, count=1)
a0 = s.index('      <p class="cats-empty">'); a0 = s.index("\n", a0) + 1
b0 = s.index('    </div>\n  </div>\n</section>', a0)
s = s[:a0] + "\n".join(card(c, i, "../") for i, c in enumerate(cards)) + "\n" + s[b0:]
items = ",\n".join('      { "@type": "ListItem", "position": %d, "url": "%s/%s/", "name": %s }' % (i + 1, DOM, c["url"], json.dumps(c["h1"], ensure_ascii=False)) for i, c in enumerate(cards))
s = re.sub(r'("@type": "ItemList",.*?"numberOfItems": )\d+(,.*?"itemListElement": \[)\n.*?(\n\s*\])', lambda m: m.group(1) + str(len(cards)) + m.group(2) + "\n" + items + m.group(3), s, count=1, flags=re.S)
s = re.sub(r'\n      \{ "@type": "ListItem", "position": 1, "url": "https://www\.inwardpro\.com/[^"]+" \}(?:,\n      \{ "@type": "ListItem", "position": \d+, "url": "https://www\.inwardpro\.com/[^"]+" \})*',
           lambda m: "\n" + ",\n".join('      { "@type": "ListItem", "position": %d, "url": "%s/%s/" }' % (i + 1, DOM, c["url"]) for i, c in enumerate(cards)), s, count=1)
s = s.replace("<!-- Articulos migrados del sitio anterior (URL en la raiz). Generado con tools/articles. -->", "<!-- Articulos por cluster tematico. Generado con tools/articles/clusters.py. -->")
open(p, "w", encoding="utf-8").write(s)

# home: los 3 pilares
p = "index.html"; s = open(p, encoding="utf-8").read()
a0 = s.index('    <div class="arts">')
arts = list(re.finditer(r'      <article class="art.*?</article>\n', s[a0:], re.S))
piliers = [c for c in cards if c["role"] == "pilier"]
s = s[:a0 + arts[0].start()] + "\n".join(card(c, i, "", cats=False) for i, c in enumerate(piliers)) + "\n" + s[a0 + arts[-1].end():]
open(p, "w", encoding="utf-8").write(s)
print(len(cards), "articulos;", [c["url"] for c in cards])
