# 📦 Fase 5 — Documentación final y entregables

> **Pre-requisito:** Fases 1-4 completadas. Capturas en `capturas/`. Bitácora actualizada en cada fase.

---

## 🎯 Objetivo

Generar el `README.md` final, completar la BITACORA con un resumen ejecutivo, y dejar la carpeta lista para que el estudiante la suba como entrega.

**Definition of Done:**
- [ ] `README.md` existe en la raíz, en español, con instrucciones para reproducir el proyecto.
- [ ] `BITACORA.md` tiene un **resumen ejecutivo** al inicio.
- [ ] `.gitignore` existe y excluye `venv/`, `__pycache__/`, `*.log`.
- [ ] La estructura de carpetas coincide con la prevista en `INSTRUCCIONES_AGENTE.md`.
- [ ] Existe un archivo `RESUMEN_ENTREGA.md` con un checklist final.

---

## 📋 Tareas

### 5.1 · Crear `README.md`

Crea el archivo `README.md` en la raíz con este contenido (puedes adaptarlo si en fases anteriores hubo decisiones distintas, pero conserva la estructura):

```markdown
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
├── docs/
│   ├── fase_1_entorno.md
│   ├── fase_2_api.md
│   ├── fase_3_dashboard.md
│   ├── fase_4_integracion.md
│   └── fase_5_entrega.md
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
Salida: `🚀 API corriendo en http://127.0.0.1:5000`

**Terminal 2 — Dashboard:**
```bash
python Dashboard.py
```
Salida: `🚀 Dashboard corriendo en http://127.0.0.1:8050`

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
```

### 5.2 · Crear `.gitignore`

Crea el archivo `.gitignore` en la raíz:

```
# Entorno virtual
venv/
.venv/

# Python
__pycache__/
*.pyc
*.pyo

# Logs y temporales
*.log
api.log
dashboard.log

# Sistema operativo
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
```

### 5.3 · Completar el resumen ejecutivo de BITACORA.md

Vuelve a abrir `BITACORA.md`. En la sección "Resumen ejecutivo" (al inicio) escribe un texto similar a:

```markdown
## Resumen ejecutivo

Se desarrolló e implementó el proyecto **EA1: Desarrollo de un Dashboard básico**
para la asignatura del programa de Ingeniería Mecatrónica de IU Digital de
Antioquia. El sistema consiste en una API REST Flask que gestiona datos de
sensores almacenados en `sensores.json` con cinco endpoints (GET-todos,
GET-por-id, POST, PUT, DELETE), validaciones de tipo, rango y unicidad; y un
dashboard interactivo en Dash que consume esa API cada dos segundos y
presenta filtros (tipo de sensor, sensor_id, rango temporal), tres
indicadores (promedio, mínimo, máximo) y un gráfico de líneas con las
mediciones a lo largo del tiempo.

El desarrollo se ejecutó en cinco fases: preparación del entorno (venv +
dependencias), construcción y prueba unitaria de la API, construcción del
Dashboard, pruebas integradas con verificación del refresco automático, y
generación de documentación final. Todas las pruebas pasaron, incluida la
prueba en vivo donde un POST a la API se reflejó en el dashboard sin
recargar el navegador en aproximadamente dos segundos.

**Tiempo total invertido:** [X horas / minutos]
**Sistema operativo de desarrollo:** [Linux / macOS / Windows]
**Versión de Python:** [3.X.X]
**Resultado:** ✅ Todos los criterios del enunciado se cumplen.
```

### 5.4 · Crear `RESUMEN_ENTREGA.md`

Crea este archivo en la raíz para que el estudiante tenga un checklist claro de qué entregar:

```markdown
# 📤 RESUMEN DE ENTREGA — EA1

## ✅ Checklist contra el enunciado

### Parte 1: API básica
- [x] Carga `sensores.json` al iniciar y mantiene los datos en memoria.
- [x] `GET /sensors/` devuelve todos los datos.
- [x] `GET /sensors/<id>` devuelve los datos del sensor específico.
- [x] `POST /sensors/` agrega un nuevo sensor.
- [x] `PUT /sensors/<id>` actualiza un sensor.
- [x] `DELETE /sensors/<id>` elimina un sensor.
- [x] POST/PUT/DELETE persisten al archivo `sensores.json` en tiempo real.
- [x] Validación: `type` ∈ {temperatura, presion, velocidad}.
- [x] Validación: rangos de `value` por tipo.
- [x] Validación: `sensor_id` único.

### Parte 2: Dashboard interactivo
- [x] Construido con Dash y consume la API.
- [x] Dropdown para tipo de sensor.
- [x] Dropdown para `sensor_id`.
- [x] RangeSlider para rango temporal.
- [x] Gráfico interactivo de mediciones vs tiempo.
- [x] Indicadores: promedio, mínimo, máximo.
- [x] `dcc.Interval` actualizando cada 2 s.

