"""
verificar_universo.py
----------------------
Verificacion EMPIRICA del universo de empresas para la tesis.

Objetivo: NO asumir que un ticker existe. Probar la descarga real desde Yahoo
Finance y reportar, para cada candidato, si hay datos, su rango de fechas,
numero de observaciones, moneda y un descriptivo minimo.

Candidatos (sector cobre / mineria-materiales con relacion a Chile):
  - ANTO.L      Antofagasta plc (LSE) -- pure-play cobre, grupo Luksic (cross-listed)
  - PUCV.SN     Sociedad Punta del Cobre S.A. (Pucobre) -- cobre, Bolsa de Santiago
  - CAP.SN      CAP S.A. -- hierro/acero/mineria, Bolsa de Santiago
  - SQM-B.SN    SQM -- litio/potasio (NO cobre; control/comparacion)
  - LTM.SN / otros materiales como referencia
  - Referencias internacionales (solo comparacion teorica):
      SCCO      Southern Copper (NYSE)
      FCX       Freeport-McMoRan (NYSE)
      GLEN.L    Glencore (LSE)
  - Indices / proxies:
      ^IPSA     IPSA (Bolsa de Santiago)
      HG=F      Futuro cobre COMEX
      CLP=X     USD/CLP

Salida: outputs/tables/universo_verificacion.csv y print a consola.
"""
import sys
import pandas as pd
import yfinance as yf

CANDIDATOS = {
    # Chilenas / cross-listed cobre
    "ANTO.L":   "Antofagasta plc (LSE) - cobre pure-play",
    "PUCV.SN":  "Pucobre / Punta del Cobre (Santiago) - cobre",
    "PUCOBRE.SN": "Pucobre alt ticker",
    "CAP.SN":   "CAP S.A. (Santiago) - hierro/acero/mineria",
    "SQM-B.SN": "SQM serie B (Santiago) - litio/potasio",
    "SQM-A.SN": "SQM serie A (Santiago)",
    # Referencias internacionales del cobre
    "SCCO":     "Southern Copper (NYSE) - cobre",
    "FCX":      "Freeport-McMoRan (NYSE) - cobre",
    "GLEN.L":   "Glencore (LSE) - diversificada/cobre",
    "BHP":      "BHP (NYSE) - diversificada/cobre",
    # Indices y factores
    "^IPSA":    "Indice IPSA (Bolsa de Santiago)",
    "HG=F":     "Futuro cobre COMEX",
    "CLP=X":    "USD/CLP",
    "DX-Y.NYB": "Indice dolar DXY",
    "^VIX":     "VIX",
}


def verificar(ticker, desc, start="2000-01-01"):
    try:
        df = yf.download(ticker, start=start, progress=False, auto_adjust=True)
        if df is None or len(df) == 0:
            return dict(ticker=ticker, desc=desc, ok=False, n=0,
                        inicio="", fin="", moneda="", nota="sin datos")
        # metadata moneda
        moneda = ""
        try:
            info = yf.Ticker(ticker).fast_info
            moneda = info.get("currency", "") or ""
        except Exception:
            pass
        idx = df.index
        return dict(ticker=ticker, desc=desc, ok=True, n=len(df),
                    inicio=str(idx.min().date()), fin=str(idx.max().date()),
                    moneda=moneda, nota="")
    except Exception as e:
        return dict(ticker=ticker, desc=desc, ok=False, n=0,
                    inicio="", fin="", moneda="", nota=f"ERROR: {e}")


def main():
    filas = []
    for t, d in CANDIDATOS.items():
        r = verificar(t, d)
        filas.append(r)
        estado = "OK " if r["ok"] else "-- "
        print(f"{estado} {t:12s} n={r['n']:6d}  {r['inicio']}..{r['fin']}  "
              f"[{r['moneda']:4s}]  {d}")
    res = pd.DataFrame(filas)
    out = "outputs/tables/universo_verificacion.csv"
    res.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"\nGuardado: {out}")
    print(f"Descargables: {res['ok'].sum()}/{len(res)}")


if __name__ == "__main__":
    main()
