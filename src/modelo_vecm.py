"""
modelo_vecm.py
--------------
Modelo de correccion de error vectorial (VECM) para la relacion de LARGO PLAZO
entre el log-precio del activo nucleo y [cobre, usdclp, dxy], con rango de
cointegracion r=1 (hallado por Johansen).

Reporta:
  - Vector de cointegracion (beta) normalizado al activo -> relacion de equilibrio.
  - Velocidad de ajuste (alpha) -> cuanto corrige por dia el desequilibrio.
  - Significancia del termino de correccion de error.
Salida: outputs/tables/vecm_<activo>.csv y vecm_resumen.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.vecm import VECM, select_order

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

VARS_FACTOR = ["l_cobre_comex", "l_usdclp", "l_dxy"]


def cargar():
    return pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)


def estimar(niv, ticker):
    cols = [f"lprice_{ticker}"] + VARS_FACTOR
    df = niv[cols].dropna()
    # seleccion de rezagos
    sel = select_order(df, maxlags=10, deterministic="ci")
    k = max(1, sel.aic)
    m = VECM(df, k_ar_diff=k, coint_rank=1, deterministic="ci").fit()

    # beta normalizado (primer elemento = 1 sobre el activo)
    beta = m.beta[:, 0]
    beta_norm = beta / beta[0]
    coint_vec = pd.Series(beta_norm, index=cols)
    # relacion de largo plazo: lprice = - (b_cobre*l_cobre + ...) (despejando)
    largo_plazo = -coint_vec[VARS_FACTOR]

    alpha = m.alpha[:, 0]  # velocidad de ajuste de cada ecuacion
    alpha_s = pd.Series(alpha, index=cols)

    res = dict(
        activo=ticker, n=len(df), k_ar_diff=k,
        LP_cobre=round(largo_plazo["l_cobre_comex"], 4),
        LP_usdclp=round(largo_plazo["l_usdclp"], 4),
        LP_dxy=round(largo_plazo["l_dxy"], 4),
        alpha_activo=round(alpha_s[f"lprice_{ticker}"], 4),
    )
    # guardar detalle
    det = pd.DataFrame({
        "variable": cols,
        "beta_coint_norm": np.round(coint_vec.values, 4),
        "alpha_ajuste": np.round(alpha_s.values, 4),
    })
    det.to_csv(C.TAB / f"vecm_{ticker.replace('.','_')}.csv", index=False, encoding="utf-8-sig")
    return res, largo_plazo, alpha_s


def main():
    niv = cargar()
    resumen = []
    for t in C.ACTIVOS_NUCLEO:
        res, lp, al = estimar(niv, t)
        resumen.append(res)
        print(f"\n=== VECM {t} (r=1, k_ar_diff={res['k_ar_diff']}) ===")
        print("Relación de LARGO PLAZO (elasticidades del log-precio):")
        print(f"  log P* = {res['LP_cobre']:+.3f}·log(cobre) "
              f"{res['LP_usdclp']:+.3f}·log(USDCLP) {res['LP_dxy']:+.3f}·log(DXY)")
        print(f"Velocidad de ajuste (alpha) del activo: {res['alpha_activo']:+.4f}")
        print("  (alpha<0 y significativo => corrige desequilibrios hacia el equilibrio)")
    df = pd.DataFrame(resumen)
    df.to_csv(C.TAB / "vecm_resumen.csv", index=False, encoding="utf-8-sig")
    print("\n=== VECM COMPLETO ===")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
