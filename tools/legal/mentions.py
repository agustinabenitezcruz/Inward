# -*- coding: utf-8 -*-
"""Genera /mentions-legales/ (version provisoria con el texto de la clienta)."""
import sys, os, json
sys.path.insert(0, 'tools')
from newpage import write

D = "mentions-legales"
U = "https://inwardpro.com/%s/" % D
title = "Mentions légales | INWARD"
desc = "Mentions légales du site INWARD : éditeur, directrice de la publication, hébergement, activité, propriété intellectuelle et responsabilité."
jsonld = json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": U + "#webpage", "url": U, "name": "Mentions légales", "inLanguage": "fr",
     "isPartOf": {"@id": "https://inwardpro.com/#website"}, "about": {"@id": "https://inwardpro.com/#organization"},
     "dateModified": "2026-11-19",
     "breadcrumb": {"@id": U + "#breadcrumb"}},
    {"@type": "BreadcrumbList", "@id": U + "#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://inwardpro.com/"},
        {"@type": "ListItem", "position": 2, "name": "Mentions légales", "item": U}]}]},
    ensure_ascii=False, indent=2)

def bloc(lines): return "<p>" + "<br>\n      ".join(lines) + "</p>"

body = f'''<!-- Aviso legal PROVISORIO con el texto de la clienta (19/11/2026).
     Falta: domicilio social y SIRET nuevos tras el traslado (hoy en lorem
     ipsum / SIRET actual), y revisar los datos de o2switch. -->
<header class="band pg-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane">
      <a href="../">Accueil</a> <span aria-hidden="true">/</span>
      <span aria-current="page">Mentions légales</span>
    </nav>
    <h1>Mentions légales</h1>
    <p class="lead">Dernière mise à jour : 19 novembre 2026</p>
  </div>
</header>

<section class="band sec" id="texte">
  <div class="wrap art-body legal">
    <h2>Éditeur du site</h2>
    <p>Le présent site est édité par :</p>
    {bloc(["<strong>INWARD</strong>", "SARL au capital de 1 000 €", "Siège social : Lorem ipsum dolor sit amet", "SIREN : 981 066 145", "SIRET : 981 066 145 00013", "RCS : Paris", "TVA intracommunautaire : FR03981066145", 'Téléphone : <a href="tel:+33752117887">+33 7 52 11 78 87</a>', 'E-mail : <a href="mailto:info@inwardpro.com">info@inwardpro.com</a>'])}

    <h2>Directrice de la publication</h2>
    <p>Delfina Benitez Cruz.</p>

    <h2>Hébergement</h2>
    {bloc(["<strong>o2switch</strong>", "SAS au capital de 100 000 €", "SIRET : 510 909 807 00032", "RCS : Clermont-Ferrand", "Chemin des Pardiaux", "63000 Clermont-Ferrand, France", 'Téléphone : <a href="tel:+33444446040">+33 4 44 44 60 40</a>'])}

    <h2>Activité</h2>
    <p>INWARD propose un accompagnement administratif et opérationnel aux entreprises et aux particuliers dans leurs démarches d'immigration, de mobilité internationale et d'installation en France, notamment les visas, titres de séjour, autorisations de travail, regroupement familial, naturalisation, accès à la Sécurité sociale, numéro fiscal, ouverture de compte bancaire et reconnaissance ou échange du permis de conduire.</p>
    <p>INWARD n'est pas un cabinet d'avocats et ne fournit pas de représentation juridique devant les tribunaux. Les décisions relèvent exclusivement des autorités compétentes. INWARD ne garantit pas l'issue d'une procédure.</p>

    <h2>Propriété intellectuelle</h2>
    <p>Les textes, images, logos, vidéos, graphismes, icônes et éléments de structure présents sur le site sont protégés par les règles applicables en matière de propriété intellectuelle. Toute reproduction ou diffusion non autorisée est interdite, sauf exceptions prévues par la loi.</p>

    <h2>Responsabilité</h2>
    <p>Les informations publiées sont générales et peuvent évoluer. Elles ne constituent pas un avis juridique individualisé. L'utilisateur doit vérifier les exigences applicables à sa situation avant toute démarche.</p>

    <h2>Contact</h2>
    <p>Pour toute question : <a href="mailto:info@inwardpro.com">info@inwardpro.com</a> ou <a href="tel:+33752117887">+33 7 52 11 78 87</a>.</p>
  </div>
</section>'''

rail = '  <a href="#top" aria-label="Haut de page"><span></span></a>'
write(D, title, desc, jsonld, body, rail)
p = os.path.join(D, "index.html")
s = open(p, encoding="utf-8").read().replace("<!-- shell:contact --><!-- /shell:contact -->\n", "")
open(p, "w", encoding="utf-8").write(s)
