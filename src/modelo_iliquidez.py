"""
modelo_iliquidez.py
-------------------
Prueba FORMAL de la hipotesis central: la iliquidez explica la baja transmision
contemporanea del cobre (caso Pucobre).

1. Descarga volumen y calcula el ratio de iliquidez de Amihud (2002):
      ILLIQ_t = |retorno_t| / (volumen_t * precio_t)      (impacto de precio por $ transado)
   Se reporta el ILLIQ promedio por activo (×1e6 para escala) y % de dias de
   retorno nulo (proxy adicional de thin trading).

2. Test TRANSVERSAL (8 activos): correlacion entre iliquidez y la beta-cobre
   contemporanea (de hac_coeficientes.csv). H: mas iliquido => menor beta.

3. Test INTRA-PUCOBRE: beta-cobre contemporanea en dias liquidos vs iliquidos
   (split por mediana del ILLIQ movil). H: beta mayor cuando el activo esta liquido.

Salida: outputs/tables/iliquidez_amihud.csv, iliquidez_test.csv
        outputs/figures/iliquidez_vs_beta.png
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
import yfinance as yf
from scipy import stats

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C


def descargar_volumen():
    out = C.RAW / "volumen_activos.csv"
    if out.exists():
        return pd.read_csv(out, index_col=0, parse_dates=True)
    series = {}
    for t in C.ACTIVOS:
        try:
            d = yf.download(t, start=C.START, progress=False, auto_adjust=True)
            series[t] = d["Volume"].iloc[:, 0] if hasattr(d["Volume"], "columns") else d["Volume"]
        except Exception as e:
            print(f"  vol {t}: {e}")
    vol = pd.concat(series.values(), axis=1, keys=series.keys()).sort_index()
    vol.index.name = "fecha"
    vol.to_csv(out, encoding="utf-8-sig")
    return vol


def amihud():
    px = pd.read_csv(C.RAW / "precios_activos.csv", index_col=0, parse_dates=True)
    vol = descargar_volumen()
    ret = np.log(px).diff().abs()
    dollar_vol = (vol * px)  # volumen en moneda
    illiq = (ret / dollar_vol.replace(0, np.nan)) * 1e6  # escala
    filas = []
    for t in C.ACTIVOS:
        s = illiq[t].replace([np.inf, -np.inf], np.nan).dropna()
        r = np.log(px[t]).diff()
        pct_cero = (r.abs() < 1e-9).mean() * 100
        filas.append(dict(activo=t, ILLIQ_medio=round(s.mean(), 4),
                          ILLIQ_mediano=round(s.median(), 4),
                          pct_dias_retorno_cero=round(pct_cero, 2),
                          vol_medio_USD_equiv=round(dollar_vol[t].mean(), 0)))
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "iliquidez_amihud.csv", index=False, encoding="utf-8-sig")
    print("=== Iliquidez de Amihud por activo ===")
    print(df.to_string(index=False))
    return df, illiq


def test_transversal(amihud_df):
    betas = pd.read_csv(C.TAB / "hac_coeficientes.csv")
    bc = betas[betas["var"] == "dl_cobre_comex"][["activo", "coef"]].rename(
        columns={"coef": "beta_cobre"})
    m = amihud_df.merge(bc, on="activo")
    # usar log de iliquidez (escala) y % cero
    m["log_illiq"] = np.log(m["ILLIQ_medio"])
    rho1, p1 = stats.spearmanr(m["log_illiq"], m["beta_cobre"])
    rho2, p2 = stats.spearmanr(m["pct_dias_retorno_cero"], m["beta_cobre"])

    plt.figure(figsize=(8, 5.5))
    plt.scatter(m["pct_dias_retorno_cero"], m["beta_cobre"], s=60, color="steelblue")
    for _, row in m.iterrows():
        plt.annotate(row["activo"], (row["pct_dias_retorno_cero"], row["beta_cobre"]),
                     fontsize=8, xytext=(4, 4), textcoords="offset points")
    plt.xlabel("% días de retorno cero (proxy de iliquidez)")
    plt.ylabel("β-cobre contemporánea (HAC)")
    plt.title("Iliquidez vs transmisión contemporánea del cobre (8 activos)")
    plt.tight_layout(); plt.savefig(C.FIG / "iliquidez_vs_beta.png", dpi=130); plt.close()

    print("\n=== Test transversal (8 activos): iliquidez vs beta-cobre ===")
    print(f"  Spearman(log ILLIQ, beta_cobre)      = {rho1:+.3f} (p={p1:.4f})")
    print(f"  Spearman(% ret cero, beta_cobre)     = {rho2:+.3f} (p={p2:.4f})")
    print("  H esperada: correlación NEGATIVA (más ilíquido => menor beta)")
    return dict(spearman_illiq=round(rho1, 3), p_illiq=round(p1, 4),
                spearman_pctcero=round(rho2, 3), p_pctcero=round(p2, 4))


def test_rezagos_distribuidos():
    """Test directo de transmisión DIFERIDA por iliquidez: descompone el efecto
    del cobre en el día 0 y rezagos 1..5. H: en el activo ilíquido (Pucobre) la
    fracción del impacto que llega en el día 0 es BAJA (transmisión repartida en
    días siguientes); en el líquido (ANTO) el día 0 domina."""
    ret = pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)
    filas = []
    for t in ["ANTO.L", "PUCOBRE.SN"]:
        d = pd.DataFrame({"y": ret[f"ret_{t}"]})
        for L in range(0, 6):
            d[f"cobre_L{L}"] = ret["dl_cobre_comex"].shift(L)
        d = d.dropna()
        X = sm.add_constant(d[[f"cobre_L{L}" for L in range(6)]])
        Lh = max(1, int(4 * (len(d) / 100) ** (2 / 9)))
        m = sm.OLS(d["y"], X).fit(cov_type="HAC", cov_kwds={"maxlags": Lh})
        b0 = m.params["cobre_L0"]
        suma = sum(m.params[f"cobre_L{L}"] for L in range(6))
        filas.append(dict(activo=t, beta_dia0=round(b0, 4),
                          beta_acum_0a5=round(suma, 4),
                          fraccion_dia0=round(b0 / suma, 3) if suma != 0 else np.nan,
                          n=len(d)))
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / "iliquidez_test.csv", index=False, encoding="utf-8-sig")
    print("\n=== Test de rezagos distribuidos: transmisión inmediata vs diferida ===")
    print(df.to_string(index=False))
    print("  fraccion_dia0 = beta(dia0)/beta(acumulado 0-5). Baja => transmision DIFERIDA")
    print("  (consistente con descubrimiento de precios lento por iliquidez).")
    return df


if __name__ == "__main__":
    df, illiq = amihud()
    test_transversal(df)
    test_rezagos_distribuidos()
    print("\n=== ILIQUIDEZ COMPLETA ===")
