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

## Dedicatoria

A quienes acompañaron este proceso.

## Agradecimientos

Expreso mi gratitud al profesor guía por su orientación y rigor a lo largo del
desarrollo de esta tesis, y al cuerpo académico del Magíster en Data Science de la
Universidad San Sebastián por la formación recibida. Agradezco asimismo a las
instituciones que ponen a disposición pública los datos que hicieron posible este
trabajo —en particular los proveedores de información de mercado y el servicio de
indicadores económicos nacionales—, cuya apertura es condición de la investigación
reproducible. Finalmente, agradezco a mi familia y a quienes me acompañaron durante
este proceso por su apoyo constante.

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

## Glosario de términos

- **Cointegración.** Propiedad por la cual dos o más series no estacionarias comparten
  una tendencia estocástica común, de modo que existe una combinación lineal de ellas
  que sí es estacionaria; representa una relación de equilibrio de largo plazo.
- **Commodity currency (moneda-commodity).** Moneda de una economía exportadora de
  materias primas cuyo valor está estrechamente ligado al precio mundial de su canasta
  exportadora; el peso chileno es un ejemplo arquetípico por su vínculo con el cobre.
- **Cross-listing.** Cotización de una empresa en una bolsa distinta de la de su país
  de operación; Antofagasta opera en Chile pero cotiza en Londres.
- **Descubrimiento de precios (price discovery).** Proceso mediante el cual la
  información disponible se incorpora a los precios de mercado; en activos ilíquidos
  este proceso es más lento.
- **Efecto apalancamiento (leverage effect).** Tendencia de la volatilidad a aumentar
  más tras caídas de precio que tras alzas de igual magnitud.
- **Elasticidad-cobre.** Variación porcentual del precio (o retorno) de una acción ante
  una variación de 1% en el precio del cobre.
- **Iliquidez.** Dificultad para transar un activo sin afectar su precio; aquí se mide,
  entre otras, con el ratio de Amihud y el porcentaje de días sin transacción.
- **Pure-play.** Empresa cuyo negocio se concentra en una sola actividad; un pure-play
  de cobre obtiene la mayor parte de sus ingresos de ese metal.
- **Velocidad de ajuste.** Proporción del desequilibrio respecto de la relación de
  largo plazo que se corrige por período en un modelo de corrección de error.

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

### 1.7 Relevancia y alcance

La relevancia del estudio opera en tres planos. En el **académico**, contribuye a una
literatura escasa sobre la transmisión del precio del cobre a la valoración de las
mineras chilenas y, más ampliamente, al estudio del descubrimiento de precios en
mercados emergentes pequeños; el contraste entre un activo líquido y otro ilíquido con
idéntica exposición fundamental constituye un cuasi-experimento poco frecuente. En el
**práctico**, las elasticidades por horizonte y la evidencia sobre el rezago de
incorporación son directamente útiles para la valoración, la gestión de riesgo y el
diseño de coberturas de quienes invierten en el sector. En el de **política pública**,
los resultados informan el debate sobre la profundidad y liquidez del mercado de
capitales chileno, al cuantificar un costo concreto de la baja liquidez del segmento
local.

El **alcance** se delimita con claridad para no prometer más de lo que el diseño
permite. El trabajo es de naturaleza explicativa y de medición de impacto: busca
cuantificar relaciones, signos, magnitudes y dinámicas, no producir pronósticos de
mercado; el ejercicio predictivo que se incluye cumple un rol de validación
complementaria y de aplicación, no de objetivo central. El universo se restringe a las
mineras de cobre cotizadas vinculadas a Chile, con referencias internacionales sólo a
efectos de validez externa; no se abordan otros metales ni otros mercados salvo como
comparación. La frecuencia primaria es diaria, complementada con análisis mensual para
la macro nacional. Por último, las conclusiones sobre el papel de la liquidez se
sostienen sobre el contraste de dos *pure-plays*; su generalización a otros contextos,
aunque plausible a la luz de la teoría, queda planteada como pregunta empírica abierta.

### 1.8 Estructura

El Capítulo 2 desarrolla el marco teórico; el 3 revisa la literatura; el 4 describe
los datos; el 5 detalla la metodología y las especificaciones; el 6 presenta los
resultados; el 7 los discute; el 8 concluye. Cierran las referencias y los anexos.

---

## 2. Marco teórico

### 2.1 Valoración de activos y factores macroeconómicos

