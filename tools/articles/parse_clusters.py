# -*- coding: utf-8 -*-
"""Lee los .docx de clusters/ (articulos del cluster tematico) y los pasa a
clusters.json: metadatos SEO + bloques (h2, h3, p, ul, ol, table, box, faq,
refs). Las secciones internas del redactor (notas de verificacion, elementos
multimedia) no se publican; de multimedia solo se toma la tabla comparativa
recomendada cuando trae columnas y filas."""
import docx, re, json, os, html
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.hyperlink import Hyperlink

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "clusters")

def esc(t): return html.escape(t, quote=False)

def p_html(p):
    out = []
    for it in p.iter_inner_content():
        if isinstance(it, Hyperlink):
            url = it.address or ""
            txt = esc(it.text)
            if url and txt.strip():
                out.append('<a href="%s">%s</a>' % (html.escape(url), txt))
            else:
                out.append(txt)
        else:
            t = esc(it.text)
            if it.bold and t.strip():
                t = "<strong>%s</strong>" % t
            out.append(t)
    h = "".join(out).replace("</strong><strong>", "")
    return re.sub(r"\s+", " ", h).strip()

def is_list(p):
    return (p._p.pPr is not None and p._p.pPr.numPr is not None) or p.text.strip().startswith("- ")

STOP = re.compile(r"^(NOTES DE V[ÉE]RIFICATION|Notes de vérification|NOTAS|Éléments multim|ÉLÉMENTS MULTIM)", re.I)
META_KEYS = {"TITRE SEO": "title", "SEO TITLE": "title", "META DESCRIPTION": "desc", "SLUG": "slug",
             "DATE DE PUBLICATION": "date", "TEMPS DE LECTURE": "read", "AUTEUR": "author"}

