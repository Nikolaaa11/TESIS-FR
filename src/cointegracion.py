"""
cointegracion.py
----------------
Tests de cointegracion entre log-precios I(1) de los activos nucleo cobre y los
factores I(1) relevantes (cobre, usdclp, dxy). Decide ARDL vs VECM.

  - Engle-Granger bivariado: activo ~ cobre.
  - Johansen multivariante: [lprice_activo, l_cobre, l_usdclp] (y dxy para ANTO).
Salida: outputs/tables/cointegracion_*.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen, select_coint_rank

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C


def cargar():
    return pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)


def engle_granger(niv):
    filas = []
    for t in C.ACTIVOS_NUCLEO + ["SCCO", "FCX", "BHP"]:
        col = f"lprice_{t}"
        sub = niv[[col, "l_cobre_comex"]].dropna()
        stat, p, _ = coint(sub[col], sub["l_cobre_comex"], trend="c")
        filas.append(dict(par=f"{t}~cobre", n=len(sub), EG_stat=round(stat, 3),
                          EG_p=round(p, 4),
                          cointegra="Sí (p<.05)" if p < 0.05 else "No"))
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "cointegracion_engle_granger.csv", index=False, encoding="utf-8-sig")
    print("\n=== Engle-Granger: activo vs precio del cobre ===")
    print(df.to_string(index=False))
    return df


def johansen(niv):
    print("\n=== Johansen (traza) por activo núcleo ===")
    resumen = []
    for t in C.ACTIVOS_NUCLEO:
        cols = [f"lprice_{t}", "l_cobre_comex", "l_usdclp", "l_dxy"]
        sub = niv[cols].dropna()
        jr = coint_johansen(sub, det_order=0, k_ar_diff=2)
        trace = jr.lr1                      # estadístico de traza
        cv = jr.cvt[:, 1]                   # valores críticos 95%
        r = 0
        for i in range(len(trace)):
            if trace[i] > cv[i]:
                r = i + 1
            else:
                break
        print(f"\n{t} — vars={cols}")
        for i in range(len(trace)):
            marca = "*" if trace[i] > cv[i] else " "
            print(f"  r<={i}: traza={trace[i]:8.3f}  cv95={cv[i]:8.3f} {marca}")
        print(f"  -> rango de cointegración estimado: r = {r}")
        resumen.append(dict(activo=t, rango_coint=r, n=len(sub),
                            vars=";".join(cols)))
    df = pd.DataFrame(resumen)
    df.to_csv(C.TAB / "cointegracion_johansen.csv", index=False, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    niv = cargar()
    engle_granger(niv)
    johansen(niv)
    print("\n=== COINTEGRACIÓN COMPLETA ===")
