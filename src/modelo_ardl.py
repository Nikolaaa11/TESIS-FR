"""
modelo_ardl.py
--------------
ARDL bounds test (Pesaran-Shin-Smith) como ROBUSTEZ de la relacion de largo
plazo cobre->valoracion, valido con mezcla I(0)/I(1) sin I(2).

  lprice_activo ~ l_cobre + l_usdclp   (mensual para reducir ruido diario)

Reporta: orden ARDL seleccionado, bounds F-test, coeficientes de largo plazo
y velocidad de ajuste (ECM). Salida: outputs/tables/ardl_<activo>.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.ardl import ARDL, UECM, ardl_select_order

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

# valores criticos bounds test PSS (2001), caso III (intercepto sin tendencia), k=3 regresores
# I(0) / I(1) al 5% y 1%
CV = {"5%": (3.23, 4.35), "1%": (4.29, 5.61)}  # k=3, caso III


def cargar_mensual():
    # frecuencia DIARIA (comparable a VECM/Johansen); nombre histórico conservado
    niv = pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)
    return niv


def estimar(m, ticker):
    cols = [f"lprice_{ticker}", "l_cobre_comex", "l_usdclp", "l_dxy"]
    df = m[cols].dropna()
    y = df[f"lprice_{ticker}"]
    X = df[["l_cobre_comex", "l_usdclp", "l_dxy"]]
    # Orden fijo p=2 y q=2 por exógeno (garantiza lag>=1 para la representación ECM)
    modelo = ARDL(y, 2, X, 2, trend="c")
    orden = modelo.ardl_order

    # UECM (corrección de error no restringido) para bounds test y largo plazo
    uecm = UECM.from_ardl(modelo).fit()
    bt = uecm.bounds_test(case=3)
    fstat = float(bt.stat)

    # coeficientes de largo plazo (relación de cointegración) desde el UECM
    lr = uecm.ci_params
    lp_cobre = float(lr.get("l_cobre_comex", np.nan))
    lp_usdclp = float(lr.get("l_usdclp", np.nan))
    lp_dxy = float(lr.get("l_dxy", np.nan))

    # Veredicto bounds
    def veredicto(f):
        if f > CV["1%"][1]: return "cointegra (1%)"
        if f > CV["5%"][1]: return "cointegra (5%)"
        if f < CV["5%"][0]: return "no cointegra (5%)"
        return "no concluyente"

    return dict(activo=ticker, n=len(df), orden=str(orden),
                F_bounds=round(fstat, 3),
                LP_cobre=round(lp_cobre, 4), LP_usdclp=round(lp_usdclp, 4),
                LP_dxy=round(lp_dxy, 4),
                cv5_I0=CV["5%"][0], cv5_I1=CV["5%"][1],
                veredicto=veredicto(fstat))


def main():
    m = cargar_mensual()
    filas = []
    for t in C.ACTIVOS_NUCLEO:
        try:
            r = estimar(m, t)
            filas.append(r)
            print(f"\n=== ARDL {t} (diario, 3 regresores) ===")
            print(f"  orden ARDL: {r['orden']}  n={r['n']}")
            print(f"  Bounds F = {r['F_bounds']}  (CV 5%: I0={r['cv5_I0']}, I1={r['cv5_I1']})")
            print(f"  -> {r['veredicto']}")
            print(f"  Largo plazo: cobre={r['LP_cobre']}, usdclp={r['LP_usdclp']}, dxy={r['LP_dxy']}")
        except Exception as e:
            print(f"  {t}: ERROR {e}")
    if filas:
        pd.DataFrame(filas).to_csv(C.TAB / "ardl_bounds.csv", index=False, encoding="utf-8-sig")
    print("\nNota: F>I1 confirma relación de largo plazo (cointegración), consistente con VECM.")


if __name__ == "__main__":
    main()