### Documentación
- [x] Comentarios explicativos en el código.
- [x] `README.md` con instrucciones de configuración y ejecución.
- [x] Pruebas de los endpoints con curl (capturas en `capturas/`).
- [x] Capturas del dashboard con distintos filtros.
- [x] `requirements.txt` con dependencias.

## 📁 Archivos a entregar

Comprime y sube la carpeta `proyecto_dashboard/` completa, **excluyendo**:
- `venv/`
- `__pycache__/`
- `*.log`

(El archivo `.gitignore` ya define estas exclusiones).

## 🎬 Para la sustentación

Si el profesor pide una demo en vivo:
1. Abrir dos terminales y arrancar API y Dashboard.
2. Mostrar el dashboard con los datos cargados.
3. Demostrar los filtros (cambio de tipo, cambio de id, slider).
4. Mostrar el refresco automático: hacer un POST con curl/Postman desde
   una tercera terminal y mostrar cómo aparece en el dashboard sin recargar.
5. Mencionar las validaciones (POST con valor fuera de rango → 400).
```

### 5.5 · Verificación final

Ejecuta este script de verificación (puedes nombrarlo `verificar_entrega.py`, ejecutarlo y borrarlo):

```python
import os, json

archivos_requeridos = [
    "API.py", "Dashboard.py", "sensores.json",
    "requirements.txt", "README.md", "BITACORA.md",
    "INSTRUCCIONES_AGENTE.md", ".gitignore",
    "RESUMEN_ENTREGA.md",
    "docs/fase_1_entorno.md", "docs/fase_2_api.md",
    "docs/fase_3_dashboard.md", "docs/fase_4_integracion.md",
    "docs/fase_5_entrega.md",
]

print("=== Verificación de entrega ===")
faltan = []
for archivo in archivos_requeridos:
    if not os.path.exists(archivo):
        faltan.append(archivo)
        print(f"  ❌ FALTA: {archivo}")
    else:
        print(f"  ✅ {archivo}")

# Verificar JSON
try:
    with open("sensores.json") as f:
        datos = json.load(f)
    print(f"\n  📦 sensores.json: {len(datos)} registros")
except Exception as e:
    print(f"\n  ❌ sensores.json corrupto: {e}")

# Verificar capturas
if os.path.isdir("capturas"):
    capturas = [f for f in os.listdir("capturas") if f.endswith(".png")]
    print(f"  🖼️  capturas/: {len(capturas)} archivos PNG")
else:
    print("  ⚠️ Carpeta capturas/ no existe")

if not faltan:
    print("\n🎉 Todo listo para entregar.")
else:
    print(f"\n⚠️ Faltan {len(faltan)} archivos. Revisa la lista anterior.")
```

Si todo sale ✅, la fase 5 está completa.

### 5.6 · Limpiar archivos temporales

```bash
# Linux/Mac
rm -rf __pycache__ *.log verificar_entrega.py verificar_entorno.py 2>/dev/null

# Windows
rmdir /S /Q __pycache__ 2>nul
del *.log verificar_entrega.py verificar_entorno.py 2>nul
```

---

## 📝 Actualización final en BITACORA.md

```markdown
## Fase 5 — Entrega  ✅

**Inicio:** [hora]
**Fin:** [hora]

### Archivos generados
- `README.md`
- `RESUMEN_ENTREGA.md`
- `.gitignore`
- Resumen ejecutivo agregado al inicio de BITACORA.md

### Verificación final
- ✅ 14 archivos requeridos presentes
- ✅ `sensores.json` válido (15 registros)
- ✅ 6 capturas en `capturas/`
- ✅ Limpieza de archivos temporales completada

---

## 🏁 Cierre del proyecto

El proyecto EA1 quedó listo para entregar.
Todos los criterios del enunciado se cumplen.
Ver `RESUMEN_ENTREGA.md` para el checklist contra el enunciado original.
```

---

## 🎬 Mensaje final al estudiante

Cuando todo esté listo, el agente debe decir al estudiante algo como:

> "He completado las 5 fases del proyecto EA1. La carpeta del proyecto contiene todo lo necesario para entregar: el código fuente con comentarios en español (API.py y Dashboard.py), el archivo de datos (sensores.json), las dependencias (requirements.txt), la documentación completa (README.md), una bitácora detallada del desarrollo (BITACORA.md), las capturas de las pruebas y el dashboard funcionando, y un resumen de entrega con el checklist contra el enunciado. Para subir, comprime la carpeta `proyecto_dashboard/` excluyendo `venv/` (el `.gitignore` ya lo hace si usas Git). ¿Quieres que prepare un .zip listo o prefieres revisar algo antes?"
