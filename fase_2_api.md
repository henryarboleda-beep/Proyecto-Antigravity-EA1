# 🌐 Fase 2 — Construir y probar la API Flask

> **Pre-requisito:** Fase 1 completada. El entorno virtual está activo y las dependencias instaladas.

---

## 🎯 Objetivo

Crear el archivo `sensores.json` con datos de prueba y construir `API.py` (una API REST Flask con 5 endpoints y validaciones). Verificar que cada endpoint funciona correctamente.

**Definition of Done:**
- [ ] `sensores.json` existe con al menos 15 registros válidos.
- [ ] `API.py` existe y arranca sin errores en el puerto 5000.
- [ ] Los 5 endpoints responden correctamente cuando se les llama con curl.
- [ ] Las validaciones (rango, tipo, unicidad) rechazan entradas inválidas con código 400.
- [ ] `BITACORA.md` Fase 2 está actualizada con las pruebas y sus resultados.
- [ ] La API está **detenida** al cerrar la fase (la fase 3 la volverá a arrancar).

---

## 📋 Tareas

### 2.1 · Crear `sensores.json`

Crea el archivo `sensores.json` en la raíz del proyecto con el siguiente contenido **exacto**:

```json
[
  {"sensor_id": 1, "type": "temperatura", "value": 22.4, "timestamp": "2026-04-28T08:00:00"},
  {"sensor_id": 1, "type": "temperatura", "value": 23.1, "timestamp": "2026-04-28T08:15:00"},
  {"sensor_id": 1, "type": "temperatura", "value": 24.7, "timestamp": "2026-04-28T08:30:00"},
  {"sensor_id": 1, "type": "temperatura", "value": 26.3, "timestamp": "2026-04-28T08:45:00"},
  {"sensor_id": 1, "type": "temperatura", "value": 27.8, "timestamp": "2026-04-28T09:00:00"},
  {"sensor_id": 2, "type": "presion", "value": 101.5, "timestamp": "2026-04-28T08:00:00"},
  {"sensor_id": 2, "type": "presion", "value": 105.2, "timestamp": "2026-04-28T08:15:00"},
  {"sensor_id": 2, "type": "presion", "value": 110.8, "timestamp": "2026-04-28T08:30:00"},
  {"sensor_id": 2, "type": "presion", "value": 115.4, "timestamp": "2026-04-28T08:45:00"},
  {"sensor_id": 2, "type": "presion", "value": 112.1, "timestamp": "2026-04-28T09:00:00"},
  {"sensor_id": 3, "type": "velocidad", "value": 45.0, "timestamp": "2026-04-28T08:00:00"},
  {"sensor_id": 3, "type": "velocidad", "value": 48.5, "timestamp": "2026-04-28T08:15:00"},
  {"sensor_id": 3, "type": "velocidad", "value": 52.3, "timestamp": "2026-04-28T08:30:00"},
  {"sensor_id": 3, "type": "velocidad", "value": 55.7, "timestamp": "2026-04-28T08:45:00"},
  {"sensor_id": 3, "type": "velocidad", "value": 58.0, "timestamp": "2026-04-28T09:00:00"}
]
```

**Verificación:** ejecuta `python -c "import json; print(len(json.load(open('sensores.json'))))"`. Debe imprimir `15`.

### 2.2 · Crear `API.py`

Crea el archivo `API.py` en la raíz con **exactamente** este código (los comentarios en español son parte del entregable):

