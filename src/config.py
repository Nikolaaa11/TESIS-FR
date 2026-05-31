"""
config.py
---------
Configuracion central de la tesis: rutas, universo de activos, factores,
series FRED y parametros de periodo. Fuente unica de verdad para reproducibilidad.
"""
from pathlib import Path

# ----- Rutas -----
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
OUT = ROOT / "outputs"
FIG = OUT / "figures"
TAB = OUT / "tables"
for _p in (RAW, INTERIM, PROCESSED, FIG, TAB):
    _p.mkdir(parents=True, exist_ok=True)

# ----- Periodo -----
START = "2000-01-01"   # descarga amplia; el recorte de estudio se hace despues
STUDY_START = "2004-01-01"  # periodo de estudio (limitado por CLP=X)

# ----- Universo de activos (variable dependiente) -----
# Anillo A: nucleo cobre-Chile | B: mineria-materiales Chile | C: referencia int'l
ACTIVOS = {
    "ANTO.L":    {"nombre": "Antofagasta plc",        "anillo": "A", "moneda": "GBp", "mercado": "LSE"},
    "PUCOBRE.SN":{"nombre": "Pucobre",                "anillo": "A", "moneda": "CLP", "mercado": "Santiago"},
    "CAP.SN":    {"nombre": "CAP S.A.",               "anillo": "B", "moneda": "CLP", "mercado": "Santiago"},
    "SQM-B.SN":  {"nombre": "SQM-B",                  "anillo": "B", "moneda": "CLP", "mercado": "Santiago"},
    "SCCO":      {"nombre": "Southern Copper",        "anillo": "C", "moneda": "USD", "mercado": "NYSE"},
    "FCX":       {"nombre": "Freeport-McMoRan",       "anillo": "C", "moneda": "USD", "mercado": "NYSE"},
    "BHP":       {"nombre": "BHP",                    "anillo": "C", "moneda": "USD", "mercado": "NYSE"},
    "GLEN.L":    {"nombre": "Glencore",               "anillo": "C", "moneda": "GBp", "mercado": "LSE"},
}
ACTIVOS_NUCLEO = [t for t, v in ACTIVOS.items() if v["anillo"] == "A"]
ACTIVOS_PANEL = [t for t, v in ACTIVOS.items() if v["anillo"] in ("A", "B")]

# ----- Factores de mercado (independientes) descargables de Yahoo -----
FACTORES_YF = {
    "HG=F":     "cobre_comex",      # futuro cobre COMEX (USD/lb)
    "CLP=X":    "usdclp",           # USD/CLP
    "DX-Y.NYB": "dxy",              # indice dolar
    "^VIX":     "vix",              # volatilidad implicita SP500
    "^GSPC":    "sp500",            # SP500 (mercado global)
    "^IPSA":    "ipsa",             # IPSA (mercado local Chile)
    "ECH":      "ech",              # ETF iShares MSCI Chile (proxy mercado local, NYSE)
    "^TNX":     "ust10y",           # rendimiento UST 10Y (yahoo, %)
    "^FVX":     "ust5y",            # UST 5Y
    "^IRX":     "ust13w",           # T-bill 13 semanas
    "CL=F":     "wti",              # petroleo WTI (costo energia)
}

# ----- Series FRED (CSV directo, sin API key) -----
# canal economico entre parentesis
FRED = {
    "DGS10":      "ust10y_fred",     # tasa larga EEUU (descuento)
    "DGS2":       "ust2y_fred",      # tasa corta EEUU
    "T10Y2Y":     "pendiente_10y2y", # pendiente curva (ciclo/riesgo)
    "DTWEXBGS":   "dxy_broad",       # dolar amplio (moneda)
    "VIXCLS":     "vix_fred",        # VIX (riesgo/sentimiento)
    "PCOPPUSDM":  "cobre_global_m",  # precio global cobre mensual (demanda)
    "DCOILWTICO": "wti_fred",        # WTI (energia/costos)
    "CHNPMINDXM": "china_pmi_proxy", # (puede no existir; se intenta)
    "INDPRO":     "ip_eeuu",         # produccion industrial EEUU (demanda global)
}

# ----- Banco Central de Chile (requiere credenciales del usuario) -----
# Rellenar variables de entorno BCCH_USER y BCCH_PASS para activar.
BCCH_SERIES = {
    "F022.TPM.TIN.D001.NO.Z.D":  "tpm",       # Tasa de Politica Monetaria
    "F032.IMC.IND.Z.Z.EP18.Z.Z.0.M": "imacec",# IMACEC (a confirmar codigo)
    "F019.SPC.ITR.EM.NO.D":      "embi_chile",# EMBI Chile (a confirmar codigo)
}
