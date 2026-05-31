"""
exportar_docx.py
----------------
Convierte docs/tesis.md a un documento Word (docs/Tesis_USS.docx) con:
  - Portada (Universidad San Sebastián).
  - Encabezados, párrafos, listas y TABLAS markdown convertidas a tablas Word.
  - Anexo con todas las figuras de outputs/figures embebidas.

Parser markdown ligero (suficiente para este documento). Requiere python-docx.
"""
import os, sys, re, glob
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.path.append(os.path.dirname(__file__))
import config as C

AZUL = RGBColor(0x1B, 0x2A, 0x41)  # azul USS aprox


def limpiar_inline(texto):
    # quita marcas de negrita/cursiva/código para texto plano de runs
    texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto)
    texto = re.sub(r"`(.+?)`", r"\1", texto)
    texto = re.sub(r"\*(.+?)\*", r"\1", texto)
    return texto


def add_runs_negrita(par, texto):
    # respeta **negrita** dividiendo en segmentos
    partes = re.split(r"(\*\*.+?\*\*)", texto)
    for p in partes:
        if p.startswith("**") and p.endswith("**"):
            r = par.add_run(limpiar_inline(p)); r.bold = True
        else:
            par.add_run(limpiar_inline(p))


def portada(doc):
    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("UNIVERSIDAD SAN SEBASTIÁN"); r.bold = True; r.font.size = Pt(20)
    r.font.color.rgb = AZUL
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Magíster en Data Science"); r.font.size = Pt(13)
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Impacto de las variables macroeconómicas globales y financieras "
                  "en la valoración bursátil del sector de minería de cobre en Chile")
    r.bold = True; r.font.size = Pt(16); r.font.color.rgb = AZUL
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Econometría financiera aplicada · Series de tiempo y panel\n"
              "Período 2004–2026 · Python (statsmodels, arch, linearmodels)").font.size = Pt(11)
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Tesis para optar al grado de Magíster").italic = True
    doc.add_page_break()


def tabla_markdown(doc, lineas):
    filas = [l for l in lineas if l.strip().startswith("|")]
    # quitar separador |---|
    datos = []
    for l in filas:
        if re.match(r"^\s*\|[\s:\-\|]+\|\s*$", l):
            continue
        celdas = [c.strip() for c in l.strip().strip("|").split("|")]
        datos.append(celdas)
    if not datos:
        return
    ncol = max(len(f) for f in datos)
    t = doc.add_table(rows=0, cols=ncol)
    t.style = "Light Grid Accent 1"
    for i, fila in enumerate(datos):
        fila = fila + [""] * (ncol - len(fila))
        celdas = t.add_row().cells
        for j, val in enumerate(fila):
            celdas[j].text = limpiar_inline(val)
            if i == 0:
                for par in celdas[j].paragraphs:
                    for run in par.runs:
                        run.bold = True
    doc.add_paragraph()


def convertir(doc, md):
    lineas = md.split("\n")
    i = 0
    while i < len(lineas):
        l = lineas[i]
        s = l.strip()
        if not s:
            i += 1; continue
        # tabla
        if s.startswith("|"):
            bloque = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                bloque.append(lineas[i]); i += 1
            tabla_markdown(doc, bloque); continue
        # encabezados
        if s.startswith("### "):
            doc.add_heading(limpiar_inline(s[4:]), level=3)
        elif s.startswith("## "):
            doc.add_heading(limpiar_inline(s[3:]), level=2)
        elif s.startswith("# "):
            doc.add_heading(limpiar_inline(s[2:]), level=1)
        elif s.startswith("- ") or s.startswith("* "):
            p = doc.add_paragraph(style="List Bullet"); add_runs_negrita(p, s[2:])
        elif re.match(r"^\d+\.\s", s):
            p = doc.add_paragraph(style="List Number")
            add_runs_negrita(p, re.sub(r"^\d+\.\s", "", s))
        elif s.startswith(">"):
            p = doc.add_paragraph(); p.style = "Intense Quote"
            add_runs_negrita(p, s.lstrip(">").strip())
        elif set(s) <= set("-") and len(s) >= 3:
            pass  # separador horizontal
        else:
            p = doc.add_paragraph(); add_runs_negrita(p, s)
        i += 1


def anexo_figuras(doc):
    doc.add_page_break()
    doc.add_heading("Anexo — Figuras", level=1)
    figs = sorted(glob.glob(str(C.FIG / "*.png")))
    for f in figs:
        nombre = os.path.basename(f)
        doc.add_heading(nombre, level=3)
        try:
            doc.add_picture(f, width=Inches(6.0))
        except Exception as e:
            doc.add_paragraph(f"[no se pudo insertar {nombre}: {e}]")


def main():
    md = (C.ROOT / "docs" / "tesis.md").read_text(encoding="utf-8")
    doc = Document()
    style = doc.styles["Normal"]; style.font.name = "Calibri"; style.font.size = Pt(11)
    portada(doc)
    convertir(doc, md)
    anexo_figuras(doc)
    out = C.ROOT / "docs" / "Tesis_USS.docx"
    doc.save(out)
    print(f"Documento Word generado: {out}")
    print(f"Tamaño: {out.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
