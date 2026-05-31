"""
modelo_panel.py
---------------
Datos de panel (anillos A+B: ANTO, PUCOBRE, CAP, SQM) para el impacto PROMEDIO
del sector minero-materiales chileno.

  - Pooled OLS
  - Efectos fijos (entity FE)
  - Efectos aleatorios (RE)
  - Test de Hausman (FE vs RE)
Errores agrupados por empresa (cluster). N pequeño (4) => se reporta con cautela.

Salida: outputs/tables/panel_resultados.csv
"""
import os, sys, warnings
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS, RandomEffects, PooledOLS

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(__file__))
import config as C

REGRESORES = ["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500", "dl_ipsa", "d_ust10y"]


def cargar():
    p = pd.read_csv(C.PROCESSED / "panel_largo.csv", parse_dates=["fecha"])
    p = p.dropna(subset=["ret"] + REGRESORES)
    p = p.set_index(["ticker", "fecha"])
    return p


def hausman(fe, re):
    b = fe.params; B = re.params
    common = [c for c in b.index if c in B.index]
    b, B = b[common], B[common]
    vb = fe.cov.loc[common, common]; vB = re.cov.loc[common, common]
    diff = b - B
    dvar = vb - vB
    try:
        stat = float(diff.values @ np.linalg.pinv(dvar.values) @ diff.values)
    except Exception:
        stat = np.nan
    from scipy import stats as st
    dof = len(common)
    p = 1 - st.chi2.cdf(stat, dof) if stat == stat else np.nan
    return stat, dof, p


def main():
    p = cargar()
    y = p["ret"]; X = p[REGRESORES]

    pooled = PooledOLS(y, X).fit(cov_type="clustered", cluster_entity=True)
    fe = PanelOLS(y, X, entity_effects=True).fit(cov_type="clustered", cluster_entity=True)
    re = RandomEffects(y, X).fit(cov_type="clustered", cluster_entity=True)

    h_stat, h_dof, h_p = hausman(fe, re)

    # tabla comparativa de coeficientes
    tab = pd.DataFrame({
        "Pooled": pooled.params, "Pooled_p": pooled.pvalues,
        "FE": fe.params, "FE_p": fe.pvalues,
        "RE": re.params, "RE_p": re.pvalues,
    }).round(4)
    tab.to_csv(C.TAB / "panel_resultados.csv", encoding="utf-8-sig")

    print("=== PANEL (N=4 empresas chilenas minería-materiales) ===")
    print(f"Observaciones: {fe.nobs}  | Entidades: {p.index.get_level_values(0).nunique()}")
    print("\nCoeficientes (impacto promedio del sector sobre el retorno diario):")
    print(tab.to_string())
    print(f"\nFE R2(within): {fe.rsquared_within:.4f}")
    print(f"Test de Hausman: chi2={h_stat:.2f} (dof={h_dof}) p={h_p:.4f}")
    print("  -> p<.05 favorece EFECTOS FIJOS; p>=.05 no rechaza RE.")
    print("\nADVERTENCIA: N=4 es muy pequeño; el panel se usa como robustez sectorial,")
    print("no como inferencia primaria. GMM dinámico (Arellano-Bond) NO es viable con este N.")


if __name__ == "__main__":
    main()
