"""
modelo_var.py
-------------
VAR sobre retornos (I(0)) para dinamica conjunta:
  sistema = [ret_activo, dl_cobre, dl_usdclp, dl_dxy, dl_sp500]
Produce:
  - Seleccion de rezagos (AIC/BIC).
  - Funcion impulso-respuesta (IRF) del retorno del activo ante shock del cobre.
  - Descomposicion de varianza (FEVD): % de la varianza del activo explicado por cobre.
  - Causalidad de Granger cobre -> activo.
Salida: outputs/tables/var_fevd_<activo>.csv, var_granger.csv
        outputs/figures/irf_<activo>.png
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

SISTEMA_FACTORES = ["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500"]


def cargar():
    return pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)


def estimar(ret, ticker, horizonte=20):
    cols = [f"ret_{ticker}"] + SISTEMA_FACTORES
    df = ret[cols].dropna()
    model = VAR(df)
    sel = model.select_order(maxlags=10)
    p = sel.aic if sel.aic and sel.aic > 0 else 2
    res = model.fit(p)

    # Orden de Cholesky: factores globales primero, activo al final (mas endogeno)
    orden = SISTEMA_FACTORES + [f"ret_{ticker}"]
    df2 = df[orden]
    res2 = VAR(df2).fit(p)
    irf = res2.irf(horizonte)
    fevd = res2.fevd(horizonte)

    # IRF activo ante shock de cobre
    idx_activo = orden.index(f"ret_{ticker}")
    idx_cobre = orden.index("dl_cobre_comex")
    irf_vals = irf.irfs[:, idx_activo, idx_cobre]

    plt.figure(figsize=(9, 4.5))
    plt.bar(range(horizonte + 1), irf_vals, color="steelblue")
    plt.axhline(0, color="k", lw=0.6)
    plt.title(f"IRF: respuesta del retorno de {ticker} a un shock de +1 d.e. en cobre")
    plt.xlabel("días"); plt.ylabel("respuesta (%)")
    plt.tight_layout(); plt.savefig(C.FIG / f"irf_{ticker.replace('.','_')}.png", dpi=120)
    plt.close()

    # FEVD del activo
    fevd_activo = fevd.decomp[idx_activo]  # (horizonte, k)
    fevd_df = pd.DataFrame(fevd_activo, columns=orden)
    fevd_df.index.name = "horizonte"
    fevd_df = (fevd_df * 100).round(2)
    fevd_df.to_csv(C.TAB / f"var_fevd_{ticker.replace('.','_')}.csv", encoding="utf-8-sig")

    # Granger: cobre -> activo
    gr = res.test_causality(f"ret_{ticker}", ["dl_cobre_comex"], kind="f")

    return dict(activo=ticker, p=p, n=len(df),
                irf_dia0=round(irf_vals[0], 4), irf_dia1=round(irf_vals[1], 4),
                irf_acum5=round(irf_vals[:6].sum(), 4),
                fevd_cobre_h1=fevd_df["dl_cobre_comex"].iloc[0],
                fevd_cobre_h20=fevd_df["dl_cobre_comex"].iloc[-1],
                granger_cobre_p=round(gr.pvalue, 4))


def main():
    ret = cargar()
    filas = []
    for t in C.ACTIVOS_NUCLEO:
        r = estimar(ret, t)
        filas.append(r)
        print(f"\n=== VAR {t} (p={r['p']}) ===")
        print(f"  IRF a shock cobre: día0={r['irf_dia0']}  día1={r['irf_dia1']}  "
              f"acum 5d={r['irf_acum5']}")
        print(f"  FEVD: cobre explica {r['fevd_cobre_h1']}% de la varianza a 1d, "
              f"{r['fevd_cobre_h20']}% a 20d")
        print(f"  Granger cobre->activo: p={r['granger_cobre_p']} "
              f"({'causa' if r['granger_cobre_p']<0.05 else 'no causa'} en sentido Granger)")
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "var_resumen.csv", index=False, encoding="utf-8-sig")
    print("\n=== VAR COMPLETO ===")


if __name__ == "__main__":
    main()
