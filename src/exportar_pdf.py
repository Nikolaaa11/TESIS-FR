"""
exportar_pdf.py
---------------
Genera docs/Tesis_USS.pdf con maquetación académica profesional (reportlab).

Soporta directivas dentro de docs/tesis.md:
  [[FIG: archivo.png | leyenda]]   -> figura embebida en el cuerpo, "Figura N."
  [[CSV: archivo.csv | leyenda]]   -> tabla generada desde outputs/tables, "Tabla N."

Maquetación: portada institucional · índices (general, de tablas, de figuras) ·
cuerpo Times 11.5 justificado con sangría de primera línea · encabezado y pie con
paginación · figuras y tablas numeradas con leyenda.
"""
import os, sys, re, glob
import pandas as pd
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, NextPageTemplate, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

sys.path.append(os.path.dirname(__file__))
import config as C

NAVY = colors.HexColor("#1B2A41"); COPPER = colors.HexColor("#9A6A3A")
GRAY = colors.HexColor("#555555"); LINE = colors.HexColor("#C9CCD2"); INK = colors.HexColor("#1A1A1A")
WF = r"C:\Windows\Fonts"


def _reg():
    """Tipografía según la SUGERENCIA del MIT: fuente sans-serif (más legible). Se usa
    Arial en todo el documento. Fallback a Helvetica (sans base de reportlab)."""
    fam = {"body": "Helvetica", "bold": "Helvetica-Bold", "it": "Helvetica-Oblique",
           "bolditalic": "Helvetica-BoldOblique"}
    try:
        reg = {("Body", "arial.ttf"), ("Body-Bold", "arialbd.ttf"),
               ("Body-It", "ariali.ttf"), ("Body-BI", "arialbi.ttf")}
        for name, f in reg:
            pdfmetrics.registerFont(TTFont(name, os.path.join(WF, f)))
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-It", boldItalic="Body-BI")
        fam = {"body": "Body", "bold": "Body-Bold", "it": "Body-It", "bolditalic": "Body-BI"}
    except Exception:
        pass
    return fam
FAM = _reg(); BODY, BOLD, IT, BI = FAM["body"], FAM["bold"], FAM["it"], FAM["bolditalic"]
HEAD = BOLD; HEADL = BOLD  # APA usa la misma fuente (Times) en negrita para títulos


def _clean(t):
    t = "" if t is None else str(t)
    # 1) proteger code spans `...`: contienen tickers de Yahoo (^IRX, ^IPSA), rutas y
    #    nombres snake_case que NO deben transformarse como notación matemática.
    codes = []
    def _stash(m):
        codes.append(m.group(1)); return f"\x00{len(codes)-1}\x00"
    t = re.sub(r"`([^`]+)`", _stash, t)
    # 2) markdown básico (negrita / cursiva / fórmulas inline / enlaces)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\$\$(.+?)\$\$", r"\1", t); t = re.sub(r"\\\((.+?)\\\)", r"\1", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", t)
    # 3) subíndices/superíndices -> etiquetas nativas de reportlab (look más académico).
    #    Forma con llaves (inequívoca) primero; luego formas simples seguras.
    t = re.sub(r"\^\{([^}]+)\}", r"<super>\1</super>", t)
    t = re.sub(r"_\{([^}]+)\}", r"<sub>\1</sub>", t)
    t = re.sub(r"\^([0-9]+|[a-z])\b", r"<super>\1</super>", t)              # ^t, ^2 (no toca tickers ^IRX)
    t = re.sub(r"(?<=[0-9A-Za-z\)\]Ͱ-Ͽ])_([A-Za-z0-9]+)", r"<sub>\1</sub>", t)
    # 4) escape de & y restauración de etiquetas + code spans
    t = t.replace("&", "&amp;")
    for tag in ("b", "i", "sub", "super"):
        t = t.replace(f"&lt;{tag}&gt;", f"<{tag}>").replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    for i, c in enumerate(codes):
        t = t.replace(f"\x00{i}\x00", c)
    return t


