"""
exportar_pdf.py
---------------
Genera docs/Tesis_USS.pdf con maquetación académica profesional (reportlab):
  - Portada institucional sobria (logo opcional).
  - Índice general (TOC) con números de página y líneas guía.
  - Índice de tablas.
  - Cuerpo Times 11.5, justificado, interlineado 1.4, SANGRÍA de primera línea
    (sin sangría tras un encabezado) — estándar de tesis, no de blog.
  - Encabezados jerárquicos numerados; tablas con leyenda "Tabla N.".
  - Encabezado de página (título corto) y pie con número de página.
Fuente: docs/tesis.md. Registra fuentes Unicode de Windows para acentos/símbolos.
"""
import os, sys, re, glob
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, NextPageTemplate,
                                KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

sys.path.append(os.path.dirname(__file__))
import config as C

NAVY = colors.HexColor("#1B2A41")
COPPER = colors.HexColor("#9A6A3A")
GRAY = colors.HexColor("#555555")
LINE = colors.HexColor("#C9CCD2")
INK = colors.HexColor("#1A1A1A")

WF = r"C:\Windows\Fonts"
def _reg():
    fam = {"body": "Times-Roman", "bold": "Times-Bold", "it": "Times-Italic", "head": "Helvetica-Bold"}
    reg = {("Body", "times.ttf"), ("Body-Bold", "timesbd.ttf"), ("Body-It", "timesi.ttf"),
           ("Head", "arialbd.ttf"), ("Head-Reg", "arial.ttf")}
    try:
        for name, f in reg:
            pdfmetrics.registerFont(TTFont(name, os.path.join(WF, f)))
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-It", boldItalic="Body-Bold")
        fam = {"body": "Body", "bold": "Body-Bold", "it": "Body-It", "head": "Head"}
    except Exception:
        pass
    return fam
FAM = _reg()
BODY, BOLD, IT, HEAD = FAM["body"], FAM["bold"], FAM["it"], FAM["head"]


def _clean(t):
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
    body = ParagraphStyle("body", fontName=BODY, fontSize=11.5, leading=16.5,
                          alignment=TA_JUSTIFY, spaceAfter=2, firstLineIndent=0.8*cm, textColor=INK)
    body0 = ParagraphStyle("body0", parent=body, firstLineIndent=0)  # primer párrafo tras título
    h1 = ParagraphStyle("h1", fontName=HEAD, fontSize=16, leading=20, textColor=NAVY,
                        spaceBefore=18, spaceAfter=10, keepWithNext=True)
    h2 = ParagraphStyle("h2", fontName=HEAD, fontSize=13, leading=17, textColor=NAVY,
                        spaceBefore=13, spaceAfter=6, keepWithNext=True)
    h3 = ParagraphStyle("h3", fontName=HEAD, fontSize=11.5, leading=15, textColor=colors.HexColor("#333333"),
                        spaceBefore=9, spaceAfter=4, keepWithNext=True)
    bullet = ParagraphStyle("bullet", parent=body, leftIndent=18, firstLineIndent=0, bulletIndent=6, spaceAfter=3)
    quote = ParagraphStyle("quote", parent=body, leftIndent=16, rightIndent=16, firstLineIndent=0,
                           fontName=IT, textColor=GRAY, fontSize=10, leading=14, spaceBefore=4, spaceAfter=6)
    cap = ParagraphStyle("cap", fontName=BOLD, fontSize=9.5, leading=12, textColor=NAVY,
                         spaceBefore=8, spaceAfter=3)
    fcap = ParagraphStyle("fcap", fontName=IT, fontSize=9, leading=12, textColor=GRAY,
                          alignment=TA_CENTER, spaceBefore=2, spaceAfter=10)
    return dict(body=body, body0=body0, h1=h1, h2=h2, h3=h3, bullet=bullet, quote=quote, cap=cap, fcap=fcap)


class TesisDoc(BaseDocTemplate):
    """DocTemplate que registra entradas de índice (TOC) y de tablas."""
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            st = flowable.style.name; txt = flowable.getPlainText()
            if st == "h1":
                self.notify("TOCEntry", (0, txt, self.page))
            elif st == "h2":
                self.notify("TOCEntry", (1, txt, self.page))
            elif st == "cap":
                self.notify("LOTEntry", (0, txt, self.page))


