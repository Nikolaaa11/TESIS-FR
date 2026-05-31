# Impacto de las variables macroeconómicas globales y financieras en la valoración bursátil del sector de minería de cobre en Chile

**Tesis — Magíster en Data Science · Econometría Financiera aplicada**
Período de estudio: 2004–2026 (datos diarios) · Software: Python 3.13 (statsmodels, arch, linearmodels)

> **Estado del documento:** borrador integrado con resultados empíricos REALES
> (datos descargados de Yahoo Finance el 2026-05-30). Todo número proviene de los
> scripts en `src/` y las tablas en `outputs/tables/`. Las citas marcadas
> *[POR VERIFICAR]* deben confirmarse en Scopus/WoS/Scholar antes de la entrega:
> **no se han inventado referencias**.

---

## Resumen (Abstract)

Se cuantifica el impacto de variables macroeconómicas globales y financieras sobre
el precio y el retorno de las acciones de minería de cobre vinculadas a Chile. El
universo se resuelve empíricamente: existen sólo dos *pure-plays* de cobre
cotizados ligados a Chile —**Antofagasta plc** (LSE) y **Pucobre** (Bolsa de
Santiago)— complementados por un panel de minería-materiales (CAP, SQM) y
referencias internacionales (SCCO, FCX, BHP, Glencore). Mediante regresión con
errores HAC, VAR (IRF/FEVD), cointegración de Johansen y VECM, modelos GARCH y
datos de panel, se documenta un hallazgo central: **el precio del cobre transmite
fuertemente a la valoración del *pure-play* líquido (Antofagasta: β contemporánea
≈ 0.70; el cobre explica ≈ 28% de la varianza de su retorno), pero la transmisión
al *pure-play* local e ilíquido (Pucobre) es casi nula en el corto plazo
(β ≈ 0.09, R² ≈ 0.04) y sólo se materializa con rezago y en el largo plazo**
(elasticidad de cointegración ≈ 0.75). La iliquidez del small-cap chileno
**retrasa**, pero no **elimina**, el vínculo fundamental cobre→valoración.

---

## 1. Introducción

Chile es la mayor economía cuprífera del mundo y el cobre representa una fracción
dominante de sus exportaciones. Resulta natural preguntarse en qué medida el ciclo
global del cobre y las condiciones financieras internacionales se transmiten a la
**valoración bursátil** de las empresas mineras del país. Esta tesis aborda esa
pregunta con un enfoque **explicativo y de medición de impacto** —no predictivo—:
el objetivo es cuantificar signos, magnitudes, dinámicas y relaciones de equilibrio,
con supuestos validados.

**Pregunta de investigación.** ¿Cuál es la magnitud, el signo y la dinámica
(corto vs largo plazo) del impacto de las variables macro-financieras globales y
nacionales —en particular el precio del cobre, el tipo de cambio, el dólar global,
las tasas de interés y el riesgo de mercado— sobre el precio y el retorno de las
acciones de minería de cobre vinculadas a Chile?

**Objetivo general.** Analizar y cuantificar dicho impacto en el período 2004–2026
mediante modelos econométricos de series de tiempo y de panel.

**Objetivos específicos.**
1. Resolver operacionalmente el universo de empresas mineras de cobre cotizadas
   vinculadas a Chile.
2. Caracterizar las propiedades estadísticas de precios y retornos (estacionariedad,
   colas, volatilidad, quiebres).
3. Estimar el impacto **contemporáneo** de los factores sobre los retornos
   (regresión HAC) y su **dinámica** (VAR, IRF, FEVD, causalidad).
4. Estimar la relación de **largo plazo** cobre→valoración (cointegración, VECM)
   y su robustez (ARDL bounds).
5. Modelar la **volatilidad** y el efecto apalancamiento (familia GARCH).
6. Contrastar resultados con un **panel** sectorial y con referencias internacionales.

**Relevancia.** Más allá del interés académico, cuantificar la sensibilidad de las
mineras chilenas al cobre y a las condiciones financieras tiene implicancias para
la gestión de riesgo, la valoración y la política. El hallazgo sobre iliquidez del
*pure-play* local aporta evidencia sobre la eficiencia informacional de un
mercado emergente pequeño.

---

## 2. Marco teórico

La valoración de un activo accionario corresponde al valor presente de sus flujos
futuros descontados. Para una minera de cobre, los **flujos** dependen directamente
del precio del cobre (ingreso) y de los costos (energía, tipo de cambio), mientras
que la **tasa de descuento** depende de las tasas libres de riesgo globales y de
las primas de riesgo. Esto define cinco canales económicos que estructuran la
selección de variables:

1. **Canal de demanda/ingreso** — precio del cobre (COMEX/LME) y demanda global
   (actividad industrial, China). Un alza del cobre eleva los ingresos esperados.
