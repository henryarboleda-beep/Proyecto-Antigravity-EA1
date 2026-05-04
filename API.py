"""
============================================================
 API.py  —  API REST de gestión de sensores
 EA1: Desarrollo de un Dashboard básico
 IU Digital de Antioquia · Ingeniería Mecatrónica
============================================================

Esta API expone endpoints HTTP para gestionar datos de sensores
almacenados en un archivo JSON (sensores.json).

Endpoints:
  GET    /sensors/                      -> Lista todos los sensores
  GET    /sensors/by-sensor/<sensor_id>  -> Filtra registros por sensor_id
  POST   /sensors/                      -> Crea un nuevo registro
  PUT    /sensors/<id>                   -> Actualiza un registro por su id unico
  DELETE /sensors/<id>                   -> Elimina un registro por su id unico

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

# Ruta del archivo JSON que actua como base de datos persistente
DATA_FILE = "sensores.json"

# Diccionario de tipos de sensor permitidos y sus rangos validos (min, max)
TIPOS_VALIDOS = {
    "temperatura": (-10, 100),   # °C
    "presion":     (0, 500),     # kPa
    "velocidad":   (0, 150),     # m/s
}

# Lock para evitar escrituras concurrentes al archivo JSON
file_lock = Lock()
# Lista en memoria que almacena todos los registros de sensores
sensores = []


# ----------------------------------------------------------
# Utilidades de carga / guardado
# ----------------------------------------------------------
def cargar_datos():
    """Carga los sensores desde sensores.json al iniciar la aplicación."""
    global sensores
    # Si el archivo no existe, lo crea vacio para evitar errores
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        sensores = []
        return
    # Intenta leer el JSON; si esta corrupto, arranca con lista vacia
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
    # Verificar que el cuerpo sea un diccionario JSON valido
    if not isinstance(data, dict):
        return False, "El cuerpo de la petición debe ser un objeto JSON."

    # Verificar que todos los campos obligatorios esten presentes
    requeridos = ["type", "value", "timestamp"]
    if requerir_id:
        requeridos = ["sensor_id"] + requeridos
    for campo in requeridos:
        if campo not in data:
            return False, f"Falta el campo obligatorio: '{campo}'."

    # Validar que el tipo de sensor sea uno de los permitidos
    tipo = str(data.get("type", "")).strip().lower()
    if tipo not in TIPOS_VALIDOS:
        return False, (
            f"Tipo no válido: '{data.get('type')}'. "
            f"Debe ser uno de: {list(TIPOS_VALIDOS.keys())}."
        )

    # Validar que el valor sea numerico y este dentro del rango permitido
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

    # Validar que el timestamp tenga formato ISO 8601 valido
    try:
        datetime.fromisoformat(str(data["timestamp"]).replace("Z", "+00:00"))
    except ValueError:
        return False, "El campo 'timestamp' debe estar en formato ISO 8601."

    # Si se requiere sensor_id, validar que sea un entero
    if requerir_id:
        try:
            nuevo_sensor_id = int(data["sensor_id"])
        except (TypeError, ValueError):
            return False, "El 'sensor_id' debe ser un número entero."

    # Todas las validaciones pasaron correctamente
    return True, None


# ==========================================================
# ENDPOINTS
# ==========================================================

@app.route("/sensors/", methods=["GET"])
def listar_sensores():
    """GET /sensors/ -> Devuelve todos los sensores."""
    return jsonify(sensores), 200


# Endpoint GET para filtrar registros por sensor_id (agrupador logico)
# Ruta separada /by-sensor/ para evitar conflicto con PUT/DELETE que usan /sensors/<id>
@app.route("/sensors/by-sensor/<int:sensor_id>", methods=["GET"])
def obtener_sensor(sensor_id):
    """GET /sensors/by-sensor/<sensor_id> -> Devuelve los registros de un sensor_id."""
    coincidencias = [s for s in sensores if s["sensor_id"] == sensor_id]
    if not coincidencias:
        return jsonify({"error": f"No existe sensor con sensor_id {sensor_id}."}), 404
    return jsonify(coincidencias), 200


@app.route("/sensors/", methods=["POST"])
def crear_sensor():
    """POST /sensors/ -> Crea un nuevo sensor."""
    # Obtener el cuerpo JSON de la peticion
    data = request.get_json(silent=True)
    # Validar los datos recibidos antes de procesarlos
    ok, error = validar_sensor(data, requerir_id=True)
    if not ok:
        return jsonify({"error": error}), 400

    # Generar un nuevo id unico (maximo actual + 1) y construir el registro
    nuevo = {
        "id": max([s.get("id", 0) for s in sensores], default=0) + 1,
        "sensor_id": int(data["sensor_id"]),
        "type":      str(data["type"]).strip().lower(),
        "value":     float(data["value"]),
        "timestamp": data["timestamp"],
    }
    # Agregar a la lista en memoria y persistir al archivo JSON
    sensores.append(nuevo)
    guardar_datos()
    return jsonify(nuevo), 201


@app.route("/sensors/<int:id>", methods=["PUT"])
def actualizar_sensor(id):
    """PUT /sensors/<id> -> Actualiza el registro con ese id."""
    # Buscar el indice del registro por su id unico (clave primaria)
    indice = next((i for i, s in enumerate(sensores)
                   if s.get("id") == id), None)
    if indice is None:
        return jsonify({"error": f"No existe registro con id {id}."}), 404

    # Validar los nuevos datos (no se requiere sensor_id en PUT)
    data = request.get_json(silent=True)
    ok, error = validar_sensor(data, requerir_id=False)
    if not ok:
        return jsonify({"error": error}), 400

    # Actualizar los campos del registro encontrado
    if "sensor_id" in data:
        sensores[indice]["sensor_id"] = int(data["sensor_id"])
    sensores[indice]["type"]      = str(data["type"]).strip().lower()
    sensores[indice]["value"]     = float(data["value"])
    sensores[indice]["timestamp"] = data["timestamp"]
    guardar_datos()
    return jsonify(sensores[indice]), 200


@app.route("/sensors/<int:id>", methods=["DELETE"])
def eliminar_sensor(id):
    """DELETE /sensors/<id> -> Elimina el registro con ese id."""
    global sensores
    cantidad_antes = len(sensores)
    # Filtrar la lista excluyendo el registro con el id proporcionado
    sensores = [s for s in sensores if s.get("id") != id]
    eliminados = cantidad_antes - len(sensores)

    # Si no se elimino ningun registro, el id no existia
    if eliminados == 0:
        return jsonify({"error": f"No existe registro con id {id}."}), 404

    # Persistir los cambios y devolver confirmacion
    guardar_datos()
    return jsonify({
        "mensaje": f"Registro {id} eliminado.",
        "registros_eliminados": eliminados
    }), 200


# Manejador de error 404: ruta no encontrada
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada."}), 404

# Manejador de error 405: metodo HTTP no permitido
@app.errorhandler(405)
def not_allowed(e):
    return jsonify({"error": "Método HTTP no permitido en esta ruta."}), 405


# Punto de entrada principal: carga los datos y arranca el servidor Flask
if __name__ == "__main__":
    cargar_datos()
    print(f"OK Cargados {len(sensores)} registros desde {DATA_FILE}")
    print("OK API corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
