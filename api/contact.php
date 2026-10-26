<?php
/**
 * Formulaire de contact d'INWARD.
 *
 * Reçoit la demande du formulaire (JSON), la vérifie et l'envoie par e-mail à
 * l'équipe. Le navigateur affiche ensuite le lien Calendly pour réserver le
 * créneau, avec le nom et l'e-mail déjà remplis.
 *
 * Configuration dans api/config.php (non versionné) :
 *   contact_to   : adresse(s) qui reçoivent les demandes, séparées par des
 *                  virgules.
 *   contact_from : adresse d'expédition, sur le domaine du site (ex.
 *                  no-reply@inwardpro.com) pour ne pas tomber en spam.
 *                  L'adresse du visiteur va en Reply-To : « Répondre »
 *                  répond directement à la personne.
 *
 * Anti-spam : champ piège invisible (« site ») et délai minimal de remplissage.
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function fin(int $code, array $data): void
{
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    fin(405, ['ok' => false, 'error' => 'method']);
}

$cfgFile = __DIR__ . '/config.php';
$cfg = is_file($cfgFile) ? (array)require $cfgFile : [];
$to = trim((string)($cfg['contact_to'] ?? ''));
$from = trim((string)($cfg['contact_from'] ?? ''));
if ($to === '' || $from === '') {
    fin(503, ['ok' => false, 'error' => 'not_configured']);
}

$in = json_decode((string)file_get_contents('php://input'), true);
if (!is_array($in)) {
    fin(400, ['ok' => false, 'error' => 'format']);
}

/* Robots : le champ piège est rempli, ou le formulaire a été envoyé en
   moins de trois secondes. On répond « ok » sans rien envoyer. */
if (trim((string)($in['site'] ?? '')) !== '' || (int)($in['t'] ?? 0) < 3000) {
    fin(200, ['ok' => true]);
}

function champ(array $in, string $k, int $max): string
{
    $v = trim((string)($in[$k] ?? ''));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
}

$nom     = champ($in, 'nom', 120);
$mail    = champ($in, 'mail', 160);
$profil  = champ($in, 'profil', 20) === 'entreprise' ? 'Entreprise' : 'Particulier';
$societe = champ($in, 'societe', 160);
$dem     = champ($in, 'dem', 120);
$canal   = champ($in, 'canal', 120);
$msg     = champ($in, 'msg', 4000);
$page    = champ($in, 'page', 200);

if ($nom === '' || !filter_var($mail, FILTER_VALIDATE_EMAIL)) {
    fin(422, ['ok' => false, 'error' => 'champs']);
}
/* Pas de retour à la ligne dans ce qui va dans les en-têtes. */
$nomEntete = preg_replace('/[\r\n]+/', ' ', $nom);

$sujet = 'Nouvelle demande de contact : ' . $nomEntete . ' (' . $profil . ')';
$corps = "Nouvelle demande reçue depuis le site INWARD.\n\n"
    . "Nom et prénom : $nom\n"
    . "Email : $mail\n"
    . "Profil : $profil\n"
    . ($profil === 'Entreprise' ? "Entreprise : $societe\n" : '')
    . "Démarche : $dem\n"
    . "Comment nous avez-vous connus ? $canal\n\n"
    . "Situation :\n$msg\n\n"
    . "Page : $page\n"
    . "Date : " . date('d/m/Y H:i') . "\n\n"
    . "La personne va maintenant choisir un créneau sur Calendly.\n";

$entetes = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'From: INWARD <' . $from . '>',
    'Reply-To: ' . $nomEntete . ' <' . $mail . '>',
    'X-Mailer: inwardpro.com',
];

$ok = mail(
    $to,
    '=?UTF-8?B?' . base64_encode($sujet) . '?=',
    $corps,
    implode("\r\n", $entetes),
    '-f' . $from
);

fin($ok ? 200 : 500, ['ok' => $ok]);