def parse(path, start_marker=None):
    d = docx.Document(path)
    items = []
    for el in d.element.body.iterchildren():
        if el.tag.endswith("}tbl"):
            t = Table(el, d)
            rows = [[esc(c.text.strip()) for c in r.cells] for r in t.rows]
            items.append(("table", rows, None))
        elif el.tag.endswith("}p"):
            p = Paragraph(el, d)
            if p.text.strip():
                items.append(("p", p, p.text.strip()))
    if start_marker:
        i = next(k for k, it in enumerate(items) if it[0] == "p" and it[2].startswith(start_marker))
        items = items[i:]
    meta, blocks, mode, pending_key = {}, [], "pre", None
    mm = []  # multimedia
    def add(b):
        blocks.append(b)
    i = 0
    while i < len(items):
        kind, obj, txt = items[i]; i += 1
        if kind == "table":
            if mode in ("body", "pre"): add({"t": "table", "rows": obj})
            continue
        p = obj
        style = p.style.name
        # metadatos (antes del H1)
        if mode == "pre":
            if style == "Title":
                meta.setdefault("title", txt); continue
            for line in txt.split("\n"):
                m = re.match(r"^([A-ZÉa-zé][A-Za-zÉé ’'-]+?)\s*:\s*(.+)$", line.strip())
                if m and m.group(1).strip().upper() in META_KEYS:
                    meta[META_KEYS[m.group(1).strip().upper()]] = m.group(2).strip()
            if txt.upper() in META_KEYS:
                pending_key = META_KEYS[txt.upper()]; continue
            if pending_key and not re.match(r"^H1\s*:", txt):
                meta[pending_key] = txt; pending_key = None; continue
            m = re.match(r"^H1\s*:\s*(.+)$", txt)
            if m or style == "Heading 1":
                meta["h1"] = m.group(1) if m else txt; mode = "body"; continue
            if re.match(r"^IMPORTANT\s*:", txt):
                add({"t": "box", "title": "Important", "h": p_html(p).split(":", 1)[1].strip()})
            continue
        if STOP.match(txt):
            if re.match(r"^(Éléments multim|ÉLÉMENTS MULTIM)", txt, re.I):
                mode = "mm"; continue
            mode = "skip"; continue
        if mode == "skip":
            continue
        if mode == "mm":
            mm.append(txt); continue
        # encabezados
        m = re.match(r"^H([23])\s*:\s*(.+)$", txt)
        if m:
            add({"t": "h" + m.group(1), "h": esc(m.group(2))}); mode = "body"; continue
        if style in ("Heading 2", "Heading 3"):
            if txt.strip().upper() == "FAQ":
                mode = "faq"; add({"t": "faq", "qa": []}); continue
            add({"t": "h" + style[-1], "h": p_html(p)}); mode = "body"; continue
        U = txt.upper()
        if U == "CONCLUSION":
            add({"t": "h2", "h": "Conclusion"}); mode = "body"; continue
        if U == "FAQ":
            mode = "faq"; add({"t": "faq", "qa": []}); continue
        if U.startswith("RÉFÉRENCES") or U.startswith("REFERENCES") or U.startswith("SOURCES"):
            mode = "refs"; add({"t": "refs", "items": []}); continue
        if U.startswith("ENCADRÉ") or U.startswith("ENCADRE"):
            title = "À retenir" if "RETENIR" in U else "Important"
            # el contenido del recuadro es el o los parrafos que siguen hasta el proximo encabezado
            add({"t": "box", "title": title, "h": ""}); mode = "box"; continue
        if mode == "box":
            if is_list(p):
                blocks[-1]["h"] += "<li>%s</li>" % re.sub(r"^-\s*", "", p_html(p))
            else:
                blocks[-1]["h"] += "<p>%s</p>" % p_html(p)
            nxt = items[i] if i < len(items) else None
            if not nxt or nxt[0] != "p" or re.match(r"^H[23]\s*:", nxt[2]) or nxt[1].style.name.startswith("Heading"):
                mode = "body"
            continue
        if mode == "faq":
            if txt.endswith("?") and not is_list(p):
                blocks[-1]["qa"].append([p_html(p), ""])
            elif blocks[-1]["qa"]:
                q = blocks[-1]["qa"][-1]
                q[1] += "<p>%s</p>" % p_html(p)
            continue
        if mode == "refs":
            urls = re.findall(r"https?://\S+", txt)
            label = re.sub(r"https?://\S+", "", re.sub(r"^-\s*", "", txt)).strip(" .")
            if not urls and p.hyperlinks:
                urls = [h.address for h in p.hyperlinks if h.address]
            if urls and not label and blocks[-1]["items"] and not blocks[-1]["items"][-1][1]:
                blocks[-1]["items"][-1][1] = urls[0]
            elif label:
                blocks[-1]["items"].append([esc(label.rstrip(".")), urls[0].rstrip(".") if urls else ""])
            continue
        if is_list(p):
            h = re.sub(r"^-\s*", "", p_html(p))
            if blocks and blocks[-1]["t"] == "ul":
                blocks[-1]["items"].append(h)
            else:
                add({"t": "ul", "items": [h]})
            continue
        add({"t": "p", "h": p_html(p)})
    # tabla recomendada en multimedia
    if mm:
        txt = "\n".join(mm)
        mc = re.search(r"Colonnes\s*:\s*\n?(.+?\|.+?)\n", txt)
        ml = re.search(r"Lignes\s*:\s*\n((?:.+\|.+\n?)+)", txt)
        me = re.search(r"Emplacement[^:]*:\s*après la section «\s*(.+?)\s*»", txt)
        if mc and ml:
            head = [esc(c.strip()) for c in mc.group(1).split("|")]
            rows = [[esc(c.strip(" ;.")) for c in re.sub(r"^-\s*", "", l).split("|")] for l in ml.group(1).strip().split("\n") if "|" in l]
            if all(len(r) == len(head) for r in rows):
                tbl = {"t": "table", "rows": [head] + rows}
                pos = len(blocks)
                if me:
                    target = me.group(1).rstrip(" ?").lower()
                    for k, b in enumerate(blocks):
                        if b["t"] in ("h2", "h3") and target in html.unescape(b["h"]).lower():
                            lvl = b["t"]; pos = len(blocks)
                            for j in range(k + 1, len(blocks)):
                                if blocks[j]["t"] in ("h2",) or (lvl == "h3" and blocks[j]["t"] == "h3") or blocks[j]["t"] in ("faq", "refs"):
                                    pos = j; break
                            break
                blocks.insert(pos, tbl)
    # encabezados vacios
    clean = []
    for k, b in enumerate(blocks):
        if b["t"] in ("h2", "h3"):
            nxt = blocks[k + 1] if k + 1 < len(blocks) else None
            if not nxt or (nxt["t"] == b["t"]) or (b["t"] == "h3" and nxt["t"] == "h2"):
                continue
        if b["t"] == "box" and not b["h"]:
            continue
        clean.append(b)
    return meta, clean

DOCS = [
 ("Embaucher un salarie etranger/Pilar_.docx", None),
 ("Embaucher un salarie etranger/Satelite 1.docx", None),
 ("Embaucher un salarie etranger/Satellite 2.docx", None),
 ("Passeport Talent/PILIER Brief Guide visa Talent 2026.docx", "TITRE SEO"),
 ("Passeport Talent/Article satellite 2 Passeport-Talent-salarie-qualifie-ou-Carte-Bleue-Europeenne-2026.docx", None),
 ("vvt/Pilar.docx", None),
 ("vvt/satelite 1.docx", None),
 ("vvt/Satellite 2.docx", None),
]
if __name__ == "__main__":
    out = []
    for f, sm in DOCS:
        meta, blocks = parse(os.path.join(SRC, f), sm)
        out.append({"file": f, "meta": meta, "blocks": blocks})
        c = {}
        for b in blocks: c[b["t"]] = c.get(b["t"], 0) + 1
        print(f.split("/")[-1][:30], meta.get("h1", "")[:60], c, "faq:%d" % sum(len(b["qa"]) for b in blocks if b["t"] == "faq"), "refs:%d" % sum(len(b["items"]) for b in blocks if b["t"] == "refs"))
        print("   ", {k: v[:50] for k, v in meta.items()})
    json.dump(out, open(os.path.join(HERE, "clusters.json"), "w"), ensure_ascii=False, indent=1)
