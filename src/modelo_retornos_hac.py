"""
modelo_retornos_hac.py
----------------------
Modelo de IMPACTO CONTEMPORANEO de corto plazo sobre los retornos.

  ret_activo_t = a + b1 dl_cobre_t + b2 dl_usdclp_t + b3 dl_dxy_t
                 + b4 dl_sp500_t + b5 dl_ipsa_t + b6 d_ust10y_t
                 + b7 d_vix_t + e_t

Estimacion OLS con errores estandar HAC (Newey-West). Bateria de diagnosticos:
  - Breusch-Godfrey (autocorrelacion)
  - Breusch-Pagan / White (heterocedasticidad)
  - ARCH-LM (efectos ARCH)
  - VIF (multicolinealidad)
  - Jarque-Bera (normalidad residuos)
  - Ljung-Box (autocorrelacion residual)

Salidas: outputs/tables/hac_coeficientes.csv, hac_diagnosticos.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import (acorr_breusch_godfrey, het_breuschpagan,
                                          het_white, het_arch, acorr_ljungbox)
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import jarque_bera

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

# dl_ech = ETF MSCI Chile (proxy mercado local). Se prefiere a dl_ipsa porque
# la serie ^IPSA de Yahoo es inconsistente/incompleta post-2019 (ver docs).
REGRESORES = ["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500",
              "dl_ech", "d_ust10y", "d_vix", "d_tpm"]


def cargar():
    ret = pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)
    niv = pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)
    # construir d_vix a partir del nivel vix en factores crudos
    fa = pd.read_csv(C.RAW / "factores_yahoo.csv", index_col=0, parse_dates=True)
    ret["d_vix"] = fa["vix"].reindex(ret.index).diff()
    return ret


def estimar_activo(ret, ticker):
    y = ret[f"ret_{ticker}"]
    X = ret[REGRESORES]
    df = pd.concat([y, X], axis=1).dropna()
    yy = df[f"ret_{ticker}"]
    XX = sm.add_constant(df[REGRESORES])
    # HAC Newey-West, lags ~ 4*(n/100)^(2/9)
    L = int(4 * (len(df) / 100) ** (2 / 9))
    m = sm.OLS(yy, XX).fit(cov_type="HAC", cov_kwds={"maxlags": L})

    coef = pd.DataFrame({
        "activo": ticker,
        "var": m.params.index,
        "coef": m.params.values,
        "se_HAC": m.bse.values,
        "t": m.tvalues.values,
        "p": m.pvalues.values,
    })

    # Diagnosticos
    resid = m.resid
    bg = acorr_breusch_godfrey(m, nlags=5)
    bp = het_breuschpagan(resid, XX)
    arch = het_arch(resid, nlags=5)
    jb = jarque_bera(resid)
    lb = acorr_ljungbox(resid, lags=[10], return_df=True)
    # VIF
    vifs = {XX.columns[i]: variance_inflation_factor(XX.values, i)
            for i in range(1, XX.shape[1])}
    diag = dict(
        activo=ticker, n=int(m.nobs), R2=round(m.rsquared, 4),
        R2_adj=round(m.rsquared_adj, 4), HAC_lags=L,
        BG_p=round(bg[1], 4), BP_p=round(bp[1], 4), ARCH_p=round(arch[1], 4),
        JB_p=round(jb[1], 4), LjungBox10_p=round(lb["lb_pvalue"].iloc[0], 4),
        VIF_max=round(max(vifs.values()), 2),
    )
    return coef, diag, m


def main():
    ret = cargar()
    activos = list(C.ACTIVOS.keys())
    coefs, diags = [], []
    for t in activos:
        c, d, m = estimar_activo(ret, t)
        coefs.append(c); diags.append(d)
    coef_df = pd.concat(coefs, ignore_index=True).round(4)
    diag_df = pd.DataFrame(diags)
    coef_df.to_csv(C.TAB / "hac_coeficientes.csv", index=False, encoding="utf-8-sig")
    diag_df.to_csv(C.TAB / "hac_diagnosticos.csv", index=False, encoding="utf-8-sig")

    # Mostrar betas del cobre y resumen para nucleo
    print("\n=== Beta-cobre (impacto contemporáneo de +1% en cobre sobre retorno) ===")
    bc = coef_df[coef_df["var"] == "dl_cobre_comex"][["activo", "coef", "t", "p"]]
    print(bc.to_string(index=False))

    print("\n=== Coeficientes completos — núcleo cobre (ANTO.L, PUCOBRE.SN) ===")
    for t in C.ACTIVOS_NUCLEO:
        print(f"\n--- {t} ---")
        print(coef_df[coef_df["activo"] == t][["var", "coef", "se_HAC", "t", "p"]].to_string(index=False))

    print("\n=== Diagnósticos (p<.05 indica problema salvo R2) ===")
    print(diag_df.to_string(index=False))
    print("\nNota: BG/LjungBox<.05 => autocorrelación; BP/ARCH<.05 => heterocedasticidad/ARCH")
    print("(por eso se usan errores HAC y se modela la varianza con GARCH).")


if __name__ == "__main__":
    main()
