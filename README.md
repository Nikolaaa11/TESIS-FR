# Tesis — Impacto de variables macro-financieras en la valoración bursátil del cobre en Chile

Magíster en Data Science · Universidad San Sebastián · Econometría financiera aplicada · Python 3.13.
Enfoque **explicativo / de medición de impacto** (no predictivo).

### 🌐 Plataforma en vivo: **https://web-pi-pied-45.vercel.app**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Nikolaaa11/TESIS-FR&root-directory=web)

> Redesplegar tras cambios: `vercel deploy web --prod --yes` (o conecta el repo en Vercel con **Root Directory = `web`**).

## Hallazgo central (probado formalmente)

El precio del cobre transmite fuerte e inmediatamente a la valoración del
*pure-play* líquido (**Antofagasta**, β≈0.70, ~28% de la varianza, 95% del impacto
en el día 0). En el *pure-play* local e ilíquido (**Pucobre**, 62% de días sin
transar) la transmisión contemporánea es casi nula (β≈0.09, R²≈0.04) pero su
**sensibilidad al cobre crece monótonamente con el horizonte**:

| Horizonte | β-cobre Pucobre |
|---|---|
| Diario (contemporáneo) | 0.085 |
| Acumulado 0–5 días | 0.415 |
| Mensual | 0.599 |
| Largo plazo (VECM) | 0.75 |

La iliquidez **retrasa el descubrimiento de precios pero no elimina** el vínculo
fundamental cobre→valoración (Toda-Yamamoto: cobre causa ambas acciones).

## Documento

- **`docs/Tesis_USS.pdf`** — PDF de ~25 páginas con formato profesional de magíster
  (portada académica, tipografía justificada, tablas, figuras, paginación;
  generado por `src/exportar_pdf.py` con reportlab).
- **`docs/Tesis_USS.docx`** — versión Word editable: portada, índice (TOC),
  encabezados numerados, tablas con estilo y figuras (generado por `src/exportar_docx.py`).
- **`docs/tesis.md`** — fuente del documento (con todos los números reales).

Regenerar: `python src/exportar_pdf.py` y `python src/exportar_docx.py`
(cierra el .docx en Word si está abierto, o el guardado fallará por bloqueo).

## Estructura

```
0.0.Tesis FR/
├── README.md                # este archivo
├── requirements.txt         # entorno (pip install -r requirements.txt)
├── data/{raw,interim,processed}/   # datos (raw = descargado; processed = analítico)
├── src/                     # código fuente
│   ├── config.py            # universo, factores, rutas, período (fuente de verdad)
│   ├── verificar_universo.py
│   ├── ingesta.py           # descarga Yahoo / FRED / BCCh
│   ├── preparacion.py       # limpieza y transformaciones
│   ├── eda_tests.py         # descriptivos, correlaciones, ADF/PP/KPSS, gráficos
│   ├── cointegracion.py     # Engle-Granger, Johansen
│   ├── modelo_retornos_hac.py   # impacto contemporáneo + diagnósticos
│   ├── modelo_var.py        # VAR, IRF, FEVD, Granger
│   ├── modelo_vecm.py       # relación de largo plazo
│   ├── modelo_garch.py      # volatilidad (GARCH/EGARCH/GJR)
│   ├── modelo_panel.py      # panel FE/RE/Hausman
│   ├── modelo_ardl.py       # ARDL bounds (robustez)
│   ├── robustez.py          # quiebres y submuestras
│   └── run_all.py           # orquestador (corre todo)
├── outputs/{tables,figures}/   # resultados (23 tablas, 12 figuras)
└── docs/
    ├── tesis.md             # DOCUMENTO DE TESIS (borrador con resultados reales)
    ├── 00_decisiones_fundacionales.md
    └── diccionario_datos.md
```

## Reproducir

```powershell
pip install -r requirements.txt
python src/run_all.py          # pipeline completo de principio a fin
```

Para incorporar macro del Banco Central de Chile (TPM, IMACEC, EMBI), registrar
cuenta gratuita en https://si3.bcentral.cl/Siete/ y definir variables de entorno:

```powershell
$env:BCCH_USER="tu_usuario"; $env:BCCH_PASS="tu_clave"
python src/ingesta.py
```

## Notas de datos (limitaciones declaradas)

- `^IPSA` (Yahoo) es inconsistente post-2019 → se usa `ECH` (ETF MSCI Chile) como
  proxy de mercado local.
- FRED quedó inaccesible desde el entorno de ejecución (timeouts); el cobre se
  cubre con el futuro COMEX `HG=F` y las tasas con `^TNX/^FVX/^IRX`.
- Período común efectivo de las regresiones multifactor: n ≈ 4.475 (calendarios
  LSE/Santiago/NYSE heterogéneos).

Todo número del documento proviene de `outputs/tables/`. **No hay datos ni
resultados inventados.**
