"""
modelo_nardl.py
---------------
NARDL (Shin, Yu & Greenberg, 2014) para ASIMETRIA en el efecto del cobre.

Descompone el log-precio del cobre en sumas parciales de variaciones positivas y
negativas:
    cobre_pos_t = sum_{j<=t} max(Δl_cobre_j, 0)
    cobre_neg_t = sum_{j<=t} min(Δl_cobre_j, 0)
y estima un ARDL/UECM con ambas + USDCLP. Tests:
  - Bounds F (cointegracion no lineal).
  - Asimetria de LARGO PLAZO: H0  beta_pos = beta_neg  (Wald).

Salida: outputs/tables/nardl_<activo>.csv, nardl_resumen.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.ardl import ARDL, UECM

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

# CV bounds PSS caso III, k=3 regresores
CV = {"5%": (3.23, 4.35), "1%": (4.29, 5.61)}


def cargar():
    return pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)


def sumas_parciales(l_cobre):
    d = l_cobre.diff()
    pos = d.clip(lower=0).cumsum()
    neg = d.clip(upper=0).cumsum()
    return pos.rename("cobre_pos"), neg.rename("cobre_neg")


def estimar(niv, ticker):
    y = niv[f"lprice_{ticker}"].copy()
    pos, neg = sumas_parciales(niv["l_cobre_comex"])
    X = pd.concat([pos, neg, niv["l_usdclp"]], axis=1)
    df = pd.concat([y, X], axis=1).dropna()
    y = df[f"lprice_{ticker}"]; X = df[["cobre_pos", "cobre_neg", "l_usdclp"]]

    modelo = ARDL(y, 2, X, 2, trend="c")
    uecm = UECM.from_ardl(modelo).fit()
    bt = uecm.bounds_test(case=3)
    fstat = float(bt.stat)

    lr = uecm.ci_params
    lp_pos = float(lr.get("cobre_pos", np.nan))
    lp_neg = float(lr.get("cobre_neg", np.nan))

    # Test de asimetria de largo plazo: beta_pos == beta_neg
    nombres = list(uecm.params.index)
    try:
        # construir restriccion sobre los parametros de nivel del UECM
        idx_pos = [n for n in nombres if "cobre_pos" in n and ".L1" in n]
        idx_neg = [n for n in nombres if "cobre_neg" in n and ".L1" in n]
        if idx_pos and idx_neg:
            R = f"{idx_pos[0]} = {idx_neg[0]}"
            w = uecm.wald_test(R, scalar=True)
            asim_stat, asim_p = float(w.statistic), float(w.pvalue)
        else:
            asim_stat = asim_p = np.nan
    except Exception:
        asim_stat = asim_p = np.nan

    def veredicto(f):
        if f > CV["1%"][1]: return "cointegra (1%)"
        if f > CV["5%"][1]: return "cointegra (5%)"
        if f < CV["5%"][0]: return "no cointegra (5%)"
        return "no concluyente"

    return dict(activo=ticker, n=len(df), F_bounds=round(fstat, 3),
                veredicto=veredicto(fstat),
                LP_cobre_pos=round(lp_pos, 4), LP_cobre_neg=round(lp_neg, 4),
                asim_Wald=round(asim_stat, 3) if asim_stat == asim_stat else np.nan,
                asim_p=round(asim_p, 4) if asim_p == asim_p else np.nan)


def main():
    niv = cargar()
    filas = []
    for t in C.ACTIVOS_NUCLEO + ["CAP.SN", "SQM-B.SN"]:
        try:
            r = estimar(niv, t)
            filas.append(r)
            print(f"\n=== NARDL {t} ===")
            print(f"  Bounds F={r['F_bounds']} -> {r['veredicto']}")
            print(f"  LP cobre+ (alzas)={r['LP_cobre_pos']}  | LP cobre- (caídas)={r['LP_cobre_neg']}")
            print(f"  Asimetría largo plazo (H0: +=-): Wald={r['asim_Wald']} p={r['asim_p']} "
                  f"-> {'ASIMÉTRICO' if (r['asim_p']==r['asim_p'] and r['asim_p']<0.05) else 'no se rechaza simetría'}")
        except Exception as e:
            print(f"  {t}: ERROR {e}")
    if filas:
        pd.DataFrame(filas).to_csv(C.TAB / "nardl_resumen.csv", index=False, encoding="utf-8-sig")
    print("\nNota: si beta_pos != beta_neg (Wald p<.05), la acción responde de forma")
    print("distinta a alzas vs caídas del cobre (asimetría).")


if __name__ == "__main__":
    main()
