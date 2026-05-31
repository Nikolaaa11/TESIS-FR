"""
modelo_toda_yamamoto.py
-----------------------
Causalidad de Toda-Yamamoto (1995): valida con series integradas/cointegradas sin
necesidad de pre-diferenciar. Procedimiento (enfoque uniecuacional aumentado):

  1. d_max = orden maximo de integracion (=1, log-precios y log-cobre son I(1)).
  2. p = rezago optimo (AIC) de un VAR en niveles.
  3. Regresion aumentada de Y sobre const + Y_{t-1..p+dmax} + X_{t-1..p+dmax}.
  4. Test de Wald (F) sobre los PRIMEROS p rezagos de X (se excluyen los d_max
     rezagos extra). H0: X no causa-Granger a Y. Errores HAC.

Prueba cobre<->activo y usdclp->activo. Salida: outputs/tables/toda_yamamoto.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.api import VAR

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

DMAX = 1


def cargar():
    return pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)


def lags(df, cols, p):
    out = {}
    for c in cols:
        for L in range(1, p + 1):
            out[f"{c}_L{L}"] = df[c].shift(L)
    return pd.DataFrame(out, index=df.index)


def ty_test(df, y_col, x_col, p):
    total = p + DMAX
    Y = df[y_col]
    Xl = lags(df, [y_col, x_col], total)
    data = pd.concat([Y, Xl], axis=1).dropna()
    yy = data[y_col]
    XX = sm.add_constant(data.drop(columns=[y_col]))
    L = max(1, int(4 * (len(data) / 100) ** (2 / 9)))
    m = sm.OLS(yy, XX).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    # restriccion: x_col_L1 ... x_col_Lp = 0 (NO incluir los DMAX extra)
    restr = [f"{x_col}_L{L_}" for L_ in range(1, p + 1)]
    restr = [r for r in restr if r in XX.columns]
    w = m.f_test(" = 0, ".join(restr) + " = 0")
    return float(w.statistic), float(w.pvalue), len(restr)


def main():
    niv = cargar()
    filas = []
    for t in C.ACTIVOS_NUCLEO:
        cols = [f"lprice_{t}", "l_cobre_comex", "l_usdclp"]
        df = niv[cols].dropna()
        # p optimo por VAR en niveles
        p = VAR(df).select_order(maxlags=12).aic or 2
        p = max(2, int(p))
        pares = [
            ("cobre->activo", f"lprice_{t}", "l_cobre_comex"),
            ("activo->cobre", "l_cobre_comex", f"lprice_{t}"),
            ("usdclp->activo", f"lprice_{t}", "l_usdclp"),
        ]
        print(f"\n=== Toda-Yamamoto {t} (p={p}, d_max={DMAX}) ===")
        for nombre, ycol, xcol in pares:
            stat, pval, k = ty_test(df, ycol, xcol, p)
            causa = "CAUSA" if pval < 0.05 else "no causa"
            filas.append(dict(activo=t, relacion=nombre, p=p, F=round(stat, 3),
                              p_valor=round(pval, 4), veredicto=causa))
            print(f"  {nombre:16s} F={stat:8.3f}  p={pval:.4f}  -> {causa}")
    pd.DataFrame(filas).to_csv(C.TAB / "toda_yamamoto.csv", index=False, encoding="utf-8-sig")
    print("\nTY es robusto a integracion/cointegracion (no requiere diferenciar).")


if __name__ == "__main__":
    main()
