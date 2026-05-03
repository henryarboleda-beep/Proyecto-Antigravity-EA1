# 🧪 Fase 1 — Preparación del entorno

> **Pre-requisito:** Has leído `INSTRUCCIONES_AGENTE.md` y conoces el sistema operativo del estudiante.

---

## 🎯 Objetivo

Dejar el entorno Python listo para que las fases 2-5 puedan ejecutar Flask, Dash y los demás paquetes sin contaminar la instalación global del sistema.

**Definition of Done:**
- [ ] Hay un entorno virtual activo en la carpeta `venv/`.
- [ ] El archivo `requirements.txt` existe en la raíz del proyecto.
- [ ] `pip list` (dentro del venv) muestra Flask, Dash, Plotly, Pandas y Requests.
- [ ] La sección "Fase 1" de `BITACORA.md` está completa.

---

## 📋 Tareas

### 1.1 · Verificar versión de Python

Ejecuta el comando apropiado para el OS detectado:

| OS              | Comando                |
|-----------------|------------------------|
| Linux / macOS   | `python3 --version`    |
| Windows         | `python --version`     |

**Criterio:** la versión debe ser **Python 3.9 o superior**. Si es menor, detente y pide al estudiante que lo actualice (apuntándolo a https://www.python.org/downloads/).

Registra la versión en `BITACORA.md`.

### 1.2 · Crear el entorno virtual

| OS              | Comando                       |
|-----------------|-------------------------------|
| Linux / macOS   | `python3 -m venv venv`        |
| Windows         | `python -m venv venv`         |

Esto crea una carpeta `venv/` en la raíz del proyecto. **No la edites a mano.**

### 1.3 · Activar el entorno virtual

| OS              | Comando                       |
|-----------------|-------------------------------|
| Linux / macOS   | `source venv/bin/activate`    |
| Windows (cmd)   | `venv\Scripts\activate.bat`   |
| Windows (PS)    | `venv\Scripts\Activate.ps1`   |

> ⚠️ Si en Windows PowerShell aparece un error de política de ejecución, ejecuta antes:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

**Verificación:** tras activar, el prompt debe mostrar `(venv)` al inicio. Y `which python` (Linux/Mac) o `where python` (Windows) debe apuntar a una ruta dentro de `venv/`.

### 1.4 · Crear `requirements.txt`

Crea el archivo `requirements.txt` en la raíz del proyecto con **exactamente** este contenido:

```
flask>=3.0.0
dash>=2.18.0
plotly>=5.24.0
pandas>=2.2.0
requests>=2.32.0
```

### 1.5 · Instalar dependencias

Con el venv activo, ejecuta:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

La salida debe terminar con `Successfully installed flask-X.X.X dash-X.X.X plotly-X.X.X pandas-X.X.X requests-X.X.X` (las versiones pueden variar mientras cumplan los mínimos).

### 1.6 · Verificar instalación

Ejecuta:

```bash
pip list
```

Confirma que aparecen las 5 librerías principales. Captura un fragmento de la salida para la bitácora.

Para verificación adicional, crea y ejecuta este script de prueba (puedes nombrarlo `verificar_entorno.py`, ejecutarlo, y borrarlo después):

```python
import flask, dash, plotly, pandas, requests
print("✅ Flask", flask.__version__)
print("✅ Dash", dash.__version__)
print("✅ Plotly", plotly.__version__)
print("✅ Pandas", pandas.__version__)
print("✅ Requests", requests.__version__)
```

**Si las 5 líneas imprimen sin errores → la fase 1 está completa.** Borra el archivo de prueba.

---

## 📝 Actualización en BITACORA.md

Reemplaza la sección "Fase 1 — Entorno" del BITACORA.md con algo como:

```markdown
## Fase 1 — Entorno  ✅

**Inicio:** [hora]
**Fin:** [hora]

### Comandos ejecutados
- `python3 --version` → Python 3.X.X
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `pip list`

### Versiones instaladas
- Flask X.X.X
- Dash X.X.X
- Plotly X.X.X
- Pandas X.X.X
- Requests X.X.X

### Incidencias
[Si no hubo, escribe "Ninguna". Si hubo, descríbelas brevemente.]

### Evidencias
- `capturas/01_pip_list.png` (opcional)
```

---

## 🚦 Siguiente paso

Cuando esta fase esté completa y la BITACORA actualizada, **abre `docs/fase_2_api.md`** y comienza con la siguiente fase. **Mantén el venv activo** — todas las fases siguientes lo necesitan.
