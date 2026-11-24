# -*- coding: utf-8 -*-
"""Paginas legales provisorias (texto de la clienta, 19/11/2026):
confidentialite, cookies y cgv. Los campos que faltan van en lorem ipsum."""
import sys, os, json
sys.path.insert(0, 'tools')
from newpage import write

MAIL = '<a href="mailto:info@inwardpro.com">info@inwardpro.com</a>'
TEL = '<a href="tel:+33752117887">+33 7 52 11 78 87</a>'

def ul(items): return '<ul>\n' + '\n'.join('      <li>%s</li>' % i for i in items) + '\n    </ul>'
def p(t): return '<p>%s</p>' % t

PAGES = {
"confidentialite": dict(
  title="Politique de confidentialité | INWARD", h1="Politique de confidentialité", crumb="Politique de confidentialité",
  desc="Politique de confidentialité d'INWARD : données collectées, finalités, bases juridiques, destinataires, durées de conservation et exercice de vos droits.",
  secs=[
   ("1. Responsable du traitement", [
     p("Le responsable du traitement est INWARD, SARL au capital de 1 000 €, dont le siège social est situé Lorem ipsum dolor sit amet, immatriculée au RCS de Paris sous le numéro 981 066 145. Contact : %s." % MAIL),
     p("INWARD n'a pas désigné de délégué à la protection des données. Les demandes relatives aux données personnelles sont traitées à l'adresse %s." % MAIL)]),
   ("2. Données collectées", [
     p("Selon votre utilisation du site, nous pouvons collecter votre nom et prénom, adresse e-mail, nom de votre entreprise, profil (entreprise ou particulier), type de démarche, manière dont vous avez connu INWARD et les informations contenues dans votre message. Le formulaire public ne doit pas être utilisé pour transmettre des documents d'identité ou des pièces sensibles.")]),
   ("3. Finalités et bases juridiques", [
     ul(["Répondre à une demande de contact ou de devis : mesures précontractuelles.",
         "Organiser un rendez-vous via Calendly : mesures précontractuelles ou exécution du contrat.",
         "Gérer la relation client et les prestations : exécution du contrat.",
         "Émettre et conserver les factures : obligation légale.",
         "Envoyer une newsletter : consentement préalable.",
         "Mesurer l'audience avec Google Analytics 4, si activé : consentement préalable.",
         "Afficher des vidéos YouTube ou des avis Google Business Profile : consentement lorsque la technologie utilisée le requiert."])]),
   ("4. Destinataires et sous-traitants", [
     p("Les données peuvent être accessibles aux membres autorisés de l'équipe INWARD et à des prestataires techniques, notamment o2switch, Gmail ou les services Google, Monday.com, Calendly, Mollie, Google, YouTube et Lorem ipsum (newsletter).")]),
   ("5. Transferts internationaux", [
     p("Certains prestataires peuvent traiter des données en dehors de l'Espace économique européen. Lorsque cela est nécessaire, INWARD vérifie l'existence d'un mécanisme de transfert reconnu et de garanties appropriées conformément au RGPD.")]),
   ("6. Durées de conservation", [
     ul(["Demandes de contact sans contrat : 3 ans à compter du dernier contact.",
         "Données clients et dossiers : pendant la relation contractuelle, puis pendant la durée nécessaire au respect des obligations légales et à la défense des droits d'INWARD.",
         "Données de facturation : 10 ans lorsque la loi l'exige.",
         "Newsletter : jusqu'au retrait du consentement ou à la désinscription.",
         "Consentements cookies : selon l'outil de gestion du consentement utilisé et les recommandations applicables."])]),
   ("7. Vos droits", [
     p("Vous pouvez demander l'accès, la rectification, l'effacement, la limitation, la portabilité lorsque ce droit est applicable, ou vous opposer à certains traitements. Vous pouvez retirer votre consentement à tout moment. Contact : %s." % MAIL),
     p('Vous pouvez également saisir la CNIL, 3 place de Fontenoy, TSA 80715, 75334 Paris Cedex 07, ou <a href="https://www.cnil.fr/" target="_blank" rel="noopener">www.cnil.fr</a>.')]),
   ("8. Sécurité et mise à jour", [
     p("INWARD met en œuvre des mesures raisonnables de sécurité et limite les accès aux personnes et prestataires qui en ont besoin. La présente politique peut être mise à jour, la date figurant en haut de la page.")]),
  ]),
"cookies": dict(
  title="Politique de cookies | INWARD", h1="Politique de cookies", crumb="Politique de cookies",
  desc="Politique de cookies d'INWARD : cookies nécessaires, services tiers (Google, YouTube, Calendly, LinkedIn, Mollie) et gestion de vos choix.",
  secs=[
   ("1. Fonctionnement", [
     p("Un cookie est un fichier ou identifiant susceptible d'être enregistré sur votre terminal. Les cookies nécessaires peuvent être utilisés sans consentement lorsqu'ils sont indispensables au fonctionnement du site. Les autres cookies nécessitent votre consentement préalable.")]),
   ("2. Cookies et services envisagés", [
     p("Sous réserve de leur activation effective, les services concernés peuvent inclure Google Analytics 4 et Google Tag Manager pour la mesure d'audience, YouTube pour les vidéos, Google Business Profile pour l'affichage des avis et Lorem ipsum pour la newsletter.")]),
   ("3. Calendly, LinkedIn et Mollie", [
     p("Calendly, LinkedIn et Mollie sont actuellement utilisés par liens ou boutons externes. Le site ne charge pas leur contenu avant le clic. Leurs propres politiques s'appliquent lorsque l'utilisateur accède à leurs services.")]),
   ("4. Google et YouTube", [
     p("Les vidéos YouTube et les avis Google Business Profile peuvent impliquer une connexion à Google. Si la technologie utilisée dépose des cookies ou traite des données non nécessaires, elle est bloquée jusqu'au consentement.")]),
   ("5. Gestion des choix", [
     p("Une bannière permet d'accepter, de refuser ou de personnaliser les cookies non nécessaires. Un lien « Gérer mes cookies » reste disponible dans le pied de page.")]),
  ]),
"cgv": dict(
  title="Conditions générales de vente | INWARD", h1="Conditions générales de vente", crumb="Conditions générales de vente",
  desc="Conditions générales de vente d'INWARD pour les clients professionnels et les particuliers : commande, prix, paiement, rétractation, réclamations et droit applicable.",
  secs=[
   ("Clients professionnels", None),
   ("1. Objet et services", [p("Les présentes conditions s'appliquent aux prestations d'accompagnement administratif et opérationnel fournies par INWARD à des clients professionnels. Le périmètre exact est défini dans le devis accepté.")]),
   ("2. Commande et prix", [p("La commande devient définitive après acceptation écrite du devis et, lorsque cela est prévu, paiement. Les prix professionnels sont indiqués hors taxes. La TVA applicable est ajoutée conformément à la réglementation.")]),
   ("3. Paiement", [p("Le paiement intégral est exigible avant le début de la prestation, sauf accord particulier écrit. Le paiement peut être effectué par virement bancaire ou par lien Mollie.")]),
   ("4. Obligations et absence de garantie", [p("Le client doit fournir des informations exactes, complètes et dans les délais. INWARD est tenue à une obligation de moyens. Les décisions administratives appartiennent aux autorités compétentes et aucun résultat ne peut être garanti.")]),
   ("5. Annulation et remboursement", [p("En cas d'annulation, tout remboursement éventuel est calculé selon la partie de la prestation qui n'a pas encore été réalisée, sous réserve du devis et des frais déjà engagés.")]),
   ("6. Retard de paiement", [p("Tout retard entraîne l'application des pénalités prévues par la réglementation et de l'indemnité forfaitaire légale de 40 euros pour frais de recouvrement.")]),
   ("7. Réclamations et droit applicable", [p("Les réclamations sont adressées à %s. Les présentes conditions sont soumises au droit français. Pour les clients professionnels, les juridictions compétentes sont celles déterminées par les règles applicables." % MAIL)]),
   ("Particuliers", None),
   ("1. Objet et prestations", [p("Ces conditions encadrent les prestations fournies par INWARD aux particuliers : visas, titres de séjour, changement de statut, renouvellement, naturalisation, nationalité, aide administrative, mobilité internationale et installation en France.")]),
   ("2. Prix et paiement", [p("Les prix sont indiqués toutes taxes comprises. Le paiement intégral est exigible avant le début de la prestation, sauf accord écrit. Le paiement est possible par virement bancaire ou lien Mollie.")]),
   ("3. Droit de rétractation", [p("Lorsque le contrat est conclu à distance, le client dispose en principe de quatorze jours pour se rétracter, sauf exception légale. Si le client demande expressément le début avant la fin de ce délai, il peut devoir payer la partie déjà réalisée. En cas d'exécution complète avant la fin du délai, avec accord exprès et reconnaissance de la perte du droit de rétractation, ce droit peut ne plus être exercé dans les conditions prévues par la loi.")]),
   ("4. Obligations et résultat", [p("Le client fournit des informations exactes et les documents nécessaires. INWARD est tenue à une obligation de moyens et ne garantit pas l'obtention d'un visa, titre, autorisation ou autre décision administrative.")]),
   ("5. Annulation et réclamation", [p("En cas d'annulation, le remboursement est calculé selon la partie de la prestation non réalisée, sous réserve des droits du consommateur. Toute réclamation doit d'abord être adressée à %s." % MAIL)]),
   ("6. Médiation de la consommation", [p("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")]),
   ("7. Droit applicable", [p("Les présentes conditions sont soumises au droit français, sous réserve des règles protectrices applicables aux consommateurs.")]),
   ("Formulaire de rétractation", None),
   ("", [p("À utiliser lorsque le droit de rétractation est applicable."),
         p("À l'attention de :<br>\n      <strong>INWARD</strong><br>\n      Lorem ipsum dolor sit amet<br>\n      %s" % MAIL),
         p("Je vous notifie par la présente ma rétractation du contrat portant sur la prestation suivante :"),
         p("Description : ______________________________<br>\n      Contrat accepté le : ________________________<br>\n      Nom du client : _____________________________<br>\n      Adresse : __________________________________<br>\n      E-mail : ___________________________________<br>\n      Date : ____________________________________"),
         p("Signature, uniquement en cas de notification papier :")]),
  ]),
}

