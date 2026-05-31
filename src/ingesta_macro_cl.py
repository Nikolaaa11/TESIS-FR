"""
ingesta_macro_cl.py
-------------------
Macro NACIONAL de Chile sin credenciales, via API publica gratuita mindicador.cl.
Series: TPM (Tasa Politica Monetaria, diaria), IMACEC (mensual, var%),
        IPC (mensual, var%), dolar observado (diario, CLP/USD oficial).

Itera por año (el endpoint base solo da el año corriente). Guarda:
  data/raw/macro_chile.csv  (union diaria; mensuales con fecha de publicacion)
"""
import os, sys, time
import pandas as pd
import requests

sys.path.append(os.path.dirname(__file__))
import config as C

INDICADORES = ["tpm", "imacec", "ipc", "dolar"]
ANIOS = list(range(2004, 2027))
HDR = {"User-Agent": "Mozilla/5.0"}


def bajar_indicador(ind):
    filas = []
    for a in ANIOS:
        try:
            r = requests.get(f"https://mindicador.cl/api/{ind}/{a}", timeout=30, headers=HDR)
            r.raise_for_status()
            serie = r.json().get("serie", [])
            for obs in serie:
                filas.append((pd.to_datetime(obs["fecha"]).tz_localize(None).normalize(),
                              obs["valor"]))
        except Exception as e:
            print(f"    -- {ind} {a}: {type(e).__name__}")
        time.sleep(0.15)
    if not filas:
        return None
    s = pd.Series(dict(filas)).sort_index()
    s.name = ind
    s = s[~s.index.duplicated(keep="last")]
    return s


def main():
    print("[CL] Macro Chile via mindicador.cl (sin credenciales)...")
    series = {}
    for ind in INDICADORES:
        s = bajar_indicador(ind)
        if s is not None:
            series[ind] = s
            print(f"    OK {ind:8s} n={len(s)}  {s.index.min().date()}..{s.index.max().date()}")
    df = pd.concat(series.values(), axis=1).sort_index()
    df.index.name = "fecha"
    out = C.RAW / "macro_chile.csv"
    df.to_csv(out, encoding="utf-8-sig")
    print(f"    -> {out.name}: {df.shape}")
    return df


if __name__ == "__main__":
    main()
