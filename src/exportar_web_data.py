"""
exportar_web_data.py
--------------------
Extrae los resultados reales de outputs/tables/*.csv a web/data.json para alimentar
los graficos de la plataforma web. Tambien copia las figuras a web/assets/figures.
"""
import os, sys, json, shutil, glob
import pandas as pd

sys.path.append(os.path.dirname(__file__))
import config as C

WEB = C.ROOT / "web"
FIGW = WEB / "assets" / "figures"
FIGW.mkdir(parents=True, exist_ok=True)


def t(nombre):
    return pd.read_csv(C.TAB / nombre)


def main():
    data = {}

    # Beta-cobre contemporanea por activo (HAC)
    hac = t("hac_coeficientes.csv")
    bc = hac[hac["var"] == "dl_cobre_comex"][["activo", "coef", "t", "p"]]
    diag = t("hac_diagnosticos.csv")[["activo", "R2"]]
    bc = bc.merge(diag, on="activo")
    data["beta_cobre"] = bc.to_dict("records")

    # Transmision por horizonte (Pucobre) - el hallazgo central
    ilt = t("iliquidez_test.csv")
    data["horizonte"] = {
        "labels": ["Diario (día 0)", "Acumulado 0–5d", "Mensual", "Largo plazo (VECM)"],
        "pucobre": [0.085, 0.415, 0.599, 0.753],
        "anto": [0.701, 0.862, 0.712, 0.860],
    }

    # FEVD (cobre explica % varianza) y Granger
    var = t("var_resumen.csv")
    data["var"] = var.to_dict("records")

    # VECM largo plazo
    data["vecm"] = t("vecm_resumen.csv").to_dict("records")

    # GARCH (persistencia / apalancamiento) - tomar GARCH(1,1) y GJR
    g = t("garch_resumen.csv")
    data["garch"] = g.to_dict("records")

    # Estacionariedad (conteo I0/I1)
    est = t("estacionariedad.csv")
    data["estacionariedad"] = est[["serie", "tipo", "ADF_p", "KPSS_p", "conclusion"]].to_dict("records")

    # Iliquidez (Amihud, % dias cero)
    data["iliquidez"] = t("iliquidez_amihud.csv").to_dict("records")

    # Descriptivos
    data["descriptivos"] = t("descriptivos_retornos.csv").to_dict("records")

    # NARDL asimetria
    data["nardl"] = t("nardl_resumen.csv").to_dict("records")

    # Event study TPM
    data["event_study"] = t("event_study_tpm.csv").to_dict("records")

    # Toda-Yamamoto
    data["toda_yamamoto"] = t("toda_yamamoto.csv").to_dict("records")

    # Mensual
    data["mensual"] = t("mensual_resumen.csv").to_dict("records")

    # Panel
    pan = pd.read_csv(C.TAB / "panel_resultados.csv")
    data["panel"] = pan.rename(columns={pan.columns[0]: "var"}).to_dict("records")

    # rezagos distribuidos
    data["rezagos"] = ilt.to_dict("records")

    # Universo
    data["universo"] = t("universo_verificacion.csv")[["ticker", "desc", "ok", "n", "inicio", "fin", "moneda"]].to_dict("records")

    # --- Series temporales: precios normalizados base 100 (mensual) ---
    import numpy as np
    niv = pd.read_csv(C.PROCESSED / "niveles.csv", index_col=0, parse_dates=True)
    base = np.exp(niv[["lprice_ANTO.L", "lprice_PUCOBRE.SN", "l_cobre_comex"]]).dropna()
    bm = base.resample("ME").last().dropna()
    bm = bm / bm.iloc[0] * 100
    data["series"] = {
        "fechas": [d.strftime("%Y-%m") for d in bm.index],
        "anto": [round(x, 1) for x in bm["lprice_ANTO.L"]],
        "pucobre": [round(x, 1) for x in bm["lprice_PUCOBRE.SN"]],
        "cobre": [round(x, 1) for x in bm["l_cobre_comex"]],
    }

    # --- Matriz de correlaciones ---
    corr = pd.read_csv(C.TAB / "correlaciones_retornos.csv", index_col=0)
    etq = [c.replace("ret_", "").replace("dl_", "Δ").replace("_comex", "")
           for c in corr.columns]
    data["correlacion"] = {"labels": etq,
                           "matriz": [[round(v, 2) for v in fila] for fila in corr.values]}

    # --- IRF (respuesta del activo a shock de cobre, 20 días) via VAR ---
    try:
        from statsmodels.tsa.api import VAR
        ret = pd.read_csv(C.PROCESSED / "retornos.csv", index_col=0, parse_dates=True)
        facs = ["dl_cobre_comex", "dl_usdclp", "dl_dxy", "dl_sp500"]
        irf_out = {}
        for tk in ["ANTO.L", "PUCOBRE.SN"]:
            orden = facs + [f"ret_{tk}"]
            df = ret[orden].dropna()
            res = VAR(df).fit(6)
            irf = res.irf(20)
            ia, ic = orden.index(f"ret_{tk}"), orden.index("dl_cobre_comex")
            vals = irf.irfs[:, ia, ic]
            irf_out[tk] = [round(float(v), 4) for v in vals]
        data["irf"] = {"dias": list(range(21)), "anto": irf_out["ANTO.L"],
                       "pucobre": irf_out["PUCOBRE.SN"]}
    except Exception as e:
        print("IRF export fallo:", e)

    import math

    def clean(o):
        if isinstance(o, float):
            return None if math.isnan(o) else o
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, list):
            return [clean(x) for x in o]
        return o

    data = clean(data)
    js = json.dumps(data, ensure_ascii=False, indent=2)
    (WEB / "data.json").write_text(js, encoding="utf-8")
    # data.js: inyecta los datos en window (evita fetch/CORS en file:// y Vercel)
    (WEB / "data.js").write_text("window.TESIS_DATA = " + js + ";", encoding="utf-8")
    print(f"data.json/data.js: {len(js)/1024:.1f} KB, {len(data)} bloques")

    # copiar figuras
    n = 0
    for f in glob.glob(str(C.FIG / "*.png")):
        shutil.copy(f, FIGW / os.path.basename(f)); n += 1
    print(f"Figuras copiadas: {n}")


if __name__ == "__main__":
    main()
