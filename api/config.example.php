<?php
/**
 * Copier en config.php et compléter. config.php ne se versionne pas et n'est
 * pas servi par le web (voir .htaccess).
 *
 * La fiche Google d'INWARD a pour CID 1377371409426816352
 * (https://www.google.com/maps?cid=1377371409426816352). Le place_id se
 * récupère à partir de cette fiche :
 * https://developers.google.com/maps/documentation/places/web-service/place-id
 * Le place ID peut être conservé sans limite de durée : c'est l'exception
 * explicite de la politique Places.
 *
 * api_key  : clé Places API (New). Dans la console Google Cloud, la
 *            restreindre à l'adresse IP du serveur O2Switch, PAS au domaine :
 *            ici l'appel part du serveur, pas du navigateur.
 * note_min : note minimale affichée. 4 = on ne relaie que les avis positifs.
 * max      : nombre d'avis affichés. L'API en renvoie 5 au maximum.
 * ttl      : secondes de cache. Court volontairement (politique Places).
 *
 * Formulaire de contact (api/contact.php) :
 * contact_to   : adresse(s) qui reçoivent les demandes, séparées par des
 *                virgules.
 * contact_from : adresse d'expédition sur le domaine du site (à créer dans
 *                O2Switch, ex. no-reply@inwardpro.com).
 */
return [
    'place_id' => '',
    'api_key'  => '',
    'ttl'      => 3600,
    'language' => 'fr',
    'note_min' => 4,
    'max'      => 6,
    'contact_to'   => '',
    'contact_from' => '',
];
