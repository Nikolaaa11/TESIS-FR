"""
modelo_mensual.py
-----------------
Modelo de impacto a frecuencia MENSUAL, que permite usar la macro nacional de
Chile en su frecuencia natural: IMACEC (var% actividad) e IPC (inflacion), junto a
TPM, cobre, USDCLP y DXY.

  ret_mensual_activo = a + b1 ret_cobre + b2 d_tpm + b3 imacec + b4 ipc
                       + b5 ret_usdclp + b6 ret_dxy + e

OLS con errores HAC. Salida: outputs/tables/mensual_<activo>.csv, mensual_resumen.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C


def cargar_mensual():
    px = pd.read_csv(C.RAW / "precios_activos.csv", index_col=0, parse_dates=True)
    fa = pd.read_csv(C.RAW / "factores_yahoo.csv", index_col=0, parse_dates=True)
    mc = pd.read_csv(C.RAW / "macro_chile.csv", index_col=0, parse_dates=True)

    # precios -> retorno mensual (%)
    pm = px.resample("ME").last()
    ret_act = np.log(pm).diff() * 100

    fm = fa.resample("ME").last()
    ret_cobre = np.log(fm["cobre_comex"]).diff() * 100
    ret_usdclp = np.log(fm["usdclp"]).diff() * 100
    ret_dxy = np.log(fm["dxy"]).diff() * 100

    # macro mensual: IMACEC e IPC ya vienen como var% mensual; TPM nivel -> diff
    mcm = mc.resample("ME").last()
    d_tpm = mcm["tpm"].diff()
    imacec = mcm["imacec"]
    ipc = mcm["ipc"]

    X = pd.concat([ret_cobre.rename("ret_cobre"), d_tpm.rename("d_tpm"),
                   imacec.rename("imacec"), ipc.rename("ipc"),
                   ret_usdclp.rename("ret_usdclp"), ret_dxy.rename("ret_dxy")], axis=1)
    return ret_act, X


def estimar(ret_act, X, ticker):
    df = pd.concat([ret_act[ticker].rename("y"), X], axis=1).dropna()
    if len(df) < 40:
        return None
    y = df["y"]; XX = sm.add_constant(df[X.columns])
    L = max(1, int(4 * (len(df) / 100) ** (2 / 9)))
    m = sm.OLS(y, XX).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    out = pd.DataFrame({"var": m.params.index, "coef": m.params.values,
                        "t": m.tvalues.values, "p": m.pvalues.values}).round(4)
    out.to_csv(C.TAB / f"mensual_{ticker.replace('.','_')}.csv", index=False, encoding="utf-8-sig")
    return dict(activo=ticker, n=int(m.nobs), R2=round(m.rsquared, 3),
                beta_cobre=round(m.params["ret_cobre"], 4),
                t_cobre=round(m.tvalues["ret_cobre"], 2),
                imacec=round(m.params["imacec"], 4), t_imacec=round(m.tvalues["imacec"], 2),
                d_tpm=round(m.params["d_tpm"], 4), t_tpm=round(m.tvalues["d_tpm"], 2)), m


def main():
    ret_act, X = cargar_mensual()
    filas = []
    for t in C.ACTIVOS_NUCLEO + ["CAP.SN", "SQM-B.SN"]:
        r = estimar(ret_act, X, t)
        if r is None:
            continue
        res, m = r
        filas.append(res)
        print(f"\n=== Mensual {t} (n={res['n']}, R2={res['R2']}) ===")
        print(pd.read_csv(C.TAB / f"mensual_{t.replace('.','_')}.csv").to_string(index=False))
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "mensual_resumen.csv", index=False, encoding="utf-8-sig")
    print("\n=== Resumen mensual (cobre / IMACEC / TPM) ===")
    print(df.to_string(index=False))
    print("\nIMACEC: actividad económica Chile (var% mensual). d_tpm: cambio TPM (pp).")


if __name__ == "__main__":
    main()