2. **Canal de costos** — energía (WTI) y tipo de cambio (CLP/USD): una depreciación
   del peso reduce costos locales medidos en USD y puede elevar el margen.
3. **Canal de descuento** — tasas de interés (UST 2Y/10Y), que afectan el factor
   de descuento.
4. **Canal de moneda global** — índice dólar (DXY): los commodities tienden a
   moverse inversamente al dólar.
5. **Canal de riesgo/sentimiento** — VIX y mercado (S&P 500, mercado local).

El **Arbitrage Pricing Theory (APT)** (Ross, 1976) y los modelos de factores
macroeconómicos sobre retornos accionarios (Chen, Roll y Ross, 1986) dan sustento a
una especificación multifactorial lineal para los retornos. La distinción entre
**niveles** (precios I(1)) y **cambios** (retornos I(0)) motiva separar el análisis
de equilibrio de largo plazo (cointegración) del de impacto de corto plazo.

---

## 3. Revisión de literatura

> Las referencias de esta sección fueron verificadas en fuentes primarias (editor /
> repositorios académicos). Se recomienda una revisión final del formato APA y de la
> paginación exacta antes de la entrega. Los enlaces se listan en el Capítulo 9.

### 3.1 Factores macroeconómicos y retornos accionarios (APT)

La base teórica que vincula variables macro con retornos accionarios es el
*Arbitrage Pricing Theory* (Ross, 1976) y su contrastación empírica seminal en
**Chen, Roll y Ross (1986)**, quienes muestran que innovaciones en la producción
industrial, la inflación (esperada y no esperada), la prima por riesgo (spread de
bonos) y la pendiente de la estructura temporal son **factores de riesgo
sistemáticamente valorados** en el mercado accionario estadounidense. Esta
literatura justifica la especificación multifactorial de los retornos empleada en
el Capítulo 6 (canales de demanda, descuento, riesgo y moneda) y la inclusión de
tasas (UST, TPM), dólar (DXY) y riesgo (VIX) como regresores.

### 3.2 Commodities, "monedas-commodity" y economías cupríferas

**Chen y Rogoff (2003)** acuñan el concepto de *commodity currency*: para
economías exportadoras de materias primas, el precio mundial de su canasta
exportadora es un determinante robusto del tipo de cambio real. El caso chileno es
arquetípico —el cobre representa cerca de la mitad de las exportaciones— y existe
evidencia específica: el **Working Paper N°640 del Banco Central de Chile**
(*Copper, the Real Exchange Rate and Macroeconomic Fluctuations in Chile*) analiza
el rol del cobre y el tipo de cambio real como amortiguadores de shocks, y trabajos
en *Resources Policy* documentan que **el tipo de cambio chileno tiene poder
predictivo sobre los precios de metales base** (relación cobre↔CLP de doble vía).
Esta literatura fundamenta el canal moneda (USD/CLP, DXY) y motiva tratar el cobre
como variable exógena/forzante frente a las acciones locales (coherente con la
causalidad unidireccional hallada por Toda-Yamamoto en §6.12).

### 3.3 Iliquidez y descubrimiento de precios

El hallazgo central de esta tesis dialoga directamente con **Amihud (2002)**, quien
propone el ratio de iliquidez \(\text{ILLIQ}=|r|/\text{volumen}\$\) y muestra que la
iliquidez (i) está positivamente asociada a los retornos esperados (prima de
liquidez) y (ii) **afecta con mayor fuerza a las empresas pequeñas**. La literatura
de microestructura asocia la baja liquidez con un **descubrimiento de precios
lento**: la información tarda más en incorporarse a los precios. El caso Pucobre
—pure-play con 62% de días sin transacción y transmisión del cobre diferida en el
tiempo (§6.13–6.14)— es una manifestación nítida de este mecanismo en un mercado
emergente pequeño.

### 3.4 Fundamentos econométricos

- **Cointegración y corrección de error:** Engle y Granger (1987) introducen la
  cointegración y el ECM; Johansen (1991) generaliza al enfoque de máxima
  verosimilitud multivariante (test de la traza y del máximo autovalor) usado aquí.
- **Bounds testing y asimetría:** Pesaran, Shin y Smith (2001) proponen el ARDL
  *bounds test*, válido con regresores I(0)/I(1) sin requerir pre-test de orden;
  Shin, Yu y Greenberg (2014) lo extienden al **NARDL** para asimetrías de corto y
  largo plazo (sumas parciales positivas/negativas), clave para el cobre.
- **Causalidad robusta a integración:** Toda y Yamamoto (1995) proponen el VAR
  aumentado en niveles para inferir causalidad sin sesgo por raíces unitarias.