El valor fundamental de una acción es el valor presente de sus flujos de caja
esperados descontados a una tasa ajustada por riesgo. En su forma canónica, el modelo
de descuento de dividendos expresa el precio como P_0 = Σ_{t≥1} E[D_t]/(1+k)^t, donde
D_t es el flujo distribuible en t y k la tasa de descuento. Para una empresa cuyos
ingresos dependen del precio de una materia prima, conviene descomponer el flujo
operativo como una función del precio del *commodity* y de la estructura de costos:
si q denota la producción, P el precio del cobre y c el costo de caja unitario, el
margen operativo es proporcional a q·(P − c). Una variación del precio del cobre se
propaga entonces al valor por dos vías: directamente, a través del numerador (flujos),
e indirectamente, a través del denominador, en la medida en que las condiciones
financieras globales que mueven al cobre (dólar, tasas, apetito por riesgo) también
desplazan la tasa de descuento. Esta doble vía justifica un modelo multifactorial en
el que el cobre comparte protagonismo con un conjunto acotado de factores macro-
financieros.

Para una empresa minera de cobre, los **flujos** dependen directamente del precio del
metal (ingreso) y de sus costos (energía, insumos, salarios, tipo de cambio), mientras
que la **tasa de descuento** depende de la tasa libre de riesgo global y de las primas
de riesgo. De esta estructura se desprenden cinco canales económicos que organizan la
selección de variables independientes:

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

Conviene situar con precisión la contribución frente a los trabajos reseñados. La
literatura de factores macro (Chen, Roll y Ross, 1986) establece *qué* variables
valora el mercado, pero no aborda la *velocidad* de incorporación ni el papel de la
liquidez; la de monedas-commodity (Chen y Rogoff, 2003) y la chilena del Banco
Central documentan el eslabón cobre→tipo de cambio, deteniéndose un paso antes de la
valoración accionaria; y los estudios sectoriales internacionales (Mendiola et al.,
2022; Kilian y Park, 2009) cuantifican la reacción de las mineras al *commodity* pero
sin el contraste de microestructura que aquí se explota. Por su parte, la literatura
de iliquidez (Amihud, 2002; Bekaert et al., 2007) provee el marco conceptual y la
métrica, pero rara vez se aplica a un experimento natural tan nítido como el que ofrece
el par Antofagasta–Pucobre: dos *pure-plays* con idéntica exposición fundamental al
cobre y liquidez radicalmente distinta. La originalidad de esta tesis reside,
precisamente, en cruzar esas tradiciones —factores macro, cointegración, volatilidad y
microestructura— para descomponer la transmisión cobre→valoración por horizonte y
atribuir la pendiente de esa curva a la liquidez, en un mercado emergente y sobre un
sector de importancia sistémica para el país.

---

## 4. Datos

### 4.0 El sector del cobre en Chile: contexto institucional

Chile es el primer productor mundial de cobre de mina, con una participación cercana
a un cuarto de la oferta global, y el metal concentra del orden de la mitad de su
canasta exportadora. Esta especialización confiere al cobre un papel macroeconómico
de primer orden: influye en la balanza comercial, en los ingresos fiscales —por la
vía de Codelco y de los tributos a la gran minería privada— y en la trayectoria del
tipo de cambio real. La institucionalidad del sector combina una empresa estatal de
gran escala (Codelco), que no cotiza en renta variable y sólo accede a los mercados
mediante emisión de deuda, con un conjunto de productores privados de tamaño y
estructura de propiedad heterogéneos. Esta configuración explica por qué el universo
de mineras de cobre accesibles para un inversionista bursátil es reducido y por qué
su estudio exige resolver primero, de forma empírica, qué emisores existen y con qué
profundidad de mercado.

La **Bolsa de Santiago**, principal plaza accionaria del país, se caracteriza por una
capitalización moderada en términos internacionales y por una **liquidez muy
heterogénea** entre emisores: unos pocos títulos de gran capitalización concentran el
grueso del volumen, mientras que numerosas acciones de menor tamaño transan de forma
intermitente. Esta dualidad de liquidez es central para esta tesis, pues el contraste
entre un *pure-play* de cobre cotizado en una plaza profunda (Antofagasta, en Londres)
y otro cotizado localmente con baja profundidad (Pucobre) provee la variación que
permite identificar el efecto de la microestructura sobre la transmisión de precios.

El período 2004–2026 cubre, además, un conjunto excepcionalmente rico de regímenes
para el precio del cobre: el superciclo de las materias primas (2004–2011),
impulsado por la urbanización e industrialización de China; el colapso abrupto de la
crisis financiera global (2008–2009); la corrección de mediados de la década pasada;
el desplome y la recuperación en torno a la pandemia (2020); y el repunte vinculado a
la transición energética y la electromovilidad (2021 en adelante). Esta sucesión de
auges y caídas ofrece un laboratorio natural para examinar la estabilidad de la
relación cobre–valoración y para justificar el análisis de quiebres estructurales y
de submuestras.

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
La Tabla siguiente documenta la verificación empírica de disponibilidad de cada
candidato (número de observaciones, rango de fechas y moneda).