```python
"""
============================================================
 API.py  —  API REST de gestión de sensores
 EA1: Desarrollo de un Dashboard básico
 IU Digital de Antioquia · Ingeniería Mecatrónica
============================================================

Esta API expone endpoints HTTP para gestionar datos de sensores
almacenados en un archivo JSON (sensores.json).

Endpoints:
  GET    /sensors/             -> Lista todos los sensores
  GET    /sensors/<sensor_id>  -> Devuelve un sensor por su id
  POST   /sensors/             -> Crea un nuevo sensor
  PUT    /sensors/<sensor_id>  -> Actualiza un sensor existente
  DELETE /sensors/<sensor_id>  -> Elimina un sensor

Validaciones implementadas:
  - 'type' debe ser uno de: "temperatura", "presion", "velocidad"
  - Rangos válidos por tipo:
        temperatura: -10  a  100   (°C)
        presion:       0  a  500   (kPa)
        velocidad:     0  a  150   (m/s)
  - 'sensor_id' debe ser entero único (no se puede repetir).
  - 'timestamp' debe estar en formato ISO 8601.
"""

from flask import Flask, jsonify, request
import json
import os
from datetime import datetime
from threading import Lock

# ----------------------------------------------------------
# Configuración global
# ----------------------------------------------------------
app = Flask(__name__)

DATA_FILE = "sensores.json"

TIPOS_VALIDOS = {
    "temperatura": (-10, 100),   # °C
    "presion":     (0, 500),     # kPa
    "velocidad":   (0, 150),     # m/s
}

file_lock = Lock()
sensores = []


# ----------------------------------------------------------
# Utilidades de carga / guardado
# ----------------------------------------------------------
def cargar_datos():
    """Carga los sensores desde sensores.json al iniciar la aplicación."""
    global sensores
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        sensores = []
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            sensores = json.load(f)
    except (json.JSONDecodeError, OSError):
        sensores = []


def guardar_datos():
    """Persiste la lista 'sensores' al archivo JSON."""
    with file_lock:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(sensores, f, indent=2, ensure_ascii=False)


# ----------------------------------------------------------
# Validación
# ----------------------------------------------------------
def validar_sensor(data, requerir_id=True):
    """Valida un dict que viene del cliente.
    Retorna (True, None) si OK o (False, "mensaje") si error.
    """
    if not isinstance(data, dict):
        return False, "El cuerpo de la petición debe ser un objeto JSON."

    requeridos = ["type", "value", "timestamp"]
    if requerir_id:
        requeridos = ["sensor_id"] + requeridos
    for campo in requeridos:
        if campo not in data:
            return False, f"Falta el campo obligatorio: '{campo}'."

    tipo = str(data.get("type", "")).strip().lower()
    if tipo not in TIPOS_VALIDOS:
        return False, (
            f"Tipo no válido: '{data.get('type')}'. "
            f"Debe ser uno de: {list(TIPOS_VALIDOS.keys())}."
        )

    try:
        valor = float(data["value"])
    except (TypeError, ValueError):
        return False, "El campo 'value' debe ser numérico."
    minimo, maximo = TIPOS_VALIDOS[tipo]
    if not (minimo <= valor <= maximo):
        return False, (
            f"Valor fuera de rango para '{tipo}'. "
            f"Permitido: [{minimo}, {maximo}]. Recibido: {valor}."
        )

    try:
        datetime.fromisoformat(str(data["timestamp"]).replace("Z", "+00:00"))
    except ValueError:
        return False, "El campo 'timestamp' debe estar en formato ISO 8601."

    if requerir_id:
        try:
            nuevo_id = int(data["sensor_id"])
        except (TypeError, ValueError):
            return False, "El 'sensor_id' debe ser un número entero."
        if any(s["sensor_id"] == nuevo_id for s in sensores):
            return False, f"Ya existe un sensor con sensor_id = {nuevo_id}."

    return True, None


# ==========================================================
# ENDPOINTS
# ==========================================================

@app.route("/sensors/", methods=["GET"])
def listar_sensores():
    """GET /sensors/ -> Devuelve todos los sensores."""
    return jsonify(sensores), 200


@app.route("/sensors/<int:sensor_id>", methods=["GET"])
def obtener_sensor(sensor_id):
    """GET /sensors/<id> -> Devuelve los registros de un sensor_id."""
    coincidencias = [s for s in sensores if s["sensor_id"] == sensor_id]
    if not coincidencias:
        return jsonify({"error": f"No existe sensor con id {sensor_id}."}), 404
    return jsonify(coincidencias), 200


@app.route("/sensors/", methods=["POST"])
def crear_sensor():
    """POST /sensors/ -> Crea un nuevo sensor."""
    data = request.get_json(silent=True)
    ok, error = validar_sensor(data, requerir_id=True)
    if not ok:
        return jsonify({"error": error}), 400

    nuevo = {
        "sensor_id": int(data["sensor_id"]),
        "type":      str(data["type"]).strip().lower(),
        "value":     float(data["value"]),
        "timestamp": data["timestamp"],
    }
    sensores.append(nuevo)
    guardar_datos()
    return jsonify(nuevo), 201


@app.route("/sensors/<int:sensor_id>", methods=["PUT"])
def actualizar_sensor(sensor_id):
    """PUT /sensors/<id> -> Actualiza el sensor con ese sensor_id."""
    indice = next((i for i, s in enumerate(sensores)
                   if s["sensor_id"] == sensor_id), None)
    if indice is None:
        return jsonify({"error": f"No existe sensor con id {sensor_id}."}), 404

    data = request.get_json(silent=True)
    ok, error = validar_sensor(data, requerir_id=False)
    if not ok:
        return jsonify({"error": error}), 400

    sensores[indice]["type"]      = str(data["type"]).strip().lower()
    sensores[indice]["value"]     = float(data["value"])
    sensores[indice]["timestamp"] = data["timestamp"]
    guardar_datos()
    return jsonify(sensores[indice]), 200


@app.route("/sensors/<int:sensor_id>", methods=["DELETE"])
def eliminar_sensor(sensor_id):
    """DELETE /sensors/<id> -> Elimina TODAS las entradas con ese sensor_id."""
    global sensores
    cantidad_antes = len(sensores)
    sensores = [s for s in sensores if s["sensor_id"] != sensor_id]
    eliminados = cantidad_antes - len(sensores)

    if eliminados == 0:
        return jsonify({"error": f"No existe sensor con id {sensor_id}."}), 404

    guardar_datos()
    return jsonify({
        "mensaje": f"Sensor {sensor_id} eliminado.",
        "registros_eliminados": eliminados
    }), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada."}), 404

@app.errorhandler(405)
def not_allowed(e):
    return jsonify({"error": "Método HTTP no permitido en esta ruta."}), 405


if __name__ == "__main__":
    cargar_datos()
    print(f"📦 Cargados {len(sensores)} registros desde {DATA_FILE}")
    print("🚀 API corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
```