def tabla_flow(lineas, S, ntab, titulo):
    filas = []
    for l in lineas:
        if re.match(r"^\s*\|[\s:\-\|]+\|\s*$", l):
            continue
        filas.append([c.strip() for c in l.strip().strip("|").split("|")])
    if not filas:
        return []
    ncol = max(len(f) for f in filas)
    cellH = ParagraphStyle("cH", fontName=HEAD, fontSize=8.3, leading=10.5, textColor=colors.white, alignment=TA_CENTER)
    cell = ParagraphStyle("c", fontName=BODY, fontSize=8.5, leading=11, alignment=TA_CENTER)
    data = []
    for i, fila in enumerate(filas):
        fila += [""] * (ncol - len(fila))
        data.append([Paragraph(_clean(c), cellH if i == 0 else cell) for c in fila])
    avail = A4[0] - 3*cm - 2.5*cm
    t = Table(data, colWidths=[avail/ncol]*ncol, hAlign="CENTER", repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F3F5")]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, NAVY),
        ("LINEBELOW", (0, -1), (-1, -1), 0.7, NAVY),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    tit = re.sub(r"^\d+(\.\d+)*\.?\s+", "", titulo).strip()  # quita "6.3 " inicial
    leyenda = Paragraph(f"Tabla {ntab}. {_clean(tit)}", S["cap"])
    return [leyenda, t, Spacer(1, 8)]


def construir_flow(md, S):
    flow = []; lineas = md.split("\n"); i = 0; titulo_omitido = False
    prev = "start"; ntab = 0; ultimo_tit = "Resultados"
    while i < len(lineas):
        s = lineas[i].strip()
        if not s:
            i += 1; continue
        if s.startswith("|"):
            blk = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                blk.append(lineas[i]); i += 1
            ntab += 1
            flow += tabla_flow(blk, S, ntab, ultimo_tit)
            prev = "table"; continue
        if s.startswith("# ") and not titulo_omitido:
            titulo_omitido = True; i += 1; continue
        if s.startswith("### "):
            ultimo_tit = _clean(s[4:]); flow.append(Paragraph(ultimo_tit, S["h3"])); prev = "head"
        elif s.startswith("## "):
            ultimo_tit = _clean(s[3:])
            flow += ([PageBreak(), Paragraph(ultimo_tit, S["h1"])] if re.match(r"^## (\d|Anexo)", s)
                     else [Paragraph(ultimo_tit, S["h2"])]); prev = "head"
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
            sty = S["body0"] if prev in ("head",) else S["body"]
            flow.append(Paragraph(_clean(s), sty)); prev = "para"
        i += 1
    return flow


def anexo_figuras(S):
    flow = [PageBreak(), Paragraph("Anexo A — Figuras del análisis", S["h1"])]
    nombres = {
        "precios_normalizados": "Evolución de precios normalizados (base 100) y precio del cobre.",
        "irf_ANTO_L": "Función impulso-respuesta: Antofagasta ante un shock del cobre.",
        "irf_PUCOBRE_SN": "Función impulso-respuesta: Pucobre (respuesta diferida).",
        "heatmap_correlaciones": "Matriz de correlaciones de los retornos diarios.",
        "iliquidez_vs_beta": "Iliquidez (% de días con retorno cero) frente a la elasticidad-cobre.",
        "acf_ANTO_L": "Función de autocorrelación de los retornos y de los retornos al cuadrado (Antofagasta).",
        "vol_condicional_ANTO_L": "Volatilidad condicional estimada (GJR-GARCH), Antofagasta.",
        "retornos_ANTO_L": "Log-retornos diarios y volatilidad realizada móvil (Antofagasta).",
    }
    n = 1; avail = 14.5*cm
    for f in sorted(glob.glob(str(C.FIG / "*.png"))):
        key = os.path.basename(f).replace(".png", "")
        try:
            from PIL import Image as PImg
            w, h = PImg.open(f).size
            iw = min(avail, 14.5*cm); ih = iw * h / w
            blk = [Spacer(1, 4), Image(f, width=iw, height=ih),
                   Paragraph(f"Figura A.{n}. {nombres.get(key, key.replace('_',' ') + '.')}", S["fcap"])]
            flow.append(KeepTogether(blk)); n += 1
        except Exception:
            pass
    return flow


def _cover(canvas, doc):
    canvas.saveState(); W, H = A4
    logo = C.ROOT / "assets" / "logo_uss.png"; off = 0
    if logo.exists():
        try:
            from PIL import Image as PImg
            iw, ih = PImg.open(str(logo)).size; w = 2.8*cm; h = w*ih/iw
            canvas.drawImage(str(logo), W/2-w/2, H-2.4*cm-h, width=w, height=h, preserveAspectRatio=True, mask="auto")
            off = h + 0.5*cm
        except Exception:
            off = 0

    def c(txt, y, size, font=HEAD, color=NAVY):
        canvas.setFont(font, size); canvas.setFillColor(color); canvas.drawCentredString(W/2, y, txt)
    c("UNIVERSIDAD SAN SEBASTIÁN", H-3.6*cm-off, 16)
    c("Facultad de Economía y Negocios", H-4.25*cm-off, 11.5, HEAD, GRAY)
    c("Magíster en Data Science", H-4.85*cm-off, 11.5, HEAD, GRAY)
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.6)
    canvas.line(4.5*cm, H-8.2*cm, W-4.5*cm, H-8.2*cm)
    canvas.setFont(BOLD, 18.5); canvas.setFillColor(NAVY)
    titulo = ["Impacto de las variables macroeconómicas globales y",
              "financieras en la valoración bursátil del sector de",
              "minería de cobre en Chile"]
    y = H-9.6*cm
    for ln in titulo:
        canvas.drawCentredString(W/2, y, ln); y -= 0.82*cm
    canvas.setFont(IT, 12); canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, y-0.5*cm, "Un análisis econométrico de series de tiempo y de panel, 2004–2026")
    canvas.line(4.5*cm, H-13.4*cm, W-4.5*cm, H-13.4*cm)
    canvas.setFont(IT, 11.5); canvas.setFillColor(INK)
    canvas.drawCentredString(W/2, 8.7*cm, "Tesis para optar al grado de Magíster en Data Science")
    canvas.setFont(BODY, 11.5)
    canvas.drawCentredString(W/2, 6.9*cm, "Autor:  ___________________________")
    canvas.drawCentredString(W/2, 6.1*cm, "Profesor guía:  ___________________________")
    canvas.setFont(BODY, 11.5); canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 3.6*cm, "Santiago de Chile")
    canvas.drawCentredString(W/2, 3.05*cm, "2026")
    canvas.restoreState()


