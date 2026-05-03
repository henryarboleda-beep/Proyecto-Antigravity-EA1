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
- [x] Pruebas de los endpoints con curl.
- [x] Capturas del dashboard con distintos filtros.
- [x] `requirements.txt` con dependencias.

## 📁 Archivos a entregar

Comprime y sube la carpeta `Proyecto Antigravity EA1/` completa, **excluyendo**:
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
