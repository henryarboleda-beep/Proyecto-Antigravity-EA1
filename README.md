# EA1 · Desarrollo de un Dashboard básico

**IU Digital de Antioquia · Ingeniería Mecatrónica**
Sistema de monitoreo de sensores con API REST (Flask) y dashboard interactivo (Dash).

---

## 📋 Descripción

Este proyecto contiene dos aplicaciones que corren simultáneamente:

1. **API REST (`API.py`)** — Flask, expone `sensores.json` mediante 5 endpoints HTTP con validaciones de rango y unicidad.
2. **Dashboard (`Dashboard.py`)** — Dash, consume la API cada 2 segundos y muestra gráficos, indicadores y filtros interactivos.

```
┌────────────────┐    HTTP    ┌──────────┐    HTTP    ┌─────────────┐
│ sensores.json  │  <──────>  │ API.py   │  <──────>  │ Dashboard.py│
│   (archivo)    │            │ Flask    │            │   Dash      │
└────────────────┘            │ :5000    │            │   :8050     │
                              └──────────┘            └─────────────┘
```

## 📁 Estructura

```
proyecto_dashboard/
├── API.py
├── Dashboard.py
├── sensores.json
├── requirements.txt
├── README.md
├── BITACORA.md
├── INSTRUCCIONES_AGENTE.md
├── fase_1_entorno.md
├── fase_2_api.md
├── fase_3_dashboard.md
├── fase_4_integracion.md
├── fase_5_entrega.md
└── capturas/
```

## ⚙️ Instalación

### 1. Requisitos
- Python 3.9+
- pip

### 2. Crear entorno virtual

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Ejecución

Abre **dos terminales** con el venv activo en cada una.

**Terminal 1 — API:**
```bash
python API.py
```
Salida: `OK API corriendo en http://127.0.0.1:5000`

**Terminal 2 — Dashboard:**
```bash
python Dashboard.py
```
Salida: `OK Dashboard corriendo en http://127.0.0.1:8050`

Abre en el navegador: **http://127.0.0.1:8050**

## 🌐 Endpoints

| Método | Ruta              | Descripción                                |
|--------|-------------------|--------------------------------------------|
| GET    | `/sensors/`       | Lista todos los sensores                   |
| GET    | `/sensors/<id>`   | Devuelve los registros de un sensor_id     |
| POST   | `/sensors/`       | Crea un nuevo registro                     |
| PUT    | `/sensors/<id>`   | Actualiza un registro                      |
| DELETE | `/sensors/<id>`   | Elimina los registros de un sensor_id      |

## 🔬 Validaciones

- `type`: solo `"temperatura"`, `"presion"` o `"velocidad"`.
- Rangos: temperatura `[-10, 100]`, presion `[0, 500]`, velocidad `[0, 150]`.
- `sensor_id` único al crear con POST.
- `timestamp` en formato ISO 8601.

## 🧪 Pruebas con curl

```bash
# Listar
curl http://127.0.0.1:5000/sensors/

# Crear
curl -X POST http://127.0.0.1:5000/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"sensor_id":10,"type":"temperatura","value":28.5,"timestamp":"2026-04-28T12:00:00"}'

# Actualizar
curl -X PUT http://127.0.0.1:5000/sensors/10 \
  -H "Content-Type: application/json" \
  -d '{"type":"temperatura","value":32.0,"timestamp":"2026-04-28T13:00:00"}'

# Borrar
curl -X DELETE http://127.0.0.1:5000/sensors/10
```

## 📊 Funcionalidad del Dashboard

- Dropdown "Tipo de sensor" — filtra por temperatura/presion/velocidad.
- Dropdown "Sensor ID" — filtra por sensor específico.
- RangeSlider — acota la ventana temporal.
- Tarjetas — Promedio, Mínimo y Máximo de las mediciones filtradas.
- Gráfico — valor en el tiempo, una línea por sensor_id.
- Refresco automático cada 2 s vía `dcc.Interval`.

## 📓 Bitácora

El archivo `BITACORA.md` documenta el proceso completo de desarrollo, ejecutado con Google Antigravity.

## 👤 Autor

Estudiante de Ingeniería Mecatrónica · IU Digital de Antioquia · 2026
