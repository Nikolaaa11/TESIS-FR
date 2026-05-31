"""
exportar_pdf.py
---------------
Genera docs/Tesis_USS.pdf con calidad de tesis de magíster, usando reportlab
(sin dependencias externas tipo LibreOffice/Word). Misma fuente: docs/tesis.md.

  - Portada académica.
  - Tipografía Times 11.5 justificada, interlineado 1.4, márgenes amplios.
  - Encabezados jerárquicos en azul USS; tablas con cabecera de color.
  - Figuras embebidas con caption numerado.
  - Pie con número de página y encabezado con título corto.
Registra fuentes Unicode de Windows (Arial/Times) para acentos y símbolos (β, ≈, →).
"""
import os, sys, re, glob
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, NextPageTemplate)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

sys.path.append(os.path.dirname(__file__))
import config as C

NAVY = colors.HexColor("#1B2A41")
COPPER = colors.HexColor("#C2703D")
GRAY = colors.HexColor("#555555")
LINE = colors.HexColor("#D2D2D7")

# ---- fuentes Unicode (Windows) ----
WF = r"C:\Windows\Fonts"
def _reg():
    fam = {}
    try:
        pdfmetrics.registerFont(TTFont("Body", os.path.join(WF, "times.ttf")))
        pdfmetrics.registerFont(TTFont("Body-Bold", os.path.join(WF, "timesbd.ttf")))
        pdfmetrics.registerFont(TTFont("Body-It", os.path.join(WF, "timesi.ttf")))
        fam["body"] = "Body"
    except Exception:
        fam["body"] = "Times-Roman"
    try:
        pdfmetrics.registerFont(TTFont("Head", os.path.join(WF, "arialbd.ttf")))
        pdfmetrics.registerFont(TTFont("Head-Reg", os.path.join(WF, "arial.ttf")))
        fam["head"] = "Head"
    except Exception:
        fam["head"] = "Helvetica-Bold"
    return fam
FAM = _reg()
BODY = FAM["body"]; HEAD = FAM["head"]


