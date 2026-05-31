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
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
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
    fam = {"body": "Times-Roman", "bold": "Times-Bold", "it": "Times-Italic", "head": "Helvetica-Bold"}
    try:
        for name, f in {("Body", "times.ttf"), ("Body-Bold", "timesbd.ttf"), ("Body-It", "timesi.ttf"),
                        ("Head", "arialbd.ttf")}:
            pdfmetrics.registerFont(TTFont(name, os.path.join(WF, f)))
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-It", boldItalic="Body-Bold")
        fam = {"body": "Body", "bold": "Body-Bold", "it": "Body-It", "head": "Head"}
    except Exception:
        pass
    return fam
FAM = _reg(); BODY, BOLD, IT, HEAD = FAM["body"], FAM["bold"], FAM["it"], FAM["head"]


def _clean(t):
    t = "" if t is None else str(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    t = re.sub(r"\$\$(.+?)\$\$", r"\1", t); t = re.sub(r"\\\((.+?)\\\)", r"\1", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", t)
    t = t.replace("&", "&amp;")
    for tag in ("b", "i"):
        t = t.replace(f"&lt;{tag}&gt;", f"<{tag}>").replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return t


def estilos():
    body = ParagraphStyle("body", fontName=BODY, fontSize=12, leading=19.5,
                          alignment=TA_JUSTIFY, spaceAfter=3, firstLineIndent=0.9*cm, textColor=INK)
    body0 = ParagraphStyle("body0", parent=body, firstLineIndent=0)
    h1 = ParagraphStyle("h1", fontName=HEAD, fontSize=16, leading=20, textColor=NAVY, spaceBefore=18, spaceAfter=10, keepWithNext=True)
    h2 = ParagraphStyle("h2", fontName=HEAD, fontSize=13, leading=17, textColor=NAVY, spaceBefore=13, spaceAfter=6, keepWithNext=True)
    h3 = ParagraphStyle("h3", fontName=HEAD, fontSize=11.5, leading=15, textColor=colors.HexColor("#333"), spaceBefore=9, spaceAfter=4, keepWithNext=True)
    bullet = ParagraphStyle("bullet", parent=body, leftIndent=18, firstLineIndent=0, bulletIndent=6, spaceAfter=3)
    quote = ParagraphStyle("quote", parent=body, leftIndent=16, rightIndent=16, firstLineIndent=0, fontName=IT, textColor=GRAY, fontSize=10, leading=14, spaceBefore=4, spaceAfter=6)
    cap = ParagraphStyle("cap", fontName=BOLD, fontSize=9.5, leading=12, textColor=NAVY, spaceBefore=8, spaceAfter=3)
    figcap = ParagraphStyle("figcap", fontName=IT, fontSize=9, leading=12, textColor=GRAY, alignment=TA_CENTER, spaceBefore=3, spaceAfter=11)
    return dict(body=body, body0=body0, h1=h1, h2=h2, h3=h3, bullet=bullet, quote=quote, cap=cap, figcap=figcap)


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
    avail = A4[0] - 3*cm - 2.5*cm
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
    flow = []; lineas = md.split("\n"); i = 0; titulo_omitido = False; prev = "start"
    while i < len(lineas):
        s = lineas[i].strip()
        if not s: i += 1; continue
        m = re.match(r"^\[\[FIG:\s*([^|\]]+?)\s*\|\s*(.+?)\s*\]\]$", s)
        if m:
            ctx["nfig"] += 1; ctx["shown"].add(m.group(1).strip())
            flow += fig_flow(m.group(1).strip(), S, ctx["nfig"], m.group(2).strip()); prev = "fig"; i += 1; continue
        m = re.match(r"^\[\[CSV:\s*([^|\]]+?)\s*\|\s*(.+?)\s*\]\]$", s)
        if m:
            ctx["ntab"] += 1
            flow += tabla_csv(m.group(1).strip(), S, ctx["ntab"], m.group(2).strip()); prev = "table"; i += 1; continue
        if s.startswith("|"):
            blk = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                blk.append(lineas[i]); i += 1
            ctx["ntab"] += 1; flow += tabla_md(blk, S, ctx["ntab"], ctx["tit"]); prev = "table"; continue
        if s.startswith("# ") and not titulo_omitido:
            titulo_omitido = True; i += 1; continue
        if s.startswith("### "):
            ctx["tit"] = _clean(s[4:]); flow.append(Paragraph(ctx["tit"], S["h3"])); prev = "head"
        elif s.startswith("## "):
            ctx["tit"] = _clean(s[3:])
            flow += ([PageBreak(), Paragraph(ctx["tit"], S["h1"])] if re.match(r"^## (\d|Anexo|Resumen|Glosario)", s)
                     else [Paragraph(ctx["tit"], S["h2"])]); prev = "head"
        elif s.startswith("# "):
            flow.append(Paragraph(_clean(s[2:]), S["h1"])); prev = "head"
        elif re.match(r"^[-*] ", s):
            flow.append(Paragraph("•&nbsp;&nbsp;" + _clean(s[2:]), S["bullet"])); prev = "list"
        elif re.match(r"^\d+\.\s", s):
            flow.append(Paragraph(_clean(s), S["bullet"])); prev = "list"
        elif s.startswith("> "):
            flow.append(Paragraph(_clean(s[2:]), S["quote"])); prev = "quote"
        elif set(s) <= set("-") and len(s) >= 3:
            pass
        else:
            flow.append(Paragraph(_clean(s), S["body0"] if prev == "head" else S["body"])); prev = "para"
        i += 1
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
    canvas.saveState(); W, H = A4
    logo = C.ROOT / "assets" / "logo_uss.png"; off = 0
    if logo.exists():
        try:
            from PIL import Image as PImg
            iw, ih = PImg.open(str(logo)).size; w = 2.8*cm; h = w*ih/iw
            canvas.drawImage(str(logo), W/2-w/2, H-2.4*cm-h, width=w, height=h, preserveAspectRatio=True, mask="auto")
            off = h + 0.5*cm
        except Exception: off = 0
    def c(txt, y, size, font=HEAD, color=NAVY):
        canvas.setFont(font, size); canvas.setFillColor(color); canvas.drawCentredString(W/2, y, txt)
    c("UNIVERSIDAD SAN SEBASTIÁN", H-3.6*cm-off, 16)
    c("Facultad de Economía y Negocios", H-4.25*cm-off, 11.5, HEAD, GRAY)
    c("Magíster en Data Science", H-4.85*cm-off, 11.5, HEAD, GRAY)
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.6); canvas.line(4.5*cm, H-8.2*cm, W-4.5*cm, H-8.2*cm)
    canvas.setFont(BOLD, 18.5); canvas.setFillColor(NAVY)
    for k, ln in enumerate(["Impacto de las variables macroeconómicas globales y",
                            "financieras en la valoración bursátil del sector de",
                            "minería de cobre en Chile"]):
        canvas.drawCentredString(W/2, H-9.6*cm-k*0.82*cm, ln)
    canvas.setFont(IT, 12); canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, H-12.6*cm, "Un análisis econométrico de series de tiempo y de panel, 2004–2026")
    canvas.line(4.5*cm, H-13.4*cm, W-4.5*cm, H-13.4*cm)
    canvas.setFont(IT, 11.5); canvas.setFillColor(INK)
    canvas.drawCentredString(W/2, 8.7*cm, "Tesis para optar al grado de Magíster en Data Science")
    canvas.setFont(BODY, 11.5)
    canvas.drawCentredString(W/2, 6.9*cm, "Autor:  ___________________________")
    canvas.drawCentredString(W/2, 6.1*cm, "Profesor guía:  ___________________________")
    canvas.setFillColor(GRAY); canvas.drawCentredString(W/2, 3.6*cm, "Santiago de Chile"); canvas.drawCentredString(W/2, 3.05*cm, "2026")
    canvas.restoreState()


def _frame_page(canvas, doc):
    canvas.saveState(); W, H = A4
    canvas.setFont(IT, 8); canvas.setFillColor(GRAY)
    canvas.drawString(3*cm, H-1.25*cm, "Valoración bursátil del sector de minería de cobre en Chile")
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.4); canvas.line(3*cm, H-1.4*cm, W-2.5*cm, H-1.4*cm)
    canvas.setFont(BODY, 9.5); canvas.setFillColor(GRAY); canvas.drawCentredString(W/2, 1.2*cm, str(doc.page))
    canvas.restoreState()


def construir():
    md = (C.ROOT / "docs" / "tesis.md").read_text(encoding="utf-8")
    S = estilos()
    out = C.ROOT / "docs" / "Tesis_USS.pdf"
    doc = TesisDoc(str(out), pagesize=A4, leftMargin=3*cm, rightMargin=2.5*cm, topMargin=2.2*cm, bottomMargin=2*cm,
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