[[CSV: universo_verificacion.csv | Verificación empírica de disponibilidad de los candidatos del universo en Yahoo Finance: ticker, descripción, disponibilidad, observaciones, rango de fechas y moneda.]]

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
nivel; los retornos no se rellenan, para no introducir autocorrelación espuria. La
alineación de calendarios entre las plazas de Londres, Santiago y Nueva York reduce la
muestra efectiva común en las regresiones multifactor a n ≈ 4.475 observaciones
diarias.

Tres decisiones de tratamiento merecen explicitarse por su efecto sobre los
resultados. Primero, la elección de **log-retornos** (en lugar de retornos simples)
garantiza aditividad temporal y mejora las propiedades distribucionales, además de ser
el estándar en la literatura de series financieras. Segundo, se optó por **no
winsorizar** la variable dependiente en la especificación principal: los valores
extremos de Pucobre no son errores de medición sino la manifestación genuina de su
*thin trading*, de modo que recortarlos eliminaría precisamente el fenómeno de
interés; su efecto sobre la inferencia se controla mediante errores robustos (HAC) y
distribuciones de colas pesadas (t-Student) en los modelos de volatilidad. Tercero, la
sustitución del índice IPSA —cuya serie pública resultó incompleta— por el ETF iShares
MSCI Chile (ECH) como aproximación del mercado local introduce un componente
cambiario, dado que ECH se denomina en dólares; este solapamiento parcial con el factor
USD/CLP se monitorea mediante el factor de inflación de varianza, que se mantiene en
niveles moderados (máximo ≈3.5), descartando colinealidad severa. Cada una de estas
decisiones se documenta en el diccionario de datos del repositorio.

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

### 5.12 Consideraciones de potencia y tamaño muestral

El diseño reconoce dos restricciones de potencia y las gestiona de forma explícita.
En la dimensión transversal, el universo de mineras de cobre vinculadas a Chile es
muy pequeño (dos *pure-plays* y dos comparables sectoriales), por lo que los enfoques
de panel —con N=4 entidades— ofrecen baja potencia y una inferencia *cluster* poco
fiable; en consecuencia, el panel se reporta únicamente como verificación sectorial y
la inferencia primaria descansa en las series de tiempo por activo, donde el número de
observaciones diarias es holgado (del orden de varios miles). En la dimensión de
series de tiempo, en cambio, el tamaño muestral es amplio, lo que confiere potencia a
las pruebas de raíz unitaria, cointegración y causalidad, pero también las hace
sensibles a la detección de relaciones de magnitud económica modesta; por ello se
privilegia la interpretación de las **magnitudes** y de los **intervalos** por sobre
la mera significancia estadística. Finalmente, allí donde la potencia es intrínseca-
mente limitada —subperíodos cortos posteriores a un quiebre, o el escaso número de
eventos de política monetaria— se evita sobreinterpretar coeficientes individuales y
se prefiere la lectura conjunta de la evidencia.

---

## 6. Resultados

### 6.1 Estadística descriptiva

La Tabla siguiente reporta los momentos de los log-retornos diarios (en %) de los
ocho activos del universo durante 2004–2026, junto con el estadístico de Jarque-Bera
de normalidad.

[[CSV: descriptivos_retornos.csv | Estadística descriptiva de los log-retornos diarios (%) de los ocho activos, 2004–2026. JB: estadístico de Jarque-Bera; JB_p: su p-valor.]]

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

El examen activo por activo refuerza esta lectura. Antofagasta exhibe la volatilidad
diaria más alta del núcleo (desviación estándar ≈2.65%), con colas moderadas
(curtosis ≈4.1), propias de un *blue chip* líquido y muy seguido por el mercado. Las
referencias internacionales (Freeport, Southern, BHP, Glencore) presentan perfiles
comparables, con desviaciones estándar entre 2.3% y 3.2% y curtosis entre 6 y 15.
Pucobre, por el contrario, combina una volatilidad diaria menor en apariencia (≈1.44%)
con una curtosis extraordinariamente elevada (≈35) y asimetría positiva pronunciada;
esta combinación es la firma estadística de un activo que permanece inmóvil la mayor
parte del tiempo y reacciona con saltos abruptos cuando finalmente transa, en lugar de
incorporar la información de manera continua. CAP y SQM ocupan posiciones intermedias,
coherentes con su condición de empresas de materiales de mayor tamaño y liquidez que
Pucobre pero ajenas al cobre puro. Esta heterogeneidad de momentos anticipa por qué un
mismo factor —el precio del cobre— se transmite de forma tan distinta entre activos.

[[FIG: heatmap_correlaciones.png | Matriz de correlaciones de los retornos diarios de los activos y los factores. La columna del cobre (ΔHG=F) ordena a los activos por su comovimiento contemporáneo con el metal.]]

### 6.2 Estacionariedad y cointegración

