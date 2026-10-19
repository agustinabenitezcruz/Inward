#!/usr/bin/env python3
"""Pone ?v=<hash> en los links a styles.css y main.js de todos los HTML.
Asi el navegador nunca sirve una version vieja del CSS o del JS cacheada."""
import hashlib, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent

def firma(rel):
    f = RAIZ / rel
    return hashlib.sha1(f.read_bytes()).hexdigest()[:8] if f.exists() else "0"

VCSS = firma("assets/css/styles.css")
VJS  = firma("assets/js/main.js")

PAT = re.compile(r'((?:\.\./)*assets/(?:css/styles\.css|js/main\.js))(\?v=[0-9a-f]+)?')

def sello(m):
    return m.group(1) + "?v=" + (VCSS if m.group(1).endswith(".css") else VJS)

n = 0
for h in RAIZ.rglob("*.html"):
    if ".git" in h.parts:
        continue
    s = h.read_text(encoding="utf-8")
    t = PAT.sub(sello, s)
    if t != s:
        h.write_text(t, encoding="utf-8")
        n += 1
print(f"sellados {n} archivos  css={VCSS} js={VJS}")
