# -*- coding: utf-8 -*-
"""Articulos del sitio anterior (WordPress), migrados con su URL EXACTA en la
raiz (inwardpro.com/<slug>/) para conservar el ranking. Texto tal cual del
sitio viejo (articulos_viejos.json). Solo en frances: el sitio viejo no tenia
EN/ES y estas paginas llevan "fr_only" en tools/pages.py.
Los articulos NUEVOS van en /ressources/<slug>/."""
import sys, os, json, re, html, datetime
sys.path.insert(0, 'tools')
from newpage import write

DOM = "https://www.inwardpro.com"
DATA = json.load(open(os.path.join(os.path.dirname(__file__), "articulos_viejos.json"), encoding="utf-8"))

CATS = {"etude-de-cas": "Étude de cas", "professionnel": "Visa / titre de séjour professionnel",
        "famille": "Visas famille", "independant": "Visa / titre de séjour indépendant",
        "etudiant": "Visa / titre de séjour étudiant", "renouvellement": "Renouvellement",
        "changement-de-statut": "Changement de statut", "long-sejour": "Visa long séjour",
        "court-sejour": "Visa court séjour"}

IMG = {
 "equipe-internationale-bureau-adaptation-culturelle": (1400, 788, "Équipe internationale travaillant ensemble dans un bureau"),
 "equipe-multiculturelle-reunion-travail": (874, 1200, "Équipe multiculturelle en réunion de travail autour d'une table"),
 "personne-remplit-documents-bureau": (1400, 934, "Personne remplissant des documents administratifs à un bureau"),
 "consultante-inward-entretien-salarie-etranger": (1400, 933, "Consultante INWARD en entretien avec un salarié étranger autour d'une table"),
 "visa-pvt-voyage": None,
 "avion-mobilite-internationale-nuages": (1400, 930, "Aile d'avion au-dessus des nuages au coucher du soleil"),
 "collegues-echange-ordinateur-bureau": (1400, 934, "Collègues échangeant autour d'un ordinateur dans un bureau"),
 "consultante-inward-atelier-groupe-tableau-blanc": (1400, 933, "Consultante INWARD animant un atelier au tableau blanc devant un groupe autour d'une table"),
 "signature-documents-autorisation-de-travail": (1400, 934, "Signature de documents de travail sur une table de réunion"),
 "equipe-inward-echange-ordinateurs-portables": (1400, 933, "Échange entre l'équipe INWARD et deux jeunes professionnels autour d'ordinateurs portables"),
 "consultantes-inward-travail-ordinateur-equipe": (1400, 933, "Consultantes INWARD travaillant sur un ordinateur avec un collègue autour d'une table"),
 "professionnelle-recoit-document-bureau": (1400, 934, "Professionnelle souriante recevant un document dans un bureau lumineux"),
 "reunion-equipe-inward-ordinateurs-tableau-blanc": (1400, 933, "Réunion de travail de l'équipe INWARD autour d'une table avec ordinateurs portables et tableau blanc"),
 "visa-stagiaire-tuteur": (800, 1066, "Stagiaire accompagné par son tuteur devant un ordinateur portable"),
 "consultante-inward-entretien-cliente-canape": (1400, 933, "Consultante INWARD en entretien avec une cliente qui prend des notes sur un canapé"),
 "dossier-titre-de-sejour-en-preparation": (1400, 933, "Dossier de demande de titre de séjour en préparation"),
 "entretien-deux-personnes-ordinateur-portable": (1400, 934, "Entretien entre deux personnes devant un ordinateur portable"),
 "fondatrices-inward-delfina-marina-studio": (1400, 1400, "Delfina Benitez Cruz et Marina Biedma, fondatrices d'INWARD"),
}

