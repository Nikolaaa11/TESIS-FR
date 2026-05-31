"""
iliquidez_robustez.py
---------------------
Robustez del hallazgo central: ¿la relacion negativa iliquidez <-> transmision
contemporanea del cobre se sostiene bajo MEDIDAS ALTERNATIVAS de iliquidez?

Medidas por activo:
  1. Amihud (2002):    |r| / volumen$  (impacto de precio por $)
  2. % dias retorno cero (Lesmond et al.): proxy de thin trading
  3. Spread implicito de Roll (1984): 2*sqrt(-cov(Δp_t, Δp_{t-1})) si cov<0
  4. (Inverso de) volumen medio en USD-equivalente: menos volumen = mas iliquido

Test transversal (8 activos): correlacion de Spearman de cada medida con la
beta-cobre contemporanea (HAC). H esperada: signo NEGATIVO (mas iliquido => menor
transmision contemporanea).

Salida: outputs/tables/iliquidez_robustez.csv, iliquidez_robustez_corr.csv
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


def cargar():
    px = pd.read_csv(C.RAW / "precios_activos.csv", index_col=0, parse_dates=True)
    vol = pd.read_csv(C.RAW / "volumen_activos.csv", index_col=0, parse_dates=True)
    betas = pd.read_csv(C.TAB / "hac_coeficientes.csv")
    bc = betas[betas["var"] == "dl_cobre_comex"].set_index("activo")["coef"]
    return px, vol, bc


def roll_spread(ret):
    """Spread implicito de Roll: 2*sqrt(-cov(Δp_t,Δp_{t-1})). Usa retornos como Δp."""
    r = ret.dropna()
    if len(r) < 50:
        return np.nan
    cov = np.cov(r.values[1:], r.values[:-1])[0, 1]
    return 2 * np.sqrt(-cov) if cov < 0 else 0.0


def main():
    px, vol, bc = cargar()
    ret = np.log(px).diff()
    dollar_vol = vol * px
    filas = []
    for t in C.ACTIVOS:
        r = ret[t]
        amih = ((r.abs() / dollar_vol[t].replace(0, np.nan)) * 1e6).replace([np.inf, -np.inf], np.nan).mean()
        pct_cero = (r.abs() < 1e-9).mean() * 100
        roll = roll_spread(r) * 100  # en %
        volm = dollar_vol[t].mean()
        filas.append(dict(activo=t, amihud=round(amih, 4), pct_ceros=round(pct_cero, 2),
                          roll_spread_pct=round(roll, 3), vol_medio_usd=round(volm, 0),
                          beta_cobre=round(float(bc.get(t, np.nan)), 4)))
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "iliquidez_robustez.csv", index=False, encoding="utf-8-sig")
    print("=== Medidas de iliquidez por activo ===")
    print(df.to_string(index=False))

    # correlaciones transversales con beta-cobre
    corr = []
    for medida, signo_esp in [("amihud", "-"), ("pct_ceros", "-"),
                              ("roll_spread_pct", "-"), ("vol_medio_usd", "+")]:
        d = df[[medida, "beta_cobre"]].dropna()
        x = np.log(d[medida].replace(0, np.nan)) if medida in ("amihud", "roll_spread_pct", "vol_medio_usd") else d[medida]
        dd = pd.concat([x, d["beta_cobre"]], axis=1).dropna()
        rho, p = stats.spearmanr(dd.iloc[:, 0], dd.iloc[:, 1])
        corr.append(dict(medida=medida, signo_esperado=signo_esp,
                         spearman_rho=round(rho, 3), p_valor=round(p, 4), n=len(dd)))
    cdf = pd.DataFrame(corr)
    cdf.to_csv(C.TAB / "iliquidez_robustez_corr.csv", index=False, encoding="utf-8-sig")
    print("\n=== Correlación transversal medida-iliquidez vs beta-cobre (8 activos) ===")
    print(cdf.to_string(index=False))
    print("\nVol medio (+): más volumen => más líquido => mayor beta (signo positivo esperado).")
    print("Amihud, %ceros, Roll (-): más iliquidez => menor beta contemporánea.")
    print("La consistencia de signos entre medidas robustece el hallazgo central.")


if __name__ == "__main__":
    main()