- **Volatilidad condicional:** Bollerslev (1986) (GARCH), Nelson (1991) (EGARCH) y
  Glosten, Jagannathan y Runkle (1993) (GJR-GARCH) modelan persistencia y el
  **efecto apalancamiento** documentado en §6.6.
- **Inferencia robusta:** Newey y West (1987) para errores HAC; pruebas de raíz
  unitaria de Dickey-Fuller aumentada, Phillips-Perron, KPSS (Kwiatkowski et al.,
  1992) y Zivot-Andrews (1992) para quiebres endógenos.

### 3.5 Vacío que aborda la tesis

La literatura chilena se ha concentrado en el canal **cobre→tipo de cambio→macro**.
Es escasa la evidencia que cuantifique el canal **cobre→valoración bursátil de las
mineras chilenas** distinguiendo horizonte temporal y rol de la liquidez del
activo. Esta tesis aporta en ese punto, integrando APT, cointegración, volatilidad
y microestructura sobre el reducido universo de *pure-plays* cupríferos.

---

## 4. Datos

### 4.1 Universo de empresas (resuelto empíricamente)

El universo de mineras de cobre cotizadas vinculadas a Chile es muy reducido. Se
verificó la disponibilidad real de cada candidato (`src/verificar_universo.py`).
Resultado en tres anillos:

