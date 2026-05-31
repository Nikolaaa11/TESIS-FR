"""
modelo_garch.py
---------------
Modelado de la VOLATILIDAD de los retornos (justificado por ARCH-LM significativo).
Compara GARCH(1,1), EGARCH(1,1) y GJR-GARCH(1,1) con distribucion t-Student.
Evalua persistencia y EFECTO APALANCAMIENTO (asimetria: caidas elevan mas la vol).

Salida: outputs/tables/garch_<activo>.csv, garch_resumen.csv
        outputs/figures/vol_condicional_<activo>.png
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from arch import arch_model

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C


def cargar():
    return pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)


def ajustar(serie, vol, dist="t", o=0):
    am = arch_model(serie, mean="Constant", vol=vol, p=1, o=o, q=1, dist=dist)
    return am.fit(disp="off")


def estimar_activo(ret, ticker):
    s = ret[f"ret_{ticker}"].dropna()
    modelos = {
        "GARCH(1,1)":   ajustar(s, "GARCH", o=0),
        "GJR-GARCH(1,1)": ajustar(s, "GARCH", o=1),   # GJR = GARCH con termino asimetrico
        "EGARCH(1,1)":  ajustar(s, "EGARCH", o=1),
    }
    filas = []
    for nombre, m in modelos.items():
        p = m.params
        alpha = p.get("alpha[1]", np.nan)
        beta = p.get("beta[1]", np.nan)
        gamma = p.get("gamma[1]", np.nan)  # asimetria (apalancamiento)
        persist = (alpha + beta) if nombre == "GARCH(1,1)" else np.nan
        filas.append(dict(activo=ticker, modelo=nombre, AIC=round(m.aic, 1),
                          BIC=round(m.bic, 1), loglik=round(m.loglikelihood, 1),
                          alpha=round(alpha, 4) if alpha==alpha else np.nan,
                          beta=round(beta, 4) if beta==beta else np.nan,
                          gamma_asimetria=round(gamma, 4) if gamma==gamma else np.nan,
                          persistencia=round(persist, 4) if persist==persist else np.nan))
    df = pd.DataFrame(filas)
    df.to_csv(C.TAB / f"garch_{ticker.replace('.','_')}.csv", index=False, encoding="utf-8-sig")

    # figura: vol condicional del mejor modelo por AIC
    mejor = df.loc[df["AIC"].idxmin(), "modelo"]
    m = modelos[mejor]
    plt.figure(figsize=(12, 4))
    plt.plot(s.index, m.conditional_volatility, color="firebrick", lw=0.8)
    plt.title(f"Volatilidad condicional ({mejor}) — {C.ACTIVOS[ticker]['nombre']} ({ticker})")
    plt.ylabel("vol diaria (%)")
    plt.tight_layout()
    plt.savefig(C.FIG / f"vol_condicional_{ticker.replace('.','_')}.png", dpi=120)
    plt.close()
    return df, mejor


def main():
    ret = cargar()
    todos = []
    for t in C.ACTIVOS_NUCLEO + ["CAP.SN", "SQM-B.SN"]:
        df, mejor = estimar_activo(ret, t)
        todos.append(df)
        print(f"\n=== {t} — mejor por AIC: {mejor} ===")
        print(df.to_string(index=False))
    res = pd.concat(todos, ignore_index=True)
    res.to_csv(C.TAB / "garch_resumen.csv", index=False, encoding="utf-8-sig")
    print("\nNota: gamma>0 en GJR (y gamma<0 en EGARCH) => efecto apalancamiento:")
    print("las caídas aumentan más la volatilidad futura que las alzas equivalentes.")
    print("persistencia (alpha+beta) cercana a 1 => shocks de volatilidad muy persistentes.")


if __name__ == "__main__":
    main()
