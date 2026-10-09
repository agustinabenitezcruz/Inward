#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resuelve el place ID de la ficha Google de INWARD.

    python3 tools/place_id.py TU_CLAVE_API

Hace falta una sola vez: el place ID es estable y, a diferencia del contenido
de las opiniones, la política de Places permite guardarlo sin límite de
tiempo. El resultado va en api/config.php.

La ficha se identifica por su nombre y ciudad. Si hubiera varias coincidencias
el script las lista todas para poder elegir: el CID de la ficha real es
1377371409426816352 (https://www.google.com/maps?cid=1377371409426816352).
"""
import json, sys, urllib.request

CONSULTA = "INWARD immigration Paris"
CID = "1377371409426816352"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    clave = sys.argv[1].strip()
    consulta = sys.argv[2] if len(sys.argv) > 2 else CONSULTA

    req = urllib.request.Request(
        "https://places.googleapis.com/v1/places:searchText",
        data=json.dumps({"textQuery": consulta, "languageCode": "fr"}).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": clave,
            "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("Google respondió %s:\n%s" % (e.code, e.read().decode()[:600]))

    sitios = data.get("places") or []
    if not sitios:
        sys.exit("Sin resultados para %r. Probá con otra consulta:\n"
                 "    python3 tools/place_id.py CLAVE \"otro nombre, ciudad\"" % consulta)

    print("Ficha esperada: https://www.google.com/maps?cid=%s\n" % CID)
    for s in sitios:
        print("  place_id : %s" % s.get("id", ""))
        print("  nombre   : %s" % (s.get("displayName", {}) or {}).get("text", ""))
        print("  dirección: %s" % s.get("formattedAddress", ""))
        print("  nota     : %s (%s avis)\n" % (s.get("rating", "—"), s.get("userRatingCount", "—")))

    print("Copiá el place_id correcto en api/config.php.")


if __name__ == "__main__":
    sys.exit(main())