META = {  # slug: (imagen, categorias)
 "adaptation-culturelle-travailleurs-etrangers": ("equipe-internationale-bureau-adaptation-culturelle", "professionnel"),
 "avantages-dembaucher-un-salarie-etranger": ("equipe-multiculturelle-reunion-travail", "professionnel"),
 "comment-embaucher-un-etudiant-apres-ses-etudes": ("personne-remplit-documents-bureau", "etudiant changement-de-statut"),
 "comment-embaucher-un-salarie-etranger": ("consultante-inward-entretien-salarie-etranger", "professionnel"),
 "comment-faire-un-chengement-de-statut-apres-un-visa-vvt": ("visa-pvt-voyage", "changement-de-statut long-sejour"),
 "comment-obtenir-laide-a-la-mobilite-internationale": ("avion-mobilite-internationale-nuages", "professionnel"),
 "cout-pour-recruter-un-salarie-etranger": ("collegues-echange-ordinateur-bureau", "professionnel"),
 "erreurs-a-eviter-lors-de-lembauche-des-salaries-etrangers": ("consultante-inward-atelier-groupe-tableau-blanc", "professionnel"),
 "guide-pour-obtenir-un-autorisation-de-travail": ("signature-documents-autorisation-de-travail", "professionnel"),
 "types-de-contrat-etidiant-etranger": ("equipe-inward-echange-ordinateurs-portables", "etudiant"),
 "jeune-entreprise-innovante": ("consultantes-inward-travail-ordinateur-equipe", "etude-de-cas"),
 "comment-une-entreprise-dingenierie-a-reussi-a-recruter-3-employes-etrangers-en-france": ("professionnelle-recoit-document-bureau", "etude-de-cas professionnel"),
 "comment-une-start-up-francaise-a-securise-la-situation-de-ses-employes-etrangers": ("reunion-equipe-inward-ordinateurs-tableau-blanc", "etude-de-cas"),
 "de-stagiaire-a-salariee-en-cdi-lhistoire-reussie-dune-start-up-francaise": ("visa-stagiaire-tuteur", "etude-de-cas changement-de-statut"),
 "la-cuisiniere-argentine-dun-restaurant-parisien": ("consultante-inward-entretien-cliente-canape", "etude-de-cas"),
 "carte-de-resident-inward": ("dossier-titre-de-sejour-en-preparation", "renouvellement long-sejour"),
 "embaucher-etudiant-etranger": ("entretien-deux-personnes-ordinateur-portable", "etudiant"),
 "embaucher-un-etudiant-etranger": ("fondatrices-inward-delfina-marina-studio", "etudiant changement-de-statut"),
 "embaucher-salarie-vvt": ("entretien-deux-personnes-ordinateur-portable", "professionnel"),
}
IMG["visa-pvt-voyage"] = None
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def fdate(s):
    d = datetime.date.fromisoformat(s[:10]); return "%d %s %d" % (d.day, MOIS[d.month-1], d.year)

def fix_links(h):
    h = h.replace("https://www.inwardpro.com/passeport-talent-salarie-qualifie/", "../visas/talent/")
    h = h.replace("https://www.inwardpro.com/tout-savoir-sur-la-vtt-visa-vacances-travail/", "../visas/pvt/")
    h = h.replace("https://www.inwardpro.com/limportance-de-ladaptation-culturelle-pour-les-travailleurs-etrangers/", "../adaptation-culturelle-travailleurs-etrangers/")
    h = re.sub(r'href="https?://(?:www\.)?inwardpro\.com/([^"]*)"', lambda m: 'href="../%s"' % m.group(1), h)
    h = re.sub(r'href="(https?://[^"]+)"', r'href="\1" target="_blank" rel="noopener"', h)
    return h

def words(b):
    t = " ".join([x.get("h", "") or " ".join(x.get("items", [])) for x in b])
    return len(re.sub(r"<[^>]+>", " ", t).split())

def body_html(blocks):
    out = []
    for b in blocks:
        if b["t"] == "img" or b["t"] == "table": continue
        if b["t"] in ("ul", "ol"):
            items = [fix_links(i) for i in b["items"] if re.sub(r"<[^>]+>|\s", "", i)]
            if items: out.append("    <%s>\n%s\n    </%s>" % (b["t"], "\n".join("      <li>%s</li>" % i for i in items), b["t"]))
        else:
            h = fix_links(b["h"]).strip()
            if re.sub(r"<[^>]+>|\s", "", h): out.append("    <%s>%s</%s>" % (b["t"], h, b["t"]))
    return "\n".join(out)