def _clean(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    t = re.sub(r"\$\$(.+?)\$\$", r"\1", t); t = re.sub(r"\\\((.+?)\\\)", r"\1", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", t)
    t = t.replace("&", "&amp;").replace("&amp;lt;", "&lt;")
    # re-permitir tags b/i que insertamos
    for tag in ("b", "i"):
        t = t.replace(f"&lt;{tag}&gt;", f"<{tag}>").replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return t


def estilos():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName=BODY, fontSize=11.5,
                          leading=16, alignment=TA_JUSTIFY, spaceAfter=7, textColor=colors.HexColor("#1d1d1f"))
    h1 = ParagraphStyle("h1", fontName=HEAD, fontSize=17, leading=21, textColor=NAVY,
                        spaceBefore=16, spaceAfter=9, keepWithNext=True)
    h2 = ParagraphStyle("h2", fontName=HEAD, fontSize=13.5, leading=18, textColor=NAVY,
                        spaceBefore=12, spaceAfter=6, keepWithNext=True)
    h3 = ParagraphStyle("h3", fontName=HEAD, fontSize=11.5, leading=15, textColor=COPPER,
                        spaceBefore=9, spaceAfter=4, keepWithNext=True)
    bullet = ParagraphStyle("bullet", parent=body, leftIndent=16, bulletIndent=4, spaceAfter=3)
    quote = ParagraphStyle("quote", parent=body, leftIndent=14, rightIndent=14, fontName=FAM.get("body"),
                           textColor=GRAY, borderColor=COPPER, borderWidth=0, fontSize=10.5, leading=15)
    cap = ParagraphStyle("cap", parent=body, alignment=TA_CENTER, fontSize=9, textColor=GRAY, spaceBefore=2)
    return dict(body=body, h1=h1, h2=h2, h3=h3, bullet=bullet, quote=quote, cap=cap)


def tabla_flow(lineas, S):
    filas = []
    for l in lineas:
        if re.match(r"^\s*\|[\s:\-\|]+\|\s*$", l): continue
        filas.append([c.strip() for c in l.strip().strip("|").split("|")])
    if not filas: return None
    ncol = max(len(f) for f in filas)
    cellH = ParagraphStyle("cellH", fontName=HEAD, fontSize=8.5, leading=11, textColor=colors.white, alignment=TA_CENTER)
    cell = ParagraphStyle("cell", fontName=BODY, fontSize=8.5, leading=11, alignment=TA_CENTER)
    data = []
    for i, fila in enumerate(filas):
        fila += [""] * (ncol - len(fila))
        data.append([Paragraph(_clean(c), cellH if i == 0 else cell) for c in fila])
    avail = A4[0] - 3*cm - 2.5*cm
    t = Table(data, colWidths=[avail/ncol]*ncol, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f7")]),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def construir_flow(md, S):
    flow = []; lineas = md.split("\n"); i = 0; titulo_omitido = False; nfig = 1
    while i < len(lineas):
        s = lineas[i].strip()
        if not s: i += 1; continue
        if s.startswith("|"):
            blk = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                blk.append(lineas[i]); i += 1
            t = tabla_flow(blk, S)
            if t: flow += [Spacer(1, 4), t, Spacer(1, 8)]
            continue
        if s.startswith("# ") and not titulo_omitido:
            titulo_omitido = True; i += 1; continue
        if s.startswith("### "): flow.append(Paragraph(_clean(s[4:]), S["h3"]))
        elif s.startswith("## "): flow += [PageBreak(), Paragraph(_clean(s[3:]), S["h1"])] if re.match(r"^## \d", s) else [Paragraph(_clean(s[3:]), S["h2"])]
        elif s.startswith("# "): flow.append(Paragraph(_clean(s[2:]), S["h1"]))
        elif re.match(r"^[-*] ", s): flow.append(Paragraph("•  " + _clean(s[2:]), S["bullet"]))
        elif re.match(r"^\d+\.\s", s): flow.append(Paragraph(_clean(s), S["bullet"]))
        elif s.startswith("> "): flow.append(Paragraph(_clean(s[2:]), S["quote"]))
        elif set(s) <= set("-") and len(s) >= 3: pass
        else: flow.append(Paragraph(_clean(s), S["body"]))
        i += 1
    return flow, nfig


def anexo_figuras(S):
    flow = [PageBreak(), Paragraph("Anexo A — Figuras del análisis", S["h1"])]
    nombres = {
        "precios_normalizados": "Evolución de precios normalizados (base 100) y precio del cobre",
        "irf_ANTO_L": "Función impulso-respuesta: Antofagasta ante shock del cobre",
        "irf_PUCOBRE_SN": "Función impulso-respuesta: Pucobre (respuesta diferida)",
        "heatmap_correlaciones": "Matriz de correlaciones de retornos",
        "iliquidez_vs_beta": "Iliquidez vs transmisión contemporánea del cobre",
    }
    n = 1; avail = A4[0] - 3*cm - 2.5*cm
    for f in sorted(glob.glob(str(C.FIG / "*.png"))):
        key = os.path.basename(f).replace(".png", "")
        try:
            from PIL import Image as PImg
            w, h = PImg.open(f).size
            iw = min(avail, 15*cm); ih = iw * h / w
            flow += [Spacer(1, 6), Image(f, width=iw, height=ih),
                     Paragraph(f"Figura A.{n}. {nombres.get(key, key.replace('_',' '))}", S["cap"])]
            n += 1
        except Exception:
            pass
    return flow


def _decorar(canvas, doc):
    canvas.saveState()
    canvas.setFont(BODY, 8)
    canvas.setFillColor(GRAY)
    # encabezado
    canvas.drawRightString(A4[0]-2.5*cm, A4[1]-1.3*cm, "Impacto macro-financiero en la valoración del cobre en Chile")
    canvas.setStrokeColor(LINE); canvas.line(3*cm, A4[1]-1.45*cm, A4[0]-2.5*cm, A4[1]-1.45*cm)
    # pie
    canvas.setFont(BODY, 9)
    canvas.drawCentredString(A4[0]/2, 1.2*cm, str(doc.page))
    canvas.restoreState()


def portada(canvas, doc):
    canvas.saveState(); W, H = A4
    def c(txt, y, size, font=HEAD, color=NAVY):
        canvas.setFont(font, size); canvas.setFillColor(color)
        canvas.drawCentredString(W/2, y, txt)
    c("UNIVERSIDAD SAN SEBASTIÁN", H-4*cm, 20)
    c("Facultad de Economía y Negocios", H-4.8*cm, 12, HEAD, GRAY)
    c("Magíster en Data Science", H-5.7*cm, 14, HEAD, colors.HexColor("#1d1d1f"))
    canvas.setStrokeColor(COPPER); canvas.setLineWidth(2)
    canvas.line(5*cm, H-7*cm, W-5*cm, H-7*cm)
    # título (envuelto)
    canvas.setFont(HEAD, 17); canvas.setFillColor(NAVY)
    titulo = ["Impacto de las variables macroeconómicas",
              "globales y financieras en la valoración bursátil",
              "del sector de minería de cobre en Chile"]
    y = H-9*cm
    for ln in titulo:
        canvas.drawCentredString(W/2, y, ln); y -= 0.8*cm
    canvas.setFont("Body-It" if "Body" in FAM["body"] else BODY, 12); canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, y-0.4*cm, "Un análisis econométrico de series de tiempo y panel, 2004–2026")
    canvas.setFont(BODY, 12); canvas.setFillColor(colors.HexColor("#1d1d1f"))
    canvas.drawCentredString(W/2, 8.5*cm, "Tesis para optar al grado de Magíster en Data Science")
    canvas.drawCentredString(W/2, 6.8*cm, "Autor: ____________________________")
    canvas.drawCentredString(W/2, 6.0*cm, "Profesor guía: ____________________________")
    canvas.setFont(HEAD, 12); canvas.setFillColor(NAVY)
    canvas.drawCentredString(W/2, 4.2*cm, "Santiago de Chile · 2026")
    canvas.restoreState()


def construir():
    md = (C.ROOT / "docs" / "tesis.md").read_text(encoding="utf-8")
    S = estilos()
    out = C.ROOT / "docs" / "Tesis_USS.pdf"
    doc = BaseDocTemplate(str(out), pagesize=A4, leftMargin=3*cm, rightMargin=2.5*cm,
                          topMargin=2.2*cm, bottomMargin=2*cm, title="Tesis USS — Cobre y valoración bursátil")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=portada),
        PageTemplate(id="body", frames=[frame], onPage=_decorar),
    ])
    flow = [NextPageTemplate("body"), PageBreak()]
    body_flow, _ = construir_flow(md, S)
    flow += body_flow + anexo_figuras(S)
    doc.build(flow)
    print(f"OK {out}  ({out.stat().st_size/1024:.0f} KB)")
    # copiar a web
    web = C.ROOT / "web" / "assets" / "docs" / "Tesis_USS.pdf"
    web.parent.mkdir(parents=True, exist_ok=True)
    import shutil; shutil.copy(out, web); print(f"OK {web}")


if __name__ == "__main__":
    construir()
