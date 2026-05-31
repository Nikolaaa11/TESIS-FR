# Plataforma web de la tesis — despliegue en Vercel

Sitio **estático** (HTML/CSS/JS + Chart.js) que presenta los resultados de la tesis
con estilo Apple (fondo blanco, tipografía Inter, gráficos interactivos). No
requiere build.

```
web/
├── index.html      # página única con todas las secciones
├── styles.css      # diseño estilo Apple
├── app.js          # gráficos Chart.js + tablas (datos reales)
├── data.js         # datos inyectados (generado por src/exportar_web_data.py)
├── data.json       # mismos datos en JSON
├── vercel.json     # configuración de despliegue
└── assets/figures/ # figuras Matplotlib del análisis
```

## Desplegar en Vercel (2 caminos)

### A. Desde GitHub (recomendado)
1. Entra a https://vercel.com → **Add New… → Project**.
2. Importa el repositorio `Nikolaaa11/TESIS-FR`.
3. En **Root Directory** selecciona **`web`**.
4. **Framework Preset:** *Other* (es estático, sin build).
5. **Deploy**. Vercel publica el sitio en segundos.

### B. Con Vercel CLI
```bash
npm i -g vercel
cd web
vercel --prod
```

## Regenerar los datos
Tras re-correr los modelos, actualiza los datos del sitio:
```bash
python src/exportar_web_data.py
```

Todos los números provienen de `outputs/tables/*.csv` (datos reales). Sin datos
inventados.