def img_of(key):
    if IMG.get(key) is None:
        return (key + ".webp", 800, 1066, "Voyageuse avec son sac à dos regardant le paysage")
    w, h, a = IMG[key]; return (key + ".webp", w, h, a)

CARDS = []
for a in DATA:
    s = a["slug"]
    if s not in META: continue
    import shutil; shutil.rmtree(s, ignore_errors=True)
    key, cats = META[s]
    f, w, h, alt = img_of(key)
    h1 = html.unescape(a["h1"]).replace("’", "'").strip()
    desc = html.unescape(a.get("desc") or "").strip()
    if not desc:
        first = next(re.sub(r"<[^>]+>", "", b["h"]) for b in a["blocks"] if b["t"] == "p")
        desc = html.unescape(first).strip()
        if len(desc) > 155: desc = desc[:desc.rfind(" ", 0, 152)].rstrip(" ,;:") + "…"
    U = "%s/%s/" % (DOM, s)
    kd = CATS[cats.split()[0]]
    mins = max(2, round(words(a["blocks"]) / 200))
    jsonld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": U + "#article", "headline": h1, "description": desc, "url": U,
         "inLanguage": "fr", "datePublished": a["date"], "dateModified": a["mod"],
         "isPartOf": {"@id": DOM + "/ressources/#blog"}, "publisher": {"@id": DOM + "/#organization"},
         "author": {"@id": DOM + "/#organization"}, "image": DOM + "/assets/img/" + f,
         "articleSection": kd},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": DOM + "/"},
            {"@type": "ListItem", "position": 2, "name": "Ressources", "item": DOM + "/ressources/"},
            {"@type": "ListItem", "position": 3, "name": h1, "item": U}]}]}, ensure_ascii=False, indent=2)
    pub, mod = fdate(a["date"]), fdate(a["mod"])
    dates = "Publié le %s" % pub + ("" if pub == mod else " · Mis à jour le %s" % mod)
    body = '''<!-- Articulo del sitio anterior, migrado con su URL exacta (ranking SEO).
     Texto tal cual del original. -->
<article class="band pg-head art-page">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane">
      <a href="../">Accueil</a> <span aria-hidden="true">/</span>
      <a href="../ressources/">Ressources</a> <span aria-hidden="true">/</span>
      <span aria-current="page">%s</span>
    </nav>
    <p class="label">%s</p>
    <h1>%s</h1>
    <p class="lead">%s</p>
    <p class="art-date">%s</p>
  </div>
</article>

<section class="band sec" id="texte">
  <div class="wrap art-body art-old">
    <figure class="art-fig rounded">
      <img src="../assets/img/%s" width="%d" height="%d" alt="%s" decoding="async">
    </figure>
%s
    <p class="art-back"><a href="../ressources/">&lsaquo; Tous les articles</a></p>
  </div>
</section>''' % (h1, kd, h1, desc, dates, f, w, h, alt, body_html(a["blocks"]))
    write(s, h1, desc, jsonld, body, '  <a href="#top" aria-label="Haut de page"><span></span></a>', ogtype="article")
    p = os.path.join(s, "index.html")
    t = open(p, encoding="utf-8").read()
    t = re.sub(r'<link rel="alternate" hreflang="(en|es)"[^>]*>\n', "", t)
    t = t.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="article">\n<meta property="article:published_time" content="%s">\n<meta property="article:modified_time" content="%s">' % (a["date"], a["mod"]))
    open(p, "w", encoding="utf-8").write(t)
    CARDS.append(dict(slug=s, date=a["date"], cats=cats, kd=kd, h1=h1, desc=desc, img=(f, w, h, alt), mins=mins))

json.dump(sorted(CARDS, key=lambda c: c["date"], reverse=True), open(os.path.join(os.path.dirname(__file__), "cards.json"), "w"), ensure_ascii=False, indent=1)
print(len(CARDS), "articulos")
