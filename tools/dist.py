#!/usr/bin/env python3
"""Arma dist/: la version del sitio que se sube a O2Switch.

    python3 tools/dist.py

El repo guarda las fuentes con todos sus comentarios (son la documentacion del
diseno). dist/ es la copia liviana: solo lo que el navegador necesita, sin
herramientas, sin documentos y sin comentarios.

  - HTML: sin comentarios <!-- --> (salvo los condicionales) y sin sangria.
  - CSS: sin comentarios y con los espacios compactados.
  - JS: sin comentarios de bloque ni comentarios de linea completa.
  - Copia tal cual imagenes, video, favicons, manifest, robots, sitemap,
    la API (php) y content/avis.json.

No toca nada fuera de dist/. Correrlo despues de build.py y stamp.py.
"""
import pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

# Lo que NO se publica: herramientas, documentos, fuentes y ruido.
EXCLUIR_DIR = {".git", "dist", "tools", "_fuentes", "__pycache__", ".claude", ".vscode"}
EXCLUIR_ARCH = {"DESIGN.md", "README.md", "build.py", "skills-lock.json", ".gitignore",
                "strings.csv", "config.php"}
EXCLUIR_SUF = {".md", ".py", ".pyc", ".zip"}

def html_min(s):
    s = re.sub(r"<!--(?!\[if).*?-->", "", s, flags=re.S)
    # Sin tocar el contenido de <pre>, <textarea> ni <script>.
    partes = re.split(r"(<(?:pre|textarea|script)\b.*?</(?:pre|textarea|script)>)", s, flags=re.S | re.I)
    for i in range(0, len(partes), 2):
        t = partes[i]
        t = re.sub(r"\n[ \t]+", "\n", t)
        t = re.sub(r"\n{2,}", "\n", t)
        partes[i] = t
    return "".join(partes).strip() + "\n"

def css_min(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([{};,>])\s*", r"\1", s)
    s = re.sub(r";}", "}", s)
    return s.strip() + "\n"

def js_min(s):
    # Solo lo seguro: comentarios de bloque y lineas que son nada mas que un
    # comentario. No se tocan las cadenas ni las expresiones regulares.
    s = re.sub(r"(^|\n)[ \t]*/\*.*?\*/[ \t]*(?=\n)", r"\1", s, flags=re.S)
    s = re.sub(r"(^|\n)[ \t]*//[^\n]*(?=\n)", r"\1", s)
    s = re.sub(r"\n[ \t]+", "\n", s)
    s = re.sub(r"\n{2,}", "\n", s)
    return s.strip() + "\n"

def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    antes = despues = 0
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if any(part in EXCLUIR_DIR for part in rel.parts) or not p.is_file():
            continue
        if p.name in EXCLUIR_ARCH or p.suffix in EXCLUIR_SUF or p.name.startswith("_p") \
                or (p.name.startswith(".") and p.name != ".htaccess"):
            continue
        if rel.parts[0] == "assets" and rel.parts[1:2] == ("Videos",):
            continue
        dst = DIST / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        antes += p.stat().st_size
        if p.suffix == ".html":
            dst.write_text(html_min(p.read_text(encoding="utf-8")), encoding="utf-8")
        elif p.suffix == ".css":
            dst.write_text(css_min(p.read_text(encoding="utf-8")), encoding="utf-8")
        elif p.suffix == ".js":
            dst.write_text(js_min(p.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            shutil.copy2(p, dst)
        despues += dst.stat().st_size
    print("dist/ listo: %.1f MB -> %.1f MB" % (antes / 1e6, despues / 1e6))

if __name__ == "__main__":
    main()
