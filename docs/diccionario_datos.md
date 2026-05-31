# Diccionario de datos

> Toda serie documenta: código, descripción, fuente, frecuencia nativa, unidad,
> transformación aplicada, canal económico y fecha de descarga (2026-05-30).

## A. Variable dependiente — precios de activos (`data/raw/precios_activos.csv`)

| Código | Empresa | Anillo | Mercado | Moneda | Fuente | Frec. | Unidad |
|---|---|---|---|---|---|---|---|
| `ANTO.L` | Antofagasta plc | A (núcleo cobre) | LSE | GBp | Yahoo (auto_adjust) | Diaria | Precio cierre ajustado |
| `PUCOBRE.SN` | Pucobre | A (núcleo cobre) | Santiago | CLP | Yahoo | Diaria | Precio cierre ajustado |
| `CAP.SN` | CAP S.A. | B (materiales) | Santiago | CLP | Yahoo | Diaria | Precio cierre ajustado |
| `SQM-B.SN` | SQM-B | B (materiales) | Santiago | CLP | Yahoo | Diaria | Precio cierre ajustado |
| `SCCO` | Southern Copper | C (ref. int'l) | NYSE | USD | Yahoo | Diaria | Precio cierre ajustado |
| `FCX` | Freeport-McMoRan | C (ref. int'l) | NYSE | USD | Yahoo | Diaria | Precio cierre ajustado |
| `BHP` | BHP | C (ref. int'l) | NYSE | USD | Yahoo | Diaria | Precio cierre ajustado |
| `GLEN.L` | Glencore | C (ref. int'l) | LSE | GBp | Yahoo | Diaria | Precio cierre ajustado (desde 2011) |

## B. Factores de mercado (`data/raw/factores_yahoo.csv`)

| Código | Descripción | Unidad | Canal económico |
|---|---|---|---|
| `cobre_comex` (`HG=F`) | Futuro cobre COMEX | USD/lb | **Demanda/ingreso** — driver directo del sector |
| `usdclp` (`CLP=X`) | Tipo de cambio USD/CLP | CLP/USD | **Moneda** — traspaso a ingresos/costos y valoración |
| `dxy` (`DX-Y.NYB`) | Índice dólar | índice | **Moneda global** — inverso de commodities |
| `vix` (`^VIX`) | Volatilidad implícita S&P500 | índice | **Riesgo/sentimiento** global |
| `sp500` (`^GSPC`) | S&P 500 | índice | **Mercado global** (beta) |
| `ipsa` (`^IPSA`) | IPSA Chile | índice | **Mercado local** (beta local) |
| `ust10y` (`^TNX`) | Rendimiento UST 10Y | % | **Tasa de descuento** larga |
| `ust5y` (`^FVX`) | Rendimiento UST 5Y | % | Descuento medio |
| `ust13w` (`^IRX`) | T-bill 13 semanas | % | **Tasa corta** EEUU |
| `wti` (`CL=F`) | Petróleo WTI | USD/bbl | **Costo de energía** minera |

## C. Macro FRED (`data/raw/factores_fred.csv`) — complementario

| Código | Descripción | Frec. | Canal | Estado |
|---|---|---|---|---|
| `PCOPPUSDM` | Precio global cobre | Mensual | Demanda (baja frec.) | según disponibilidad red |
| `T10Y2Y` | Pendiente curva 10Y-2Y | Diaria | Ciclo/recesión | " |
| `INDPRO` | Producción industrial EEUU | Mensual | Demanda global | " |
| `DTWEXBGS` | Dólar amplio | Diaria | Moneda | " |

## D. Macro Chile — `mindicador.cl` (`data/raw/macro_chile.csv`) — SIN credenciales

| Código | Descripción | Frec. | Unidad | Canal | Estado |
|---|---|---|---|---|---|
| `tpm` | Tasa de Política Monetaria | Diaria | % | Descuento local | **incorporada** (5.560 obs) |
| `imacec` | Actividad económica | Mensual | var% | Demanda interna | incorporada (267) |
| `ipc` | Inflación | Mensual | var% | Precios/UF | incorporada (264) |
| `dolar` | Dólar observado oficial | Diaria | CLP/USD | Moneda (oficial) | incorporada (5.587) |

Transformaciones: `tpm` (nivel %) y `d_tpm` (cambio diario, puntos %). IMACEC/IPC
quedan para modelos mensuales.

## D-bis. Banco Central de Chile (`data/raw/macro_bcch.csv`) — requiere credenciales

| Código | Descripción | Canal | Estado |
|---|---|---|---|
| EMBI Chile | Riesgo soberano | Riesgo país | requiere `BCCH_USER/PASS` |
| BCU/BTU | Tasas largas locales | Descuento | " |

## Transformaciones (en `data/processed/`)

- `ret_<código>`: log-retorno diario `ln(P_t/P_{t-1})` (×100 para %). Base I(0).
- `lprice_<código>`: log-precio `ln(P_t)`. Para cointegración (I(1) esperado).
- `dl_<factor>`: variación log del factor (cobre, dxy, usdclp, sp500, ipsa, wti).
- `d_<tasa>`: primera diferencia de tasas en nivel (ust10y, etc.).
- Winsorización al 0.5%/99.5% sólo para diagnóstico de outliers (versión `_w`).
