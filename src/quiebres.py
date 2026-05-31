"""
quiebres.py
-----------
Prueba de QUIEBRE ESTRUCTURAL con fecha endogena (Quandt-Andrews / sup-Chow) sobre
la regresion de transmision del cobre, para evaluar la estabilidad de la beta-cobre
a lo largo de 2004-2026 (GFC 2008, superciclo, COVID, boom pospandemia).

Para cada activo nucleo estima r_t = a + b1 dl_cobre + b2 dl_dxy + b3 dl_sp500 + e y
calcula el estadistico sup-Chow sobre todas las fechas candidatas de quiebre en el
rango central [15%, 85%]. Reporta supF, la fecha de quiebre estimada y la beta-cobre
pre/post. Valores criticos de Andrews (1993/2003) para k restricciones: el sup-F al
5% ronda ~ (k=4) 16.5 (trim 15%); se reporta supF y veredicto aproximado.

Salida: outputs/tables/quiebres_estructurales.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

REG = ["dl_cobre_comex", "dl_dxy", "dl_sp500"]
TRIM = 0.15
# valor critico aproximado sup-Wald (Andrews) 5%, trim 0.15, segun nº de parametros k
CV5 = {2: 11.79, 3: 13.81, 4: 16.45, 5: 18.04, 6: 20.26}


def cargar():
    return pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)


def sup_chow(df, ycol):
    d = df[[ycol] + REG].dropna()
    y = d[ycol].values
    X = sm.add_constant(d[REG]).values
    n, k = X.shape
    # SSR restringido (sin quiebre)
    b_r = np.linalg.lstsq(X, y, rcond=None)[0]
    ssr_r = np.sum((y - X @ b_r) ** 2)
    lo, hi = int(TRIM * n), int((1 - TRIM) * n)
    mejorF, mejor_i = -1, None
    paso = max(1, (hi - lo) // 400)  # submuestreo para velocidad
    for i in range(lo, hi, paso):
        X1, y1 = X[:i], y[:i]
        X2, y2 = X[i:], y[i:]
        try:
            b1 = np.linalg.lstsq(X1, y1, rcond=None)[0]
            b2 = np.linalg.lstsq(X2, y2, rcond=None)[0]
        except Exception:
            continue
        ssr_u = np.sum((y1 - X1 @ b1) ** 2) + np.sum((y2 - X2 @ b2) ** 2)
        F = ((ssr_r - ssr_u) / k) / (ssr_u / (n - 2 * k))
        if F > mejorF:
            mejorF, mejor_i = F, i
    fecha = d.index[mejor_i]
    # betas pre/post del cobre
    pre = sm.OLS(d[ycol].iloc[:mejor_i], sm.add_constant(d[REG].iloc[:mejor_i])).fit(
        cov_type="HAC", cov_kwds={"maxlags": 5})
    post = sm.OLS(d[ycol].iloc[mejor_i:], sm.add_constant(d[REG].iloc[mejor_i:])).fit(
        cov_type="HAC", cov_kwds={"maxlags": 5})
    return dict(activo=ycol.replace("ret_", ""), n=n, supF=round(mejorF, 2),
                cv5=CV5.get(k + 1, 16.45),
                quiebre=str(fecha.date()),
                beta_cobre_pre=round(pre.params["dl_cobre_comex"], 4),
                beta_cobre_post=round(post.params["dl_cobre_comex"], 4),
                hay_quiebre="Sí" if mejorF > CV5.get(k + 1, 16.45) else "No al 5%")


def main():
    df = cargar()
    filas = []
    for t in C.ACTIVOS_NUCLEO + ["CAP.SN", "SQM-B.SN"]:
        r = sup_chow(df, f"ret_{t}")
        filas.append(r)
        print(f"{r['activo']:11s} supF={r['supF']:7.2f} (cv5≈{r['cv5']})  quiebre={r['quiebre']}  "
              f"beta_cobre {r['beta_cobre_pre']} -> {r['beta_cobre_post']}  [{r['hay_quiebre']}]")
    out = pd.DataFrame(filas)
    out.to_csv(C.TAB / "quiebres_estructurales.csv", index=False, encoding="utf-8-sig")
    print("\nQuandt-Andrews sup-Chow: H0 = no quiebre. supF>cv5 => quiebre significativo.")
    print("La beta-cobre pre/post documenta cómo cambió la transmisión en torno al quiebre.")


if __name__ == "__main__":
    main()
