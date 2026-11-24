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
    {"dir": "ressources",         "title": "Blog"},
    {"dir": "videos",       "title": "Vidéos", "noindex": True},  # oculta: sin enlaces, solo por URL
    {"dir": "videos/presentation-inward-palais-garnier",
     "title": "Vidéo : INWARD devant le Palais Garnier", "noindex": True},  # oculta
    {"dir": "qui-sommes-nous", "title": "Qui sommes-nous"},
    {"dir": "visas/talent", "title": "Landing Visa Talent",
     "contact_lead": "Vous souhaitez savoir si votre profil ou celui de votre collaborateur correspond à l'une des catégories de la carte de séjour «&nbsp;talent&nbsp;»&nbsp;? Contactez notre équipe pour bénéficier d'une première évaluation de votre situation."},
    {"dir": "visas/salarie-travailleur-temporaire", "title": "Landing Visa Salarié / Travailleur temporaire"},
    {"dir": "visas/saisonnier", "title": "Landing Visa Saisonnier"},
    {"dir": "visas/famille", "title": "Landing Visa Famille"},
    {"dir": "visas/entrepreneur", "title": "Landing Visa Entrepreneur"},
    {"dir": "visas/etudiant", "title": "Landing Visa Étudiant"},
    {"dir": "visas/rece", "title": "Landing Visa RECE"},
    {"dir": "visas/pvt", "title": "Landing Visa PVT"},
    {"dir": "visas/stagiaire", "title": "Landing Visa Stagiaire"},
    {"dir": "visas/detachement", "title": "Landing Détachement"},
    {"dir": "visas/schengen", "title": "Landing Visa Schengen"},
    {"dir": "visas/visiteur", "title": "Landing Visa Visiteur"},
    # Articulos del sitio anterior: URL exacta en la raiz, solo en frances.
    {"dir": "embaucher-etudiant-etranger", "title": "Article : Embaucher un étudiant étranger : Tout savoir", "fr_only": True},
    {"dir": "jeune-entreprise-innovante", "title": "Article : L'Histoire Réussie d'une Jeune Entreprise Innovante", "fr_only": True},
    {"dir": "carte-de-resident-inward", "title": "Article : La carte de résident de 10 ans", "fr_only": True},
    {"dir": "embaucher-un-etudiant-etranger", "title": "Article : Embaucher un étudiant étranger après ses études en France, c'est possible !", "fr_only": True},
    {"dir": "comment-une-entreprise-dingenierie-a-reussi-a-recruter-3-employes-etrangers-en-france", "title": "Article : Comment une entreprise d'ingénierie a réussi à recruter 3 employés étrangers en France", "fr_only": True},
    {"dir": "de-stagiaire-a-salariee-en-cdi-lhistoire-reussie-dune-start-up-francaise", "title": "Article : De Stagiaire à Salariée en CDI – L'Histoire Réussie d'une Start-up Française", "fr_only": True},
    {"dir": "la-cuisiniere-argentine-dun-restaurant-parisien", "title": "Article : La Cuisinière Argentine d'un Restaurant Parisien", "fr_only": True},
    {"dir": "comment-une-start-up-francaise-a-securise-la-situation-de-ses-employes-etrangers", "title": "Article : Comment une start-up française a sécurisé la situation de ses employés étrangers", "fr_only": True},
    {"dir": "comment-embaucher-un-etudiant-apres-ses-etudes", "title": "Article : Comment embaucher un étudiant après ses études?", "fr_only": True},
    {"dir": "types-de-contrat-etidiant-etranger", "title": "Article : Types de contrat disponibles pour un étudiant étranger", "fr_only": True},
    {"dir": "embaucher-salarie-vvt", "title": "Article : Puis-je embaucher un employé qui a un visa VVT ?", "fr_only": True},
    {"dir": "comment-faire-un-chengement-de-statut-apres-un-visa-vvt", "title": "Article : Comment faire un changement de statut après un visa VVT ?", "fr_only": True},
    {"dir": "comment-embaucher-un-salarie-etranger", "title": "Article : Comment faire pour embaucher un salarié étranger ?", "fr_only": True},
    {"dir": "erreurs-a-eviter-lors-de-lembauche-des-salaries-etrangers", "title": "Article : Erreurs à éviter lors de l'embauche de salariés étrangers", "fr_only": True},
    {"dir": "comment-obtenir-laide-a-la-mobilite-internationale", "title": "Article : Comment obtenir l'aide à la mobilité internationale ?", "fr_only": True},
    {"dir": "guide-pour-obtenir-un-autorisation-de-travail", "title": "Article : Le guide ultime pour obtenir un permis de travail pour votre employé étranger", "fr_only": True},
    {"dir": "cout-pour-recruter-un-salarie-etranger", "title": "Article : Coût pour recruter un salarié étranger", "fr_only": True},
    {"dir": "adaptation-culturelle-travailleurs-etrangers", "title": "Article : L'importance de l'adaptation culturelle pour les travailleurs étrangers", "fr_only": True},
    {"dir": "avantages-dembaucher-un-salarie-etranger", "title": "Article : Avantages et inconvénients de l'embauche de travailleurs étrangers", "fr_only": True},
    {"dir": "mentions-legales", "title": "Mentions légales"},
    {"dir": "confidentialite", "title": "Politique de confidentialité"},
    {"dir": "cookies", "title": "Politique de cookies"},
    {"dir": "cgv", "title": "Conditions générales de vente"},
]

# Prioridad y frecuencia del sitemap. No son una orden para Google, son una
# pista; se escriben igual porque no cuestan nada y dejan el criterio escrito.
SITEMAP = {
    "":             (1.0, "weekly"),
    "entreprises":  (0.9, "monthly"),
    "particuliers": (0.9, "monthly"),
    "ressources":   (0.8, "weekly"),
    "videos":       (0.5, "monthly"),
    "mentions-legales": (0.2, "yearly"),
    "confidentialite": (0.2, "yearly"),
    "cookies": (0.2, "yearly"),
    "cgv": (0.2, "yearly"),
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


def fr_only(page):
    """Pagina solo en frances (articulos migrados del sitio anterior)."""
    return bool(page.get("fr_only"))


def indexable(page):
    return not page.get("noindex")


def sitemap_hint(d):
    return SITEMAP.get(d, SITEMAP_DEFAULT)