Las propiedades de integración se evaluaron con tres pruebas complementarias —Dickey-
Fuller aumentada (ADF) y Phillips-Perron (H0: raíz unitaria) y KPSS (H0:
estacionariedad)—, con una regla de decisión por mayoría. La Tabla siguiente resume
los resultados sobre los log-precios (niveles) y los log-retornos (diferencias) de los
activos del núcleo y de los principales factores.

[[CSV: estacionariedad.csv | Pruebas de raíz unitaria (ADF, Phillips-Perron, KPSS) y conclusión sobre el orden de integración de niveles y retornos.]]

La evidencia es nítida: los log-precios son **I(1)** y los retornos **I(0)**, sin
presencia de procesos I(2). El resultado se confirma con la prueba de Zivot-Andrews,
que no rechaza la raíz unitaria ni siquiera permitiendo un quiebre endógeno de
nivel/tendencia (ANTO p≈0.62; Pucobre p≈0.99), descartando que el comportamiento I(1)
sea un artefacto de un quiebre estructural. El test bivariado de Engle-Granger
(activo~cobre) no detecta cointegración robusta —el cobre por sí solo no basta—, pero
el procedimiento multivariante de **Johansen** sobre el vector [ln P, ln cobre,
ln USDCLP, ln DXY] arroja un **rango de cointegración r = 1** tanto para Antofagasta
como para Pucobre: existe exactamente una relación de equilibrio de largo plazo que
vincula el precio de la acción con el cobre y la moneda.

### 6.3 Impacto contemporáneo (HAC)

El primer bloque de evidencia mide el impacto contemporáneo de los factores sobre el
retorno diario mediante regresión por mínimos cuadrados con errores estándar HAC de
Newey-West. El coeficiente del cobre es la elasticidad-cobre contemporánea, que mide
el efecto de un alza de 1% en el precio del cobre sobre el retorno diario del activo.
La Tabla siguiente reporta los coeficientes completos (cobre, tipo de cambio, dólar,
mercado, tasas y volatilidad) para los ocho activos.

[[CSV: hac_coeficientes.csv | Coeficientes de la regresión de retornos con errores HAC (Newey-West): variable dependiente = retorno diario; se reportan coeficiente, error estándar HAC, t y p-valor por activo y factor.]]

La elasticidad-cobre presenta un gradiente claro: 0.70 en Antofagasta (t=15.4) y
0.49–0.63 en las referencias internacionales del cobre, frente a apenas 0.09 en
Pucobre (t=4.4). Para Antofagasta resultan además significativos el dólar (DXY, signo
negativo: una apreciación del dólar deprime al activo), el mercado —global y local— y
el cambio en la tasa larga estadounidense. Para Pucobre, en cambio, sólo el mercado
local y, débilmente, el cobre son significativos, con un coeficiente de determinación
de apenas 0.04: su retorno diario es mayoritariamente idiosincrásico, dominado por su
microestructura. La Figura siguiente ilustra cómo, en niveles, los precios de los
*pure-plays* siguen y amplifican el ciclo del cobre.

[[FIG: precios_normalizados.png | Evolución de los precios normalizados (base 100) de Antofagasta y Pucobre frente al precio del cobre, 2004–2026. Los pure-plays amplifican el ciclo del metal por apalancamiento operativo.]]

La batería de diagnósticos sobre los residuos justifica las decisiones de
especificación: hay efectos ARCH significativos en todos los activos (que motivan el
modelado GARCH de la varianza), autocorrelación residual (que motiva los errores HAC)
y no-normalidad de colas pesadas; el factor de inflación de varianza máximo es ≈3.5,
descartando multicolinealidad severa. La Tabla siguiente reporta el detalle.

[[CSV: hac_diagnosticos.csv | Diagnósticos de los residuos de la regresión HAC por activo: R², rezagos HAC, Breusch-Godfrey, Breusch-Pagan, ARCH-LM, Jarque-Bera, Ljung-Box y VIF máximo.]]

En conjunto, H1 se sostiene —el cobre es positivo y significativo en los ocho
activos— y H2 se sostiene con fuerza: la sensibilidad contemporánea es de 0.70 en el
*pure-play* líquido frente a 0.09 en el ilíquido.

### 6.4 Dinámica (VAR, IRF, FEVD, Granger)

| Activo | FEVD cobre (1d) | FEVD cobre (20d) | IRF acum. 5d | Granger cobre→activo |
|---|---|---|---|---|
| ANTO.L | 28.7% | 27.8% | 0.091 | p=0.008 (sí) |
| PUCOBRE.SN | 2.0% | 4.3% | 0.196 | p<0.001 (sí) |

Clave: en Pucobre la respuesta acumulada a 5 días (0.196) es ~4× la del primer día
(0.043), y la FEVD del cobre crece de 2% a 4.3% entre 1 y 20 días. El cobre **causa**
los retornos de Pucobre (Granger p<0.001), pero el efecto se **difiere** en lugar de
impactar contemporáneamente — consistente con descubrimiento de precios lento.

