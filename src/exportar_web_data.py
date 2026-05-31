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