### 2.3 · Arrancar la API

Asumiendo `venv` activo, ejecuta la API **en segundo plano** para poder probarla con curl en la misma terminal o en otra:

| OS              | Comando                                          |
|-----------------|--------------------------------------------------|
| Linux / macOS   | `python API.py > api.log 2>&1 &`                 |
| Windows (cmd)   | `start /B python API.py > api.log 2>&1`          |
| Antigravity     | Lanza la terminal integrada en una pestaña aparte y deja `python API.py` corriendo allí. |

Espera **2-3 segundos** para que arranque. Luego verifica:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5000/sensors/
```

Debe imprimir `200`. Si imprime `000` o falla, mira `api.log` para ver el error.

📸 **Captura:** `capturas/01_api_arrancada.png` mostrando la consola con los mensajes de arranque.

### 2.4 · Probar los 5 endpoints

Ejecuta cada prueba **en orden** y registra resultado + código HTTP en BITACORA.

#### Test 1: GET todos
```bash
curl -s -w "\nHTTP %{http_code}\n" http://127.0.0.1:5000/sensors/
```
**Esperado:** lista JSON con 15 elementos · HTTP 200.

#### Test 2: GET por id
```bash
curl -s -w "\nHTTP %{http_code}\n" http://127.0.0.1:5000/sensors/1
```
**Esperado:** lista con los 5 registros del sensor 1 · HTTP 200.

#### Test 3: POST válido
```bash
curl -s -w "\nHTTP %{http_code}\n" -X POST http://127.0.0.1:5000/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"sensor_id": 99, "type": "temperatura", "value": 30.5, "timestamp": "2026-04-28T10:00:00"}'
```
**Esperado:** el sensor creado · HTTP 201.

#### Test 4: POST inválido (valor fuera de rango)
```bash
curl -s -w "\nHTTP %{http_code}\n" -X POST http://127.0.0.1:5000/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"sensor_id": 100, "type": "temperatura", "value": 999, "timestamp": "2026-04-28T10:00:00"}'
```
**Esperado:** mensaje de error con "Valor fuera de rango" · HTTP 400.

#### Test 5: POST con sensor_id duplicado
```bash
curl -s -w "\nHTTP %{http_code}\n" -X POST http://127.0.0.1:5000/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"sensor_id": 99, "type": "temperatura", "value": 30.5, "timestamp": "2026-04-28T10:00:00"}'
```
**Esperado:** mensaje "Ya existe un sensor con sensor_id = 99" · HTTP 400.

#### Test 6: PUT
```bash
curl -s -w "\nHTTP %{http_code}\n" -X PUT http://127.0.0.1:5000/sensors/99 \
  -H "Content-Type: application/json" \
  -d '{"type": "temperatura", "value": 35.0, "timestamp": "2026-04-28T11:00:00"}'
