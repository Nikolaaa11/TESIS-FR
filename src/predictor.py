"""
predictor.py
------------
Predictor del precio/retorno para la PLATAFORMA (herramienta aplicada, separada del
enfoque explicativo de la tesis). Dos componentes, ambos honestos:

  1. BACKTEST de un modelo lineal transparente que predice el retorno del DÍA
     SIGUIENTE con informacion disponible hoy:
         ret_{t+1} = a + b1 ret_t + b2 dl_cobre_t + b3 dl_cobre_{t-1}
                     + b4 dl_dxy_t + b5 dl_sp500_t + e
     Estimacion en ventana expansiva (out-of-sample real). Metricas: R2 OOS,
     RMSE, y PRECISION DIRECCIONAL (% de aciertos de signo) vs un benchmark naive.

  2. SIMULADOR de escenarios: elasticidades-cobre por horizonte (del analisis de la
     tesis) para un calculo what-if cliente: "si el cobre sube X%, el precio se
     mueve ~elasticidad*X% a cada horizonte".

Salidas: outputs/tables/predictor_metrics.csv, predictor_scenario.csv,
         outputs/tables/predictor_backtest_<activo>.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

ACTIVOS_PRED = ["ANTO.L", "PUCOBRE.SN"]


def _ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def backtest(ret, niv, ticker):
    d = pd.DataFrame({"y_next": ret[f"ret_{ticker}"].shift(-1)})   # objetivo: t+1
    d["y"] = ret[f"ret_{ticker}"]
    d["c0"] = ret["dl_cobre_comex"]
    d["c1"] = ret["dl_cobre_comex"].shift(1)
    d["dxy"] = ret["dl_dxy"]
    d["sp"] = ret["dl_sp500"]
    feats = ["y", "c0", "c1", "dxy", "sp"]
    d = d.dropna()
    X = np.column_stack([np.ones(len(d))] + [d[f].values for f in feats])
    y = d["y_next"].values
    lprice = niv[f"lprice_{ticker}"].reindex(d.index)
    n = len(d); start = int(0.6 * n)
    preds, acts, dates, pp, ap = [], [], [], [], []
    for t in range(start, n):
        b = _ols(X[:t], y[:t]); f = X[t] @ b
        preds.append(f); acts.append(y[t]); dates.append(d.index[t])
        # precio implicito: P_hoy * exp(ret_pred/100)
        p_hoy = float(np.exp(lprice.iloc[t])) if np.isfinite(lprice.iloc[t]) else np.nan
        pp.append(p_hoy * np.exp(f / 100)); ap.append(p_hoy * np.exp(y[t] / 100))
    preds, acts = np.array(preds), np.array(acts)
    rmse = float(np.sqrt(np.mean((acts - preds) ** 2)))
    rmse_naive = float(np.sqrt(np.mean(acts ** 2)))           # benchmark: predecir 0 (caminata)
    r2_oos = 1 - (rmse / rmse_naive) ** 2                      # R2 OOS vs benchmark caminata
    # precision direccional SOLO en dias de retorno no nulo (evita el artefacto de
    # los dias sin transaccion de los activos iliquidos, donde sign(0) nunca coincide)
    nz = np.abs(acts) > 1e-9
    dir_acc = float(np.mean(np.sign(preds[nz]) == np.sign(acts[nz])) * 100) if nz.sum() else np.nan
    # serie para graficar (ultimos 180 dias, precio real vs predicho)
    bt = pd.DataFrame({"fecha": dates, "precio_real": ap, "precio_pred": pp}).dropna().tail(180)
    bt.to_csv(C.TAB / f"predictor_backtest_{ticker.replace('.','_')}.csv", index=False, encoding="utf-8-sig")
    return dict(activo=ticker, n_oos=len(preds), RMSE=round(rmse, 4),
                RMSE_naive=round(rmse_naive, 4),
                mejora_vs_naive_pct=round((1 - rmse / rmse_naive) * 100, 2),
                R2_oos_pct=round(r2_oos * 100, 3),
                precision_direccional_pct=round(dir_acc, 1))


def main():
    ret = pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)
    niv = pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)

    met = [backtest(ret, niv, t) for t in ACTIVOS_PRED]
    mdf = pd.DataFrame(met)
    mdf.to_csv(C.TAB / "predictor_metrics.csv", index=False, encoding="utf-8-sig")
    print("=== Backtest del predictor (out-of-sample, retorno t+1) ===")
    print(mdf.to_string(index=False))

    # escenario: elasticidades-cobre por horizonte (de la tesis)
    esc = pd.DataFrame([
        {"activo": "ANTO.L", "dia0": 0.70, "acum5": 0.86, "mensual": 0.71, "largo_plazo": 0.86, "elast_dxy": -0.35},
        {"activo": "PUCOBRE.SN", "dia0": 0.085, "acum5": 0.42, "mensual": 0.60, "largo_plazo": 0.75, "elast_dxy": -0.07},
    ])
    esc.to_csv(C.TAB / "predictor_scenario.csv", index=False, encoding="utf-8-sig")
    print("\n=== Elasticidades del simulador (cobre por horizonte) ===")
    print(esc.to_string(index=False))
    print("\nNota: predecir retornos diarios es intrínsecamente difícil (R2 OOS pequeño);")
    print("se reporta precisión direccional y mejora vs benchmark naive con honestidad.")
    print("El simulador what-if se apoya en elasticidades ESTIMADAS, no en un pronóstico ciego.")


if __name__ == "__main__":
    main()
