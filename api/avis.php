<?php
/**
 * Avis Google pour INWARD.
 *
 * La page n'appelle jamais Google : elle appelle ce fichier. La clé reste
 * côté serveur et ne descend jamais dans le navigateur. Aucune session,
 * aucun cookie, aucun script tiers sur la page (CNIL).
 *
 * Trois niveaux, dans cet ordre :
 *   1. cache local encore valide  -> servi tel quel, sans appel réseau
 *   2. appel à l'API Places       -> filtré, trié, mis en cache
 *   3. échec de Google            -> dernière copie connue, même périmée
 * Et si rien n'est configuré, content/avis.json prend le relais : des avis
 * réels recopiés à la main, pour que la section ne soit jamais vide.
 *
 * Mise en cache : la politique Places interdit de conserver le contenu des
 * avis au-delà de ce qu'exige la performance. TTL court volontairement, et
 * aucune accumulation d'un historique d'avis. Le place ID, lui, peut être
 * conservé sans limite : c'est l'exception explicite de la politique.
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=900');

/** Avis recopiés à la main, utilisés tant que l'API n'est pas configurée. */
function secours(): void
{
    $f = dirname(__DIR__) . '/content/avis.json';
    if (is_file($f)) {
        $j = json_decode((string)file_get_contents($f), true);
        if (is_array($j)) {
            $j['source'] = 'manuel';
            echo json_encode($j, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
            exit;
        }
    }
    http_response_code(503);
    echo json_encode(['error' => 'not_configured']);
    exit;
}

$cfgFile = __DIR__ . '/config.php';
if (!is_file($cfgFile)) {
    secours();
}
$cfg = require $cfgFile;

$placeId = trim((string)($cfg['place_id'] ?? ''));
$apiKey  = trim((string)($cfg['api_key']  ?? ''));
$ttl     = (int)($cfg['ttl'] ?? 3600);
$lang    = $cfg['language'] ?? 'fr';
$noteMin = (float)($cfg['note_min'] ?? 4);   // on n'affiche pas les avis tièdes
$max     = (int)($cfg['max'] ?? 6);

if ($placeId === '' || $apiKey === '') {
    secours();
}

$cacheFile = sys_get_temp_dir() . '/inward-avis-' . md5($placeId . $lang) . '.json';

if (is_file($cacheFile) && (time() - filemtime($cacheFile)) < $ttl) {
    readfile($cacheFile);
    exit;
}

$url = 'https://places.googleapis.com/v1/places/' . rawurlencode($placeId)
     . '?languageCode=' . rawurlencode($lang);

$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 8,
    CURLOPT_HTTPHEADER     => [
        'X-Goog-Api-Key: ' . $apiKey,
        // Uniquement les champs affichés : chaque champ en plus est facturé.
        'X-Goog-FieldMask: rating,userRatingCount,googleMapsUri,reviews',
    ],
]);
$raw  = curl_exec($ch);
$code = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

// Google en panne : on sert la dernière copie plutôt qu'une section vide.
if ($raw === false || $code !== 200) {
    if (is_file($cacheFile)) { readfile($cacheFile); exit; }
    secours();
}

$data = json_decode((string)$raw, true);
$out = [
    'rating'  => $data['rating'] ?? null,
    'count'   => $data['userRatingCount'] ?? null,
    'mapsUri' => $data['googleMapsUri'] ?? null,
    'source'  => 'google',
    'reviews' => [],
];

foreach (($data['reviews'] ?? []) as $r) {
    $note = (float)($r['rating'] ?? 0);
    if ($note < $noteMin) {
        continue;                       // on ne relaie que les avis positifs
    }
    $texte = $r['originalText']['text'] ?? ($r['text']['text'] ?? '');
    if (trim($texte) === '') {
        continue;                       // une note sans texte n'a rien à dire
    }
    $out['reviews'][] = [
        'author' => $r['authorAttribution']['displayName'] ?? '',
        'photo'  => $r['authorAttribution']['photoUri'] ?? '',
        'uri'    => $r['authorAttribution']['uri'] ?? ($r['googleMapsUri'] ?? ''),
        'rating' => $note,
        'when'   => $r['relativePublishTimeDescription'] ?? '',
        'time'   => $r['publishTime'] ?? '',
        'text'   => $texte,
    ];
}

// Les plus récents d'abord : l'API ne garantit aucun ordre chronologique.
usort($out['reviews'], static fn($a, $b) => strcmp((string)$b['time'], (string)$a['time']));
$out['reviews'] = array_slice($out['reviews'], 0, $max);

// Aucun avis positif avec texte : plutôt qu'un bloc vide, on bascule sur les
// avis recopiés à la main.
if (!$out['reviews']) {
    secours();
}

$json = json_encode($out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
@file_put_contents($cacheFile, $json, LOCK_EX);
echo $json;
