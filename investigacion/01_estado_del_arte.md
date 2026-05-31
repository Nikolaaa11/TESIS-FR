# Estado del arte

**Impacto de variables macro-financieras (con énfasis en el precio del cobre) sobre
la valoración bursátil de las mineras de cobre en Chile: el rol de la liquidez y el
descubrimiento de precios.**

> Documento de investigación de apoyo a la tesis. Las citas fueron verificadas en los
> sitios de los editores y repositorios (Wiley, Elsevier/ScienceDirect, Oxford,
> University of Chicago Press, CFA Institute, Springer, Banco Central de Chile, NBER,
> CLADEA). Marcadas como "verificar" las no confirmadas plenamente.

Este estado del arte organiza la literatura en seis corrientes interrelacionadas. La
pregunta —cómo se transmiten los choques macro-financieros, en particular el precio del
cobre, a la valoración bursátil de las mineras chilenas, y cómo la (i)liquidez modula
esa transmisión— se sitúa en la intersección de la teoría de valoración de activos, la
economía de *commodities*, la literatura de *commodity currencies* y la microestructura
de mercados emergentes.

## 1. Factores macroeconómicos y retornos accionarios

La base conceptual es la *Arbitrage Pricing Theory* (Ross, 1976): los retornos
responden linealmente a factores de riesgo sistemático no diversificable. La
contrastación canónica es **Chen, Roll & Ross (1986)**, que muestra que innovaciones en
la producción industrial, la inflación esperada y no esperada, el *spread* de plazos y
el *spread* de riesgo de incumplimiento están sistemáticamente valoradas en el mercado
accionario (doi: 10.1086/296344). **Se sabe** que los factores macro afectan los
retornos de forma robusta en mercados desarrollados; **se discute** su estabilidad
temporal y su transferibilidad a emergentes; **vacío**: la APT no especifica los
factores *a priori*, lo que abre la puerta a factores sectoriales (el precio del
*commodity* subyacente) no capturados por los factores macro estándar.

## 2. Precios de *commodities* (cobre, petróleo) y mercados accionarios

Para empresas de recursos, el precio del producto es plausiblemente el factor
dominante. **Mendiola, Wallenstein & Chávez-Bedoya (2022)** —"Analysis of the Reaction
of Mining Stocks to the Development of Copper Prices" (CLADEA)— analizan mineras de
cobre en NYSE, LSE, TSX y la Bolsa de Lima y documentan una relación **positiva pero
inelástica** entre el precio del cobre y los retornos, con efectos de la crisis de 2008
más marcados en el mercado menos desarrollado (Lima).
**Kilian & Park (2009)** muestran que la respuesta de los retornos depende del *origen*
del choque (oferta vs. demanda), explicando ~22% de la varianza de largo plazo de los
retornos reales de EE. UU. (doi: 10.1111/j.1468-2354.2009.00568.x): **no basta el nivel
del precio; importa la naturaleza del choque**. **Gorton & Rouwenhorst (2006)** muestran
que un índice de futuros de *commodities* ofreció retornos comparables a las acciones
con correlación negativa frente a acciones y bonos (doi: 10.2469/faj.v62.n2.4083).
**Discusión/vacío**: asimetrías (¿igual respuesta a alzas que a bajas?) y dinámica de
corto vs. largo plazo; pocos trabajos descomponen el choque de cobre *y* examinan
empresas en un mercado emergente ilíquido.

## 3. *Commodity currencies* y el caso chileno cobre↔peso