def estilos():
    # Norma MIT (Specifications for Thesis Preparation): Times New Roman 12, ALINEADO
    # A LA IZQUIERDA (margen derecho irregular, NO justificado), INTERLINEADO DOBLE en
    # el cuerpo; resumen/notas/bibliografía a espacio simple.
    HY = "es_ES"
    body = ParagraphStyle("body", fontName=BODY, fontSize=12, leading=24,  # doble (2.0)
                          alignment=TA_JUSTIFY, spaceAfter=6, firstLineIndent=1.27*cm, textColor=INK,
                          hyphenationLang=HY, spaceShrinkage=0.05)
    body0 = ParagraphStyle("body0", parent=body, firstLineIndent=0)
    body_s = ParagraphStyle("body_s", parent=body, leading=14)             # espacio simple
    body_s0 = ParagraphStyle("body_s0", parent=body_s, firstLineIndent=0)
    # Títulos: Nivel 1 centrado/negrita; Nivel 2 izq/negrita; Nivel 3 izq/negrita-cursiva
    h1 = ParagraphStyle("h1", fontName=BOLD, fontSize=15, leading=20, textColor=NAVY,
                        alignment=TA_CENTER, spaceBefore=22, spaceAfter=16, keepWithNext=True)
    h2 = ParagraphStyle("h2", fontName=BOLD, fontSize=13, leading=17, textColor=INK,
                        alignment=TA_LEFT, spaceBefore=16, spaceAfter=8, keepWithNext=True)
    h3 = ParagraphStyle("h3", fontName=BI, fontSize=12, leading=16, textColor=INK,
                        alignment=TA_LEFT, spaceBefore=12, spaceAfter=5, keepWithNext=True)
    bullet = ParagraphStyle("bullet", parent=body, leading=15, leftIndent=20, firstLineIndent=0,
                            bulletIndent=8, spaceAfter=5)   # listas/bibliografía: espacio simple
    quote = ParagraphStyle("quote", parent=body, leading=14, leftIndent=1.27*cm, rightIndent=0,
                           firstLineIndent=0, fontName=BODY, textColor=INK, fontSize=11,
                           spaceBefore=4, spaceAfter=8, alignment=TA_JUSTIFY)
    cap = ParagraphStyle("cap", fontName=BOLD, fontSize=10, leading=13, textColor=INK, spaceBefore=10, spaceAfter=4)
    figcap = ParagraphStyle("figcap", fontName=IT, fontSize=10, leading=13, textColor=INK, alignment=TA_CENTER, spaceBefore=4, spaceAfter=13)
    return dict(body=body, body0=body0, body_s=body_s, body_s0=body_s0,
                h1=h1, h2=h2, h3=h3, bullet=bullet, quote=quote, cap=cap, figcap=figcap)


class TesisDoc(BaseDocTemplate):
    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph):
            st = fl.style.name; txt = fl.getPlainText()
            if st == "h1": self.notify("TOCEntry", (0, txt, self.page))
            elif st == "h2": self.notify("TOCEntry", (1, txt, self.page))
            elif st == "cap": self.notify("LOTEntry", (0, txt, self.page))
            elif st == "figcap": self.notify("LOFEntry", (0, txt, self.page))


