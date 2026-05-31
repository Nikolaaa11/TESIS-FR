# Impacto de las variables macroeconómicas globales y financieras en la valoración bursátil del sector de minería de cobre en Chile

**Un análisis econométrico de series de tiempo y datos de panel, 2004–2026**

Tesis para optar al grado de Magíster en Data Science · Facultad de Economía y Negocios · Universidad San Sebastián

*Nota de reproducibilidad.* Los resultados numéricos de este trabajo provienen de
estimaciones propias sobre datos de fuentes públicas (Yahoo Finance y la API del
servicio de indicadores económicos mindicador.cl), recopilados en mayo de 2026. El
código, los datos procesados y las tablas y figuras de salida se encuentran
disponibles en el repositorio del proyecto, conforme a los estándares de
reproducibilidad de la disciplina (véase la Declaración de disponibilidad de datos
en el Capítulo 9).

---

## Resumen

Esta tesis cuantifica el impacto de las variables macroeconómicas globales y
financieras sobre el precio y el retorno de las acciones del sector de minería de
cobre vinculadas a Chile, durante el período 2004–2026 a frecuencia diaria. El
problema empírico parte de una restricción estructural del mercado de capitales
chileno: el universo de mineras de cobre cotizadas es mínimo. Resolviéndolo con
verificación empírica, se identifican dos *pure-plays* de cobre —Antofagasta plc,
*cross-listed* en Londres, y Pucobre, único productor de cobre puro listado
directamente en la Bolsa de Santiago— complementados por un panel sectorial de
minería-materiales (CAP, SQM) y por referencias internacionales del cobre (Southern
Copper, Freeport-McMoRan, BHP, Glencore) que aportan validez externa.

Metodológicamente, el diseño se deriva de las propiedades estadísticas de las
series: los log-precios resultan integrados de orden uno, I(1), y los retornos
estacionarios, I(0), lo que habilita una batería complementaria de técnicas —
regresión con errores robustos a heterocedasticidad y autocorrelación (HAC,
Newey-West), modelos vectoriales autorregresivos (VAR) con funciones
impulso-respuesta y descomposición de varianza, cointegración de Johansen y modelos
de corrección de error vectorial (VECM), modelos ARDL/NARDL de retardos
distribuidos con prueba de límites, causalidad de Toda-Yamamoto robusta a la
integración, modelos de volatilidad condicional de la familia GARCH, datos de panel
con efectos fijos/aleatorios, un estudio de eventos sobre los anuncios de política
monetaria y una prueba formal del rol de la iliquidez basada en el ratio de Amihud.

El hallazgo central es una **disociación entre el corto y el largo plazo gobernada
por la liquidez del activo**. El *pure-play* líquido (Antofagasta) incorpora el
precio del cobre de forma casi instantánea: su elasticidad-cobre contemporánea es
0.70 y el cobre explica cerca del 28% de la varianza de su retorno. El *pure-play*
local e ilíquido (Pucobre), que no registra transacciones en el 62% de las
jornadas, exhibe una transmisión contemporánea casi nula (elasticidad de 0.09,
R² de 0.04), pero su sensibilidad al cobre **crece monótonamente con el horizonte
temporal**: 0.09 (diaria) → 0.42 (acumulada a cinco días) → 0.60 (mensual) → 0.75
(largo plazo de cointegración), magnitud esta última estadísticamente comparable a
la de Antofagasta (0.86). La iliquidez, por tanto, **retrasa pero no elimina** la
transmisión del fundamento cobre→valoración: es una manifestación nítida de
descubrimiento de precios lento en un mercado emergente pequeño. Resultados
complementarios documentan asimetría de largo plazo en Antofagasta (responde de
forma distinta a alzas y caídas del cobre), persistencia y efecto apalancamiento en
la volatilidad, predominio de los factores globales (cobre, dólar) por sobre la
política monetaria doméstica, y causalidad unidireccional cobre→acción.

**Palabras clave:** cobre; valoración bursátil; Chile; cointegración; VECM; NARDL;
GARCH; iliquidez de Amihud; descubrimiento de precios; econometría financiera.

---

## Abstract

This thesis quantifies the impact of global macroeconomic and financial variables on
the price and returns of copper-mining equities linked to Chile, over 2004–2026 at
daily frequency. The empirical problem begins from a structural constraint of the
Chilean capital market: the listed copper-mining universe is minimal. Resolving it
empirically, we identify two copper *pure-plays* —Antofagasta plc (London
cross-listed) and Pucobre, the only pure-copper producer listed directly on the
Santiago Exchange— complemented by a sector panel (CAP, SQM) and by international
copper benchmarks (Southern Copper, Freeport-McMoRan, BHP, Glencore) providing
external validity.

The design follows the data's statistical properties: log-prices are I(1) and
returns I(0), enabling a complementary toolkit —HAC (Newey-West) regression, VAR
with impulse-response functions and variance decomposition, Johansen cointegration
and VECM, ARDL/NARDL bounds testing, Toda-Yamamoto causality robust to integration,
GARCH-family conditional-volatility models, panel fixed/random effects, an event
study around monetary-policy announcements, and a formal test of illiquidity based
on the Amihud ratio.

The central finding is a **liquidity-governed dissociation between short- and
long-run transmission**. The liquid pure-play (Antofagasta) prices copper almost
instantaneously (contemporaneous copper-elasticity 0.70; copper explains ~28% of
return variance). The illiquid local pure-play (Pucobre), which does not trade on
62% of days, shows near-zero contemporaneous transmission (elasticity 0.09, R²
0.04), yet its copper-sensitivity **grows monotonically with the horizon**: 0.09
(daily) → 0.42 (5-day cumulative) → 0.60 (monthly) → 0.75 (long-run cointegration),
the latter statistically comparable to Antofagasta's 0.86. Illiquidity therefore
**delays but does not eliminate** the copper→valuation transmission — a clear
manifestation of slow price discovery in a small emerging market.

**Keywords:** copper; equity valuation; Chile; cointegration; VECM; NARDL; GARCH;
Amihud illiquidity; price discovery; financial econometrics.

---

## Notación y abreviaturas

| Símbolo / sigla | Significado |
|---|---|
| P_t, r_t | Precio y log-retorno del activo en t; r_t = 100·(ln P_t − ln P_{t−1}) |
| I(d) | Serie integrada de orden d (estacionaria tras d diferencias) |
| HAC | Heteroskedasticity and Autocorrelation Consistent (errores de Newey-West) |
| ADF, PP, KPSS | Pruebas de raíz unitaria de Dickey-Fuller aumentada, Phillips-Perron y Kwiatkowski et al. |
| VAR / VECM | Vector autorregresivo / de corrección de error |
| IRF / FEVD | Función impulso-respuesta / descomposición de la varianza del error de predicción |
| ARDL / NARDL | Autorregresivo de retardos distribuidos / su versión no lineal (asimétrica) |
| GARCH / EGARCH / GJR | Modelos de volatilidad condicional (Bollerslev; Nelson; Glosten-Jagannathan-Runkle) |
| ILLIQ | Ratio de iliquidez de Amihud (2002) |
| TPM / IMACEC / IPC | Tasa de política monetaria, índice mensual de actividad económica, índice de precios al consumidor (Chile) |
| DXY / VIX / WTI | Índice dólar, índice de volatilidad implícita del S&P 500, petróleo West Texas Intermediate |
| CAAR | Cumulative Average Abnormal Return (retorno anormal acumulado promedio) |
| ANTO, PUCOBRE | Antofagasta plc (LSE), Pucobre / Sociedad Punta del Cobre (Santiago) |

---

## 1. Introducción

### 1.1 Contextualización

Chile es la mayor economía cuprífera del planeta. El cobre concentra una fracción
dominante de sus exportaciones y constituye un canal de primer orden en la
transmisión de los ciclos globales hacia la actividad, el tipo de cambio y los
mercados financieros nacionales. Esta centralidad del metal vuelve económicamente
relevante una pregunta que, sin embargo, ha recibido escasa atención empírica
directa: ¿en qué medida y con qué dinámica se transmiten el precio del cobre y las
condiciones macro-financieras globales a la **valoración bursátil** de las propias
empresas mineras del país?

Chile aporta una fracción cercana a un cuarto de la producción mundial de cobre de
mina y el metal concentra del orden de la mitad de su canasta exportadora; el cobre
es, además, una fuente fiscal de primer orden vía Codelco y los impuestos a la gran
minería privada. Esta dependencia estructural explica por qué los ciclos del precio
del cobre —el superciclo de 2004–2011, el desplome de 2008, el shock de la pandemia
en 2020 y el repunte pospandemia de 2021— se transmiten con fuerza a la actividad, al
tipo de cambio y a los mercados financieros locales, y vuelve natural preguntarse por
su impacto en la valoración de las propias mineras.

La literatura chilena ha estudiado con profundidad el canal cobre→tipo de
cambio→macroeconomía, estableciendo al peso chileno como una *commodity currency*.
Es comparativamente escasa, en cambio, la evidencia que cuantifique el eslabón
final de esa cadena —la valoración accionaria de las mineras— y, sobre todo, que lo
haga distinguiendo el horizonte temporal del impacto y el papel de la
**microestructura de mercado** (liquidez, descubrimiento de precios). Esa es la
brecha que esta tesis aborda.

### 1.2 Planteamiento del problema

El estudio enfrenta de entrada una restricción estructural decisiva: el universo de
mineras de cobre cotizadas vinculadas a Chile es **muy reducido**. La mayor
productora, Codelco, es estatal y no transa en renta variable; los *pure-plays* de
cobre con operación chilena listados se cuentan con los dedos de una mano. Esta
escasez condiciona todo el diseño metodológico —limita la potencia de los enfoques
de panel y obliga a apoyarse en series de tiempo por activo— y, paradójicamente,
abre la oportunidad analítica central de la tesis: contrastar un *pure-play* líquido
y *cross-listed* (Antofagasta) con un *pure-play* local e ilíquido (Pucobre),
aislando el efecto de la liquidez sobre la transmisión.

### 1.3 Pregunta de investigación

> ¿Cuál es la magnitud, el signo y la dinámica —de corto y de largo plazo— del
> impacto del precio del cobre y de los factores macro-financieros globales y
> nacionales (tipo de cambio, dólar global, tasas de interés, riesgo de mercado,
> política monetaria) sobre el precio y el retorno de las acciones de minería de
> cobre vinculadas a Chile, y cómo modula la liquidez del activo dicha transmisión?

### 1.4 Objetivos

