"""
robustez.py
-----------
1. Quiebre estructural en el log-precio (Zivot-Andrews) -> fecha de quiebre endógena.
2. Estabilidad de la beta-cobre por submuestras (pre/post crisis 2008, COVID 2020).
Salida: outputs/tables/robustez_quiebres.csv, robustez_submuestras.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from arch.unitroot import ZivotAndrews

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

REGRESORES = ["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500", "dl_ech", "d_ust10y"]
SUBM = {
    "pre-crisis 2004-2007": ("2004-01-01", "2007-12-31"),
    "crisis 2008-2009":     ("2008-01-01", "2009-12-31"),
    "supraciclo 2010-2014": ("2010-01-01", "2014-12-31"),
    "2015-2019":            ("2015-01-01", "2019-12-31"),
    "COVID+ 2020-2026":     ("2020-01-01", "2026-12-31"),
}


def quiebres(niv):
    filas = []
    for t in C.ACTIVOS_NUCLEO:
        s = niv[f"lprice_{t}"].dropna()
        try:
            za = ZivotAndrews(s, trend="c")
            filas.append(dict(activo=t, ZA_stat=round(za.stat, 3),
                              ZA_p=round(za.pvalue, 4)))
        except Exception as e:
            filas.append(dict(activo=t, ZA_stat=np.nan, ZA_p=np.nan))
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "robustez_quiebres.csv", index=False, encoding="utf-8-sig")
    print("=== Zivot-Andrews (raíz unitaria con quiebre endógeno en log-precio) ===")
    print(df.to_string(index=False))
    return df


def submuestras(ret):
    filas = []
    for t in C.ACTIVOS_NUCLEO:
        for nombre, (a, b) in SUBM.items():
            sub = ret.loc[a:b]
            df = sub[[f"ret_{t}"] + REGRESORES].dropna()
            if len(df) < 50:
                continue
            y = df[f"ret_{t}"]; X = sm.add_constant(df[REGRESORES])
            L = max(1, int(4 * (len(df) / 100) ** (2 / 9)))
            m = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": L})
            filas.append(dict(activo=t, submuestra=nombre, n=len(df),
                              beta_cobre=round(m.params["dl_cobre_comex"], 4),
                              t_cobre=round(m.tvalues["dl_cobre_comex"], 2),
                              R2=round(m.rsquared, 3)))
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "robustez_submuestras.csv", index=False, encoding="utf-8-sig")
    print("\n=== Estabilidad de la beta-cobre por submuestras (HAC) ===")
    for t in C.ACTIVOS_NUCLEO:
        print(f"\n--- {t} ---")
        print(df[df["activo"] == t][["submuestra", "n", "beta_cobre", "t_cobre", "R2"]].to_string(index=False))
    return df


if __name__ == "__main__":
    niv = pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)
    ret = pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)
    quiebres(niv)
    submuestras(ret)
    print("\n=== ROBUSTEZ COMPLETA ===")