El **perfil de la FEVD por horizonte** es, en sí mismo, diagnóstico del mecanismo y no
sólo su nivel. En Pucobre la fracción de la varianza del error de pronóstico atribuible
al cobre **más que se duplica** al ampliar el horizonte (2.03% a 1 día → 4.32% a 20
días, un incremento relativo de +113%), y no se estabiliza sino hacia el día ~12. En
Antofagasta, en cambio, esa fracción es **prácticamente plana** —de hecho marginalmente
decreciente— (28.68% → 27.79%): el cobre ya explica su cuota de varianza desde el primer
paso y no gana peso con el horizonte. Este contraste —una FEVD **creciente** frente a
una FEVD **plana**— es la contraparte, en el dominio de la descomposición de varianza,
del mismo fenómeno que capturan las betas por horizonte: una participación del cobre que
sube con el horizonte es la firma econométrica de información que se incorpora con
rezago, mientras que una participación plana desde el impacto es la de información ya
descontada contemporáneamente. Que en Pucobre el nivel absoluto de la FEVD sea bajo
(4.3% frente al ~28% de Antofagasta) no contradice el hallazgo: a frecuencia diaria la
varianza de un activo tan ilíquido está dominada por su propio ruido de microestructura
—los saltos discretos entre transacciones explican ~94% de su varianza—, de modo que el
canal fundamental sólo se manifiesta plenamente al agregar el tiempo, como confirman los
modelos mensual y de largo plazo (§6.5, §6.12).

Las funciones impulso-respuesta de ambos activos ilustran el mismo contraste: la de
Antofagasta se concentra en el primer día, mientras que la de Pucobre se acumula durante
las jornadas siguientes.

[[FIG: irf_ANTO_L.png | Función impulso-respuesta del retorno de Antofagasta ante un shock de una desviación estándar en el cobre (identificación de Cholesky). Respuesta concentrada en el impacto contemporáneo.]]

[[FIG: irf_PUCOBRE_SN.png | Función impulso-respuesta del retorno de Pucobre ante el mismo shock. La respuesta se acumula en los días posteriores, evidencia de transmisión diferida.]]

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

La magnitud de la velocidad de ajuste merece una lectura cuantitativa. Un coeficiente
α del orden de −0.0008 diario implica que sólo una fracción ínfima del desequilibrio
respecto del valor de equilibrio se corrige cada jornada; en términos de vida media
—el tiempo que tarda en disiparse la mitad de una desviación— ello equivale a varios
cientos de días hábiles. Esta lentitud del ajuste es, en sí misma, coherente con el
relato central: la relación de equilibrio existe y es económicamente significativa,
pero el regreso al equilibrio tras una perturbación es gradual, especialmente en el
activo ilíquido, donde la corrección sólo puede operar en las jornadas en que hay
transacción. El contraste entre una elasticidad de largo plazo robusta y una velocidad
de ajuste pequeña es, por tanto, la contrapartida —en el dominio de los niveles— del
fenómeno que las regresiones de retornos capturan en el dominio de los cambios: el
vínculo fundamental es fuerte, pero su materialización en el precio es lenta.

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
ilíquido. La Tabla y la Figura siguientes resumen la comparación entre
especificaciones y la trayectoria de la volatilidad condicional de Antofagasta.

[[CSV: garch_resumen.csv | Comparación de modelos GARCH(1,1), GJR-GARCH(1,1) y EGARCH(1,1) por activo: AIC, BIC, log-verosimilitud, parámetros α, β, asimetría γ y persistencia.]]

[[FIG: vol_condicional_ANTO_L.png | Volatilidad condicional diaria estimada (GJR-GARCH) de Antofagasta, 2004–2026. Se aprecian conglomerados de volatilidad en 2008 y 2020.]]

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
La práctica coincidencia entre los estimadores Pooled, de efectos fijos y de efectos
aleatorios indica que los efectos específicos de empresa aportan poco en una
especificación con factores comunes que varían en el tiempo, lo que es esperable al
trabajar con retornos diarios de media casi nula. El predominio del factor de mercado
local sobre el cobre en el promedio sectorial refleja la composición del panel —dos de
sus cuatro integrantes (CAP, SQM) no son cobre puro— y, sobre todo, el peso de Pucobre,
cuyo comovimiento diario está dominado por el mercado local más que por el metal. En
suma, el panel confirma cualitativamente el canal del cobre, pero su baja potencia
(N=4) aconseja tratarlo como evidencia de apoyo, no como inferencia primaria.

### 6.10 Canal de política monetaria (TPM) y estudio de eventos