def _tabla_de_filas(filas, S):
    ncol = max(len(f) for f in filas)
    cH = ParagraphStyle("cH", fontName=HEAD, fontSize=8.3, leading=10.5, textColor=colors.white, alignment=TA_CENTER)
    cc = ParagraphStyle("cc", fontName=BODY, fontSize=8.5, leading=11, alignment=TA_CENTER)
    data = [[Paragraph(_clean(c), cH if i == 0 else cc) for c in (fila + [""] * (ncol - len(fila)))]
            for i, fila in enumerate(filas)]
    avail = letter[0] - 3.8*cm - 2.54*cm
    t = Table(data, colWidths=[avail/ncol]*ncol, hAlign="CENTER", repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F3F5")]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, NAVY), ("LINEBELOW", (0, -1), (-1, -1), 0.7, NAVY),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def tabla_md(lineas, S, ntab, titulo):
    filas = [[c.strip() for c in l.strip().strip("|").split("|")]
             for l in lineas if not re.match(r"^\s*\|[\s:\-\|]+\|\s*$", l)]
    if not filas: return []
    tit = re.sub(r"^\d+(\.\d+)*\.?\s+", "", titulo).strip()
    return [Paragraph(f"Tabla {ntab}. {_clean(tit)}", S["cap"]), _tabla_de_filas(filas, S), Spacer(1, 8)]


def tabla_csv(nombre, S, ntab, leyenda, maxrows=14, cols=None):
    p = C.TAB / nombre
    if not p.exists(): return []
    df = pd.read_csv(p)
    if cols: df = df[[c for c in cols if c in df.columns]]
    df = df.head(maxrows)
    filas = [list(df.columns)] + df.astype(str).values.tolist()
    return [Paragraph(f"Tabla {ntab}. {_clean(leyenda)}", S["cap"]), _tabla_de_filas(filas, S), Spacer(1, 8)]


def fig_flow(archivo, S, nfig, leyenda, ancho=15.0):
    p = C.FIG / archivo
    if not p.exists(): return []
    try:
        from PIL import Image as PImg
        w, h = PImg.open(str(p)).size
        iw = ancho*cm; ih = iw*h/w
        if ih > 11.0*cm: ih = 11.0*cm; iw = ih*w/h
        blk = [Spacer(1, 4), Image(str(p), width=iw, height=ih),
               Paragraph(f"Figura {nfig}. {_clean(leyenda)}", S["figcap"])]
        return [KeepTogether(blk)]
    except Exception:
        return []


def construir_flow(md, S, ctx):
    flow = []; lineas = md.split("\n"); i = 0; titulo_omitido = False; prev = ["start"]; buf = []

    def flush():
        # une las líneas acumuladas en UN solo párrafo (markdown: párrafo = líneas
        # consecutivas no vacías separadas por líneas en blanco)
        if not buf:
            return
        texto = " ".join(x.strip() for x in buf)
        if ctx.get("single"):
            st = S["body_s0"] if prev[0] == "head" else S["body_s"]
        else:
            st = S["body0"] if prev[0] == "head" else S["body"]
        flow.append(Paragraph(_clean(texto), st)); buf.clear(); prev[0] = "para"

    while i < len(lineas):
        s = lineas[i].strip()
        if not s:
            flush(); i += 1; continue
        m = re.match(r"^\[\[FIG:\s*([^|\]]+?)\s*\|\s*(.+?)\s*\]\]$", s)
        if m:
            flush(); ctx["nfig"] += 1; ctx["shown"].add(m.group(1).strip())
            flow += fig_flow(m.group(1).strip(), S, ctx["nfig"], m.group(2).strip()); prev[0] = "fig"; i += 1; continue
        m = re.match(r"^\[\[CSV:\s*([^|\]]+?)\s*\|\s*(.+?)\s*\]\]$", s)
        if m:
            flush(); ctx["ntab"] += 1
            flow += tabla_csv(m.group(1).strip(), S, ctx["ntab"], m.group(2).strip()); prev[0] = "table"; i += 1; continue
        if s.startswith("|"):
            flush(); blk = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                blk.append(lineas[i]); i += 1
            ctx["ntab"] += 1; flow += tabla_md(blk, S, ctx["ntab"], ctx["tit"]); prev[0] = "table"; continue
        if s.startswith("# ") and not titulo_omitido:
            titulo_omitido = True; i += 1; continue
        if s.startswith("### "):
            flush(); ctx["tit"] = _clean(s[4:]); flow.append(Paragraph(ctx["tit"], S["h3"])); prev[0] = "head"
        elif s.startswith("## "):
            flush(); ctx["tit"] = _clean(s[3:])
            ctx["single"] = bool(re.match(r"^## (Resumen|Abstract|Dedicatoria|Agradecimientos|Notaci|Glosario|9\.)", s))
            flow += ([PageBreak(), Paragraph(ctx["tit"], S["h1"])] if re.match(r"^## (\d|Anexo|Resumen|Glosario)", s)
                     else [Paragraph(ctx["tit"], S["h2"])]); prev[0] = "head"
        elif s.startswith("# "):
            flush(); flow.append(Paragraph(_clean(s[2:]), S["h1"])); prev[0] = "head"
        elif re.match(r"^[-*] ", s) or re.match(r"^\d+\.\s", s):
            flush()
            es_vinheta = bool(re.match(r"^[-*] ", s))
            txt = s[2:] if es_vinheta else s
            # absorbe líneas de continuación (sangradas) en el mismo ítem de lista
            j = i + 1
            while j < len(lineas):
                raw = lineas[j]
                if raw.strip() and (raw[:1] in (" ", "\t")) and not re.match(r"^\s*([-*]|\d+\.)\s", raw):
                    txt += " " + raw.strip(); j += 1
                else:
                    break
            pref = "•&nbsp;&nbsp;" if es_vinheta else ""
            flow.append(Paragraph(pref + _clean(txt), S["bullet"])); prev[0] = "list"
            i = j; continue
        elif s.startswith("> "):
            flush(); qt = s[2:]; j = i + 1
            while j < len(lineas) and lineas[j].strip().startswith("> "):
                qt += " " + lineas[j].strip()[2:]; j += 1
            flow.append(Paragraph(_clean(qt), S["quote"])); prev[0] = "quote"; i = j; continue
        elif set(s) <= set("-") and len(s) >= 3:
            flush()
        else:
            buf.append(s)
        i += 1
    flush()
    return flow


def anexo_figuras(S, ctx):
    flow = [PageBreak(), Paragraph("Anexo D — Figuras complementarias", S["h1"])]
    nombres = {
        "precios_normalizados": "Evolución de precios normalizados (base 100) y precio del cobre.",
        "irf_ANTO_L": "Función impulso-respuesta: Antofagasta ante un shock del cobre.",
        "irf_PUCOBRE_SN": "Función impulso-respuesta: Pucobre (respuesta diferida).",
        "heatmap_correlaciones": "Matriz de correlaciones de los retornos diarios.",
        "iliquidez_vs_beta": "Iliquidez frente a la elasticidad-cobre contemporánea.",
        "acf_ANTO_L": "ACF de retornos y de retornos al cuadrado (Antofagasta).",
        "acf_PUCOBRE_SN": "ACF de retornos y de retornos al cuadrado (Pucobre).",
        "vol_condicional_ANTO_L": "Volatilidad condicional estimada (GJR-GARCH), Antofagasta.",
        "vol_condicional_PUCOBRE_SN": "Volatilidad condicional estimada, Pucobre.",
        "vol_condicional_CAP_SN": "Volatilidad condicional estimada, CAP.",
        "vol_condicional_SQM-B_SN": "Volatilidad condicional estimada, SQM.",
        "retornos_ANTO_L": "Log-retornos diarios y volatilidad realizada móvil (Antofagasta).",
        "retornos_PUCOBRE_SN": "Log-retornos diarios y volatilidad realizada móvil (Pucobre).",
    }
    any_added = False
    for f in sorted(glob.glob(str(C.FIG / "*.png"))):
        key = os.path.basename(f).replace(".png", "")
        if (key + ".png") in ctx["shown"]:
            continue
        try:
            from PIL import Image as PImg
            w, h = PImg.open(f).size; iw = 14.0*cm; ih = iw*h/w
            ctx["nfig"] += 1
            flow.append(KeepTogether([Spacer(1, 4), Image(f, width=iw, height=ih),
                        Paragraph(f"Figura {ctx['nfig']}. {nombres.get(key, key.replace('_',' ')+'.')}", S["figcap"])]))
            any_added = True
        except Exception:
            pass
    return flow if any_added else []


def _cover(canvas, doc):
    # Portada con la ESTRUCTURA del MIT (Specifications for Thesis Preparation),
    # adaptada a la Universidad San Sebastián: bloque centrado (título, autor,
    # declaración de presentación, fecha) y bloque de firmas alineado a la izquierda.
    canvas.saveState(); W, H = canvas._pagesize
    LX = 3.8*cm  # margen izquierdo MIT
    def ctr(txt, y, size, font=BODY, color=INK):
        canvas.setFont(font, size); canvas.setFillColor(color); canvas.drawCentredString(W/2, y, txt)
    def lft(txt, x, y, size, font=BODY, color=INK):
        canvas.setFont(font, size); canvas.setFillColor(color); canvas.drawString(x, y, txt)

    logo = C.ROOT / "assets" / "logo_uss.png"; top = H - 2.6*cm
    if logo.exists():
        try:
            from PIL import Image as PImg
            iw, ih = PImg.open(str(logo)).size; w = 2.6*cm; h = w*ih/iw
            canvas.drawImage(str(logo), W/2-w/2, top-h, width=w, height=h, preserveAspectRatio=True, mask="auto")
            top -= h + 0.4*cm
        except Exception: pass

    # Título (centrado, negrita)
    canvas.setFont(BOLD, 16); canvas.setFillColor(NAVY); y = top - 1.0*cm
    for ln in ["Impacto de las variables macroeconómicas globales y financieras",
               "en la valoración bursátil del sector de minería de cobre en Chile"]:
        canvas.drawCentredString(W/2, y, ln); y -= 0.78*cm
    ctr("Un análisis econométrico de series de tiempo y de panel, 2004–2026", y-0.2*cm, 11.5, IT, GRAY)

    # por / Autor
    y -= 1.6*cm; ctr("por", y, 12, IT, INK)
    y -= 0.8*cm; ctr("[Nombre del autor o autora]", y, 12.5, BOLD, INK)

    # Declaración de presentación (estilo MIT: "Submitted to ... in partial fulfillment ...")
    y -= 1.5*cm; canvas.setFont(BODY, 11.5); canvas.setFillColor(INK)
    for ln in ["Trabajo Final de Graduación presentado a la",
               "Facultad de Economía y Negocios",
               "en cumplimiento parcial de los requisitos para el grado de"]:
        canvas.drawCentredString(W/2, y, ln); y -= 0.62*cm
    y -= 0.12*cm; ctr("Magíster en Data Science", y, 12.5, BOLD, NAVY)
    y -= 0.62*cm; ctr("en la", y, 11.5, BODY, INK)
    y -= 0.62*cm; ctr("Universidad San Sebastián", y, 12.5, BOLD, NAVY)
    y -= 0.7*cm; ctr("Santiago de Chile — [mes] de 2026", y, 11.5, BODY, INK)

    # Bloque de firmas alineado a la IZQUIERDA (Authored / Certified / Accepted by)
    y -= 1.7*cm
    lft("Autor(a):", LX, y, 11.5, BOLD, INK)
    lft("__________________________________________", LX+3.0*cm, y, 11.5, BODY, INK)
    y -= 0.55*cm; lft("[Nombre del autor o autora] — Facultad de Economía y Negocios", LX+3.0*cm, y, 9.5, IT, GRAY)
    y -= 1.2*cm
    lft("Certificado por:", LX, y, 11.5, BOLD, INK)
    lft("__________________________________________", LX+3.0*cm, y, 11.5, BODY, INK)
    y -= 0.55*cm; lft("[Profesor(a) guía], Profesor(a) guía de la tesis", LX+3.0*cm, y, 9.5, IT, GRAY)
    y -= 1.2*cm
    lft("Aceptado por:", LX, y, 11.5, BOLD, INK)
    lft("__________________________________________", LX+3.0*cm, y, 11.5, BODY, INK)
    y -= 0.55*cm; lft("[Director(a) del Programa de Magíster en Data Science]", LX+3.0*cm, y, 9.5, IT, GRAY)
    canvas.restoreState()


def _frame_page(canvas, doc):
    canvas.saveState(); W, H = canvas._pagesize
    canvas.setFont(BODY, 11); canvas.setFillColor(INK)
    # Paginación MIT: numeración consecutiva (la portada es la página 1)
    canvas.drawCentredString(W/2, 1.4*cm, str(doc.page))
    canvas.restoreState()


def construir():
    md = (C.ROOT / "docs" / "tesis.md").read_text(encoding="utf-8")
    S = estilos()
    out = C.ROOT / "docs" / "Tesis_USS.pdf"
    doc = TesisDoc(str(out), pagesize=letter, leftMargin=3.8*cm, rightMargin=2.54*cm,
                   topMargin=2.54*cm, bottomMargin=2.54*cm,
                   title="Impacto macro-financiero en la valoración del cobre en Chile", author="Universidad San Sebastián")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame], onPage=_cover),
                          PageTemplate(id="body", frames=[frame], onPage=_frame_page)])
    toc = TableOfContents(); toc.levelStyles = [
        ParagraphStyle("toc0", fontName=HEAD, fontSize=11, leading=18, textColor=NAVY),
        ParagraphStyle("toc1", fontName=BODY, fontSize=10.5, leading=15, leftIndent=14, textColor=INK)]
    lot = TableOfContents(); lot.levelStyles = [ParagraphStyle("lot0", fontName=BODY, fontSize=10, leading=14, textColor=INK)]
    lof = TableOfContents(); lof.levelStyles = [ParagraphStyle("lof0", fontName=BODY, fontSize=10, leading=14, textColor=INK)]
    lot.notify = lambda k, s: lot.addEntry(*s) if k == "LOTEntry" else None
    lof.notify = lambda k, s: lof.addEntry(*s) if k == "LOFEntry" else None

    ctx = {"nfig": 0, "ntab": 0, "shown": set(), "tit": "Resultados"}
    flow = [NextPageTemplate("body"), PageBreak(),
            Paragraph("Índice general", S["h1"]), toc, PageBreak(),
            Paragraph("Índice de tablas", S["h1"]), lot, PageBreak(),
            Paragraph("Índice de figuras", S["h1"]), lof, PageBreak()]
    flow += construir_flow(md, S, ctx) + anexo_figuras(S, ctx)
    doc.multiBuild(flow)
    print(f"OK {out}  ({out.stat().st_size/1024:.0f} KB)")
    web = C.ROOT / "web" / "assets" / "docs" / "Tesis_USS.pdf"
    web.parent.mkdir(parents=True, exist_ok=True)
    import shutil; shutil.copy(out, web); print(f"OK {web}")


if __name__ == "__main__":
    construir()
