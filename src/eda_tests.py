"""
eda_tests.py
------------
Analisis exploratorio + tests previos sobre datos REALES.

Produce:
  outputs/tables/descriptivos_retornos.csv
  outputs/tables/correlaciones_retornos.csv
  outputs/tables/estacionariedad.csv      (ADF, PP, KPSS sobre niveles y retornos)
  outputs/figures/precios_normalizados.png
  outputs/figures/retornos_<activo>.png
  outputs/figures/acf_pacf_<activo>.png
  outputs/figures/vol_rolling.png
  outputs/figures/heatmap_correlaciones.png
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch.unitroot import ADF, KPSS, PhillipsPerron

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

sns.set_theme(style="whitegrid", context="notebook")


def cargar():
    niv = pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)
    ret = pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)
    return niv, ret


# ---------------------------------------------------------------
def descriptivos(ret):
    cols = [f"ret_{t}" for t in C.ACTIVOS]
    filas = []
    for c in cols:
        s = ret[c].dropna()
        jb, jb_p = stats.jarque_bera(s)[:2]
        filas.append(dict(
            serie=c.replace("ret_", ""), n=len(s),
            media=s.mean(), sd=s.std(), min=s.min(), max=s.max(),
            asimetria=stats.skew(s), curtosis=stats.kurtosis(s, fisher=True),
            JarqueBera=jb, JB_pvalor=jb_p,
        ))
    df = pd.DataFrame(filas).round(4)
    df.to_csv(C.TAB / "descriptivos_retornos.csv", index=False, encoding="utf-8-sig")
    print("\n=== Descriptivos de log-retornos diarios (%) ===")
    print(df.to_string(index=False))
    return df


# ---------------------------------------------------------------
def correlaciones(ret):
    cols = [f"ret_{t}" for t in C.ACTIVOS] + \
           ["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500", "dl_ech", "dl_wti"]
    cols = [c for c in cols if c in ret.columns]
    corr = ret[cols].corr()
    corr.to_csv(C.TAB / "correlaciones_retornos.csv", encoding="utf-8-sig")
    plt.figure(figsize=(11, 9))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                square=True, cbar_kws={"shrink": .8}, annot_kws={"size": 7})
    plt.title("Correlaciones de retornos diarios (activos y factores)")
    plt.tight_layout()
    plt.savefig(C.FIG / "heatmap_correlaciones.png", dpi=130)
    plt.close()
    print("\n=== Correlación retorno activo vs retorno cobre (HG=F) ===")
    print(corr["dl_cobre_comex"].loc[[f"ret_{t}" for t in C.ACTIVOS]].round(3).to_string())
    return corr


# ---------------------------------------------------------------
def _tres_tests(serie):
    s = serie.dropna()
    out = {}
    try:
        a = ADF(s, trend="c"); out["ADF_stat"] = a.stat; out["ADF_p"] = a.pvalue
    except Exception as e:
        out["ADF_stat"] = np.nan; out["ADF_p"] = np.nan
    try:
        pp = PhillipsPerron(s, trend="c"); out["PP_stat"] = pp.stat; out["PP_p"] = pp.pvalue
    except Exception:
        out["PP_stat"] = np.nan; out["PP_p"] = np.nan
    try:
        k = KPSS(s, trend="c"); out["KPSS_stat"] = k.stat; out["KPSS_p"] = k.pvalue
    except Exception:
        out["KPSS_stat"] = np.nan; out["KPSS_p"] = np.nan
    return out


def estacionariedad(niv, ret):
    filas = []
    # niveles (log-precio) -> esperado I(1)
    for t in C.ACTIVOS:
        col = f"lprice_{t}"
        if col in niv.columns:
            r = _tres_tests(niv[col]); r.update(serie=col, tipo="nivel"); filas.append(r)
    for f in ["l_cobre_comex", "l_usdclp", "l_dxy", "l_sp500", "l_ipsa", "l_wti"]:
        if f in niv.columns:
            r = _tres_tests(niv[f]); r.update(serie=f, tipo="nivel"); filas.append(r)
    for f in ["ust10y", "ust5y", "ust13w"]:
        if f in niv.columns:
            r = _tres_tests(niv[f]); r.update(serie=f, tipo="nivel"); filas.append(r)
    # retornos / diferencias -> esperado I(0)
    for t in C.ACTIVOS:
        col = f"ret_{t}"
        if col in ret.columns:
            r = _tres_tests(ret[col]); r.update(serie=col, tipo="retorno"); filas.append(r)
    for f in ["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500", "dl_ipsa", "dl_wti",
              "d_ust10y"]:
        if f in ret.columns:
            r = _tres_tests(ret[f]); r.update(serie=f, tipo="diferencia"); filas.append(r)

    df = pd.DataFrame(filas)[["serie", "tipo", "ADF_stat", "ADF_p",
                              "PP_stat", "PP_p", "KPSS_stat", "KPSS_p"]].round(4)

    # Conclusion cruzada: ADF/PP rechazan raiz unitaria (p<.05) y KPSS NO rechaza estacionariedad (p>.05) -> I(0)
    def concluir(row):
        adf_i0 = row["ADF_p"] < 0.05
        pp_i0 = row["PP_p"] < 0.05
        kpss_i0 = row["KPSS_p"] > 0.05
        votos = sum([adf_i0, pp_i0, kpss_i0])
        return "I(0)" if votos >= 2 else "I(1)"
    df["conclusion"] = df.apply(concluir, axis=1)
    df.to_csv(C.TAB / "estacionariedad.csv", index=False, encoding="utf-8-sig")
    print("\n=== Tests de estacionariedad (ADF/PP/KPSS) — conclusión cruzada ===")
    print(df.to_string(index=False))
    return df


# ---------------------------------------------------------------
def graficos(niv, ret):
    # Precios normalizados (base 100) activos nucleo + cobre
    base = np.exp(niv[[f"lprice_{t}" for t in C.ACTIVOS_NUCLEO]])
    base = base.join(np.exp(niv[["l_cobre_comex"]]).rename(columns={"l_cobre_comex": "Cobre HG=F"}))
    base = base.dropna()
    norm = base / base.iloc[0] * 100
    plt.figure(figsize=(12, 6))
    for c in norm.columns:
        plt.plot(norm.index, norm[c], label=c, lw=1.2)
    plt.title("Precios normalizados (base 100) — núcleo cobre vs precio del cobre")
    plt.ylabel("Índice base 100"); plt.legend()
    plt.tight_layout(); plt.savefig(C.FIG / "precios_normalizados.png", dpi=130); plt.close()

    # Retornos + ACF/PACF de los activos nucleo
    for t in C.ACTIVOS_NUCLEO:
        s = ret[f"ret_{t}"].dropna()
        fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=False)
        ax[0].plot(s.index, s, lw=0.5, color="steelblue")
        ax[0].set_title(f"Log-retorno diario (%) — {C.ACTIVOS[t]['nombre']} ({t})")
        ax[1].plot(s.index, (s.rolling(21).std()), color="firebrick", lw=1)
        ax[1].set_title("Volatilidad realizada (sd móvil 21d)")
        plt.tight_layout(); plt.savefig(C.FIG / f"retornos_{t.replace('.','_')}.png", dpi=120); plt.close()

        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        plot_acf(s, lags=30, ax=ax[0], title=f"ACF retornos {t}")
        plot_acf(s**2, lags=30, ax=ax[1], title=f"ACF retornos^2 {t} (efecto ARCH)")
        plt.tight_layout(); plt.savefig(C.FIG / f"acf_{t.replace('.','_')}.png", dpi=120); plt.close()
    print("\nFiguras guardadas en outputs/figures/")


def main():
    niv, ret = cargar()
    descriptivos(ret)
    correlaciones(ret)
    estacionariedad(niv, ret)
    graficos(niv, ret)
    print("\n=== EDA COMPLETO ===")


if __name__ == "__main__":
    main()
