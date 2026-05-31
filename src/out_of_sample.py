"""
out_of_sample.py
----------------
Validacion FUERA DE MUESTRA de la transmision del cobre, por via predictiva.

Idea (prueba predictiva de H5): si la transmision en Pucobre es DIFERIDA por
iliquidez, entonces el cobre REZAGADO debe ayudar a predecir su retorno futuro mas
que en Antofagasta (donde el cobre ya esta incorporado contemporaneamente).

Esquema recursivo (expanding window) desde el 50% de la muestra:
  - Benchmark (anidado): y_t = a + b y_{t-1}                         (AR(1))
  - Modelo: y_t = a + b y_{t-1} + c1 dl_cobre_{t-1} + c2 dl_cobre_{t-2}
Se computan: R2 fuera de muestra (Campbell-Thompson) y el test de Clark-West
(apropiado para modelos anidados). CW>0 y significativo => el cobre rezagado mejora
la prediccion fuera de muestra.

Salida: outputs/tables/out_of_sample.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C


def _ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def oos(ret, ticker):
    d = pd.DataFrame({"y": ret[f"ret_{ticker}"]})
    d["y1"] = d["y"].shift(1)
    d["c1"] = ret["dl_cobre_comex"].shift(1)
    d["c2"] = ret["dl_cobre_comex"].shift(2)
    d = d.dropna()
    y = d["y"].values
    Xb = np.column_stack([np.ones(len(d)), d["y1"].values])                 # benchmark
    Xm = np.column_stack([np.ones(len(d)), d["y1"].values, d["c1"].values, d["c2"].values])  # modelo
    n = len(d); start = n // 2
    eb, em, cw_terms = [], [], []
    for t in range(start, n):
        bb = _ols(Xb[:t], y[:t]); fb = Xb[t] @ bb
        bm = _ols(Xm[:t], y[:t]); fm = Xm[t] @ bm
        eb.append(y[t] - fb); em.append(y[t] - fm)
        # termino Clark-West: (e_b^2) - (e_m^2) + (f_b - f_m)^2
        cw_terms.append(eb[-1] ** 2 - em[-1] ** 2 + (fb - fm) ** 2)
    eb = np.array(eb); em = np.array(em); cw = np.array(cw_terms)
    mspe_b = np.mean(eb ** 2); mspe_m = np.mean(em ** 2)
    r2_oos = 1 - mspe_m / mspe_b                       # Campbell-Thompson
    # Clark-West: regresion de cw sobre constante, t-stat (una cola)
    cw_mean = cw.mean(); cw_se = cw.std(ddof=1) / np.sqrt(len(cw))
    cw_t = cw_mean / cw_se
    cw_p = 1 - stats.norm.cdf(cw_t)                    # H1: modelo mejora (una cola)
    return dict(activo=ticker, n_oos=len(eb),
                R2_oos_pct=round(r2_oos * 100, 3),
                MSPE_bench=round(mspe_b, 4), MSPE_modelo=round(mspe_m, 4),
                ClarkWest_t=round(cw_t, 2), CW_pvalor=round(cw_p, 4),
                mejora="Sí (cobre rezagado ayuda)" if cw_p < 0.05 else "No significativa")


def main():
    ret = pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)
    filas = [oos(ret, t) for t in C.ACTIVOS_NUCLEO + ["CAP.SN", "SQM-B.SN"]]
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "out_of_sample.csv", index=False, encoding="utf-8-sig")
    print("=== Validación fuera de muestra: ¿el cobre REZAGADO mejora la predicción? ===")
    print(df.to_string(index=False))
    print("\nR2_oos>0 y Clark-West significativo => el cobre rezagado aporta poder")
    print("predictivo fuera de muestra. Se espera mayor aporte en el activo ilíquido")
    print("(Pucobre), consistente con transmisión diferida (H5).")


if __name__ == "__main__":
    main()