for d, c in PAGES.items():
    U = "https://inwardpro.com/%s/" % d
    jsonld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": U + "#webpage", "url": U, "name": c["h1"], "inLanguage": "fr",
         "isPartOf": {"@id": "https://inwardpro.com/#website"}, "about": {"@id": "https://inwardpro.com/#organization"},
         "dateModified": "2026-11-19", "breadcrumb": {"@id": U + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": U + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://inwardpro.com/"},
            {"@type": "ListItem", "position": 2, "name": c["crumb"], "item": U}]}]}, ensure_ascii=False, indent=2)
    parts = []
    for h, blocks in c["secs"]:
        if blocks is None:
            parts.append('    <h2 class="legal-part">%s</h2>' % h)
            continue
        if h: parts.append('    <h3>%s</h3>' % h)
        parts += ['    ' + b for b in blocks]
    hx = "h3" if any(b is None for _, b in c["secs"]) else "h2"
    inner = "\n".join(parts)
    if hx == "h2": inner = inner.replace("<h3>", "<h2>").replace("</h3>", "</h2>")
    body = '''<!-- Pagina legal PROVISORIA con el texto de la clienta (19/11/2026).
     Lo que falta (domicilio, mediador, newsletter...) va en lorem ipsum. -->
<header class="band pg-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane">
      <a href="../">Accueil</a> <span aria-hidden="true">/</span>
      <span aria-current="page">%s</span>
    </nav>
    <h1>%s</h1>
    <p class="lead">Dernière mise à jour : 19 novembre 2026</p>
  </div>
</header>

<section class="band sec" id="texte">
  <div class="wrap art-body legal">
%s
  </div>
</section>''' % (c["crumb"], c["h1"], inner)
    write(d, c["title"], c["desc"], jsonld, body, '  <a href="#top" aria-label="Haut de page"><span></span></a>')
    f = os.path.join(d, "index.html")
    s = open(f, encoding="utf-8").read().replace("<!-- shell:contact --><!-- /shell:contact -->\n", "")
    open(f, "w", encoding="utf-8").write(s)
