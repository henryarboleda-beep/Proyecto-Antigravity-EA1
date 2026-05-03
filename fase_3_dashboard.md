# 📊 Fase 3 — Construir el Dashboard

> **Pre-requisito:** Fase 2 completada. La API está probada y actualmente **detenida**.

---

## 🎯 Objetivo

Crear `Dashboard.py` (una app Dash que consume la API y muestra dropdowns, slider, gráfico e indicadores con refresco automático cada 2 segundos). Verificar que renderiza correctamente.

**Definition of Done:**
- [ ] `Dashboard.py` existe y arranca sin errores en el puerto 8050.
- [ ] Al abrir `http://127.0.0.1:8050` en el navegador se ve la interfaz completa.
- [ ] Los 3 controles (dropdown tipo, dropdown id, range slider) están presentes.
- [ ] Los 3 indicadores (promedio, mínimo, máximo) muestran valores numéricos.
- [ ] El gráfico de líneas muestra los datos.
- [ ] `BITACORA.md` Fase 3 está actualizada.

> En esta fase la **integración real** (probar el refresco de 2s con la API arrancada en paralelo) se hace en la **Fase 4**. Aquí solo validamos que el dashboard arranque y renderice.

---

## 📋 Tareas

### 3.1 · Crear `Dashboard.py`

Crea el archivo `Dashboard.py` en la raíz con **exactamente** este código:

```python
"""
============================================================
 Dashboard.py  —  Dashboard interactivo con Dash
 EA1: Desarrollo de un Dashboard básico
 IU Digital de Antioquia · Ingeniería Mecatrónica
============================================================

Consume la API Flask (API.py) cada 2 segundos y muestra:
    - Dropdown para tipo de sensor (temperatura/presion/velocidad)
    - Dropdown para sensor_id
    - RangeSlider para acotar un rango temporal
    - Gráfico de líneas con valores vs tiempo
    - Tarjetas con indicadores: promedio, mínimo, máximo

⚠️  Antes de ejecutar este archivo, asegúrate de que API.py
    ya esté corriendo en otra terminal (puerto 5000).
"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests

API_URL = "http://127.0.0.1:5000/sensors/"

app = dash.Dash(__name__)
app.title = "Dashboard de Sensores · EA1"


def obtener_datos():
    """Consulta la API y devuelve un DataFrame con los sensores."""
    try:
        respuesta = requests.get(API_URL, timeout=2)
        respuesta.raise_for_status()
        df = pd.DataFrame(respuesta.json())
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.dropna(subset=["timestamp"])
        return df
    except Exception as e:
        print(f"⚠️  No se pudo consultar la API: {e}")
        return pd.DataFrame(columns=["sensor_id", "type", "value", "timestamp"])


# ==========================================================
# LAYOUT
# ==========================================================
app.layout = html.Div(
    style={
        "fontFamily": "Inter, Arial, sans-serif",
        "padding": "24px",
        "backgroundColor": "#F0F3F7",
        "minHeight": "100vh",
    },
    children=[
        html.H1("📊 Dashboard de Sensores",
                style={"color": "#0A2540", "marginBottom": "4px"}),
        html.P("EA1 · Monitoreo en tiempo real · IU Digital de Antioquia",
               style={"color": "#8892B0", "marginTop": 0,
                      "marginBottom": "24px"}),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr 2fr",
                "gap": "20px",
                "background": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "marginBottom": "20px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
            },
            children=[
                html.Div([
                    html.Label("Tipo de sensor",
                               style={"fontWeight": 600, "fontSize": "13px"}),
                    dcc.Dropdown(id="dropdown-tipo", options=[],
                                 value=None,
                                 placeholder="Todos los tipos",
                                 clearable=True),
                ]),
                html.Div([
                    html.Label("Sensor ID",
                               style={"fontWeight": 600, "fontSize": "13px"}),
                    dcc.Dropdown(id="dropdown-id", options=[],
                                 value=None,
                                 placeholder="Todos los IDs",
                                 clearable=True),
                ]),
                html.Div([
                    html.Label("Rango temporal",
                               style={"fontWeight": 600, "fontSize": "13px"}),
                    dcc.RangeSlider(id="slider-tiempo",
                                    min=0, max=100, value=[0, 100],
                                    marks=None,
                                    tooltip={"placement": "bottom",
                                             "always_visible": False}),
                    html.Div(id="rango-texto",
                             style={"fontSize": "11px",
                                    "color": "#8892B0",
                                    "marginTop": "6px",
                                    "fontFamily": "monospace"}),
                ]),
            ],
        ),

        html.Div(id="indicadores",
                 style={"display": "grid",
                        "gridTemplateColumns": "repeat(3, 1fr)",
                        "gap": "20px",
                        "marginBottom": "20px"}),

        html.Div(
            style={"background": "white",
                   "padding": "20px",
                   "borderRadius": "12px",
                   "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"},
            children=[dcc.Graph(id="grafico-temporal")],
        ),

        dcc.Interval(id="interval", interval=2000, n_intervals=0),
        dcc.Store(id="store-data"),
    ],
)


@app.callback(
    Output("store-data",      "data"),
    Output("dropdown-tipo",   "options"),
    Output("dropdown-id",     "options"),
    Output("slider-tiempo",   "min"),
    Output("slider-tiempo",   "max"),
    Input("interval",         "n_intervals"),
)
def refrescar_datos(_n):
    df = obtener_datos()
    if df.empty:
        return [], [], [], 0, 1

    tipos = [{"label": t.capitalize(), "value": t}
             for t in sorted(df["type"].unique())]
    ids = [{"label": f"Sensor {int(i)}", "value": int(i)}
           for i in sorted(df["sensor_id"].unique())]

    t_min = df["timestamp"].min().timestamp()
    t_max = df["timestamp"].max().timestamp()
    if t_min == t_max:
        t_max = t_min + 1

    df["timestamp"] = df["timestamp"].astype(str)
    return df.to_dict("records"), tipos, ids, t_min, t_max


@app.callback(
    Output("grafico-temporal", "figure"),
    Output("indicadores",      "children"),
    Output("rango-texto",      "children"),
    Input("store-data",        "data"),
    Input("dropdown-tipo",     "value"),
    Input("dropdown-id",       "value"),
    Input("slider-tiempo",     "value"),
)
def actualizar_vista(data, tipo, sensor_id, rango):
    if not data:
        figura = go.Figure().update_layout(
            title="No hay datos disponibles",
            template="simple_white")
        return figura, [tarjeta("Promedio", "—"),
                        tarjeta("Mínimo", "—"),
                        tarjeta("Máximo", "—")], ""

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if tipo:
        df = df[df["type"] == tipo]
    if sensor_id is not None:
        df = df[df["sensor_id"] == sensor_id]

    rango_texto = ""
    if rango and not df.empty:
        t_min = pd.to_datetime(rango[0], unit="s")
        t_max = pd.to_datetime(rango[1], unit="s")
        df = df[(df["timestamp"] >= t_min) & (df["timestamp"] <= t_max)]
        rango_texto = (f"Desde {t_min.strftime('%Y-%m-%d %H:%M')} "
                       f"hasta {t_max.strftime('%Y-%m-%d %H:%M')}")

    if df.empty:
        figura = go.Figure().update_layout(
            title="Sin datos para los filtros seleccionados",
            template="simple_white")
        return figura, [tarjeta("Promedio", "—"),
                        tarjeta("Mínimo", "—"),
                        tarjeta("Máximo", "—")], rango_texto

    df = df.sort_values("timestamp")
    figura = px.line(
        df, x="timestamp", y="value", color="sensor_id",
        markers=True,
        title="Mediciones a lo largo del tiempo",
        labels={"timestamp": "Tiempo",
                "value":     "Valor",
                "sensor_id": "Sensor"},
    )
    figura.update_layout(template="simple_white",
                         margin=dict(l=20, r=20, t=50, b=20))

    promedio = df["value"].mean()
    minimo   = df["value"].min()
    maximo   = df["value"].max()

    kpis = [
        tarjeta("Promedio", f"{promedio:.2f}", color="#0066CC"),
        tarjeta("Mínimo",   f"{minimo:.2f}",   color="#00C896"),
        tarjeta("Máximo",   f"{maximo:.2f}",   color="#FF7847"),
    ]

    return figura, kpis, rango_texto


def tarjeta(titulo, valor, color="#0A2540"):
    """Tarjeta de indicador (KPI)."""
    return html.Div(
        style={"background": "white",
               "padding": "20px",
               "borderRadius": "12px",
               "textAlign": "center",
               "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"},
        children=[
            html.Div(titulo, style={"fontSize": "13px",
                                    "color": "#8892B0",
                                    "textTransform": "uppercase",
                                    "letterSpacing": "1.5px"}),
            html.Div(valor, style={"fontSize": "32px",
                                   "fontWeight": 700,
                                   "color": color,
                                   "marginTop": "8px"}),
        ],
    )


if __name__ == "__main__":
    print("🚀 Dashboard corriendo en http://127.0.0.1:8050")
    print("ℹ️  Recuerda: API.py debe estar corriendo en el puerto 5000.")
    app.run(debug=True, port=8050)
```

