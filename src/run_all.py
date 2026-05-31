"""
run_all.py
----------
Orquestador: ejecuta el pipeline completo de la tesis de principio a fin.
Uso:  python src/run_all.py
"""
import subprocess, sys, os

PASOS = [
    ("Verificación de universo", "verificar_universo.py"),
    ("Ingesta de datos (Yahoo/FRED/BCCh)", "ingesta.py"),
    ("Ingesta macro Chile (mindicador.cl)", "ingesta_macro_cl.py"),
    ("Preparación / transformación", "preparacion.py"),
    ("EDA y tests previos",       "eda_tests.py"),
    ("Cointegración",             "cointegracion.py"),
    ("Modelo HAC (corto plazo)",  "modelo_retornos_hac.py"),
    ("VAR / IRF / FEVD",          "modelo_var.py"),
    ("VECM (largo plazo)",        "modelo_vecm.py"),
    ("NARDL (asimetrías cobre)",  "modelo_nardl.py"),
    ("GARCH (volatilidad)",       "modelo_garch.py"),
    ("Panel (FE/RE/Hausman)",     "modelo_panel.py"),
    ("ARDL bounds (robustez)",    "modelo_ardl.py"),
    ("Estudio de eventos (TPM)",  "modelo_event_study.py"),
    ("Toda-Yamamoto (causalidad)", "modelo_toda_yamamoto.py"),
    ("Iliquidez de Amihud (prueba formal)", "modelo_iliquidez.py"),
    ("Modelo mensual (macro nacional)", "modelo_mensual.py"),
    ("Robustez (quiebres/submuestras)", "robustez.py"),
    ("Quiebres estructurales (Quandt-Andrews)", "quiebres.py"),
    ("Iliquidez: robustez multi-proxy", "iliquidez_robustez.py"),
    ("Validación fuera de muestra (Clark-West)", "out_of_sample.py"),
    ("Predictor / backtest (plataforma)", "predictor.py"),
    ("Exportar datos web (data.js)", "exportar_web_data.py"),
    ("Exportar tesis a Word",     "exportar_docx.py"),
    ("Exportar tesis a PDF",      "exportar_pdf.py"),
    ("Exportar PPT de defensa",   "exportar_ppt.py"),
]

AQUI = os.path.dirname(__file__)


def main():
    for nombre, script in PASOS:
        print(f"\n{'='*70}\n>>> {nombre}  ({script})\n{'='*70}")
        r = subprocess.run([sys.executable, os.path.join(AQUI, script)])
        if r.returncode != 0:
            print(f"[AVISO] {script} terminó con código {r.returncode} (continúa).")
    print("\n=== PIPELINE COMPLETO ===")
    print("Resultados en outputs/tables y outputs/figures; documento en docs/tesis.md")


if __name__ == "__main__":
    main()
