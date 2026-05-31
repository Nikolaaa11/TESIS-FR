"""
preparacion.py
--------------
Limpieza y transformacion de datos crudos -> dataset analitico.

Pasos:
  1. Cargar precios de activos y factores.
  2. Alinear a dias habiles, unir por fecha.
  3. Recorte al periodo de estudio (STUDY_START).
  4. Construir log-precios, log-retornos (%), variaciones de factores.
  5. Manejo de missing (ffill acotado para niveles; retornos NO se rellenan).
  6. Guardar:
       data/processed/niveles.csv   (log-precios + niveles de factores)
       data/processed/retornos.csv  (retornos % + variaciones de factores)
       data/processed/panel_largo.csv (formato long para datos de panel)
"""
import os, sys
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(__file__))
import config as C


def _cargar():
    px = pd.read_csv(C.RAW / "precios_activos.csv", index_col=0, parse_dates=True)
    fa = pd.read_csv(C.RAW / "factores_yahoo.csv", index_col=0, parse_dates=True)
    # macro Chile (mindicador.cl) si existe
    mp = C.RAW / "macro_chile.csv"
    if mp.exists():
        mc = pd.read_csv(mp, index_col=0, parse_dates=True)
        mc = mc.rename(columns={"tpm": "tpm", "dolar": "usdclp_obs",
                                "imacec": "imacec", "ipc": "ipc"})
        fa = fa.join(mc[["tpm", "usdclp_obs"]], how="outer")
    df = px.join(fa, how="outer").sort_index()
    df = df[df.index >= pd.Timestamp(C.START)]
    return px, fa, df


def construir():
    px, fa, df = _cargar()

    activos = list(C.ACTIVOS.keys())
    factores = list(C.FACTORES_YF.values())
    tiene_tpm = "tpm" in df.columns
    extra = ["tpm"] if tiene_tpm else []

    # --- Niveles: ffill acotado (max 3 dias) solo para series de nivel/precio ---
    niveles = df.copy()
    niveles[activos + factores + extra] = niveles[activos + factores + extra].ffill(limit=5)

    # Log-precios de activos
    lprice = np.log(niveles[activos]).add_prefix("lprice_")

    # Factores: separar tasas (nivel) de precios/indices (log)
    tasas = ["ust10y", "ust5y", "ust13w"] + extra
    precios_factor = [f for f in factores if f not in tasas]
    lfact = np.log(niveles[precios_factor].where(niveles[precios_factor] > 0)).add_prefix("l_")
    niv_tasas = niveles[tasas]  # se dejan en nivel (%)

    niveles_out = pd.concat([lprice, lfact, niv_tasas], axis=1)
    niveles_out = niveles_out[niveles_out.index >= pd.Timestamp(C.STUDY_START)]
    niveles_out.index.name = "fecha"
    niveles_out.to_csv(C.PROCESSED / "niveles.csv", encoding="utf-8-sig")

    # --- Retornos (%) ---
    ret_act = (np.log(niveles[activos]).diff() * 100).add_prefix("ret_")
    dl_fact = (np.log(niveles[precios_factor].where(niveles[precios_factor] > 0)).diff() * 100).add_prefix("dl_")
    d_tasas = niveles[tasas].diff().add_prefix("d_")  # cambio en puntos %
    retornos = pd.concat([ret_act, dl_fact, d_tasas], axis=1)
    retornos = retornos[retornos.index >= pd.Timestamp(C.STUDY_START)]
    retornos.index.name = "fecha"
    retornos.to_csv(C.PROCESSED / "retornos.csv", encoding="utf-8-sig")

    # --- Panel largo (solo activos del panel A+B) ---
    largo = []
    for t in C.ACTIVOS_PANEL:
        sub = pd.DataFrame({
            "fecha": retornos.index,
            "empresa": C.ACTIVOS[t]["nombre"],
            "ticker": t,
            "anillo": C.ACTIVOS[t]["anillo"],
            "ret": retornos[f"ret_{t}"].values,
            "lprice": niveles_out[f"lprice_{t}"].reindex(retornos.index).values,
        })
        largo.append(sub)
    panel = pd.concat(largo, ignore_index=True)
    # añadir factores comunes
    fac_cols = ["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500", "dl_ipsa",
                "dl_wti", "d_ust10y", "vix_nivel"]
    retornos["vix_nivel"] = niveles[["vix"]].reindex(retornos.index)["vix"].values
    panel = panel.merge(
        retornos[["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500",
                  "dl_ipsa", "dl_wti", "d_ust10y", "vix_nivel"]],
        left_on="fecha", right_index=True, how="left")
    panel.to_csv(C.PROCESSED / "panel_largo.csv", index=False, encoding="utf-8-sig")

    print("Niveles :", niveles_out.shape, "->", (C.PROCESSED / 'niveles.csv').name)
    print("Retornos:", retornos.shape, "->", (C.PROCESSED / 'retornos.csv').name)
    print("Panel   :", panel.shape, "->", (C.PROCESSED / 'panel_largo.csv').name)
    return niveles_out, retornos, panel


if __name__ == "__main__":
    construir()