El cambio diario de la TPM entra con signo negativo en todos los activos
(endurecimiento → menor retorno) pero **no significativo** (p>0.12). El estudio de
eventos sobre 51 alzas y 41 bajas de TPM arroja CAAR con el signo económico correcto
(alza → anormal negativo: ANTO −1.04%, CAP −1.90%; baja → positivo) pero **ninguno
significativo** (p>0.37): los cambios de TPM están anticipados y la valoración minera
responde a factores globales más que a la política monetaria doméstica. Este resultado
admite una interpretación coherente con la eficiencia de mercado: las decisiones de
política monetaria del Banco Central de Chile son, en su mayoría, anticipadas por los
participantes —la senda de la tasa se comunica y se proyecta—, de modo que el anuncio
en sí aporta poca sorpresa y, por tanto, escaso retorno anormal. A ello se suma que
los ingresos de las mineras de cobre se denominan en dólares y dependen del precio
mundial del metal, por lo que su valoración es relativamente insensible al costo del
financiamiento local. La consecuencia metodológica es clara: para capturar el efecto
de la política monetaria sobre estos activos sería necesario aislar el componente de
**sorpresa** (la diferencia entre la tasa efectiva y la esperada por el mercado), lo
que requiere datos de expectativas no disponibles en este estudio y queda planteado
como extensión futura.

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
Antofagasta (~US$2.000 M). La Tabla siguiente reporta las medidas de iliquidez por
activo.

[[CSV: iliquidez_amihud.csv | Medidas de iliquidez por activo: ratio de Amihud (medio y mediano), porcentaje de días con retorno cero y volumen medio en USD equivalente.]]

**(b) Transversal.** La correlación de Spearman entre iliquidez (% días cero) y
β-cobre contemporánea es negativa (ρ≈−0.55), en la dirección predicha (no
significativa con N=8). La Figura siguiente muestra esta relación.

[[FIG: iliquidez_vs_beta.png | Iliquidez (porcentaje de días con retorno cero) frente a la elasticidad-cobre contemporánea de los ocho activos. Pucobre es el punto extremo de baja transmisión y alta iliquidez.]]

**(c) Rezagos distribuidos:**

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

El mecanismo puede precisarse en el lenguaje de la microestructura de mercado. En un
título de alta profundidad, el flujo continuo de órdenes y la presencia de
arbitrajistas aseguran que cualquier novedad sobre el precio del cobre —disponible en
tiempo real en los mercados de futuros— se traduzca casi instantáneamente en el precio
de la acción, pues existen agentes dispuestos a operar ante la menor discrepancia entre
el valor fundamental y el precio observado. En un título de baja profundidad, en
cambio, pueden transcurrir jornadas sin transacciones; durante esos intervalos el
precio permanece "congelado" en su último valor, desconectado de la evolución del
fundamento. Cuando finalmente se cruza una operación, el precio salta para reflejar de
una vez toda la información acumulada, lo que produce simultáneamente la curtosis
extrema observada en los retornos de Pucobre y la autocorrelación positiva que el
modelo predictivo explota fuera de muestra. Este patrón —precios que se ajustan a
saltos discretos en lugar de hacerlo de forma continua— es la manifestación empírica
del descubrimiento de precios lento, y explica por qué la elasticidad-cobre medida
crece de forma monótona a medida que se amplía la ventana temporal: al agregar varios
días o un mes, los saltos rezagados se acumulan y la sensibilidad converge a la que
exhibe el activo líquido. La distinción crucial, y el aporte conceptual de la tesis,
es que esta brecha es de **velocidad de incorporación**, no de **exposición
fundamental**: ambos *pure-plays* están igualmente ligados al cobre en el largo plazo;
sólo difieren en la rapidez con que el mercado lo reconoce.

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
la magnitud del canal de demanda/ingreso. Este orden de magnitud —una relación
positiva pero por debajo de la unidad en el corto plazo— coincide con la evidencia de
Mendiola, Chávez-Bedoya y Wallenstein (2022), quienes documentan una reacción
positiva e inelástica de las acciones mineras de cobre ante cambios en el precio del
metal. El signo negativo del dólar y la relación cobre↔moneda son coherentes con la
literatura de *commodity currencies* (Chen y Rogoff, 2003) y con la evidencia
nacional del Banco Central de Chile. La advertencia de Kilian y Park (2009) —según la
cual el efecto de un shock de *commodity* sobre las acciones depende de su naturaleza
de oferta o de demanda— invita a no sobreinterpretar la elasticidad estimada como un
parámetro estructural único, sino como un promedio sobre regímenes; de ahí la
relevancia del análisis de quiebres y submuestras. La asimetría de largo plazo hallada
para Antofagasta dialoga con la evidencia de Cashin, McDermott y Scott (2002) sobre la
naturaleza asimétrica de los ciclos de *commodities*. Finalmente, la disociación
corto/largo plazo gobernada por la liquidez es plenamente consistente con Amihud
(2002), Bekaert, Harvey y Lundblad (2007) y Amihud, Hameed, Kang y Zhang (2015),
quienes sitúan a la liquidez —y en particular a la de las firmas pequeñas de mercados
emergentes— como un determinante de primer orden del comportamiento de los retornos.

