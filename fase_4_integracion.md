# 🔁 Fase 4 — Pruebas integradas y capturas

> **Pre-requisito:** Fases 1, 2 y 3 completadas. Ambos servidores **detenidos** al iniciar esta fase.

---

## 🎯 Objetivo

Verificar que API y Dashboard **funcionan juntos** de forma realista. Esto incluye demostrar el refresco automático: cuando se modifican datos en la API (con curl/Postman), el dashboard los muestra **dentro de 2 segundos sin recargar**.

**Definition of Done:**
- [ ] API y Dashboard corriendo simultáneamente sin errores.
- [ ] Captura del dashboard en estado inicial.
- [ ] Captura del dashboard con filtros aplicados.
- [ ] Captura del dashboard tras un POST/DELETE en vivo (mostrando que se actualizó).
- [ ] BITACORA Fase 4 documentada.

---

## 📋 Tareas

### 4.1 · Arrancar ambos servidores

Necesitamos los dos corriendo en paralelo. La forma más limpia: **dos terminales**.

**Terminal A — API:**
```bash
python API.py
```

**Terminal B — Dashboard:**
```bash
python Dashboard.py
```

Si trabajas en background:
```bash
python API.py > api.log 2>&1 &
sleep 3
python Dashboard.py > dashboard.log 2>&1 &
sleep 8
```

Verifica que ambos puertos respondan:
```bash
curl -s -o /dev/null -w "API:%{http_code}\n"      http://127.0.0.1:5000/sensors/
curl -s -o /dev/null -w "Dashboard:%{http_code}\n" http://127.0.0.1:8050/
```
Esperado: `API:200` y `Dashboard:200`.

### 4.2 · Captura: estado inicial

Abre el navegador en `http://127.0.0.1:8050` (o si Antigravity tiene browser-in-the-loop, úsalo).

Espera 3 segundos para que cargue los datos.

📸 **Captura:** `capturas/04_dashboard_inicial.png` mostrando los 3 tipos de sensor visibles en el gráfico, sin filtros aplicados.

### 4.3 · Aplicar filtros y capturar

#### Filtro 1: solo temperatura
- Selecciona en el dropdown "Tipo de sensor" → **Temperatura**.
- El gráfico debe mostrar solo las líneas del sensor 1.
- Las tarjetas deben actualizar valores (ej. mín ≈ 22.4, máx ≈ 27.8).

📸 **Captura:** `capturas/05_dashboard_filtrado.png`

#### Filtro 2: combinación
- Tipo: **Presión**
- Sensor ID: **Sensor 2**
- Mueve el RangeSlider para acotar a las primeras 3 mediciones.
- Verifica que el gráfico se reduce a esos puntos.

📸 **Captura:** `capturas/05b_dashboard_filtrado_combinado.png` (opcional pero recomendada)

### 4.4 · Prueba del refresco automático en vivo

**Esta es la prueba más importante de la EA1.**

Con el dashboard abierto en el navegador (sin tocarlo), ve a una **tercera terminal** y ejecuta:

```bash
curl -X POST http://127.0.0.1:5000/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"sensor_id": 50, "type": "temperatura", "value": 45.0, "timestamp": "2026-04-28T10:00:00"}'
```

Cambia al navegador y observa el dashboard durante **3-4 segundos**.

**Resultado esperado:**
- El dropdown "Sensor ID" debe **incluir ahora "Sensor 50"**.
- Si el filtro "Tipo" estaba en "Temperatura", el gráfico debe mostrar un punto nuevo en `45.0`.
- Las tarjetas (especialmente Máximo) deben actualizarse.

📸 **Captura:** `capturas/06_dashboard_actualizado.png` mostrando el sensor 50 ya visible.

### 4.5 · Prueba de eliminación en vivo

Desde la tercera terminal:

```bash
curl -X DELETE http://127.0.0.1:5000/sensors/50
```

Vuelve al navegador, observa 3 segundos. El sensor 50 debe **desaparecer** de las opciones del dropdown y del gráfico.

### 4.6 · Verificar el archivo JSON

Después de las pruebas, verifica que `sensores.json` quedó con los 15 registros originales:

```bash
python -c "import json; d=json.load(open('sensores.json')); print('Total:', len(d))"
```
Esperado: `Total: 15`. (Si quedó otro número, no es problema crítico, pero anótalo.)

### 4.7 · Detener ambos servidores

```bash
# Linux/Mac
pkill -f "python API.py"
pkill -f "python Dashboard.py"

# Windows: cierra las terminales o usa taskkill
```

---

## 📝 Actualización en BITACORA.md

```markdown
## Fase 4 — Integración  ✅

**Inicio:** [hora]
**Fin:** [hora]

### Pruebas realizadas

| # | Prueba                                          | Resultado |
|---|-------------------------------------------------|-----------|
| 1 | API y Dashboard arrancados simultáneamente      | ✅        |
| 2 | Dashboard renderiza datos iniciales             | ✅        |
| 3 | Filtro por tipo de sensor                       | ✅        |
| 4 | Filtro combinado (tipo + id + rango)            | ✅        |
| 5 | Refresco automático tras POST                   | ✅ (~2s)  |
| 6 | Refresco automático tras DELETE                 | ✅ (~2s)  |

### Observaciones
- El refresco efectivo se mide en ~2-3 s, consistente con el `dcc.Interval` configurado a 2000 ms.
- El callback consulta la API en cada tick, lo cual es aceptable para el alcance de esta práctica.

### Incidencias
[Ninguna / o describir]

### Evidencias
- `capturas/04_dashboard_inicial.png`
- `capturas/05_dashboard_filtrado.png`
- `capturas/05b_dashboard_filtrado_combinado.png` (opcional)
- `capturas/06_dashboard_actualizado.png`
```

---

## 🚦 Siguiente paso

Abre `docs/fase_5_entrega.md` para preparar los entregables finales.