El cobre afecta a las mineras chilenas por el canal directo (precio del producto) y el
indirecto (tipo de cambio). **Chen & Rogoff (2003)** acuñan el concepto de *commodity
currency* (doi: 10.1016/S0022-1996(02)00072-7). **Cashin, McDermott & Scott (2002)**
documentan que los ciclos de precios de *commodities* son asimétricos —las caídas duran
más que las alzas— (doi: 10.1016/S0304-3878(02)00062-7), lo que sugiere no linealidades
y quiebres. Para Chile, **De Gregorio & Labbé (2011)**, Documento de Trabajo N°640 del
Banco Central de Chile ("Copper, the Real Exchange Rate and Macroeconomic Fluctuations
in Chile"), estiman que en el largo plazo una depreciación real del dólar de 10% se
asocia a un alza de ~18% en el precio real del cobre y ~12% en los términos de
intercambio ([BCCh WP640](https://www.bcentral.cl/en/content/-/details/working-papers-n-640)).
**Vacío**: la literatura *commodity currency* es macro (tipo de cambio agregado); su
articulación con la valoración *bursátil de empresas individuales* está poco explorada.

## 4. Iliquidez, microestructura y descubrimiento de precios

Corriente diferenciadora de la tesis. La medida estándar es la de **Amihud (2002)**
—razón entre el valor absoluto del retorno y el volumen— que captura el impacto de
precio por unidad de volumen y revela una prima de iliquidez (doi:
10.1016/S1386-4181(01)00024-6). **Amihud, Hameed, Kang & Zhang (2015)** la confirman en
45 países (doi: 10.1016/j.jfineco.2015.04.005), mayor en mercados menos desarrollados.
**Bekaert, Harvey & Lundblad (2007)** —referencia para emergentes— usan la proporción
de retornos cero como proxy y muestran que la liquidez predice retornos futuros (doi:
10.1093/rfs/hhm030). Las raíces teóricas son **Kyle (1985)** (impacto de precio y
profundidad; doi: 10.2307/1913210) y **Roll (1984)** (spread efectivo desde la
autocovarianza; doi: 10.1111/j.1540-6261.1984.tb03897.x). **Lesmond, Ogden & Trzcinka
(1999)** proponen el estimador basado en retornos cero, útil sin datos intradía (doi:
10.1093/rfs/12.5.1113). **Vacío**: pocos estudios examinan la iliquidez como
**moderadora de la transmisión de un factor fundamental** (el cobre) hacia el precio.

## 5. Métodos econométricos

Cointegración: enfoque bietápico de **Engle & Granger (1987)** (doi: 10.2307/1913236) y
de máxima verosimilitud de **Johansen (1988, 1991)**. Con órdenes de integración
mixtos, el *bounds testing* **ARDL de Pesaran, Shin & Smith (2001)** (doi:
10.1002/jae.616) y su extensión no lineal **NARDL de Shin, Yu & Greenwood-Nimmo
(2014)** (doi: 10.1007/978-1-4899-8008-3_9), que captura asimetrías. Causalidad robusta
a integración: **Toda & Yamamoto (1995)** (doi: 10.1016/0304-4076(94)01616-8).
Volatilidad: **Bollerslev (1986)** (GARCH; doi: 10.1016/0304-4076(86)90063-1),
**Nelson (1991)** (EGARCH; doi: 10.2307/2938260) y **Glosten, Jagannathan & Runkle
(1993)** (GJR; doi: 10.1111/j.1540-6261.1993.tb05128.x).

## 6. El vacío que la tesis aborda

Tres brechas convergen: (i) la literatura macro-factorial rara vez estudia *empresas
individuales* en un mercado emergente delgado con escasos *pure-plays* de cobre; (ii) la
de *commodity currencies* es agregada y no separa, a nivel de empresa, el canal
precio-del-cobre del cambiario; (iii) la microestructura demuestra que la iliquidez está
valorada, pero casi ningún trabajo la modela como **moderadora de la velocidad e
intensidad con que un choque fundamental de cobre se incorpora a la valoración**. La
tesis integra un marco APT ampliado con el cobre como factor sectorial, la separación
de canales, la liquidez como moderadora del descubrimiento de precios y un arsenal
econométrico (VECM/ARDL/NARDL, Toda-Yamamoto, GARCH) para capturar largo plazo,
asimetrías y dinámica condicional.

---

*Verificar:* autoría/año exactos del DT N°310 del BCCh; DOI de Boyer & Filion (2007);
revisita de Chen-Roll-Ross; DOI de Johansen (1991). El resto tiene autor, año, revista
y DOI/URL confirmados.