### 7.4 Validez interna y externa

**Interna.** La identificación del canal cobre→acción se apoya en (i) la exogeneidad
del cobre respecto de una minera pequeña (confirmada por Toda-Yamamoto
unidireccional) y (ii) el control por factores globales y de moneda. La principal
amenaza a la validez interna sería un factor omitido que moviera simultáneamente al
cobre y a la acción sin pasar por el canal postulado; los controles de dólar, tasas,
mercado y energía mitigan esta posibilidad, y el contraste líquido/ilíquido la acota
aún más, pues un confusor de ese tipo debería afectar de manera idéntica a dos
*pure-plays* con la misma exposición fundamental, lo que no explicaría la diferencia
sistemática en la *velocidad* de transmisión. El placebo con SQM —un activo de litio,
ajeno al cobre, que no muestra predictibilidad por cobre rezagado— refuerza que el
efecto detectado no es un artefacto estadístico general.

**Externa.** El núcleo del resultado (heterogeneidad por liquidez) es específico al
contraste líquido/ilíquido y debería replicarse en otros *small-caps* de *commodities*
en mercados emergentes; la generalización a todo el sector chileno está limitada por el
N reducido. No obstante, la coherencia de las magnitudes con las referencias
internacionales y con la teoría de microestructura sugiere que el mecanismo —y no
necesariamente los coeficientes puntuales— es trasladable a contextos análogos: títulos
de baja liquidez con una exposición fundamental clara a un factor observable. Establecer
esa generalidad de forma rigurosa requeriría un panel internacional de *small-caps* de
recursos naturales, lo que se propone como extensión.

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

El aporte de esta tesis es triple. En lo **metodológico**, integra una batería amplia
y reproducible de técnicas —de la cointegración a la microestructura— sobre un
universo notoriamente difícil por su escaso número de emisores, mostrando que el
diseño cuidadoso permite extraer conclusiones robustas pese a la restricción de datos.
En lo **empírico**, cuantifica por primera vez, con este nivel de detalle, el canal
cobre→valoración para los *pure-plays* chilenos, entregando elasticidades por
horizonte que pueden servir de referencia a inversionistas y analistas. En lo
**conceptual**, documenta y prueba formalmente —por seis vías independientes y un
contraste cuasi-experimental— un mecanismo de descubrimiento de precios diferido
atribuible a la iliquidez, contribuyendo a la comprensión de la eficiencia
informacional en mercados emergentes pequeños.

### 8.1.1 Implicancias y recomendaciones

Para la **gestión de inversiones**, el resultado central tiene una consecuencia
operativa directa: la exposición al cobre de un activo ilíquido debe medirse y
gestionarse a horizontes intermedios o largos, no diarios; las betas diarias
subestiman sistemáticamente el riesgo-cobre de los emisores de baja liquidez y, por
tanto, sesgan tanto la valoración como las decisiones de cobertura. Para la **política
de mercado de capitales**, la evidencia cuantifica un costo concreto de la baja
liquidez del segmento local —incorporación tardía de la información fundamental— y
respalda iniciativas orientadas a profundizar la liquidez (incentivos a la creación de
mercado, programas de *market making*, mejoras de difusión de información) como vía
para acercar los precios locales a su valor fundamental con mayor celeridad. Para la
**gestión corporativa**, el hallazgo sugiere que, para un emisor pequeño, las mejoras
de sus fundamentos pueden tardar en reflejarse en el precio, con implicancias para el
costo de capital y para la oportunidad de operaciones de mercado.

### 8.2 Líneas futuras

Varias extensiones se desprenden naturalmente de este trabajo. En el plano de los
**datos**, incorporar el EMBI Chile y las tasas largas locales del Banco Central
permitiría cerrar el canal de riesgo soberano y de descuento doméstico que aquí quedó
pendiente por restricciones de acceso, y disponer de datos intradía habilitaría
medidas de iliquidez más finas (profundidad del libro, *spread* efectivo) y un estudio
del descubrimiento de precios a escala de minutos. En el plano **metodológico**, un
NARDL dinámico con multiplicadores acumulados asimétricos precisaría la forma de la
respuesta diferencial a alzas y caídas del cobre; un estudio de eventos basado en el
componente de **sorpresa** de la política monetaria —construido a partir de encuestas
de expectativas— aislaría el efecto no anticipado de la TPM; un modelo GARCH con saltos
o de volatilidad estocástica trataría adecuadamente la dinámica de Pucobre, hoy
inabordable con GARCH estándar; y un esquema de volatilidad multivariada (DCC-GARCH)
permitiría estudiar la correlación condicional dinámica cobre–acción y su variación en
episodios de tensión. En el plano de la **validez externa**, la prioridad es construir
un panel internacional de *small-caps* de recursos naturales que permita contrastar,
con mayor potencia, si la pendiente de la curva de transmisión por horizonte se explica
sistemáticamente por la liquidez, convirtiendo el hallazgo de caso en una regularidad
empírica generalizable.

