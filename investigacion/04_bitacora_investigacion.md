# Bitácora de la investigación

> Historia del proceso de investigación: decisiones, hitos, callejones y aprendizajes.
> Documenta *cómo* se construyó la tesis, no sólo el resultado.

## Fase 0 — Planteamiento y restricción crítica

El punto de partida fue una pregunta amplia —el impacto de variables macro-financieras
sobre la valoración bursátil del sector cobre en Chile— y una restricción que
condicionó todo: el universo de mineras de cobre cotizadas es mínimo. La primera
decisión metodológica fue **no asumir** qué empresas existen, sino resolverlo
empíricamente.

## Fase 1 — Resolución empírica del universo

Se probó la disponibilidad real de cada candidato descargando sus series. Hallazgo
clave: **Pucobre (PUCOBRE.SN) es el único *pure-play* de cobre listado directamente en
la Bolsa de Santiago**, mientras que **Antofagasta (ANTO.L)** cotiza en Londres. El
ticker PUCV.SN devolvía error 404; el correcto es PUCOBRE.SN. Este contraste
líquido/ilíquido se convirtió, sin estar previsto al inicio, en el eje de la tesis.

## Fase 2 — Datos

Precios y volúmenes de Yahoo Finance (2004–2026 diario). Macro de Chile vía la API
pública mindicador.cl (TPM, IMACEC, IPC, dólar observado), tras constatar que el
acceso al Banco Central requería credenciales y que FRED resultaba inaccesible desde
el entorno. Se documentó cada serie en un diccionario de datos. Un hallazgo de calidad:
la serie `^IPSA` de Yahoo era inconsistente post-2019, por lo que se sustituyó por el
ETF iShares MSCI Chile (ECH) como proxy del mercado local, registrando el costo
(componente cambiario) y controlándolo por VIF.

## Fase 3 — Pruebas previas

Estacionariedad por decisión cruzada (ADF, Phillips-Perron, KPSS): log-precios I(1),
retornos I(0). Confirmación con Zivot-Andrews (raíz unitaria robusta a quiebre).
Cointegración: Engle-Granger bivariado débil, pero Johansen multivariante con rango
r=1 para ambos *pure-plays*. Esto fijó el árbol de modelos (VECM para el largo plazo;
HAC/VAR para el corto).

## Fase 4 — Modelamiento

Se estimaron, en orden: regresión de retornos con errores HAC (impacto contemporáneo),
VAR con IRF/FEVD y causalidad de Granger, VECM (largo plazo), familia GARCH
(volatilidad), panel FE/RE (robustez sectorial), ARDL/NARDL (asimetría y bounds) y un
estudio de eventos de TPM. La pieza que cristalizó el hallazgo fue el contraste de la
elasticidad-cobre por horizonte.

## Fase 5 — El hallazgo central y su triangulación

Se documentó que la elasticidad-cobre de Pucobre crece monótonamente con el horizonte
(0.09 diaria → 0.42 a cinco días → 0.60 mensual → 0.75 de largo plazo), mientras que
en Antofagasta es alta en todos los horizontes. Para blindar el resultado se sumaron,
en una segunda iteración: quiebres estructurales endógenos (Quandt-Andrews), robustez
multi-proxy de la iliquidez (Amihud, % de días cero, Roll, volumen), causalidad de
Toda-Yamamoto (robusta a integración) y una validación fuera de muestra (Clark-West)
con un placebo (SQM, litio). Las seis vías convergen en la misma lectura.

## Fase 6 — Revisión de literatura y posicionamiento

Búsqueda dirigida de literatura real (con DOI): factores macro (Chen-Roll-Ross),
*commodity currencies* (Chen-Rogoff; De Gregorio-Labbé para Chile), iliquidez
(Amihud; Bekaert-Harvey-Lundblad; Lesmond et al.), evidencia aplicada
(Kilian-Park; Díaz-Hansen-Cabrera; Wallenstein-Mendiola-Chávez-Bedoya) y métodos
(Pesaran-Shin-Smith; Shin-Yu-Greenwood-Nimmo; Toda-Yamamoto; familia GARCH). El vacío
identificado: la iliquidez como **moderadora del descubrimiento de precios** de un
choque fundamental de cobre a nivel de empresa, poco explorado en Chile.

## Fase 7 — Documentación y difusión

Se produjo el documento de tesis (PDF y Word, con índices, figuras y tablas
numeradas), una presentación de defensa, y una plataforma web interactiva (proyecto
separado) con los resultados y un simulador. Todo el código y los datos quedaron en un
repositorio público, conforme a estándares de reproducibilidad.

## Aprendizajes metodológicos

1. **Resolver el universo con datos** antes de modelar evita supuestos frágiles.
2. La **iliquidez** no era una nota al pie: explica el resultado central.
3. Con **N pequeño** en el panel, la inferencia primaria debe venir de las series de
   tiempo por activo, no del panel.
4. La **triangulación** por métodos independientes es más persuasiva que un único test.
5. Reportar lo que **no** salió limpio (GARCH inestable en Pucobre; ARDL no unánime)
   fortalece la credibilidad en lugar de debilitarla.