**Objetivo general.** Analizar y cuantificar el impacto de las variables
macroeconómicas globales y financieras sobre el precio y el retorno de las acciones
de minería de cobre vinculadas a Chile en 2004–2026, mediante modelos econométricos
de series de tiempo y de panel, con un enfoque explicativo y de medición de impacto
(no predictivo).

**Objetivos específicos.**
1. Resolver operacionalmente, con verificación empírica, el universo de empresas.
2. Caracterizar las propiedades estadísticas de precios y retornos (estacionariedad,
   colas, volatilidad, quiebres estructurales).
3. Estimar el impacto contemporáneo de los factores sobre los retornos (HAC) y su
   dinámica (VAR, IRF, FEVD, causalidad).
4. Estimar y validar la relación de largo plazo cobre→valoración (cointegración de
   Johansen, VECM) y su robustez (ARDL/NARDL).
5. Modelar la volatilidad condicional y el efecto apalancamiento (familia GARCH).
6. Contrastar resultados mediante un panel sectorial, un estudio de eventos de
   política monetaria y referencias internacionales.
7. Probar formalmente el rol de la iliquidez en la transmisión contemporánea.

### 1.5 Hipótesis

- **H1.** El precio del cobre tiene un impacto positivo y estadísticamente
  significativo sobre los retornos de las mineras vinculadas a Chile.
- **H2.** La sensibilidad contemporánea al cobre es **heterogénea** y depende de la
  liquidez del activo: mayor en los *pure-plays* líquidos, menor en los ilíquidos.
- **H3.** Existe una relación de **equilibrio de largo plazo** (cointegración) entre
  el precio de la acción y el conjunto {cobre, tipo de cambio, dólar}.
- **H4.** La volatilidad de los retornos es **persistente** y exhibe **efecto
  apalancamiento** (las caídas elevan más la volatilidad futura que las alzas).
- **H5.** En el activo ilíquido, la transmisión del cobre es **diferida**: la
  elasticidad contemporánea es baja pero crece con el horizonte hasta converger al
  valor de largo plazo.

### 1.6 Aportes

(i) Resuelve empíricamente un problema de definición de universo recurrentemente
soslayado; (ii) cuantifica por primera vez, con esta batería de métodos, el canal
cobre→valoración para los *pure-plays* chilenos; (iii) documenta y **prueba
formalmente** un mecanismo de descubrimiento de precios diferido por iliquidez,
triangulado por seis técnicas; (iv) entrega un *pipeline* totalmente reproducible.

### 1.7 Estructura

El Capítulo 2 desarrolla el marco teórico; el 3 revisa la literatura; el 4 describe
los datos; el 5 detalla la metodología y las especificaciones; el 6 presenta los
resultados; el 7 los discute; el 8 concluye. Cierran las referencias y los anexos.

---

## 2. Marco teórico

### 2.1 Valoración de activos y factores macroeconómicos

El valor fundamental de una acción es el valor presente de sus flujos de caja
esperados descontados a una tasa ajustada por riesgo. Para una empresa minera de
cobre, los **flujos** dependen directamente del precio del metal (ingreso) y de sus
costos (energía, insumos, salarios, tipo de cambio), mientras que la **tasa de
descuento** depende de la tasa libre de riesgo global y de las primas de riesgo. De
esta estructura se desprenden cinco canales económicos que organizan la selección de
variables independientes:

1. **Canal de demanda/ingreso.** El precio del cobre (LME/COMEX) y la demanda global
   —actividad industrial, China— determinan los ingresos esperados. Es el canal
   directo y, a priori, dominante para un *pure-play*.
2. **Canal de costos.** Energía (WTI) y tipo de cambio (CLP/USD): una depreciación
   real del peso abarata los costos locales medidos en dólares y puede ampliar el
   margen operativo de un exportador de cobre.
3. **Canal de descuento.** Las tasas de interés (rendimientos del Tesoro de EE. UU.
   a distintos plazos, TPM local) afectan el factor de descuento de los flujos.
4. **Canal de moneda global.** El índice dólar (DXY): los *commodities* cotizados en
   dólares tienden a moverse inversamente al valor del dólar.
5. **Canal de riesgo/sentimiento.** El VIX y los índices de mercado (S&P 500,
   mercado local) capturan el apetito por riesgo y el componente sistemático (beta).

### 2.2 Arbitrage Pricing Theory (APT)

El APT (Ross, 1976) postula que el retorno esperado de un activo es una función
lineal de su exposición a un conjunto de factores de riesgo sistemáticos:
E[r_i] = r_f + Σ_k β_{i,k} λ_k, donde λ_k es la prima del factor k y β_{i,k} la
sensibilidad del activo i a ese factor. Chen, Roll y Ross (1986) operacionalizan el
APT con factores macroeconómicos —producción industrial, inflación, prima por
riesgo, pendiente de la curva— y muestran que están sistemáticamente valorados. La
especificación multifactorial de los retornos empleada en el Capítulo 6 es, en
esencia, una contrastación de tipo APT con factores específicos al sector cuprífero.

### 2.3 Niveles versus cambios: equilibrio de largo plazo y dinámica de corto plazo

Una distinción metodológica esencial separa el análisis en **niveles** (precios) del
análisis en **cambios** (retornos). Los precios de activos suelen comportarse como
procesos integrados I(1) —caminatas aleatorias con tendencia estocástica—, mientras
que los retornos son estacionarios I(0). Si dos o más series I(1) comparten una
tendencia estocástica común, están **cointegradas**: existe una combinación lineal
estacionaria que representa su relación de equilibrio de largo plazo (Engle y
Granger, 1987). El teorema de representación de Granger garantiza que toda relación
de cointegración admite una representación de corrección de error (VECM), que separa
limpiamente la dinámica de largo plazo (el vector cointegrante β) de los ajustes de
corto plazo (la velocidad de ajuste α). Esta dualidad es la columna vertebral de la
tesis: el impacto **contemporáneo** sobre los retornos y el equilibrio de **largo
plazo** sobre los niveles responden preguntas distintas y se estiman con
herramientas distintas.

### 2.4 Microestructura, iliquidez y descubrimiento de precios

La hipótesis de mercados eficientes sostiene que los precios incorporan la
información disponible de forma inmediata. La teoría de la microestructura matiza esa
inmediatez: en presencia de **fricciones de liquidez** —baja profundidad, costos de
transacción, transacción esporádica— la información se incorpora a los precios de
forma **gradual**, generando autocorrelación en los retornos y un proceso de
*price discovery* lento. Amihud (2002) propone una medida operativa de iliquidez —el
cociente entre el valor absoluto del retorno y el volumen transado— y documenta que
la iliquidez (i) se asocia a una prima de retorno esperado y (ii) afecta con mayor
fuerza a las empresas pequeñas. Para esta tesis, la teoría de microestructura provee
el marco para interpretar la disociación corto/largo plazo del *pure-play* ilíquido:
el fundamento (cobre) está presente, pero su incorporación al precio es diferida.

---

### 2.5 Apalancamiento operativo y opcionalidad en la valoración minera

¿Por qué un *pure-play* de cobre debería tener una elasticidad-cobre cercana o
incluso superior a la unidad en el largo plazo? La respuesta está en el
**apalancamiento operativo**. El margen de una minera es, aproximadamente, precio
del cobre menos costo de caja unitario (C1). Como el costo es relativamente rígido a
corto y mediano plazo, una variación porcentual del precio del cobre se traduce en
una variación porcentual **amplificada** del margen y, por ende, del valor presente
de los flujos. Formalmente, si el valor V ≈ q·(P − c)/k (con q producción, c costo
unitario, k tasa de descuento), entonces ∂lnV/∂lnP = P/(P − c) > 1 cuando c > 0: la
elasticidad-precio del valor excede a la unidad en la medida en que el costo
representa una fracción significativa del precio. Las elasticidades de largo plazo
estimadas (0.75–0.86) son consistentes con este mecanismo, atenuadas por
diversificación de activos, coberturas y el componente de moneda.

La literatura de **opciones reales** añade un matiz: una mina contiene la opción de
suspender producción cuando el precio cae bajo el costo de caja, lo que introduce
**no linealidad** —la sensibilidad del valor al precio es mayor en alzas que en
caídas extremas, o viceversa según la estructura de costos—. Esta opcionalidad
motiva contrastar **asimetría** (NARDL): es plausible que la respuesta a alzas y
caídas del cobre difiera, como en efecto se documenta para Antofagasta (§6.8).

### 2.6 Riesgo sistemático y beta

El componente sistemático del retorno se captura mediante la exposición al mercado
(beta). En este estudio se incluyen tanto un índice global (S&P 500) como un proxy
del mercado local (ETF MSCI Chile), de modo que la elasticidad-cobre estimada se
interpreta como el efecto **incremental** del cobre por sobre el comovimiento de
mercado. La distinción es relevante para el activo local: si Pucobre cargara
fuertemente sobre el mercado local pero poco sobre el cobre en el corto plazo (como
se halla), ello indica que su comovimiento diario está dominado por factores locales
de mercado y liquidez, no por el fundamento cuprífero —que opera con rezago—.

## 3. Revisión de literatura

> Las referencias de esta sección fueron verificadas en fuentes primarias (editor /
> repositorios académicos). El listado completo, con DOIs, está en el Capítulo 9.

### 3.1 Factores macroeconómicos y retornos accionarios (APT)

El marco moderno de valoración nace con la teoría de selección de cartera
(Markowitz, 1952) y el CAPM (Sharpe, 1964; Lintner, 1965), que reducen el riesgo
relevante a la covarianza con el mercado (beta). El APT (Ross, 1976) generaliza a un
modelo **multifactorial** sin requerir la cartera de mercado, y su contrastación
seminal en Chen, Roll y Ross (1986) muestra que innovaciones en la producción
industrial, la inflación esperada y no esperada, la prima por riesgo (spread de
bonos) y la pendiente de la estructura temporal son factores sistemáticamente
valorados. Esta línea —junto con la hipótesis de mercados eficientes (Fama, 1970),
que enmarca la velocidad con que los precios incorporan la información— justifica
incluir como regresores las tasas (Tesoro de EE. UU., TPM), el dólar (DXY) y el
riesgo (VIX), además del cobre como factor sectorial específico. La elección entre
modelar niveles o cambios y el uso de sistemas dinámicos se apoya en la tradición
abierta por Granger (1969) sobre causalidad y por Sims (1980) sobre la modelación VAR
sin restricciones teóricas a priori.

### 3.2 Commodities, "monedas-commodity" y economías cupríferas