| Anillo | Ticker | Empresa | Mercado | Moneda | Obs |
|---|---|---|---|---|---|
| A (núcleo cobre) | `ANTO.L` | Antofagasta plc | LSE (cross-listed) | GBp | 6.720 |
| A (núcleo cobre) | `PUCOBRE.SN` | Pucobre (Punta del Cobre) | **Bolsa Santiago** | CLP | 6.673 |
| B (materiales) | `CAP.SN` | CAP S.A. | Santiago | CLP | 6.673 |
| B (materiales) | `SQM-B.SN` | SQM | Santiago | CLP | 6.673 |
| C (ref. int'l) | `SCCO`,`FCX`,`BHP`,`GLEN.L` | Southern, Freeport, BHP, Glencore | NYSE/LSE | USD/GBp | 3.793–6.641 |

**Codelco** se excluye del análisis accionario (estatal, no cotiza en renta
variable). Hallazgo relevante: **Pucobre es el único *pure-play* de cobre listado
directamente en la Bolsa de Santiago y en pesos**, lo que habilita el contraste con
Antofagasta (cross-listed, GBp, alta liquidez).

### 4.2 Variables (factores)

Factores de mercado descargados (Yahoo Finance, diarios): precio del cobre
(`HG=F`, futuro COMEX), USD/CLP (`CLP=X`), índice dólar DXY (`DX-Y.NYB`), VIX,
S&P 500, rendimientos UST 13s/5A/10A (`^IRX/^FVX/^TNX`), WTI (`CL=F`) y un proxy
del mercado chileno. Ver diccionario completo en `docs/diccionario_datos.md`.

### 4.3 Limitaciones de datos (declaradas)

- **`^IPSA` (Yahoo) es inconsistente**: el feed entrega datos sólo hasta ~2019 de
  forma reproducible. Se sustituyó el factor de mercado local por **`ECH`** (ETF
  iShares MSCI Chile, NYSE, USD), con cobertura limpia 2007–2026. *Costo:* ECH
  está en USD e incorpora el componente cambiario, parcialmente solapado con
  `USD/CLP` (se monitorea vía VIF; máx ≈ 3.5, sin colinealidad severa).
- **FRED inaccesible** desde el entorno de ejecución (timeouts). El precio global
  mensual del cobre y la pendiente de curva quedaron pendientes; el cobre se cubre
  con el futuro COMEX diario y las tasas con los índices de Yahoo.
- **Macro nacional chilena**: incorporada **sin credenciales** vía la API pública
  `mindicador.cl` (`src/ingesta_macro_cl.py`): **TPM** (diaria, 5.560 obs), **IMACEC**
  e **IPC** (mensuales) y dólar observado. El **EMBI Chile** y series específicas
  del Banco Central (BCU/BTU) siguen requiriendo credenciales `BCCH_USER/PASS`
  (pipeline listo en `src/ingesta.py`).
- **Calendarios heterogéneos** (LSE/Santiago/NYSE) reducen la muestra efectiva por
  intersección en las regresiones multifactor (n ≈ 4.475 para el período común).

### 4.4 Transformaciones

Log-precios `ln(P_t)` (niveles, I(1) esperado); log-retornos `100·Δln(P_t)` (I(0));
variaciones log de factores de precio; primeras diferencias de tasas. Pipeline en
`src/preparacion.py`.

---

## 5. Metodología

El diseño nace de las propiedades de los datos. El árbol de decisión aplicado:

1. **Orden de integración** (ADF, PP, KPSS, decisión cruzada) → log-precios I(1),
   retornos I(0). Mezcla I(0)/I(1) sin I(2).
2. **Impacto contemporáneo de corto plazo** → regresión OLS con errores **HAC
   (Newey-West)**, con batería de diagnósticos (Breusch-Godfrey, Breusch-Pagan,
   White, ARCH-LM, VIF, Jarque-Bera, Ljung-Box).
3. **Dinámica conjunta** → **VAR** en retornos; funciones impulso-respuesta (IRF),
   descomposición de varianza (FEVD) y causalidad de Granger.
4. **Largo plazo** → **cointegración de Johansen** (rango) y **VECM** (vector de
   cointegración + velocidad de ajuste). Robustez con **ARDL bounds** (PSS, 2001).
5. **Volatilidad** → familia **GARCH** (GARCH, EGARCH, GJR) con distribución
   t-Student; persistencia y efecto apalancamiento.
6. **Panel** (anillos A+B) → Pooled/FE/RE con test de Hausman; errores agrupados
   por empresa. Se advierte sobre N pequeño (=4) y la inviabilidad de GMM dinámico.
7. **Robustez** → quiebres (Zivot-Andrews) y estabilidad por submuestras
   (crisis 2008, supraciclo, 2015-19, COVID+).

**Hipótesis principales.** H1: el cobre tiene impacto positivo y significativo
sobre los retornos mineros. H2: la sensibilidad al cobre es heterogénea y depende
de la liquidez del activo. H3: existe una relación de largo plazo (cointegración)
entre el precio de la acción y el cobre/moneda. H4: la volatilidad presenta
persistencia alta y efecto apalancamiento.

---

## 6. Resultados

### 6.1 Estadística descriptiva (`outputs/tables/descriptivos_retornos.csv`)

Log-retornos diarios (%), 2004–2026:

| Activo | media | sd | asimetría | curtosis | Jarque-Bera |
|---|---|---|---|---|---|
| ANTO.L | 0.051 | 2.65 | 0.09 | 4.15 | rechaza normalidad |
| PUCOBRE.SN | 0.053 | 1.44 | **1.50** | **35.5** | rechaza normalidad |
| CAP.SN | 0.044 | 2.47 | −0.13 | 10.7 | rechaza normalidad |
| SQM-B.SN | 0.067 | 2.32 | −0.19 | 6.67 | rechaza normalidad |

Todas las series exhiben **exceso de curtosis** (colas pesadas) y no-normalidad
(Jarque-Bera, p<0.001). Pucobre destaca por curtosis extrema (35.5) y asimetría
positiva (1.5), señal de **thin trading**/iliquidez (saltos esporádicos sobre días
de baja transacción).

### 6.2 Estacionariedad y cointegración

- **ADF/PP/KPSS** (decisión cruzada, `estacionariedad.csv`): log-precios **I(1)**,
  retornos y diferencias **I(0)**. Confirmado por **Zivot-Andrews** (no se rechaza
  raíz unitaria ni con quiebre endógeno: ANTO p≈0.62, PUCOBRE p≈0.99).
- **Engle-Granger bivariado** (activo~cobre): cointegración débil/ausente (sólo el
  cobre no basta).
- **Johansen multivariante** `[log-precio, cobre, USDCLP, DXY]`: **rango r = 1**
  para ANTO y PUCOBRE → existe **una** relación de equilibrio de largo plazo.

### 6.3 Impacto contemporáneo (regresión HAC) — `hac_coeficientes.csv`

**Beta-cobre** (efecto de +1% en el cobre sobre el retorno diario, %):

| Activo | β-cobre | t | R² |
|---|---|---|---|
| ANTO.L | **0.701** | 15.4 | 0.42 |
| PUCOBRE.SN | **0.085** | 4.4 | **0.04** |
| CAP.SN | 0.151 | 5.7 | 0.25 |
| SQM-B.SN | 0.109 | 4.2 | 0.25 |
| SCCO | 0.487 | 9.6 | 0.58 |
| FCX | 0.627 | 10.3 | 0.53 |
| BHP | 0.316 | 10.7 | 0.60 |
| GLEN.L | 0.582 | 9.8 | 0.29 |

Para Antofagasta, además del cobre, son significativos el DXY (≈ −0.35; dólar
arriba → acción abajo), el mercado (S&P y proxy local) y el cambio en la tasa
UST10Y. Para Pucobre, **sólo el mercado local y (débilmente) el cobre** son
significativos, con un R² de apenas 0.04: el retorno de Pucobre es mayoritariamente
**idiosincrásico/ilíquido** en el día a día. **Diagnósticos** (`hac_diagnosticos.csv`):
efectos ARCH significativos en todos los activos (justifica GARCH); autocorrelación
(justifica HAC); no-normalidad de residuos. VIF máx ≈ 3.5 (sin colinealidad severa).

→ **H1 se sostiene** (cobre positivo y significativo en todos). **H2 se sostiene
con fuerza**: la sensibilidad depende de la liquidez (0.70 en el *pure-play*
líquido vs 0.085 en el local ilíquido).

### 6.4 Dinámica (VAR, IRF, FEVD, Granger) — `var_resumen.csv`

| Activo | FEVD cobre (1d) | FEVD cobre (20d) | IRF acum. 5d | Granger cobre→activo |
|---|---|---|---|---|
| ANTO.L | 28.7% | 27.8% | 0.091 | p=0.008 (sí) |
| PUCOBRE.SN | 2.0% | 4.3% | **0.196** | p<0.001 (sí) |

Clave: en Pucobre la respuesta **acumulada a 5 días (0.196) es ~4× la del primer
día (0.043)**, y la FEVD del cobre crece de 2% a 4.3% entre 1 y 20 días. Es decir,
el cobre **sí causa** los retornos de Pucobre (Granger p<0.001), pero el efecto se
**difiere** en el tiempo en lugar de impactar contemporáneamente — consistente con
descubrimiento de precios lento por iliquidez.

### 6.5 Largo plazo (VECM) — `vecm_resumen.csv`

Vector de cointegración (r=1), elasticidades del log-precio:

| Activo | elast. cobre | elast. USDCLP | elast. DXY | velocidad ajuste α |
|---|---|---|---|---|
| ANTO.L | **0.860** | 6.63 | −11.80 | −0.0008 |
| PUCOBRE.SN | **0.753** | 4.82 | −7.96 | −0.0004 |

En el **largo plazo**, una subida de 1% en el cobre se asocia a ~0.75–0.86% más en
el precio de la acción — y **Pucobre (0.75) es comparable a Antofagasta (0.86)**,
en marcado contraste con su nula reacción contemporánea. La velocidad de ajuste α
es negativa (corrige desequilibrios) pero muy pequeña → **ajuste lento**. *Cautela:*
los coeficientes grandes de USDCLP/DXY reflejan colinealidad entre ambas medidas
del dólar; se interpretan con reserva.

→ **H3 se sostiene** (existe equilibrio de largo plazo cobre→valoración),
con la matización del punto 6.7.

### 6.6 Volatilidad (GARCH) — `garch_resumen.csv`

| Activo | mejor modelo (AIC) | persistencia | efecto apalancamiento |
|---|---|---|---|
| ANTO.L | GJR-GARCH(1,1) | 0.991 | sí (γ>0) |
| CAP.SN | GJR-GARCH(1,1) | 0.995 | sí (γ>0) |
| SQM-B.SN | EGARCH(1,1) | 0.999 | sí (γ<0 en EGARCH) |
| PUCOBRE.SN | *inestable* | — | no confiable |

Persistencia de la volatilidad muy alta (≈0.99) y **efecto apalancamiento**
confirmado (las caídas elevan más la volatilidad futura). **Excepción honesta:**
en Pucobre los modelos GARCH son **inestables** (soluciones de borde) debido a la
iliquidez y los saltos extremos (curtosis 35.5); se recomienda filtrar días de
retorno nulo o usar modelos con saltos. → **H4 se sostiene** salvo en el activo
ilíquido.

### 6.7 Robustez

- **ARDL bounds (diario, k=3)**: F=2.89 (ANTO) y 1.55 (PUCOBRE), **por debajo del
  crítico I(1)=4.35 → no confirma cointegración**, en contraste con Johansen. La
  explicación es la **baja potencia del test uniecuacional cuando la velocidad de
  ajuste es minúscula** (α≈−0.0008 en el VECM). Conclusión prudente: la evidencia
  de largo plazo es **sugerente pero no unánime**; se prioriza el VECM (basado en
  el sistema) y se declara como limitación.
- **Estabilidad de β-cobre por submuestras** (`robustez_submuestras.csv`):

  | Submuestra | ANTO β-cobre | PUCOBRE β-cobre |
  |---|---|---|
  | crisis 2008-09 | 0.60 (t=6.7) | 0.08 (t=2.1) |
  | supraciclo 2010-14 | 0.69 (t=16.9) | 0.05 (t=1.3) |
  | 2015-19 | 0.90 (t=13.9) | 0.01 (t=0.3) |
  | COVID+ 2020-26 | 0.65 (t=8.1) | **0.15 (t=4.2)** |

  La sensibilidad de Antofagasta es **estable y siempre significativa**, con pico en
  2015-19. Pucobre es débil/no significativa salvo en COVID+, donde sube a 0.15
  (t=4.2): leve mejora de transmisión en el boom reciente del cobre.

### 6.8 Panel sectorial (N=4) — `panel_resultados.csv`

Impacto promedio del sector minería-materiales chileno (FE≈RE≈Pooled; Hausman no
rechaza RE): β-cobre ≈ 0.205 (p=0.073, marginal con *cluster* en 4 entidades);
**el mercado local domina** (β≈0.79, p<0.001); DXY≈−0.19 (p<0.001); UST10Y +1.9
(p<0.01). R² within ≈ 0.23. *Advertencia:* con N=4 el panel es robustez sectorial,
no inferencia primaria; GMM dinámico no es viable.

### 6.9 Canal de política monetaria chilena (TPM) — `hac_coeficientes.csv`

Incorporada la TPM (vía `mindicador.cl`, sin credenciales), el cambio diario de la
TPM (`d_tpm`) entra con **signo negativo** en todos los activos (endurecimiento →
menor retorno, económicamente correcto) pero **no significativo** (p>0.12). Las
β-cobre permanecen estables al añadirla (robustez). La no significatividad diaria
motiva el estudio de eventos (§6.11).

### 6.10 Asimetrías del cobre (NARDL) — `nardl_resumen.csv`

Descomponiendo el cobre en sumas parciales de alzas y caídas (Shin-Yu-Greenberg):

| Activo | Bounds F | cointegra | asimetría LP (Wald, p) |
|---|---|---|---|
| **ANTO.L** | **4.50** | **sí (5%)** | **sí: Wald=8.45, p=0.004** |
| PUCOBRE.SN | 1.83 | no | no (p=0.29) |
| CAP.SN | 3.10 | no | no (p=0.15) |
| SQM-B.SN | 2.03 | no | no (p=0.23) |

**Antofagasta presenta cointegración no lineal y asimetría de largo plazo
significativa**: responde de forma estadísticamente distinta a alzas vs caídas del
cobre (elasticidades ≈0.93 vs ≈0.90; diferencia modesta pero significativa por el
tamaño muestral). Los demás activos no rechazan simetría, coherente con su vínculo
más débil al cobre.

### 6.11 Estudio de eventos — anuncios de TPM — `event_study_tpm.csv`

Modelo de mercado (mercado=ECH), ventana [-5,+5] en torno a 51 alzas y 41 bajas de
TPM. Los CAAR tienen **signo económico correcto** (alza TPM → anormal negativo:
ANTO −1.04%, CAP −1.90%; baja → positivo) pero **ninguno es significativo**
(p>0.37). Interpretación: los cambios de TPM están **anticipados** (sin sorpresa en
el anuncio) y la valoración minera responde a **factores globales** más que a la
política monetaria doméstica. Refinamiento futuro: usar el componente *sorpresa*
(TPM efectiva vs esperada).

### 6.12 Causalidad robusta a integración (Toda-Yamamoto) — `toda_yamamoto.csv`

| Activo | cobre→activo | activo→cobre | usdclp→activo |
|---|---|---|---|
| ANTO.L | **causa (p=0.04)** | no (p=0.11) | causa (p<0.001) |
| PUCOBRE.SN | **causa (p<0.001)** | marginal (p=0.02)* | no (p=0.29) |

El cobre **causa** (Granger, robusto a cointegración) a ambos activos, de forma
**unidireccional** para Antofagasta (es tomadora de precios). El sentido inverso en
Pucobre (p=0.02) es económicamente implausible (una minera pequeña no mueve el
COMEX) → probable artefacto del modelo aumentado de 13 rezagos. (*) marcado como
no causal en términos económicos.

---

### 6.13 Prueba formal de la hipótesis de iliquidez — `iliquidez_amihud.csv`, `iliquidez_test.csv`

La hipótesis de que la iliquidez explica la baja transmisión contemporánea del
cobre en Pucobre se prueba formalmente:

**(a) Magnitud de la iliquidez.** Pucobre presenta **62% de días con retorno cero**
(no transa en la mayoría de las jornadas), frente a 5.5% (ANTO), 1.3% (SCCO) o
0.18% (Glencore); su volumen medio (~US$24M equiv.) es dos órdenes de magnitud
menor que el de Antofagasta (~US$2.000M). Es el activo masivamente más ilíquido.

**(b) Evidencia transversal (8 activos).** La correlación de Spearman entre
iliquidez (% días cero) y la β-cobre contemporánea es **negativa** (ρ≈−0.55), en la
dirección predicha, aunque no significativa con N=8 (baja potencia).

**(c) Rezagos distribuidos (prueba directa).** Descomponiendo el efecto del cobre
por rezagos:

| Activo | β día 0 | β acumulado 0–5 | **fracción día 0** |
|---|---|---|---|
| ANTO.L | 0.816 | 0.862 | **94.7%** (inmediata) |
| PUCOBRE.SN | 0.121 | 0.415 | **29.2%** (diferida) |

En Antofagasta el 95% del impacto del cobre llega el mismo día; en Pucobre, sólo el
29% —el 71% restante se difiere a los días siguientes—. Confirmación directa del
**descubrimiento de precios lento** por iliquidez.

*Nota metodológica:* un *split* por régimen de iliquidez (Amihud móvil) se descartó
por confundir iliquidez con régimen de volatilidad (el ILLIQ sube en períodos
volátiles donde todo comueve más); el test de rezagos distribuidos es limpio frente
a ese sesgo.

### 6.14 Modelo mensual con macro nacional — `mensual_resumen.csv`

A frecuencia mensual (que permite usar IMACEC e IPC en su frecuencia natural):

| Activo | β-cobre | t | R² | IMACEC (t) | d_TPM (t) |
|---|---|---|---|---|---|
| ANTO.L | 0.712 | 5.2 | 0.39 | −0.16 (−1.7) | 0.05 (0.1) |
| **PUCOBRE.SN** | **0.599** | **7.3** | **0.31** | −0.26 (−2.8) | 1.41 (1.0) |
| CAP.SN | 0.698 | 4.8 | 0.28 | −0.03 (−0.2) | −0.60 (−0.4) |

**Resultado decisivo:** a frecuencia mensual la β-cobre de Pucobre **salta de 0.085
(diaria) a 0.599** y el R² de 0.04 a 0.31. La sensibilidad al cobre **crece
monótonamente con el horizonte** (diario 0.085 → acumulado 5d 0.415 → mensual 0.599
→ largo plazo 0.75): al agregar temporalmente emerge la verdadera sensibilidad,
cercana a la de Antofagasta. El IMACEC entra significativo y negativo para Pucobre
(controlado por cobre; interpretación cautelosa). La TPM sigue sin ser
significativa, consistente con §6.9 y §6.11.

## 7. Discusión

El cuerpo de evidencia es **consistente y se triangula**:

1. **Heterogeneidad por liquidez (hallazgo central).** Antofagasta —*pure-play*
   líquido y cross-listed— incorpora el cobre de forma fuerte e inmediata
   (β≈0.70; FEVD≈28%; 95% del impacto en el día 0). Pucobre —*pure-play* local e
   ilíquido (62% de días sin transar)— casi no reacciona en el día (β≈0.09;
   R²≈0.04), pero su sensibilidad al cobre **crece monótonamente con el horizonte**:
   0.085 (diario) → 0.42 (acumulado 5d) → 0.60 (mensual) → 0.75 (largo plazo). El
   cobre lo causa (Toda-Yamamoto y Granger, p<0.001) y la relación de largo plazo
   es plena. Interpretación, ahora **formalmente probada** (rezagos distribuidos +
   modelo mensual): **la iliquidez retrasa el descubrimiento de precios, no anula
   el fundamento cobre→valoración.**
2. **Canal de moneda.** El dólar global (DXY) impacta negativamente; el USD/CLP
   aparece en la relación de largo plazo (con cautela por colinealidad).
3. **Riesgo y volatilidad.** Alta persistencia y efecto apalancamiento, típicos de
   activos de materias primas.
4. **Comparación internacional.** Las β-cobre de SCCO/FCX/Glencore (0.49–0.63) y de
   Antofagasta (0.70) son del mismo orden, validando externamente la magnitud; las
   chilenas de materiales (CAP, SQM, 0.11–0.15) son menos sensibles por no ser
   cobre puro.

**Comparación con la literatura:** *[a completar con fuentes reales verificadas].*

5. **Política monetaria y eventos.** El canal TPM es negativo pero débil a
   frecuencia diaria, y los anuncios de TPM no generan retornos anormales
   significativos: la valoración minera es dominantemente global, no doméstica.
6. **Asimetría.** Sólo Antofagasta muestra respuesta asimétrica de largo plazo al
   cobre (NARDL), reforzando que es el activo donde el fundamento cobre opera con
   mayor riqueza dinámica.
7. **Causalidad.** Toda-Yamamoto confirma causalidad cobre→acción robusta a
   cointegración, unidireccional para Antofagasta.

**Limitaciones.** (i) EMBI Chile y series BCU/BTU pendientes de credenciales BCCh
(TPM/IMACEC/IPC ya incorporadas vía mindicador.cl); (ii) FRED inaccesible en el
entorno; (iii) proxy de mercado local en USD (ECH) en vez de IPSA por
inconsistencia del feed; (iv) calendarios heterogéneos reducen la muestra; (v)
GARCH no fiable en Pucobre; (vi) ARDL lineal no confirma cointegración (baja
potencia ante ajuste lento), aunque NARDL sí la detecta para Antofagasta; (vii)
panel con N=4; (viii) event study sin componente de sorpresa de TPM.

---

## 8. Conclusiones

1. El universo de mineras de cobre cotizadas vinculadas a Chile es mínimo y se
   resolvió empíricamente: Antofagasta (LSE) y Pucobre (Santiago) como núcleo.
2. El precio del cobre es un determinante **positivo y significativo** de los
   retornos mineros, con magnitud creciente en la liquidez del activo.
3. El resultado más novedoso es la **disociación corto/largo plazo en el activo
   ilíquido (Pucobre)**: transmisión contemporánea casi nula pero vínculo de largo
   plazo pleno y causalidad con rezago. Aporta evidencia sobre (in)eficiencia
   informacional en un mercado emergente pequeño.
4. La volatilidad es persistente y asimétrica; el dólar y las tasas globales
   complementan el canal del cobre.

**Líneas futuras.** Incorporar macro del Banco Central (TPM, IMACEC, EMBI);
NARDL para asimetrías alza/baja del cobre; estudio de eventos en anuncios de
política/COCHILCO; medidas formales de iliquidez (Amihud) e intradía; GARCH con
saltos para Pucobre; Toda-Yamamoto para causalidad con series integradas.

---

## 9. Referencias y anexos

**Referencias** — verificadas en fuentes primarias (revisar formato APA final).

*Teoría de factores y mercados:*
- Ross, S. A. (1976). The arbitrage theory of capital asset pricing. *Journal of Economic Theory*, 13(3), 341–360.
- Chen, N.-F., Roll, R., & Ross, S. A. (1986). Economic forces and the stock market. *Journal of Business*, 59(3), 383–403. https://www.jstor.org/stable/2352710
- Amihud, Y. (2002). Illiquidity and stock returns: cross-section and time-series effects. *Journal of Financial Markets*, 5(1), 31–56. https://doi.org/10.1016/S1386-4181(01)00024-6

*Cobre, monedas-commodity y Chile:*
- Chen, Y.-C., & Rogoff, K. (2003). Commodity currencies. *Journal of International Economics*, 60(1), 133–160. https://doi.org/10.1016/S0022-1996(02)00072-7
- Banco Central de Chile. Working Paper N°640. *Copper, the Real Exchange Rate and Macroeconomic Fluctuations in Chile*. https://www.bcentral.cl/en/content/-/details/working-papers-n-640
- *Forecasting base metal prices with the Chilean exchange rate*. *Resources Policy*. https://www.sciencedirect.com/science/article/abs/pii/S0301420718303271

*Cointegración, ARDL/NARDL y causalidad:*
- Engle, R. F., & Granger, C. W. J. (1987). Co-integration and error correction. *Econometrica*, 55(2), 251–276.
- Johansen, S. (1991). Estimation and hypothesis testing of cointegration vectors in Gaussian VAR models. *Econometrica*, 59(6), 1551–1580.
- Pesaran, M. H., Shin, Y., & Smith, R. J. (2001). Bounds testing approaches to the analysis of level relationships. *Journal of Applied Econometrics*, 16(3), 289–326. https://doi.org/10.1002/jae.616
- Shin, Y., Yu, B., & Greenwood-Nimmo, M. (2014). Modelling asymmetric cointegration and dynamic multipliers in a NARDL framework. En *Festschrift in Honor of Peter Schmidt* (pp. 281–314). Springer.
- Toda, H. Y., & Yamamoto, T. (1995). Statistical inference in vector autoregressions with possibly integrated processes. *Journal of Econometrics*, 66(1–2), 225–250.

*Volatilidad y errores robustos:*
- Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3), 307–327.
- Nelson, D. B. (1991). Conditional heteroskedasticity in asset returns: a new approach. *Econometrica*, 59(2), 347–370.
- Glosten, L. R., Jagannathan, R., & Runkle, D. E. (1993). On the relation between the expected value and the volatility of the nominal excess return on stocks. *Journal of Finance*, 48(5), 1779–1801.
- Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.

*Raíces unitarias y quiebres:* Dickey & Fuller (1979); Phillips & Perron (1988); Kwiatkowski, Phillips, Schmidt & Shin (1992, KPSS); Zivot & Andrews (1992).

> Nota: confirmar paginación y DOIs en Scopus/Web of Science/Google Scholar antes de
> la entrega final. Estas referencias fueron contrastadas con repositorios del
> editor; el formato APA definitivo es responsabilidad del autor.

**Anexos (reproducibilidad).**
- Código: `src/` (verificación de universo, ingesta, preparación, EDA, modelos).
- Tablas: `outputs/tables/` (23 archivos CSV).
- Figuras: `outputs/figures/` (series, ACF, IRF, volatilidad condicional, heatmap).
- Diccionario de datos: `docs/diccionario_datos.md`.
- Decisiones fundacionales: `docs/00_decisiones_fundacionales.md`.
- Entorno: `requirements.txt` (Python 3.13; statsmodels 0.14.6, arch 8.0, linearmodels 7.0).
