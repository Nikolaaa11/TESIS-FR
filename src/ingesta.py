"""
ingesta.py
----------
Descarga de datos REALES para la tesis. Tres fuentes:
  1. Yahoo Finance (yfinance): precios de activos y factores de mercado.
  2. FRED (CSV directo, sin API key): macro/tasas EEUU y precio global del cobre.
  3. Banco Central de Chile (API, requiere credenciales): TPM, IMACEC, EMBI.

Guarda todo en data/raw/ (un CSV por serie/grupo) con metadatos de descarga.
Reproducible: no inventa nada; si una fuente falla, lo reporta y continua.
"""
import os
import io
import sys
import time
import datetime as dt

import pandas as pd
import requests
import yfinance as yf

sys.path.append(os.path.dirname(__file__))
import config as C

HOY = "2026-05-30"  # fecha de descarga (entorno sin reloj de sistema fiable)


# ----------------------------------------------------------------------
# 1) Precios de activos (variable dependiente)
# ----------------------------------------------------------------------
def descargar_precios():
    print("[1] Precios de activos (Yahoo)...")
    tickers = list(C.ACTIVOS.keys())
    df = yf.download(tickers, start=C.START, progress=False, auto_adjust=True)
    close = df["Close"].copy()
    close.index.name = "fecha"
    out = C.RAW / "precios_activos.csv"
    close.to_csv(out, encoding="utf-8-sig")
    print(f"    -> {out.name}: {close.shape[0]} filas x {close.shape[1]} activos")
    return close


# ----------------------------------------------------------------------
# 2) Factores de mercado (Yahoo)
# ----------------------------------------------------------------------
def descargar_factores_yf():
    # Descarga UNO A UNO para evitar NaN por desalineación de calendarios en el
    # modo multi-ticker de yfinance (problema detectado con ^IPSA post-2020).
    print("[2] Factores de mercado (Yahoo, individual)...")
    series = {}
    for tk, nombre in C.FACTORES_YF.items():
        try:
            d = yf.download(tk, start=C.START, progress=False, auto_adjust=True)["Close"]
            s = d.iloc[:, 0] if hasattr(d, "columns") else d
            s.name = nombre
            series[nombre] = s
            print(f"    OK {tk:10s} -> {nombre:14s} n={s.notna().sum()}")
        except Exception as e:
            print(f"    -- {tk:10s} FALLO: {e}")
    close = pd.concat(series.values(), axis=1).sort_index()
    close.index.name = "fecha"
    out = C.RAW / "factores_yahoo.csv"
    close.to_csv(out, encoding="utf-8-sig")
    print(f"    -> {out.name}: {close.shape[0]} filas x {close.shape[1]} factores")
    return close


# ----------------------------------------------------------------------
# 3) FRED (CSV directo)
# ----------------------------------------------------------------------
def _fred_csv(series_id):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    s = pd.read_csv(io.StringIO(r.text))
    # FRED entrega columnas: observation_date, <ID>  (o DATE en versiones viejas)
    fecha_col = s.columns[0]
    val_col = s.columns[1]
    s[fecha_col] = pd.to_datetime(s[fecha_col], errors="coerce")
    s[val_col] = pd.to_numeric(s[val_col], errors="coerce")
    s = s.dropna(subset=[fecha_col]).set_index(fecha_col)[[val_col]]
    s.columns = [series_id]
    return s


def descargar_fred():
    print("[3] Series FRED (CSV directo)...")
    series = {}
    for sid, nombre in C.FRED.items():
        try:
            s = _fred_csv(sid)
            s.columns = [nombre]
            series[nombre] = s
            print(f"    OK {sid:12s} -> {nombre:18s} n={len(s)}")
        except Exception as e:
            print(f"    -- {sid:12s} FALLO: {e}")
        time.sleep(0.4)
    if not series:
        return None
    df = pd.concat(series.values(), axis=1).sort_index()
    df.index.name = "fecha"
    out = C.RAW / "factores_fred.csv"
    df.to_csv(out, encoding="utf-8-sig")
    print(f"    -> {out.name}: {df.shape[0]} filas x {df.shape[1]} series")
    return df


# ----------------------------------------------------------------------
# 4) Banco Central de Chile (requiere credenciales)
# ----------------------------------------------------------------------
def descargar_bcch():
    user = os.environ.get("BCCH_USER")
    pw = os.environ.get("BCCH_PASS")
    print("[4] Banco Central de Chile (API)...")
    if not user or not pw:
        print("    -- SALTADO: definir BCCH_USER y BCCH_PASS en variables de entorno.")
        print("       Registro gratuito en https://si3.bcentral.cl/Siete/")
        return None
    base = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    series = {}
    for sid, nombre in C.BCCH_SERIES.items():
        try:
            params = {"user": user, "pass": pw, "function": "GetSeries",
                      "timeseries": sid, "firstdate": "2000-01-01"}
            r = requests.get(base, params=params, timeout=40)
            r.raise_for_status()
            js = r.json()
            obs = js.get("Series", {}).get("Obs", [])
            if not obs:
                print(f"    -- {sid}: sin observaciones")
                continue
            s = pd.DataFrame(obs)
            s["indexDateString"] = pd.to_datetime(s["indexDateString"], dayfirst=True, errors="coerce")
            s["value"] = pd.to_numeric(s["value"], errors="coerce")
            s = s.dropna(subset=["indexDateString"]).set_index("indexDateString")[["value"]]
            s.columns = [nombre]
            series[nombre] = s
            print(f"    OK {nombre}: n={len(s)}")
        except Exception as e:
            print(f"    -- {sid}: FALLO {e}")
    if not series:
        return None
    df = pd.concat(series.values(), axis=1).sort_index()
    df.index.name = "fecha"
    out = C.RAW / "macro_bcch.csv"
    df.to_csv(out, encoding="utf-8-sig")
    print(f"    -> {out.name}")
    return df


def main():
    print(f"=== INGESTA DE DATOS (descarga {HOY}) ===")
    descargar_precios()
    descargar_factores_yf()
    descargar_fred()
    descargar_bcch()
    print("=== FIN INGESTA ===")


if __name__ == "__main__":
    main()
