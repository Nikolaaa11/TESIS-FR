"""
modelo_event_study.py
----------------------
Estudio de eventos: reaccion de las acciones a ANUNCIOS DE CAMBIO DE TPM
(Banco Central de Chile), separando alzas y bajas.

Metodologia clasica:
  - Eventos = dias en que la TPM cambia respecto al dia previo.
  - Modelo de mercado estimado en ventana [-130,-11] dias: R_it = a + b R_mt + e.
    (mercado = ECH, proxy MSCI Chile)
  - Retorno anormal AR_it = R_it - (a + b R_mt) en ventana de evento [-5,+5].
  - CAR por evento; CAAR promedio entre eventos; test t.
Salida: outputs/tables/event_study_tpm.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

EST_INI, EST_FIN = -130, -11      # ventana de estimacion
EV_INI, EV_FIN = -5, 5            # ventana de evento
MERCADO = "ret_mercado"           # se construye desde dl_ech


def cargar():
    ret = pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)
    niv = pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)
    ret[MERCADO] = ret["dl_ech"]
    return ret, niv


def fechas_eventos(niv):
    tpm = niv["tpm"].dropna()
    cambio = tpm.diff()
    ev = cambio[cambio != 0].dropna()
    alzas = ev[ev > 0].index
    bajas = ev[ev < 0].index
    return alzas, bajas


def car_evento(ret, ticker, fecha):
    y = ret[f"ret_{ticker}"]; m = ret[MERCADO]
    idx = ret.index
    if fecha not in idx:
        # ubicar el dia habil mas cercano
        pos = idx.searchsorted(fecha)
        if pos >= len(idx):
            return None
        fecha = idx[pos]
    t0 = idx.get_loc(fecha)
    est = slice(t0 + EST_INI, t0 + EST_FIN)
    if t0 + EST_INI < 0 or t0 + EV_FIN >= len(idx):
        return None
    ye, me = y.iloc[est], m.iloc[est]
    d = pd.concat([ye, me], axis=1).dropna()
    if len(d) < 40:
        return None
    b, a = np.polyfit(d[MERCADO], d[f"ret_{ticker}"], 1)
    ev = slice(t0 + EV_INI, t0 + EV_FIN + 1)
    yev, mev = y.iloc[ev], m.iloc[ev]
    ar = yev - (a + b * mev)
    return ar.sum()  # CAR ventana completa


def caar(ret, ticker, fechas):
    cars = [car_evento(ret, ticker, f) for f in fechas]
    cars = [c for c in cars if c is not None and np.isfinite(c)]
    if len(cars) < 3:
        return dict(n=len(cars), CAAR=np.nan, t=np.nan, p=np.nan)
    arr = np.array(cars)
    t, p = stats.ttest_1samp(arr, 0)
    return dict(n=len(cars), CAAR=round(arr.mean(), 4), t=round(t, 2), p=round(p, 4))


def main():
    ret, niv = cargar()
    alzas, bajas = fechas_eventos(niv)
    print(f"Eventos TPM detectados: {len(alzas)} alzas, {len(bajas)} bajas")
    print(f"Ventana evento [{EV_INI},{EV_FIN}]; estimacion [{EST_INI},{EST_FIN}]; mercado=ECH\n")
    filas = []
    for t in C.ACTIVOS_NUCLEO + ["CAP.SN", "SQM-B.SN"]:
        for tipo, fechas in [("alza TPM", alzas), ("baja TPM", bajas)]:
            r = caar(ret, t, fechas)
            r.update(activo=t, evento=tipo)
            filas.append(r)
            sig = "*" if (r["p"] == r["p"] and r["p"] < 0.05) else " "
            print(f"  {t:11s} {tipo:9s}  n={r['n']:3d}  CAAR={r['CAAR']:+.3f}%  "
                  f"t={r['t']}  p={r['p']} {sig}")
    df = pd.DataFrame(filas)[["activo", "evento", "n", "CAAR", "t", "p"]]
    df.to_csv(C.TAB / "event_study_tpm.csv", index=False, encoding="utf-8-sig")
    print("\nCAAR = retorno anormal acumulado promedio en la ventana [-5,+5] alrededor")
    print("del cambio de TPM. * = significativo al 5%.")


if __name__ == "__main__":
    main()