```
**Esperado:** el sensor actualizado · HTTP 200.

#### Test 7: DELETE
```bash
curl -s -w "\nHTTP %{http_code}\n" -X DELETE http://127.0.0.1:5000/sensors/99
```
**Esperado:** mensaje de eliminación · HTTP 200.

#### Test 8: GET inexistente
```bash
curl -s -w "\nHTTP %{http_code}\n" http://127.0.0.1:5000/sensors/9999
```
**Esperado:** error · HTTP 404.

📸 **Captura:** `capturas/02_curl_get_todos.png` y `capturas/03_curl_post_invalido.png` mostrando dos de las pruebas representativas.

### 2.5 · Verificar persistencia

Después de los tests:
```bash
cat sensores.json | python -m json.tool | head -20
```
**Esperado:** los registros del sensor 99 deben **NO estar** (porque los borraste en el Test 7), pero el archivo sigue válido y con los originales.

### 2.6 · Detener la API

| OS              | Comando                                                  |
|-----------------|----------------------------------------------------------|
| Linux / macOS   | `pkill -f "python API.py"`                               |
| Windows         | Cierra la ventana de la terminal donde corre, o `taskkill /F /IM python.exe` (cuidado: mata todos los Python) |
| Antigravity     | Cierra el panel de terminal donde la lanzaste.           |

Verifica que se detuvo: `curl http://127.0.0.1:5000/sensors/` debe fallar con "connection refused".

---

## 📝 Actualización en BITACORA.md

Reemplaza la sección "Fase 2 — API" con:

```markdown
## Fase 2 — API  ✅

**Inicio:** [hora]
**Fin:** [hora]

### Archivos creados
- `sensores.json` (15 registros iniciales)
- `API.py` (~200 líneas, 5 endpoints)

### Pruebas ejecutadas

| # | Test                          | HTTP esperado | HTTP obtenido | Resultado |
|---|-------------------------------|---------------|---------------|-----------|
| 1 | GET todos                     | 200           | 200           | ✅        |
| 2 | GET por id                    | 200           | 200           | ✅        |
| 3 | POST válido                   | 201           | 201           | ✅        |
| 4 | POST inválido (rango)         | 400           | 400           | ✅        |
| 5 | POST duplicado                | 400           | 400           | ✅        |
| 6 | PUT                           | 200           | 200           | ✅        |
| 7 | DELETE                        | 200           | 200           | ✅        |
| 8 | GET inexistente               | 404           | 404           | ✅        |

### Incidencias
[Ninguna / o describir]

### Evidencias
- `capturas/01_api_arrancada.png`
- `capturas/02_curl_get_todos.png`
- `capturas/03_curl_post_invalido.png`
```

---

## 🚦 Siguiente paso

Asegúrate de que la API está **detenida**. Luego abre `docs/fase_3_dashboard.md`.