### 3.2 · Verificación sintáctica

Antes de arrancarlo, comprueba que importa sin errores:

```bash
python -c "import Dashboard; print('OK')"
```

Debe imprimir `OK`. Si hay errores de import, repasa que el archivo se haya creado completo.

### 3.3 · Arrancar la API (de nuevo)

Para que el dashboard tenga datos que mostrar, la API debe estar corriendo. Vuelve a arrancarla en background:

| OS              | Comando                                          |
|-----------------|--------------------------------------------------|
| Linux / macOS   | `python API.py > api.log 2>&1 &`                 |
| Windows         | Abre una terminal aparte y ejecuta `python API.py` |

Espera 2-3 segundos y verifica con `curl http://127.0.0.1:5000/sensors/` que responde.

### 3.4 · Arrancar el Dashboard

Lanza Dash **también en background** (o en una terminal aparte):

| OS              | Comando                                                    |
|-----------------|------------------------------------------------------------|
| Linux / macOS   | `python Dashboard.py > dashboard.log 2>&1 &`               |
| Windows         | Otra terminal: `python Dashboard.py`                       |

Espera **5-10 segundos** (Dash tarda más en arrancar que Flask).

### 3.5 · Verificar que renderiza

#### Verificación headless (texto)
```bash
curl -s http://127.0.0.1:8050/ | grep -o "<title>[^<]*</title>"
```
Debe imprimir `<title>Dashboard de Sensores · EA1</title>`.

#### Verificación visual (navegador)
Si tu entorno (Antigravity con browser-in-the-loop) puede abrir un navegador:

1. Abre `http://127.0.0.1:8050`.
2. Espera a que cargue (puede tardar 2-4 s en hacer la primera consulta a la API).
3. Verifica que ves:
   - Título "📊 Dashboard de Sensores"
   - Dos dropdowns y un slider en una fila
   - Tres tarjetas (Promedio, Mínimo, Máximo) con valores numéricos
   - Un gráfico de líneas con datos

📸 **Captura obligatoria:** `capturas/04_dashboard_inicial.png` con la vista completa.

#### Si el navegador muestra "No hay datos disponibles"
Significa que el dashboard no pudo conectarse a la API. Verifica:
- ¿La API está corriendo? `curl http://127.0.0.1:5000/sensors/`
- ¿`API_URL` en `Dashboard.py` apunta a `http://127.0.0.1:5000/sensors/`?
- Mira `dashboard.log` para errores.

### 3.6 · Detener procesos

Antes de cerrar la fase, detén tanto la API como el Dashboard:

| OS              | Comando                                                  |
|-----------------|----------------------------------------------------------|
| Linux / macOS   | `pkill -f "python API.py"; pkill -f "python Dashboard.py"` |
| Windows         | Cierra ambas terminales o `taskkill /F /IM python.exe`   |

> **Nota:** En la Fase 4 los volveremos a arrancar para hacer la prueba integrada con interacción.

---

## 📝 Actualización en BITACORA.md

Reemplaza la sección "Fase 3 — Dashboard" con:

```markdown
## Fase 3 — Dashboard  ✅

**Inicio:** [hora]
**Fin:** [hora]

### Archivos creados
- `Dashboard.py` (~210 líneas, 2 callbacks)

### Verificaciones
- ✅ Importa sin errores (`python -c "import Dashboard"`)
- ✅ API arrancada en :5000 antes de lanzar el dashboard
- ✅ Dashboard arrancado en :8050
- ✅ Título correcto en el HTML
- ✅ Navegador renderiza la interfaz completa

### Componentes visibles
- ✅ Dropdown "Tipo de sensor"
- ✅ Dropdown "Sensor ID"
- ✅ RangeSlider de tiempo
- ✅ Tarjetas Promedio / Mínimo / Máximo
- ✅ Gráfico de líneas con datos

### Incidencias
[Ninguna / o describir]

### Evidencias
- `capturas/04_dashboard_inicial.png`
```

---

## 🚦 Siguiente paso

Cuando esta fase esté completa, abre `docs/fase_4_integracion.md`.