def _frame_page(canvas, doc):
    canvas.saveState(); W, H = A4
    canvas.setFont(IT, 8); canvas.setFillColor(GRAY)
    canvas.drawString(3*cm, H-1.25*cm, "Valoración bursátil del sector de minería de cobre en Chile")
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.4)
    canvas.line(3*cm, H-1.4*cm, W-2.5*cm, H-1.4*cm)
    canvas.setFont(BODY, 9.5); canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 1.2*cm, str(doc.page))
    canvas.restoreState()


def construir():
    md = (C.ROOT / "docs" / "tesis.md").read_text(encoding="utf-8")
    S = estilos()
    out = C.ROOT / "docs" / "Tesis_USS.pdf"
    doc = TesisDoc(str(out), pagesize=A4, leftMargin=3*cm, rightMargin=2.5*cm,
                   topMargin=2.2*cm, bottomMargin=2*cm,
                   title="Impacto macro-financiero en la valoración del cobre en Chile",
                   author="Universidad San Sebastián")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=_cover),
        PageTemplate(id="body", frames=[frame], onPage=_frame_page),
    ])

    # Índice general
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName=HEAD, fontSize=11, leading=18, textColor=NAVY),
        ParagraphStyle("toc1", fontName=BODY, fontSize=10.5, leading=15, leftIndent=14, textColor=INK),
    ]
    # Índice de tablas
    lot = TableOfContents(); lot.levelStyles = [
        ParagraphStyle("lot0", fontName=BODY, fontSize=10, leading=14, textColor=INK)]
    # asociar LOT a una segunda lista de notify
    lot_added = []

    flow = [NextPageTemplate("body"), PageBreak(),
            Paragraph("Índice", S["h1"]), toc, PageBreak(),
            Paragraph("Índice de tablas", S["h1"]), lot, PageBreak()]
    flow += construir_flow(md, S) + anexo_figuras(S)

    # reportlab dirige TOCEntry a todos los TableOfContents; para separar LOT,
    # usamos un truco: el doc notifica 'TOCEntry' (índice) y 'LOTEntry' (tablas).
    toc.notify  # no-op
    # parchar: TableOfContents escucha 'TOCEntry'; creamos uno que escuche 'LOTEntry'
    def lot_notify(kind, stuff):
        if kind == "LOTEntry":
            lot.addEntry(*stuff)
    lot.notify = lot_notify

    doc.multiBuild(flow)
    print(f"OK {out}  ({out.stat().st_size/1024:.0f} KB)")
    web = C.ROOT / "web" / "assets" / "docs" / "Tesis_USS.pdf"
    web.parent.mkdir(parents=True, exist_ok=True)
    import shutil; shutil.copy(out, web); print(f"OK {web}")


if __name__ == "__main__":
    construir()
