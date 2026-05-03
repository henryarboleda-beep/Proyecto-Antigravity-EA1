"""
============================================================
 Dashboard.py  —  Dashboard interactivo con Dash
 EA1: Desarrollo de un Dashboard basico
 IU Digital de Antioquia - Ingenieria Mecatronica
============================================================

Consume la API Flask (API.py) cada 2 segundos y muestra:
    - Dropdown para tipo de sensor (temperatura/presion/velocidad)
    - Dropdown para sensor_id
    - DatePickerRange para filtrar por fecha
    - Grafico de lineas con valores vs tiempo
    - Tarjetas con indicadores: promedio, minimo, maximo

ATENCION:  Antes de ejecutar este archivo, asegurate de que API.py
    ya este corriendo en otra terminal (puerto 5000).
"""

import dash
from dash import dcc, html, Input, Output
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests

# URL base de la API REST que provee los datos de sensores
API_URL = "http://127.0.0.1:5000/sensors/"

# Instancia principal de la aplicacion Dash
app = dash.Dash(__name__)
app.title = "Dashboard de Sensores - EA1"


def obtener_datos():
    """Consulta la API y devuelve un DataFrame con los sensores."""
    try:
        # Realizar peticion GET a la API con timeout de 2 segundos
        respuesta = requests.get(API_URL, timeout=2)
        respuesta.raise_for_status()
        # Convertir la respuesta JSON a un DataFrame de pandas
        df = pd.DataFrame(respuesta.json())
        if not df.empty:
            # Convertir la columna timestamp a formato datetime para facilitar filtros
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            # Eliminar filas con timestamps invalidos (NaT)
            df = df.dropna(subset=["timestamp"])
        return df
    except Exception as e:
        print(f"WARN  No se pudo consultar la API: {e}")
        # Retornar DataFrame vacio con las columnas esperadas para evitar errores
        return pd.DataFrame(columns=["sensor_id", "type", "value", "timestamp"])


# Consulta inicial a la API al arrancar para obtener las fechas limite
# Esto permite configurar el DatePickerRange de forma estatica en el layout,
# evitando que el callback del Interval lo sobrescriba cada 2 segundos
_df_init = obtener_datos()
if not _df_init.empty:
    _min_date = _df_init["timestamp"].min().date()
    _max_date = _df_init["timestamp"].max().date()
else:
    # Valores por defecto si la API no esta disponible al arrancar
    _min_date = date(2026, 1, 1)
    _max_date = date(2026, 12, 31)


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
        html.H1("Dashboard de Sensores",
                style={"color": "#0A2540", "marginBottom": "4px"}),
        html.P("EA1 - Monitoreo en tiempo real - IU Digital de Antioquia",
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
                    dcc.DatePickerRange(
                        id="date-picker-range",
                        display_format="YYYY-MM-DD",
                        min_date_allowed=_min_date,
                        max_date_allowed=_max_date,
                        start_date=_min_date,
                        end_date=_max_date,
                        style={"marginTop": "5px"},
                    ),
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

        # Componente Interval: dispara el callback de refresco cada 2000 ms (2 segundos)
        dcc.Interval(id="interval", interval=2000, n_intervals=0),
        # Store: almacena los datos en el navegador del cliente para compartir entre callbacks
        dcc.Store(id="store-data"),
    ],
)


# ----------------------------------------------------------
# Callback 1: Refrescar datos cada 2s (NO toca el calendario)
# ----------------------------------------------------------
@app.callback(
    Output("store-data",    "data"),
    Output("dropdown-tipo", "options"),
    Output("dropdown-id",   "options"),
    Input("interval",       "n_intervals"),
)
def refrescar_datos(_n):
    """Consulta la API cada 2s y actualiza el Store y los dropdowns."""
    df = obtener_datos()
    if df.empty:
        return [], [], []

    # Construir las opciones para el dropdown de tipos (temperatura, presion, velocidad)
    tipos = [{"label": t.capitalize(), "value": t}
             for t in sorted(df["type"].unique())]
    # Construir las opciones para el dropdown de IDs de sensor
    ids = [{"label": f"Sensor {int(i)}", "value": int(i)}
           for i in sorted(df["sensor_id"].unique())]

    # Convertir timestamps a string para poder serializar en el Store (JSON)
    df["timestamp"] = df["timestamp"].astype(str)
    return df.to_dict("records"), tipos, ids


# ----------------------------------------------------------
# Callback 2: Actualizar grafico e indicadores
# ----------------------------------------------------------
@app.callback(
    Output("grafico-temporal", "figure"),
    Output("indicadores",      "children"),
    Output("rango-texto",      "children"),
    Input("store-data",        "data"),
    Input("dropdown-tipo",     "value"),
    Input("dropdown-id",       "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def actualizar_vista(data, tipo, sensor_id, start_date, end_date):
    """Filtra los datos segun los controles y actualiza el grafico y los KPIs."""
    # Si no hay datos cargados, mostrar mensaje y tarjetas vacias
    if not data:
        figura = go.Figure().update_layout(
            title="No hay datos disponibles",
            template="simple_white")
        return figura, [tarjeta("Promedio", "--"),
                        tarjeta("Minimo", "--"),
                        tarjeta("Maximo", "--")], ""

    # Reconstruir el DataFrame desde los registros del Store
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Aplicar filtro por tipo de sensor si el usuario selecciono uno
    if tipo:
        df = df[df["type"] == tipo]
    # Aplicar filtro por sensor_id si el usuario selecciono uno
    if sensor_id is not None:
        df = df[df["sensor_id"] == sensor_id]

    # Aplicar filtro de rango temporal si ambas fechas estan definidas
    rango_texto = ""
    if start_date and end_date and not df.empty:
        try:
            # Tomar solo la parte YYYY-MM-DD del string para evitar problemas de formato
            t_min = pd.to_datetime(str(start_date)[:10])
            # Agregar 23:59:59 al final del dia para incluir todo el dia seleccionado
            t_max = pd.to_datetime(str(end_date)[:10]) + pd.Timedelta(hours=23, minutes=59, seconds=59)
            df = df[(df["timestamp"] >= t_min) & (df["timestamp"] <= t_max)]
            rango_texto = f"Desde {t_min.strftime('%Y-%m-%d')} hasta {t_max.strftime('%Y-%m-%d')}"
        except Exception as e:
            print(f"Error parsing dates: {e}")

    # Si despues de filtrar no quedan datos, mostrar mensaje informativo
    if df.empty:
        figura = go.Figure().update_layout(
            title="Sin datos para los filtros seleccionados",
            template="simple_white")
        return figura, [tarjeta("Promedio", "--"),
                        tarjeta("Minimo", "--"),
                        tarjeta("Maximo", "--")], rango_texto

    # Ordenar por timestamp y crear el grafico de lineas con Plotly Express
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

    # Calcular indicadores estadisticos (KPIs) sobre los datos filtrados
    promedio = df["value"].mean()
    minimo   = df["value"].min()
    maximo   = df["value"].max()

    kpis = [
        tarjeta("Promedio", f"{promedio:.2f}", color="#0066CC"),
        tarjeta("Minimo",   f"{minimo:.2f}",   color="#00C896"),
        tarjeta("Maximo",   f"{maximo:.2f}",   color="#FF7847"),
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


# Punto de entrada: arranca el servidor de Dash en el puerto 8050
if __name__ == "__main__":
    print("OK Dashboard corriendo en http://127.0.0.1:8050")
    print("INFO Recuerda: API.py debe estar corriendo en el puerto 5000.")
    app.run(debug=True, port=8050)