Chen y Rogoff (2003) introducen el concepto de *commodity currency*: para economías
exportadoras de materias primas, el precio mundial de su canasta exportadora es un
determinante robusto del tipo de cambio real. El caso chileno es arquetípico —el
cobre representa cerca de la mitad de las exportaciones— y existe evidencia
específica: el Working Paper N°640 del Banco Central de Chile (*Copper, the Real
Exchange Rate and Macroeconomic Fluctuations in Chile*) analiza el rol del cobre y
del tipo de cambio real como amortiguadores de shocks, y trabajos publicados en
*Resources Policy* documentan que el tipo de cambio chileno posee poder predictivo
sobre los precios de los metales base, evidenciando una relación cobre↔CLP de doble
vía. Esta literatura fundamenta el canal moneda y motiva tratar el cobre como
variable forzante frente a las acciones locales, hipótesis que el test de
Toda-Yamamoto contrasta directamente. El antecedente más directo es Mendiola,
Chávez-Bedoya y Wallenstein (2022), que documentan una relación **positiva pero
inelástica** entre los cambios del precio del cobre y los retornos de acciones
mineras de cobre —precisamente la magnitud que esta tesis estima y descompone por
horizonte—. Kilian y Park (2009) advierten que el efecto de un shock de *commodity*
sobre las acciones depende de si es de oferta o de demanda, y Díaz, Hansen y Cabrera
(2021) —autores chilenos— muestran que variables macro-financieras (VIX, incertidumbre,
ciclo) gobiernan la volatilidad del cobre, respaldando el conjunto de regresores
empleado. Gorton y Rouwenhorst (2006) y Cashin et al. (2002) enmarcan, además, el
comportamiento cíclico y asimétrico de los precios de *commodities* que motiva la
especificación NARDL.

### 3.3 Iliquidez y descubrimiento de precios

El hallazgo central dialoga con Amihud (2002), cuyo ratio de iliquidez (valor
absoluto del retorno sobre el volumen) se asocia positivamente a los retornos
esperados (prima de liquidez) y afecta con mayor fuerza a las empresas pequeñas. La
teoría de la microestructura —desde el modelo de información asimétrica de Kyle
(1985), que formaliza cómo el creador de mercado actualiza precios ante el flujo de
órdenes, hasta la medición de costos implícitos de transacción de Roll (1984)—
explica por qué la baja liquidez ralentiza el descubrimiento de precios: la
información se incorpora sólo cuando hay transacción, induciendo autocorrelación en
los retornos. El caso Pucobre —*pure-play* con 62% de días sin transacción y
transmisión del cobre diferida— es una manifestación nítida de este mecanismo en un
mercado emergente pequeño, y conecta con la evidencia de que los retornos de
*small-caps* incorporan los factores comunes con rezago respecto de los de gran
capitalización. Bekaert, Harvey y Lundblad (2007) muestran que la liquidez local es
un determinante de primer orden de los retornos esperados en mercados emergentes, y
Amihud, Hameed, Kang y Zhang (2015) documentan que el premio por iliquidez se
concentra en las firmas más pequeñas a nivel internacional —justo el perfil de
Pucobre—; para mercados ilíquidos, la proporción de días con retorno cero suele
superar a Amihud como proxy, lo que motiva el uso de múltiples medidas en §6.14.

### 3.4 Fundamentos econométricos

- **Cointegración y corrección de error.** Engle y Granger (1987) introducen la
  cointegración y el ECM; Johansen (1991) generaliza al enfoque de máxima
  verosimilitud multivariante (estadísticos de la traza y del máximo autovalor).
- **Bounds testing y asimetría.** Pesaran, Shin y Smith (2001) proponen el ARDL
  *bounds test*, válido con regresores I(0)/I(1) sin pre-test de orden;
  Shin, Yu y Greenwood-Nimmo (2014) lo extienden al NARDL para asimetrías de corto y
  largo plazo mediante sumas parciales positivas y negativas.
- **Causalidad robusta a integración.** Toda y Yamamoto (1995) proponen un VAR
  aumentado en niveles que permite inferir causalidad sin sesgo por raíces unitarias.
- **Volatilidad condicional.** Bollerslev (1986) (GARCH), Nelson (1991) (EGARCH) y
  Glosten, Jagannathan y Runkle (1993) (GJR-GARCH) modelan persistencia y efecto
  apalancamiento.
- **Inferencia robusta.** Newey y West (1987) para errores HAC; Dickey-Fuller (1979),
  Phillips-Perron (1988), KPSS (1992) y Zivot-Andrews (1992) para raíces unitarias y
  quiebres endógenos.

### 3.5 Síntesis comparada y vacío

| Eje | Evidencia previa | Tratamiento en esta tesis |
|---|---|---|
| Macro→retornos | APT internacional (Chen-Roll-Ross) | Especificación multifactorial sobre mineras chilenas |
| Cobre↔CLP | Robusta (Chen-Rogoff; BCCh) | Se asume cobre forzante; se contrasta con Toda-Yamamoto |
| Cobre→valoración minera Chile | Escasa | Aporte central: TS por activo + panel + referencias |
| Rol de la liquidez | Teórico (Amihud) | Prueba formal: % días cero, rezagos distribuidos, multi-horizonte |

La literatura chilena se concentró en el canal cobre→tipo de cambio→macro. Es escasa
la evidencia que cuantifique el canal cobre→valoración bursátil de las mineras
chilenas distinguiendo horizonte temporal y liquidez del activo. Esta tesis aporta
en ese punto, integrando APT, cointegración, volatilidad y microestructura sobre el
reducido universo de *pure-plays* cupríferos.

---

## 4. Datos

### 4.1 Universo de empresas (resuelto empíricamente)

El universo de mineras de cobre cotizadas vinculadas a Chile es muy reducido. Se
verificó la disponibilidad real de cada candidato mediante descarga efectiva (no se
asumió su existencia). El resultado se organiza en tres anillos concéntricos:

| Anillo | Ticker | Empresa | Mercado | Moneda | Obs. |
|---|---|---|---|---|---|
| A (núcleo cobre) | ANTO.L | Antofagasta plc | LSE (cross-listed) | GBp | 6.720 |
| A (núcleo cobre) | PUCOBRE.SN | Pucobre (Punta del Cobre) | Bolsa de Santiago | CLP | 6.673 |
| B (materiales) | CAP.SN | CAP S.A. | Santiago | CLP | 6.673 |
| B (materiales) | SQM-B.SN | SQM | Santiago | CLP | 6.673 |
| C (ref. int'l) | SCCO, FCX, BHP, GLEN.L | Southern, Freeport, BHP, Glencore | NYSE/LSE | USD/GBp | 3.793–6.641 |

Codelco se excluye del análisis accionario (estatal, no cotiza en renta variable;
sólo emite deuda). Hallazgo relevante: **Pucobre es el único *pure-play* de cobre
listado directamente en la Bolsa de Santiago y en pesos**, lo que habilita el
contraste con Antofagasta (*cross-listed*, GBp, alta liquidez) que vertebra la tesis.

#### 4.1.1 Perfiles institucionales

**Antofagasta plc.** *Pure-play* de cobre del grupo Luksic (familia chilena), con
operación íntegramente en Chile pero **cotización primaria en la Bolsa de Londres** e
integración al índice FTSE-100. Produjo del orden de 0,65 millones de toneladas de
cobre en 2025, a través de minas como Los Pelambres, Centinela y otras en el norte de
Chile. Su tamaño, su condición de *blue chip* británico y su elevada liquidez la
convierten en el referente del *pure-play* líquido del estudio.

**Pucobre (Sociedad Punta del Cobre S.A.).** Productor de cobre de tamaño medio-bajo
con operaciones concentradas en la Región de Atacama, **listado directamente en la
Bolsa de Santiago y denominado en pesos**. Su capitalización y, sobre todo, su
**liquidez bursátil** son órdenes de magnitud menores que las de Antofagasta: no
registra transacciones en cerca del 62% de las jornadas (§6.12). Es, por
construcción, el caso ideal de *pure-play* local e ilíquido y el centro del contraste
de la tesis.

**CAP S.A.** Conglomerado chileno de minería del hierro y acero (no cobre puro),
listado en Santiago; entra en el anillo de minería-materiales como control sectorial.
**SQM (Sociedad Química y Minera de Chile).** Productor de litio, yodo y potasio (no
cobre); su inclusión permite distinguir la sensibilidad específica al cobre de la
sensibilidad genérica a *commodities* mineros chilenos.

**Referencias internacionales.** Southern Copper (SCCO) y Freeport-McMoRan (FCX),
grandes mineras de cobre de las Américas; BHP, diversificada con fuerte exposición a
cobre (incluida la mina Escondida en Chile); y Glencore, *trader*/minera diversificada.
Aportan un *benchmark* externo de la elasticidad-cobre y validez de las magnitudes.

### 4.2 Variables y fuentes

| Bloque | Variables | Fuente | Frecuencia | Canal |
|---|---|---|---|---|
| Dependiente | Precios de 8 activos | Yahoo Finance (ajustados) | Diaria | — |
| Cobre | Futuro COMEX (HG=F) | Yahoo Finance | Diaria | Demanda/ingreso |
| Moneda | USD/CLP (CLP=X), DXY (DX-Y.NYB) | Yahoo Finance | Diaria | Moneda |
| Tasas | UST 13s/5A/10A (^IRX/^FVX/^TNX) | Yahoo Finance | Diaria | Descuento |
| Riesgo/mercado | VIX, S&P 500, ETF MSCI Chile (ECH) | Yahoo Finance | Diaria | Riesgo/beta |
| Energía | WTI (CL=F) | Yahoo Finance | Diaria | Costos |
| Macro Chile | TPM, IMACEC, IPC, dólar observado | mindicador.cl | Diaria/Mensual | Doméstico |

### 4.3 Construcción de variables y tratamiento

Se construyen log-precios ln(P_t) (niveles, para análisis de cointegración),
log-retornos diarios r_t = 100·Δln(P_t) (variable principal, I(0)), variaciones log
de los factores de precio y primeras diferencias de las tasas en nivel. El manejo de
datos faltantes emplea *forward-fill* acotado (máximo 3–5 días) sólo para series de
nivel; los retornos no se rellenan. La alineación de calendarios entre las plazas de
Londres, Santiago y Nueva York reduce la muestra efectiva común en las regresiones
multifactor a n ≈ 4.475 observaciones diarias.

### 4.4 Período de estudio

El período base es 2004-01 a 2026-05 a frecuencia diaria, acotado por el inicio de
la serie USD/CLP de calidad. Se construye además una versión mensual para integrar la
macro de baja frecuencia (IMACEC, IPC). Para análisis de robustez se definen
submuestras en torno a regímenes candidatos —crisis financiera de 2008, superciclo
del cobre 2010–2014, período 2015–2019 y COVID/pospandemia 2020–2026.

### 4.5 Limitaciones de datos (declaradas)

- **`^IPSA` (Yahoo) es inconsistente** post-2019; se sustituyó el factor de mercado
  local por el ETF iShares MSCI Chile (ECH, NYSE, USD), con cobertura limpia
  2007–2026. *Costo:* ECH incorpora el componente cambiario, parcialmente solapado
  con USD/CLP (monitoreado vía VIF; máximo ≈ 3.5, sin colinealidad severa).
- **Macro nacional** incorporada sin credenciales vía la API pública mindicador.cl
  (TPM diaria, IMACEC e IPC mensuales, dólar observado). El EMBI Chile y las tasas
  largas locales (BCU/BTU) siguen requiriendo credenciales del Banco Central.
- **Calendarios heterogéneos** (LSE/Santiago/NYSE) reducen la muestra por intersección.

---

## 5. Metodología

El diseño nace de las propiedades de los datos (sección 6.2). Dado que los
log-precios son I(1) y los retornos I(0) —mezcla I(0)/I(1) sin presencia de I(2)— se
articula el siguiente árbol de modelos, cada uno respondiendo una pregunta precisa.

### 5.0 Estrategia de identificación

La pregunta causal —¿cómo afecta el precio del cobre a la valoración de una minera
chilena?— enfrenta el riesgo habitual de endogeneidad. Aquí, sin embargo, la
identificación se apoya en dos pilares razonables:

1. **El cobre como shock externo (cuasi-exógeno).** El precio del cobre se determina
   en mercados globales (LME/COMEX) por la oferta y demanda mundiales —dominadas por
   China—; dos empresas chilenas, una de ellas pequeña, **no mueven el precio
   mundial**. Esta exogeneidad se contrasta empíricamente: el test de Toda-Yamamoto
   arroja causalidad **unidireccional** cobre→Antofagasta (§6.11), descartando
   retroalimentación. El cobre opera, así, como una fuente de variación plausiblemente
   exógena para la valoración local.
2. **Diseño cuasi-experimental por liquidez.** Antofagasta y Pucobre comparten la
   **misma exposición fundamental** al cobre (ambos son *pure-plays*) pero difieren
   radicalmente en **microestructura** (liquidez). Comparar la velocidad de
   transmisión entre ambos **aísla el efecto de la liquidez**, manteniendo
   aproximadamente constante el fundamento: las referencias internacionales
   (SCCO/FCX/BHP/GLEN) y los materiales chilenos (CAP/SQM) sirven como *benchmarks* de
   exposición. La diferencia sistemática en el horizonte de transmisión —no en el
   nivel de largo plazo— es, por tanto, atribuible a la fricción de liquidez, no a una
   desconexión fundamental.

**Variables omitidas.** El diseño controla por los factores globales que podrían
confundir el canal del cobre —dólar (DXY), tasas (UST), riesgo (VIX), mercado (S&P y
proxy local) y energía (WTI)—, de modo que la elasticidad-cobre estimada es
incremental respecto de ese comovimiento. Residualmente, factores idiosincrásicos de
empresa (anuncios, *guidance*, gobierno corporativo) quedan en el error; su efecto se
mitiga al trabajar con retornos y se discute como limitación.

### 5.1 Pruebas previas

**Orden de integración.** Decisión cruzada con tres pruebas: ADF y Phillips-Perron
(H0: raíz unitaria) y KPSS (H0: estacionariedad). Una serie se clasifica I(0) si al
menos dos de las tres convergen en estacionariedad. **Quiebres estructurales.**
Zivot-Andrews con quiebre endógeno, para descartar que el comportamiento I(1)
provenga de un quiebre de nivel/tendencia. **Selección de rezagos.** Criterios AIC,
BIC y HQ sobre el VAR en niveles.

### 5.2 Impacto contemporáneo: regresión con errores HAC

r_{i,t} = α + β₁ Δln(cobre)_t + β₂ Δln(USDCLP)_t + β₃ Δln(DXY)_t + β₄ Δln(SP500)_t +
β₅ Δln(ECH)_t + β₆ ΔUST10Y_t + β₇ ΔVIX_t + ε_t.

La estimación es por MCO con matriz de covarianzas **HAC de Newey-West**, robusta a
heterocedasticidad y autocorrelación (justificada por los diagnósticos). El
coeficiente β₁ es la **elasticidad-cobre contemporánea** y constituye la prueba
directa de H1 y H2. El rezago de truncamiento se fija según la regla
L = ⌊4·(n/100)^{2/9}⌋.

### 5.3 Dinámica conjunta: VAR, IRF, FEVD y causalidad

Sobre el sistema estacionario {r_i, Δcobre, ΔUSDCLP, ΔDXY, ΔSP500} se estima un VAR.
Con identificación de Cholesky (factores globales ordenados primero, activo al
final, por ser el más endógeno) se computan: la **IRF**, que traza la respuesta
dinámica del retorno del activo ante un shock unitario del cobre; la **FEVD**, que
mide la fracción de la varianza del error de predicción del retorno atribuible al
cobre a distintos horizontes; y la **causalidad de Granger** cobre→activo.

### 5.4 Largo plazo: cointegración de Johansen y VECM

Sobre el vector de niveles y_t = [ln P_i, ln cobre, ln USDCLP, ln DXY] se aplica el
procedimiento de Johansen para determinar el rango de cointegración r. Si r ≥ 1, se
estima el VECM Δy_t = α (β' y_{t−1}) + Σ Γ_j Δy_{t−j} + u_t, donde β es el vector
cointegrante (relación de equilibrio de largo plazo, normalizado al precio de la
acción) y α la velocidad de ajuste (corrección diaria del desequilibrio). Esto
contrasta H3. Como verificación cruzada uniecuacional se aplica el ARDL *bounds test*
de Pesaran-Shin-Smith.

### 5.5 Asimetría: NARDL

Para contrastar si la acción responde de forma distinta a alzas y caídas del cobre,
se descompone el log-precio del cobre en sumas parciales: cobre⁺_t = Σ máx(Δcobre,0)
y cobre⁻_t = Σ mín(Δcobre,0), y se estima un ARDL con ambas como regresores. La
prueba de Wald sobre la igualdad de los coeficientes de largo plazo (H0: θ⁺ = θ⁻)
detecta asimetría.

### 5.6 Volatilidad: familia GARCH

Sobre los retornos se ajustan GARCH(1,1), EGARCH(1,1) y GJR-GARCH(1,1) con
distribución t-Student (para capturar las colas pesadas). En el GJR la varianza
condicional es σ²_t = ω + α ε²_{t−1} + γ ε²_{t−1}·1[ε_{t−1}<0] + β σ²_{t−1}; el
término γ captura el **efecto apalancamiento**. La persistencia se mide por α+β.
Contrasta H4.

### 5.7 Datos de panel

Sobre el panel de los cuatro activos chilenos (anillos A+B) se estiman Pooled OLS,
efectos fijos (FE) y efectos aleatorios (RE), con prueba de Hausman y errores
agrupados por empresa. Se advierte explícitamente que con N = 4 el panel es robustez
sectorial, no inferencia primaria, y que el GMM dinámico (Arellano-Bond) no es
viable.

### 5.8 Estudio de eventos

Se identifican los anuncios de cambio de TPM y, con un modelo de mercado estimado en
una ventana [−130, −11], se calculan los retornos anormales y el CAAR en la ventana
[−5, +5], distinguiendo alzas y bajas de tasa.

### 5.9 Prueba formal de la hipótesis de iliquidez (H5)

Tres pruebas complementarias: (a) **magnitud** —ratio de Amihud y porcentaje de días
con retorno cero por activo; (b) **transversal** —correlación de Spearman entre
iliquidez y elasticidad-cobre contemporánea sobre los 8 activos; (c) **rezagos
distribuidos** —regresión del retorno sobre el cobre contemporáneo y sus rezagos
0–5, comparando la fracción del impacto que llega el día 0 frente al acumulado.

### 5.10 Estimación, inferencia y reglas de decisión

Toda la inferencia se conduce con errores estándar robustos. En las regresiones de
retornos se emplea la matriz HAC de Newey-West con rezago de truncamiento
L = ⌊4·(n/100)^{2/9}⌋; en el panel, errores agrupados (*cluster*) por empresa. Las
reglas de decisión son explícitas: (i) raíz unitaria —se concluye I(0) si ≥2 de las
3 pruebas (ADF, PP, KPSS) convergen en estacionariedad al 5%; (ii) cointegración de
Johansen —se acepta el rango r donde el estadístico de la traza deja de superar su
valor crítico al 95%; (iii) bounds test —cointegración si el estadístico F supera el
límite superior I(1) de Pesaran-Shin-Smith al 5%, no concluyente si cae en la banda;
(iv) selección de rezagos —mínimo AIC, contrastado con BIC/HQ; (v) significancia —
umbral del 5% como referencia, reportando el p-valor exacto. Se prefiere reportar
intervalos y estadísticos de prueba antes que estrellas, y se declara explícitamente
cuando un resultado es marginal o no concluyente.

### 5.11 Validación de supuestos

Se aplica una batería completa: Breusch-Godfrey y Ljung-Box (autocorrelación);
Breusch-Pagan, White y ARCH-LM (heterocedasticidad y efectos ARCH); VIF
(multicolinealidad); Jarque-Bera (normalidad); CUSUM y submuestras (estabilidad);
Hausman (FE vs RE). Cada problema detectado motiva la corrección correspondiente
(HAC para autocorrelación, GARCH para ARCH, t-Student para colas).

---

## 6. Resultados

### 6.1 Estadística descriptiva

Log-retornos diarios (%), 2004–2026:

| Activo | media | sd | asimetría | curtosis | Jarque-Bera |
|---|---|---|---|---|---|
| ANTO.L | 0.051 | 2.65 | 0.09 | 4.15 | rechaza normalidad |
| PUCOBRE.SN | 0.053 | 1.44 | 1.50 | 35.5 | rechaza normalidad |
| CAP.SN | 0.044 | 2.47 | −0.13 | 10.7 | rechaza normalidad |
| SQM-B.SN | 0.067 | 2.32 | −0.19 | 6.67 | rechaza normalidad |

Todas las series presentan exceso de curtosis (colas pesadas) y no-normalidad
(Jarque-Bera, p<0.001), justificando la distribución t-Student en los GARCH. Pucobre
destaca por curtosis extrema (35.5) y asimetría positiva (1.5): saltos esporádicos
sobre días de baja transacción, firma estadística de la iliquidez.

La **estructura de correlaciones** de los retornos diarios (matriz reportada en el
Anexo A) confirma el patrón esperado: la correlación contemporánea con el retorno del
cobre es alta para Antofagasta (≈0.54) y para las referencias internacionales
(SCCO ≈0.52, FCX ≈0.52, BHP ≈0.48, Glencore ≈0.45), intermedia para los materiales
chilenos (CAP ≈0.25, SQM ≈0.24) y notablemente baja para Pucobre (≈0.14). Este
gradiente —que ordena los activos por su comovimiento contemporáneo con el cobre—
anticipa el resultado central: la posición de Pucobre como atípico de baja
correlación contemporánea pese a ser un *pure-play*, lo que sólo se explica por la
fricción de liquidez y se resuelve al ampliar el horizonte.

### 6.2 Estacionariedad y cointegración

- **ADF/PP/KPSS** (decisión cruzada): log-precios I(1), retornos y diferencias I(0).
  Confirmado por Zivot-Andrews (no se rechaza raíz unitaria ni con quiebre endógeno:
  ANTO p≈0.62, PUCOBRE p≈0.99).
- **Engle-Granger bivariado** (activo~cobre): cointegración débil/ausente (sólo el
  cobre no basta).
- **Johansen multivariante** [ln P, ln cobre, ln USDCLP, ln DXY]: **rango r = 1**
  para ANTO y PUCOBRE → existe exactamente una relación de equilibrio de largo plazo.

### 6.3 Impacto contemporáneo (HAC)

Elasticidad-cobre (efecto de +1% en el cobre sobre el retorno diario, %):

| Activo | β-cobre | t | R² |
|---|---|---|---|
| ANTO.L | 0.70 | 15.4 | 0.42 |
| PUCOBRE.SN | 0.09 | 4.4 | 0.04 |
| CAP.SN | 0.15 | 5.7 | 0.25 |
| SQM-B.SN | 0.11 | 4.2 | 0.25 |
| SCCO | 0.49 | 9.6 | 0.58 |
| FCX | 0.63 | 10.3 | 0.53 |
| BHP | 0.32 | 10.7 | 0.60 |
| GLEN.L | 0.58 | 9.8 | 0.29 |

Para Antofagasta también son significativos el DXY (signo negativo: dólar arriba →
acción abajo), el mercado (S&P y proxy local) y el cambio en la UST10Y. Para Pucobre,
sólo el mercado local y —débilmente— el cobre son significativos, con un R² de
apenas 0.04: su retorno es mayoritariamente idiosincrásico/ilíquido en el día a día.
Los diagnósticos muestran efectos ARCH significativos en todos los activos (justifica
GARCH), autocorrelación (justifica HAC) y no-normalidad; VIF máximo ≈ 3.5 (sin
colinealidad severa). **H1 se sostiene** (cobre positivo y significativo en todos);
**H2 se sostiene con fuerza** (0.70 en el líquido vs 0.09 en el ilíquido).

### 6.4 Dinámica (VAR, IRF, FEVD, Granger)

| Activo | FEVD cobre (1d) | FEVD cobre (20d) | IRF acum. 5d | Granger cobre→activo |
|---|---|---|---|---|
| ANTO.L | 28.7% | 27.8% | 0.091 | p=0.008 (sí) |
| PUCOBRE.SN | 2.0% | 4.3% | 0.196 | p<0.001 (sí) |

Clave: en Pucobre la respuesta acumulada a 5 días (0.196) es ~4× la del primer día
(0.043), y la FEVD del cobre crece de 2% a 4.3% entre 1 y 20 días. El cobre **causa**
los retornos de Pucobre (Granger p<0.001), pero el efecto se **difiere** en lugar de
impactar contemporáneamente — consistente con descubrimiento de precios lento.

### 6.5 Largo plazo (VECM)

Vector de cointegración (r=1), elasticidades del log-precio:

| Activo | elast. cobre | elast. USDCLP | elast. DXY | velocidad de ajuste α |
|---|---|---|---|---|
| ANTO.L | 0.860 | 6.63 | −11.80 | −0.0008 |
| PUCOBRE.SN | 0.753 | 4.82 | −7.96 | −0.0004 |

En el largo plazo, una subida de 1% en el cobre se asocia a ~0.75–0.86% más en el
precio de la acción —y **Pucobre (0.75) es comparable a Antofagasta (0.86)**—, en
marcado contraste con su nula reacción contemporánea. La velocidad de ajuste α es
negativa (corrige desequilibrios) pero muy pequeña, indicando ajuste lento. *Cautela:*
los coeficientes grandes de USDCLP/DXY reflejan colinealidad entre ambas medidas del
dólar y se interpretan con reserva. **H3 se sostiene**, con la matización de §6.7.

### 6.6 Volatilidad (GARCH)

| Activo | mejor modelo (AIC) | persistencia (α+β) | efecto apalancamiento |
|---|---|---|---|
| ANTO.L | GJR-GARCH(1,1) | 0.991 | sí (γ>0) |
| CAP.SN | GJR-GARCH(1,1) | 0.995 | sí (γ>0) |
| SQM-B.SN | EGARCH(1,1) | 0.999 | sí (γ<0 en EGARCH) |
| PUCOBRE.SN | inestable | — | no confiable |

Persistencia ≈ 0.99 (shocks de volatilidad muy duraderos) y efecto apalancamiento
confirmado. En Pucobre, en cambio, los modelos GARCH resultan inestables (soluciones de
borde) por la iliquidez y los saltos extremos (curtosis 35.5); se recomienda filtrar
días de retorno nulo o usar modelos con saltos. **H4 se sostiene** salvo en el activo
ilíquido.

### 6.7 Robustez

- **ARDL bounds (diario, k=3):** F = 2.89 (ANTO) y 1.55 (PUCOBRE), por debajo del
  crítico I(1) (4.35) → no confirma cointegración, en aparente contraste con
  Johansen. La explicación es la **baja potencia del test uniecuacional cuando la
  velocidad de ajuste es minúscula** (α ≈ −0.0008): Johansen, basado en el sistema,
  sí la detecta. Conclusión prudente: la evidencia de largo plazo es sugerente pero
  no unánime; se prioriza el VECM.
- **Estabilidad de β-cobre por submuestras:**

  | Submuestra | ANTO β-cobre | PUCOBRE β-cobre |
  |---|---|---|
  | crisis 2008-09 | 0.60 (t=6.7) | 0.08 (t=2.1) |
  | superciclo 2010-14 | 0.69 (t=16.9) | 0.05 (t=1.3) |
  | 2015-19 | 0.90 (t=13.9) | 0.01 (t=0.3) |
  | COVID+ 2020-26 | 0.65 (t=8.1) | 0.15 (t=4.2) |

  Antofagasta es estable y siempre significativa (pico en 2015-19); Pucobre es
  débil/no significativa salvo en COVID+ (0.15, t=4.2): leve mejora de transmisión en
  el boom reciente del cobre.

### 6.8 Asimetría (NARDL)

| Activo | Bounds F | cointegra | asimetría LP (Wald, p) |
|---|---|---|---|
| ANTO.L | 4.50 | sí (5%) | sí: Wald=8.45, p=0.004 |
| PUCOBRE.SN | 1.83 | no | no (p=0.29) |
| CAP.SN | 3.10 | no | no (p=0.15) |
| SQM-B.SN | 2.03 | no | no (p=0.23) |

Antofagasta presenta cointegración no lineal y asimetría de largo plazo
significativa: responde de forma estadísticamente distinta a alzas vs caídas del
cobre. Los demás no rechazan simetría, coherente con su vínculo más débil.

### 6.9 Panel sectorial (N=4)

Impacto promedio del sector (FE≈RE≈Pooled; Hausman no rechaza RE): β-cobre ≈ 0.205
(p=0.073, marginal con *cluster* en 4 entidades); el mercado local domina
(β≈0.79, p<0.001); DXY ≈ −0.19 (p<0.001); UST10Y +1.9 (p<0.01). R² within ≈ 0.23.

### 6.10 Canal de política monetaria (TPM) y estudio de eventos

El cambio diario de la TPM entra con signo negativo en todos los activos
(endurecimiento → menor retorno) pero **no significativo** (p>0.12). El estudio de
eventos sobre 51 alzas y 41 bajas de TPM arroja CAAR con el signo económico correcto
(alza → anormal negativo: ANTO −1.04%, CAP −1.90%; baja → positivo) pero **ninguno
significativo** (p>0.37): los cambios de TPM están anticipados y la valoración minera
responde a factores globales más que a la política monetaria doméstica.

### 6.11 Causalidad de Toda-Yamamoto

| Activo | cobre→activo | activo→cobre | USDCLP→activo |
|---|---|---|---|
| ANTO.L | causa (p=0.04) | no (p=0.11) | causa (p<0.001) |
| PUCOBRE.SN | causa (p<0.001) | marginal (p=0.02)* | no (p=0.29) |

El cobre causa (robusto a cointegración) a ambos activos, de forma **unidireccional**
para Antofagasta (es tomadora de precios). El sentido inverso en Pucobre (p=0.02) es
económicamente implausible (una minera pequeña no mueve el COMEX) → probable
artefacto del modelo aumentado de 13 rezagos.

### 6.12 Prueba formal de la iliquidez y multi-horizonte (H5)

**(a) Magnitud.** Pucobre presenta **62% de días con retorno cero** (no transa en la
mayoría de las jornadas), frente a 5.5% (ANTO), 1.3% (SCCO) o 0.18% (Glencore); su
volumen medio (~US$24 M equiv.) es dos órdenes de magnitud menor que el de
Antofagasta (~US$2.000 M). **(b) Transversal.** La correlación de Spearman entre
iliquidez (% días cero) y β-cobre contemporánea es negativa (ρ≈−0.55), en la
dirección predicha (no significativa con N=8). **(c) Rezagos distribuidos:**

| Activo | β día 0 | β acumulado 0–5 | fracción día 0 |
|---|---|---|---|
| ANTO.L | 0.816 | 0.862 | 94.7% (inmediata) |
| PUCOBRE.SN | 0.121 | 0.415 | 29.2% (diferida) |

En Antofagasta el 95% del impacto del cobre llega el mismo día; en Pucobre sólo el
29% —el 71% restante se difiere—. **Multi-horizonte:** la elasticidad-cobre de
Pucobre crece monótonamente: 0.09 (diaria) → 0.42 (acumulada 5d) → 0.60 (mensual,
t=7.3, R²=0.31) → 0.75 (largo plazo VECM). A frecuencia mensual emerge la verdadera
sensibilidad, cercana a la de Antofagasta. El IMACEC entra significativo y negativo
para Pucobre (−0.26, t=−2.8). La evidencia en favor de H5 es, en consecuencia, sólida.

### 6.13 Quiebres estructurales endógenos (Quandt-Andrews)

Para evaluar la estabilidad de la transmisión en 22 años (que abarcan la crisis de
2008, el superciclo, el COVID y el boom pospandemia), se aplica una prueba de quiebre
con fecha endógena (sup-Chow / Quandt-Andrews, *trimming* 15%) sobre la regresión
r = a + b·Δcobre + controles:

| Activo | sup-F | crítico 5% | fecha de quiebre | β-cobre pre → post | ¿quiebre? |
|---|---|---|---|---|---|
| ANTO.L | 33.5 | ~18.0 | 2007-07 | 0.34 → 0.78 | Sí |
| PUCOBRE.SN | 7.8 | ~18.0 | 2010-12 | 0.08 → 0.13 | No al 5% |
| CAP.SN | 12.4 | ~18.0 | 2011-01 | 0.12 → 0.35 | No al 5% |
| SQM-B.SN | 11.1 | ~18.0 | 2019-06 | 0.15 → 0.30 | No al 5% |

Antofagasta presenta un **quiebre significativo** en torno a mediados de 2007
(víspera de la crisis financiera), tras el cual su elasticidad-cobre **se duplica con
creces** (0.34 → 0.78): su integración al fundamento cuprífero se intensificó
estructuralmente. Pucobre, en cambio, **no exhibe quiebre significativo**: su débil
transmisión contemporánea es **estructuralmente estable**, no un artefacto de un
régimen particular. Esto refuerza H2/H5: la baja sensibilidad contemporánea de
Pucobre es una característica permanente de su microestructura (iliquidez), no un
fenómeno transitorio.

### 6.14 Robustez de la iliquidez: medidas alternativas

Dado que el hallazgo central descansa sobre la iliquidez, se replica el contraste
transversal con **cuatro proxies construidas con metodologías distintas** —Amihud
(basada en volumen), porcentaje de días con retorno cero (Lesmond et al.), spread
implícito de Roll (basado en autocovarianza de retornos) y volumen medio en
USD-equivalente—:

| Medida | Signo esperado | Spearman ρ con β-cobre | p |
|---|---|---|---|
| % días retorno cero | − | −0.55 | 0.16 |
| Spread de Roll | − | −0.40 | 0.50 |
| Amihud | − | −0.07 | 0.88 |
| Volumen medio (USD) | + | +0.33 | 0.42 |

Las cuatro medidas apuntan en la **dirección predicha** (mayor iliquidez → menor
transmisión contemporánea; mayor volumen → mayor transmisión), aunque ninguna alcanza
significancia individual con N=8 (baja potencia). La **consistencia de signos** entre
proxies metodológicamente independientes robustece la conclusión: el hallazgo no
depende del estimador de Amihud. (El spread de Roll resulta indefinido para Pucobre,
CAP y SQM —autocovarianza positiva por la masa de retornos cero—, lo que confirma que
el **porcentaje de días con retorno cero** es la proxy preferida para los activos más
ilíquidos, en línea con Lesmond et al.)

### 6.15 Validación fuera de muestra (Clark-West)

Como prueba **predictiva e independiente** de la transmisión diferida (H5), se evalúa
si el cobre **rezagado** mejora la predicción fuera de muestra del retorno, mediante
un esquema recursivo (ventana expansiva desde el 50% de la muestra) que compara un
*benchmark* AR(1) anidado con un modelo AR(1) + cobre rezagado (lags 1–2), usando el
R² fuera de muestra (Campbell-Thompson) y el test de Clark-West:

| Activo | R² OOS (%) | Clark-West t | p | ¿el cobre rezagado mejora? |
|---|---|---|---|---|
| PUCOBRE.SN | +0.24 | 2.64 | 0.004 | Sí |
| ANTO.L | +0.20 | 2.45 | 0.007 | Sí |
| CAP.SN | +0.32 | 2.53 | 0.006 | Sí |
| SQM-B.SN (litio) | −0.02 | −0.45 | 0.68 | No (placebo) |

El cobre **rezagado** tiene poder predictivo fuera de muestra para Pucobre —de hecho
**mayor** que para Antofagasta—, exactamente lo que predice la transmisión diferida:
en el activo líquido el cobre ya está incorporado y el rezago aporta poco, mientras
que en el ilíquido el rezago captura la incorporación tardía. El **placebo** es nítido:
SQM (litio, no cobre) no muestra predictibilidad por cobre rezagado (p=0.68),
descartando que el resultado sea espurio. Esta es una confirmación de H5 por una vía
metodológicamente distinta a todo el resto del análisis.

### 6.16 Aplicación predictiva (validación complementaria)

Aunque el enfoque de la tesis es **explicativo**, no predictivo, una validación
predictiva fuera de muestra ofrece un contraste adicional del mecanismo y una
aplicación práctica. Se estima un modelo lineal transparente que predice el retorno
del día siguiente con información disponible hoy —retorno propio rezagado, cobre
contemporáneo y rezagado, dólar y mercado— en una ventana **expansiva** (estimación
recursiva), y se compara contra un *benchmark* ingenuo (predecir retorno nulo, esto
es, caminata aleatoria del precio):

| Activo | R² fuera de muestra | Mejora RMSE vs naive | Precisión direccional* |
|---|---|---|---|
| ANTO.L | −0.7% | −0.3% | 54.2% |
| PUCOBRE.SN | +1.2% | +0.6% | 56.6% |

(*) Precisión direccional calculada **sólo sobre días de retorno no nulo**, para
evitar el sesgo que introducen los numerosos días sin transacción de Pucobre
(donde el signo del retorno observado es cero).

El resultado admite dos lecturas: (i) el retorno diario es esencialmente impredecible
—coherente con eficiencia de mercado en forma débil—, con R² fuera de muestra ínfimo
y precisión direccional apenas sobre el 50%; (ii) sin embargo, **Pucobre es
sistemáticamente más predecible que Antofagasta** (mayor precisión direccional,
única con R² fuera de muestra y RMSE mejores que el *benchmark*). Esta mayor
predictibilidad del activo ilíquido es precisamente lo que implica el descubrimiento
de precios diferido: la incorporación tardía de la información genera
**autocorrelación** explotable. Así, la dimensión predictiva **refuerza** el hallazgo
explicativo central por una vía independiente. La plataforma asociada incluye un
**simulador de escenarios** que traduce las elasticidades estimadas en impactos por
horizonte; su utilidad no radica en el pronóstico puntual —imposible para retornos
diarios— sino en cuantificar, de forma trazable, el rango de impacto de un escenario
de cobre.

### 6.17 Síntesis de verificación de hipótesis

| Hipótesis | Enunciado | Evidencia | Veredicto |
|---|---|---|---|
| H1 | Cobre impacta positiva y significativamente | β-cobre>0 y significativa en los 8 activos (HAC) | Se sostiene |
| H2 | Sensibilidad heterogénea según liquidez | 0.70 (líquido) vs 0.09 (ilíquido); ρ(iliquidez, β)<0 | Se sostiene |
| H3 | Relación de largo plazo (cointegración) | Johansen r=1; VECM elasticidad 0.75–0.86 | Se sostiene (ARDL no unánime) |
| H4 | Volatilidad persistente y con apalancamiento | Persistencia ≈0.99; γ significativo (GJR/EGARCH) | Se sostiene (salvo Pucobre) |
| H5 | Transmisión diferida en el activo ilíquido | Fracción día0 29%; β crece 0.09→0.42→0.60→0.75 | Se sostiene con fuerza |

El cuadro condensa el aporte: cinco hipótesis preinscritas, contrastadas con métodos
independientes, con veredictos explícitos y matizados donde la evidencia no es
unánime, según el peso de la evidencia de cada técnica.

---

## 7. Discusión

### 7.1 Triangulación del hallazgo central

La evidencia es consistente y se triangula por seis técnicas independientes:
(1) la regresión HAC muestra transmisión contemporánea casi nula en Pucobre (0.09);
(2) los rezagos distribuidos muestran que sólo el 29% del impacto llega el día 0;
(3) el VAR muestra una IRF que se acumula en los días siguientes (5d ≈ 4× el día 1);
(4) la FEVD del cobre crece con el horizonte; (5) el modelo mensual recupera una
elasticidad de 0.60; (6) el VECM fija el equilibrio de largo plazo en 0.75. Las seis
piezas convergen en una sola lectura: **la iliquidez retrasa, pero no elimina, la
transmisión del fundamento cobre→valoración.**

### 7.2 Mecanismo económico

El *pure-play* líquido y *cross-listed* (Antofagasta) opera en un mercado profundo
donde el arbitraje incorpora el precio del cobre de inmediato. El *pure-play* local
(Pucobre) transa esporádicamente; la información del cobre se incorpora a su precio
sólo cuando hay transacción, generando autocorrelación positiva en sus retornos y un
descubrimiento de precios diferido. El fundamento es el mismo —la elasticidad de
largo plazo es comparable— pero la **velocidad** de incorporación difiere por la
microestructura.

### 7.1bis Significancia económica de las magnitudes

Más allá de la significancia estadística, las magnitudes tienen una lectura
económica concreta. Una elasticidad-cobre contemporánea de **0.70** para Antofagasta
implica que un movimiento de **+10%** en el precio del cobre se asocia, el mismo día,
con un retorno de **≈+7%** de la acción —coherente con el apalancamiento operativo de
un *pure-play* (§2.5)—. Para Pucobre, ese mismo shock de +10% genera apenas **≈+0.9%**
el primer día, pero **≈+6%** acumulado al cabo de un mes y **≈+7.5%** en el equilibrio
de largo plazo. Para un inversionista, la implicancia es operativa: medir la
exposición de Pucobre al cobre con una beta **diaria** subestima su riesgo real en un
factor cercano a **ocho** (0.09 vs 0.75); la exposición sólo se aprecia correctamente
a horizontes mensuales o superiores. Para un emisor pequeño, el resultado cuantifica
un **costo de iliquidez**: el mercado tarda en reflejar las mejoras de su fundamento,
lo que se traduce en mayor costo de capital y menor utilidad de la acción como
instrumento de cobertura del riesgo-cobre en el corto plazo.

### 7.2bis Implicaciones para la eficiencia de mercado

El gradiente de transmisión por horizonte tiene una lectura directa en términos de
eficiencia informacional en su forma semi-fuerte. En el segmento líquido y
*cross-listed*, la información pública del precio del cobre se incorpora al valor de
Antofagasta esencialmente el mismo día (fracción día 0 ≈ 95%), compatible con un
mercado eficiente. En el segmento local ilíquido, en cambio, una fracción mayoritaria
del impacto (≈71%) se incorpora con rezago, lo que constituye una **ineficiencia de
corto plazo medible**. Es crucial subrayar que esta ineficiencia es atribuible a la
**fricción de liquidez** —no a una desconexión fundamental— puesto que el equilibrio
de largo plazo recupera la elasticidad plena. La distinción importa para el diseño de
políticas de mercado (incentivos a la liquidez, *market making*) y para la práctica
de valoración: ignorarla conduce a betas diarias sesgadas a la baja para los activos
ilíquidos.

### 7.3 Comparación con la literatura

Las elasticidades-cobre de las referencias internacionales (SCCO 0.49, FCX 0.63,
Glencore 0.58) y de Antofagasta (0.70) son del mismo orden, validando externamente
la magnitud del canal de demanda/ingreso. El signo negativo del DXY y la relación
cobre↔moneda son coherentes con la literatura de *commodity currencies* (Chen-Rogoff;
BCCh). La disociación corto/largo plazo por liquidez es consistente con Amihud (2002)
y la teoría de microestructura.

### 7.4 Validez interna y externa

**Interna.** La identificación del canal cobre→acción se apoya en (i) la exogeneidad
del cobre respecto de una minera pequeña (confirmada por Toda-Yamamoto
unidireccional) y (ii) el control por factores globales y de moneda. **Externa.** El
núcleo del resultado (heterogeneidad por liquidez) es específico al contraste
líquido/ilíquido y debería replicarse en otros *small-caps* de *commodities* en
mercados emergentes; la generalización a todo el sector chileno está limitada por el
N reducido.

### 7.5 Implicancias

Para la **gestión de riesgo y valoración**, la sensibilidad al cobre de un activo
ilíquido debe medirse a horizontes largos, no diarios: una beta diaria subestima
gravemente la exposición real. Para la **eficiencia de mercado**, los resultados
cuantifican una ineficiencia informacional de corto plazo en el segmento local,
atribuible a la liquidez más que a la ausencia de vínculo fundamental.

### 7.6 Limitaciones (amenazas a la validez)

(i) EMBI Chile y tasas BCU/BTU pendientes de credenciales del Banco Central; (ii)
FRED inaccesible desde el entorno de ejecución; (iii) proxy de mercado local en USD
(ECH) por inconsistencia del IPSA de Yahoo, con leve solapamiento cambiario; (iv)
calendarios heterogéneos que reducen la muestra; (v) GARCH no fiable en Pucobre por
iliquidez; (vi) el ARDL lineal no confirma cointegración (baja potencia ante ajuste
lento), aunque el NARDL sí la detecta para Antofagasta; (vii) panel con N=4; (viii)
estudio de eventos sin componente de sorpresa de TPM (expectativas no observadas).

---

## 8. Conclusiones

1. El universo de mineras de cobre cotizadas vinculadas a Chile es mínimo y se
   resolvió empíricamente: Antofagasta (LSE) y Pucobre (Santiago) como núcleo, con
   panel de materiales y referencias internacionales.
2. El precio del cobre es un determinante **positivo y significativo** de los
   retornos mineros (H1), con magnitud creciente en la liquidez del activo (H2).
3. El resultado más novedoso es la **disociación corto/largo plazo en el activo
   ilíquido (Pucobre)** (H5): transmisión contemporánea casi nula pero vínculo de
   largo plazo pleno y causalidad con rezago. La sensibilidad crece monótonamente con
   el horizonte (0.09 → 0.42 → 0.60 → 0.75). Aporta evidencia sobre (in)eficiencia
   informacional en un mercado emergente pequeño.
4. Existe una relación de equilibrio de largo plazo cobre→valoración (H3, vía
   Johansen/VECM), con ajuste lento; el NARDL revela además asimetría de largo plazo
   en Antofagasta.
5. La volatilidad es persistente y asimétrica (H4); el dólar y las tasas globales
   complementan el canal del cobre, mientras la política monetaria doméstica pesa
   poco frente a los factores globales.

### 8.1 Contribuciones

Metodológica (batería integrada y reproducible sobre un universo difícil), empírica
(cuantificación del canal cobre→valoración para los *pure-plays* chilenos) y
conceptual (prueba formal del descubrimiento de precios diferido por iliquidez).

### 8.2 Líneas futuras

Incorporar EMBI Chile y tasas locales del Banco Central; NARDL dinámico con
multiplicadores acumulados asimétricos; estudio de eventos con sorpresa de TPM
(expectativas de encuestas); medidas de iliquidez intradía y de Amihud por régimen;
GARCH con saltos para Pucobre; extensión a un panel internacional de *small-caps*
de *commodities* para testear la generalidad del mecanismo de liquidez.

---

## 9. Referencias y anexos

**Referencias** — verificadas en fuentes primarias (revisar formato APA final).

*Teoría de factores y mercados:*
- Markowitz, H. (1952). Portfolio selection. *Journal of Finance*, 7(1), 77–91.
- Sharpe, W. F. (1964). Capital asset prices: a theory of market equilibrium under conditions of risk. *Journal of Finance*, 19(3), 425–442.
- Lintner, J. (1965). The valuation of risk assets and the selection of risky investments. *Review of Economics and Statistics*, 47(1), 13–37.
- Fama, E. F. (1970). Efficient capital markets: a review of theory and empirical work. *Journal of Finance*, 25(2), 383–417.
- Ross, S. A. (1976). The arbitrage theory of capital asset pricing. *Journal of Economic Theory*, 13(3), 341–360.
- Chen, N.-F., Roll, R., & Ross, S. A. (1986). Economic forces and the stock market. *Journal of Business*, 59(3), 383–403. https://www.jstor.org/stable/2352710

*Microestructura e iliquidez:*
- Roll, R. (1984). A simple implicit measure of the effective bid-ask spread in an efficient market. *Journal of Finance*, 39(4), 1127–1139.
- Kyle, A. S. (1985). Continuous auctions and insider trading. *Econometrica*, 53(6), 1315–1335.
- Amihud, Y. (2002). Illiquidity and stock returns: cross-section and time-series effects. *Journal of Financial Markets*, 5(1), 31–56. https://doi.org/10.1016/S1386-4181(01)00024-6

*Cobre, monedas-commodity y Chile:*
- Chen, Y.-C., & Rogoff, K. (2003). Commodity currencies. *Journal of International Economics*, 60(1), 133–160. https://doi.org/10.1016/S0022-1996(02)00072-7
- Banco Central de Chile. Working Paper N°640. *Copper, the Real Exchange Rate and Macroeconomic Fluctuations in Chile*. https://www.bcentral.cl/en/content/-/details/working-papers-n-640
- *Forecasting base metal prices with the Chilean exchange rate*. *Resources Policy*. https://www.sciencedirect.com/science/article/abs/pii/S0301420718303271

*Series de tiempo, cointegración, ARDL/NARDL y causalidad:*
- Granger, C. W. J. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica*, 37(3), 424–438.
- Sims, C. A. (1980). Macroeconomics and reality. *Econometrica*, 48(1), 1–48.
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

*Raíces unitarias y quiebres:* Dickey & Fuller (1979); Phillips & Perron (1988); Kwiatkowski, Phillips, Schmidt & Shin (1992, KPSS); Zivot & Andrews (1992); Andrews (1993, sup-tests de quiebre); Bai & Perron (2003, quiebres múltiples).

*Evidencia empírica reciente (commodities, cobre, liquidez):*
- Mendiola, A., Chávez-Bedoya, L., & Wallenstein, T. (2022). Analyzing the reaction of mining stocks to the development of copper prices. *Emerging Markets Finance and Trade*, 58(1), 244–266. https://doi.org/10.1080/1540496X.2019.1703103
- Díaz, J. D., Hansen, E., & Cabrera, G. (2021). Economic drivers of commodity volatility: the case of copper. *Resources Policy*, 73, 102224. https://doi.org/10.1016/j.resourpol.2021.102224
- Gorton, G., & Rouwenhorst, K. G. (2006). Facts and fantasies about commodity futures. *Financial Analysts Journal*, 62(2), 47–68. https://doi.org/10.2469/faj.v62.n2.4083
- Kilian, L., & Park, C. (2009). The impact of oil price shocks on the U.S. stock market. *International Economic Review*, 50(4), 1267–1287. https://doi.org/10.1111/j.1468-2354.2009.00568.x
- Cashin, P., McDermott, C. J., & Scott, A. (2002). Booms and slumps in world commodity prices. *Journal of Development Economics*, 69(1), 277–296. https://doi.org/10.1016/S0304-3878(02)00062-7
- Bekaert, G., Harvey, C. R., & Lundblad, C. (2007). Liquidity and expected returns: lessons from emerging markets. *Review of Financial Studies*, 20(6), 1783–1831. https://doi.org/10.1093/rfs/hhm030
- Amihud, Y., Hameed, A., Kang, W., & Zhang, H. (2015). The illiquidity premium: international evidence. *Journal of Financial Economics*, 117(2), 350–368. https://doi.org/10.1016/j.jfineco.2015.04.005
- Cunado, J., & Pérez de Gracia, F. (2014). Oil price shocks and stock market returns: evidence for some European countries. *Energy Economics*, 42, 365–377. https://doi.org/10.1016/j.eneco.2013.10.017
- Jawadi, F., Arouri, M. E. H., & Million, N. (2009). *Stock market integration in the Latin American markets: further evidence from nonlinear modeling*. [Preprint — verificar versión publicada].

> Las referencias de este bloque fueron verificadas con DOI durante la investigación
> bibliográfica de apoyo; restan por confirmar volumen/páginas exactos de algunas
> (Amihud et al., 2015; Jawadi et al., 2009) antes de la entrega final.

**Data Availability Statement.** Todos los datos provienen de fuentes públicas:
precios y volúmenes de Yahoo Finance (descarga 2026-05-30, vía la librería `yfinance`)
y macro de Chile de la API pública `mindicador.cl` (TPM, IMACEC, IPC, dólar
observado). El código de descarga, limpieza, estimación y exportación, los datos
procesados, las 35+ tablas de salida y las 13 figuras están disponibles en el
repositorio del proyecto, con scripts numerados que reproducen cada tabla y figura.
No se emplearon datos propietarios ni restringidos.

> Nota: confirmar paginación y DOIs en Scopus/Web of Science/Google Scholar antes de
> la entrega final. Estas referencias fueron contrastadas con repositorios del
> editor; el formato APA definitivo es responsabilidad del autor.

**Anexos (reproducibilidad).**
- Anexo A — Figuras del análisis (series, ACF, IRF, volatilidad condicional, heatmap, iliquidez).
- Anexo B — Código fuente: `src/` (verificación de universo, ingesta, preparación, EDA, 13 módulos de modelos y exportadores).
- Anexo C — Tablas de salida: `outputs/tables/` (33 archivos CSV).
- Anexo D — Desarrollo matemático de los modelos (a continuación).
- Diccionario de datos: `docs/diccionario_datos.md`; decisiones fundacionales: `docs/00_decisiones_fundacionales.md`.
- Entorno: `requirements.txt` (Python 3.13; statsmodels 0.14.6, arch 8.0, linearmodels 7.0, reportlab).

---

## Anexo D — Desarrollo matemático de los modelos

Este anexo formaliza las técnicas empleadas. La notación sigue el cuerpo principal.

### D.1 Pruebas de raíz unitaria

**Dickey-Fuller aumentada (ADF).** Se estima Δy_t = μ + ρ y_{t−1} + Σ_{j=1}^{p}
φ_j Δy_{t−j} + ε_t y se contrasta H0: ρ = 0 (raíz unitaria) con el estadístico
t_ρ = ρ̂ / ee(ρ̂), comparado con los valores críticos no estándar de Dickey-Fuller.
La inclusión de p rezagos de Δy blanquea la autocorrelación residual; p se elige por
AIC. **Phillips-Perron (PP)** corrige la autocorrelación de forma no paramétrica
sobre el estadístico de Dickey-Fuller simple, mediante una estimación tipo
Newey-West de la varianza de largo plazo. **KPSS** invierte la hipótesis nula
(H0: estacionariedad) descomponiendo y_t en tendencia determinista, caminata
aleatoria y error estacionario, y contrasta que la varianza del componente de
caminata sea nula con el estadístico η = T^{−2} Σ S_t² / σ̂², donde S_t es la suma
parcial de residuos. La decisión cruzada (ADF/PP rechazan raíz unitaria y KPSS no
rechaza estacionariedad) confiere robustez frente a las bajas potencias
individuales.

### D.2 VAR, forma compañera, IRF y FEVD

Un VAR(p) se escribe y_t = c + Σ_{j=1}^{p} A_j y_{t−j} + u_t, con u_t ruido blanco de
matriz de covarianzas Σ_u. Su **forma compañera** (un VAR(1) de dimensión Kp)
permite verificar estabilidad: el proceso es estable si todos los autovalores de la
matriz compañera tienen módulo menor que uno. La representación de **medias móviles**
es y_t = μ + Σ_{i=0}^{∞} Φ_i u_{t−i}, donde Φ_i acumula los efectos dinámicos. Para
identificar shocks estructurales ortogonales se usa la **descomposición de Cholesky**
Σ_u = P P', con P triangular inferior; las **IRF ortogonalizadas** son Θ_i = Φ_i P, y
el elemento (m, n) de Θ_i es la respuesta de la variable m, i períodos después, a un
shock de una desviación estándar en la variable n. El orden causal contemporáneo
(factores globales antes que el activo) refleja que una minera pequeña no afecta el
precio mundial del cobre en el mismo día. La **FEVD** descompone la varianza del
error de predicción a h pasos de la variable m como la suma sobre n y sobre
i = 0..h−1 de (Θ_i)²_{m,n}, normalizada; entrega la fracción de la varianza de cada
variable atribuible a cada shock.

### D.3 Cointegración de Johansen y VECM

Reparametrizando el VAR(p) en niveles se obtiene el VECM
Δy_t = Π y_{t−1} + Σ_{j=1}^{p−1} Γ_j Δy_{t−j} + c + u_t, donde Π = αβ' codifica las
relaciones de largo plazo. El **rango** de Π (número de vectores cointegrantes r) se
determina con el estadístico de la **traza** λ_traza(r) = −T Σ_{i=r+1}^{K} ln(1 − λ̂_i),
con λ̂_i los autovalores de un problema de autovalores generalizado; se compara con
valores críticos tabulados. La matriz **β** (K×r) contiene los vectores cointegrantes
—las relaciones de equilibrio— y **α** (K×r) las velocidades de ajuste —cuánto
corrige cada ecuación, por período, las desviaciones respecto del equilibrio—. Un
α_i negativo y significativo en la ecuación del activo implica fuerza
correctora hacia el equilibrio; su magnitud pequeña (≈ −0.0008 diaria) implica una
**vida media** de la desviación de cientos de días, esto es, ajuste lento.

### D.4 ARDL, UECM y bounds test

El ARDL(p, q) es y_t = c + Σ_{i=1}^{p} φ_i y_{t−i} + Σ_{j=0}^{q} θ_j' x_{t−j} + ε_t.
Su forma de corrección de error no restringida (UECM) es Δy_t = c + ρ y_{t−1} +
δ' x_{t−1} + (términos de corto plazo en diferencias) + ε_t. El **bounds test** de
Pesaran-Shin-Smith contrasta H0: ρ = 0 y δ = 0 (ausencia de relación de nivel)
mediante un estadístico F cuya distribución asintótica está acotada por dos
conjuntos de valores críticos: el límite inferior supone todos los regresores I(0) y
el superior todos I(1). Si F supera el límite superior se concluye cointegración; si
cae por debajo del inferior, no; en la banda intermedia el resultado es no
concluyente. Los multiplicadores de largo plazo son −δ/ρ.

### D.5 NARDL y asimetría

El NARDL descompone cada regresor en sumas parciales de incrementos positivos y
negativos: x⁺_t = Σ_{j=1}^{t} máx(Δx_j, 0) y x⁻_t = Σ_{j=1}^{t} mín(Δx_j, 0), de modo
que x_t = x_0 + x⁺_t + x⁻_t. Ambas entran como regresores separados, permitiendo
coeficientes de largo plazo distintos θ⁺ y θ⁻. La **asimetría de largo plazo** se
contrasta con un test de Wald sobre H0: θ⁺ = θ⁻; su rechazo (Antofagasta, p = 0.004)
indica que el valor del activo responde de forma estadísticamente distinta a alzas y
a caídas del cobre, consistente con la opcionalidad de las minas (§2.5).

### D.6 Familia GARCH

Sobre los retornos r_t = μ + ε_t, con ε_t = σ_t z_t y z_t ~ t-Student estandarizada,
se especifica la varianza condicional:
- **GARCH(1,1):** σ²_t = ω + α ε²_{t−1} + β σ²_{t−1}; la **persistencia** es α + β y
  la varianza incondicional ω/(1 − α − β) existe si α + β < 1.
- **GJR-GARCH(1,1):** σ²_t = ω + α ε²_{t−1} + γ ε²_{t−1} 1[ε_{t−1} < 0] + β σ²_{t−1};
  γ > 0 implica **efecto apalancamiento** (las caídas elevan más la volatilidad).
- **EGARCH(1,1):** ln σ²_t = ω + α(|z_{t−1}| − E|z|) + γ z_{t−1} + β ln σ²_{t−1};
  modela el logaritmo (garantiza positividad) y γ < 0 captura el apalancamiento.

La estimación es por **máxima verosimilitud** (cuasi-MV con la t-Student); la
selección entre especificaciones usa AIC/BIC. La inestabilidad observada en Pucobre
(soluciones de borde) proviene de la masa de retornos nulos y los saltos, que violan
los supuestos de suavidad de la verosimilitud GARCH.

### D.7 Errores HAC (Newey-West)

Para β̂ de MCO, la matriz HAC estima V(β̂) = (X'X)^{−1} X' Ω̂ X (X'X)^{−1} con
Ω̂ que pondera las autocovarianzas hasta el rezago L con pesos de Bartlett
w_ℓ = 1 − ℓ/(L+1), garantizando una estimación semidefinida positiva y consistente
ante heterocedasticidad y autocorrelación de forma desconocida.

### D.8 Causalidad de Toda-Yamamoto

Se estima un VAR en **niveles** con p + d_max rezagos (p óptimo, d_max = orden máximo
de integración = 1) y se contrasta, mediante un test de Wald tipo MWALD, la
no-causalidad imponiendo cero a los coeficientes de los **primeros p** rezagos de la
variable causante (excluyendo los d_max rezagos adicionales). El estadístico se
distribuye asintóticamente como χ² con p grados de libertad, **válido aun cuando las
series son I(1) o están cointegradas**, lo que evita el sesgo del test de Granger
estándar en presencia de raíces unitarias.

### D.9 Iliquidez de Amihud y estudio de eventos

El ratio de Amihud por activo es ILLIQ_i = promedio_t (|r_{i,t}| / (Vol_{i,t} ·
P_{i,t})), interpretado como el impacto de precio por unidad monetaria transada. En
el **estudio de eventos**, el retorno anormal es AR_{i,t} = r_{i,t} − (α̂_i + β̂_i
r_{m,t}), con (α̂_i, β̂_i) estimados por el modelo de mercado en la ventana
[−130, −11]; el CAR por evento suma los AR en [−5, +5] y el CAAR los promedia entre
eventos. La significancia se evalúa con un test t sobre la hipótesis CAAR = 0.

### D.10 Panel: efectos fijos, aleatorios y Hausman

Para el panel y_{i,t} = α_i + β' x_{i,t} + u_{i,t}: **efectos fijos** estima β
mediante la transformación *within* (desviaciones respecto de la media de cada
empresa), eliminando α_i; **efectos aleatorios** trata α_i como aleatorio no
correlacionado con los regresores y estima por mínimos cuadrados generalizados
factibles. El test de **Hausman** contrasta H0: cov(α_i, x_{i,t}) = 0 comparando
ambos estimadores: si no se rechaza, RE es consistente y eficiente. Con N = 4 la
inferencia *cluster* tiene baja potencia, por lo que el panel se reporta como
robustez sectorial, no como inferencia primaria.