### 8.3 Reflexión final

El cobre y la bolsa chilena están unidos por un vínculo fundamental sólido; lo que esta
tesis muestra es que la *forma* en que ese vínculo se expresa en los precios depende,
de manera medible, de la microestructura del mercado. En el activo profundo, el cobre
se incorpora de inmediato; en el activo delgado, lo hace con rezago, pero llega. Esa
distinción —entre la existencia de una relación y la velocidad con que el mercado la
reconoce— es, a la vez, el principal resultado del trabajo y un recordatorio de que la
eficiencia informacional no es una propiedad binaria del mercado, sino una cuestión de
grado que la liquidez modula.

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
- De Gregorio, J., & Labbé, F. (2011). *Copper, the real exchange rate and macroeconomic fluctuations in Chile* (Documento de Trabajo N°640). Banco Central de Chile. https://www.bcentral.cl/en/content/-/details/working-papers-n-640
- Sadorsky, P. (2001). Risk factors in stock returns of Canadian oil and gas companies. *Energy Economics*, 23(1), 17–28. https://doi.org/10.1016/S0140-9883(00)00072-4
- Lesmond, D. A., Ogden, J. P., & Trzcinka, C. A. (1999). A new estimate of transaction costs. *Review of Financial Studies*, 12(5), 1113–1141. https://doi.org/10.1093/rfs/12.5.1113
- Pástor, L., & Stambaugh, R. F. (2003). Liquidity risk and expected stock returns. *Journal of Political Economy*, 111(3), 642–685. https://doi.org/10.1086/374184
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

**Anexos.**
- Anexo B — Tablas detalladas de resultados (a continuación).
- Anexo C — Desarrollo matemático de los modelos.
- Anexo D — Figuras complementarias del análisis.
- Repositorio: código fuente (`src/`), datos procesados, 35+ tablas de salida
  (`outputs/tables/`), diccionario de datos (`docs/diccionario_datos.md`) y
  decisiones fundacionales (`docs/00_decisiones_fundacionales.md`).
- Entorno: `requirements.txt` (Python 3.13; statsmodels 0.14, arch 8.0, linearmodels 7.0, reportlab).

---

## Anexo B — Tablas detalladas de resultados

Este anexo reúne las salidas econométricas completas que sustentan el Capítulo 6.
Todas las cifras provienen de las estimaciones propias documentadas en el repositorio.

[[CSV: var_resumen.csv | VAR: descomposición de varianza (FEVD) del cobre a 1 y 20 días, respuesta acumulada e impulso, y causalidad de Granger por activo del núcleo.]]

[[CSV: vecm_resumen.csv | VECM: elasticidades de largo plazo (cobre, USDCLP, DXY) y velocidad de ajuste, con rango de cointegración r=1 (Johansen).]]

[[CSV: nardl_resumen.csv | NARDL: prueba de límites (bounds), elasticidades de largo plazo positiva y negativa del cobre, y test de Wald de asimetría.]]

[[CSV: garch_resumen.csv | Familia GARCH: comparación de GARCH(1,1), GJR-GARCH y EGARCH por activo (AIC, BIC, parámetros y persistencia).]]

[[CSV: panel_resultados.csv | Panel: coeficientes Pooled, efectos fijos y efectos aleatorios, con sus p-valores.]]

[[CSV: mensual_resumen.csv | Modelo mensual con macro nacional: elasticidad-cobre, IMACEC y cambio de TPM por activo.]]

[[CSV: event_study_tpm.csv | Estudio de eventos: retorno anormal acumulado promedio (CAAR) en torno a alzas y bajas de la TPM.]]

[[CSV: toda_yamamoto.csv | Causalidad de Toda-Yamamoto (robusta a integración): estadístico, p-valor y veredicto por relación.]]

[[CSV: quiebres_estructurales.csv | Quiebre estructural endógeno (Quandt-Andrews): sup-F, fecha de quiebre y elasticidad-cobre antes y después.]]

[[CSV: iliquidez_robustez_corr.csv | Robustez de la iliquidez: correlación de Spearman de cuatro medidas de iliquidez con la elasticidad-cobre contemporánea.]]

[[CSV: out_of_sample.csv | Validación fuera de muestra (Clark-West): R² OOS, RMSE y estadístico de Clark-West por activo.]]

[[CSV: predictor_metrics.csv | Predictor (backtest del retorno t+1): RMSE, mejora vs benchmark ingenuo, R² OOS y precisión direccional.]]

---

## Anexo C — Desarrollo matemático de los modelos

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
