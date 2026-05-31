# Decisiones fundacionales de la tesis

> Resueltas con evidencia empírica (ver `src/verificar_universo.py` y
> `outputs/tables/universo_verificacion.csv`). Fecha: 2026-05-30.

## Decisión 1 — Universo de empresas

El planteamiento pedía "todas las empresas". Operacionalmente, el universo de
mineras de cobre listadas y vinculadas a Chile es **muy reducido** y se define en
tres anillos concéntricos:

| Anillo | Tickers | Justificación |
|---|---|---|
| **A. Núcleo cobre-Chile** | `ANTO.L` (Antofagasta plc, LSE, GBp), `PUCOBRE.SN` (Pucobre, Santiago, CLP) | Únicos *pure-plays* de cobre con operación chilena listados. Antofagasta cross-listed en Londres; Pucobre listado directo en la Bolsa de Santiago. |
| **B. Minería-materiales Chile (panel ampliado)** | + `CAP.SN` (hierro/acero), `SQM-B.SN` (litio/potasio) | Amplía N para datos de panel. NO son cobre puro → entran como control de "minería-materiales" y permiten contrastar la sensibilidad específica al cobre. |
| **C. Referencias internacionales** | `SCCO`, `FCX`, `BHP` (NYSE), `GLEN.L` (LSE) | Sólo comparación de validez externa. No son "empresas chilenas". |

**Excluido:** Codelco (estatal, no cotiza en renta variable; sólo deuda).

**Implicancia metodológica:**
- Series de tiempo univariada de impacto → factible en `ANTO.L` y `PUCOBRE.SN`.
- Panel → posible con anillos A+B (N=4), pero **N pequeño**: cuidado con potencia
  estadística y con GMM dinámico (Arellano-Bond/Blundell-Bond pierde validez con N bajo).
- Recomendación: **diseño mixto** → TS por activo (núcleo) + panel FE de baja
  dimensión como robustez sectorial, más comparación con referencias internacionales.

## Decisión 2 — Período y frecuencia

El planteamiento pedía "todos los períodos". Operacionalmente:

- **Frecuencia base: diaria** (máxima resolución común a precios y factores de
  mercado). Disponibilidad: 2000-01-03 → presente para casi todas las series.
- **Frecuencia mensual** derivada para integrar macro de baja frecuencia (IMACEC,
  IPC, TPM efectiva mensual) en modelos ARDL/VECM.
- **Período de estudio propuesto:** **2004-01 → 2026-05**, condicionado por el
  inicio de `CLP=X` (2003-12). Para TS univariada de Antofagasta puede extenderse a 2000.
- Submuestras para robustez en torno a quiebres candidatos: crisis 2008,
  superciclo del cobre, COVID-2020, shock inflacionario 2021-2023 (a confirmar con
  tests de Bai-Perron / Zivot-Andrews).

## Decisión 3 — Variable dependiente

El planteamiento indicaba "precios / retorno". Se modelan **ambas** porque
responden preguntas distintas y tienen propiedades estadísticas distintas:

1. **Log-retornos diarios** `r_t = ln(P_t) - ln(P_{t-1})` → variable principal.
   Típicamente I(0); base para regresión con HAC, GARCH, event study.
2. **Precio en niveles (log-precio)** → para relaciones de **largo plazo**
   (cointegración: VECM / ARDL). Típicamente I(1).

> Regla: el análisis de **retornos** mide impacto/transmisión de corto plazo y
> riesgo; el análisis de **niveles cointegrados** mide la relación de equilibrio
> de largo plazo cobre→valoración. Se reportan los dos.
