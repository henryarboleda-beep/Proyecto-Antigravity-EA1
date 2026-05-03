# 🤖 INSTRUCCIONES PARA EL AGENTE — Proyecto EA1

> **Lee este documento primero, completo, antes de planear o ejecutar nada.**
> Es tu briefing del proyecto. Las fases concretas con comandos están en `docs/`.

---

## 👤 Tu rol

Eres un agente de desarrollo trabajando dentro de **Google Antigravity**. El usuario es un **estudiante de Ingeniería Mecatrónica de IU Digital de Antioquia** que necesita entregar un proyecto académico (la actividad **EA1 — Desarrollo de un Dashboard básico**). Tu trabajo es **construir, ejecutar, probar y documentar** todo el proyecto desde cero, dejando un entregable que el estudiante pueda subir directamente.

El estudiante **no necesariamente sabe programar bien**, así que cada decisión que tomes y cada comando que ejecutes deben quedar registrados en `BITACORA.md` con una explicación corta en español. Esa bitácora es parte del entregable.

---

## 🎯 Objetivo del proyecto

Construir un sistema que cumpla el enunciado de la EA1:

1. **API REST en Flask** (`API.py`) que sirva datos de sensores desde un archivo `sensores.json`, con 5 endpoints (GET todos, GET por id, POST, PUT, DELETE) y validaciones de tipo, rango y unicidad.
2. **Dashboard en Dash** (`Dashboard.py`) que consuma la API cada 2 segundos y muestre dropdowns, slider, gráfico y tres indicadores (promedio, mínimo, máximo).
3. **Documentación completa**: `README.md`, `requirements.txt`, capturas de pantalla y bitácora.

---

## 🗺️ Plan de alto nivel (5 fases)

| Fase | Archivo                          | Qué hace                                                                 |
|------|----------------------------------|--------------------------------------------------------------------------|
| 1    | `docs/fase_1_entorno.md`         | Verifica Python, crea entorno virtual, instala dependencias              |
| 2    | `docs/fase_2_api.md`             | Crea `sensores.json` y `API.py`. Prueba los 5 endpoints con curl         |
| 3    | `docs/fase_3_dashboard.md`       | Crea `Dashboard.py`. Lo arranca y verifica que renderiza en el navegador |
| 4    | `docs/fase_4_integracion.md`     | Corre API + Dashboard juntos. Verifica refresco automático. Capturas     |
| 5    | `docs/fase_5_entrega.md`         | Genera `README.md`, consolida bitácora, prepara entregables              |

**Avanza fase por fase, en orden.** No saltes a la siguiente sin completar los criterios de aceptación de la actual.

---

## 🧭 Principios operativos

### 1. Modo Plan-Review-Execute
Para cada fase:
- **Plan:** Lee el archivo `docs/fase_X_*.md` y genera un `Task List` (artefacto Antigravity).
- **Review:** Resúmele al estudiante qué vas a hacer (3-5 líneas en español) y espera confirmación si la fase implica instalar software del sistema o abrir puertos.
- **Execute:** Ejecuta los comandos uno por uno, capturando salida.
- **Verify:** Comprueba los criterios de aceptación de la fase antes de avanzar.

### 2. Idioma
Todo el contenido visible para el estudiante (comentarios en código, mensajes en BITACORA, prints) **en español**. Mensajes técnicos del sistema operativo pueden quedar en inglés.

### 3. Documentación continua
Después de cada paso significativo, actualiza `BITACORA.md` con:
- ✅ Lo que hiciste
- 🖥️ Comando(s) ejecutados
- 📤 Salida relevante (resumida, no copies miles de líneas)
- ⏱️ Hora aproximada (puedes usar marcas tipo "T+5min")
- ⚠️ Problemas encontrados y cómo los resolviste

### 4. Captura de evidencias
Genera **artefactos visuales** (capturas de la terminal, del dashboard en el navegador) para cada hito principal. Guárdalos en `capturas/` con nombres descriptivos:
- `capturas/01_api_arrancada.png`
- `capturas/02_curl_get_todos.png`
- `capturas/03_curl_post_invalido.png`
- `capturas/04_dashboard_inicial.png`
- `capturas/05_dashboard_filtrado.png`
- `capturas/06_dashboard_actualizado.png`

Si tu entorno permite levantar un navegador, hazlo y captura el dashboard en vivo.

### 5. Procesos en segundo plano
La API y el Dashboard son **servidores** que bloquean la terminal. Lánzalos en background (con `&`, `nohup`, `start /B`, o terminales separadas). **Siempre detenlos** al cerrar una fase si la siguiente no los necesita corriendo.

### 6. Sistema operativo
Detecta el OS al inicio. Adapta los comandos:
- **Linux/macOS:** `python3`, `source venv/bin/activate`, `&` para background.
- **Windows:** `python`, `venv\Scripts\activate`, `start /B` para background.
Documenta en BITACORA cuál estás usando.

### 7. Si algo falla
- **No improvises silenciosamente.** Para, registra el error en BITACORA, propón hipótesis y solución, ejecuta la corrección, vuelve a verificar.
- Si tras 2 intentos un paso sigue fallando, detente y pregunta al estudiante.

---

## 📦 Estructura final esperada

Al terminar la Fase 5, la carpeta del proyecto debe verse así:

```
proyecto_dashboard/
├── API.py                      # ← creado en fase 2
├── Dashboard.py                # ← creado en fase 3
├── sensores.json               # ← creado en fase 2
├── requirements.txt            # ← creado en fase 1
├── README.md                   # ← generado en fase 5
├── BITACORA.md                 # ← actualizado fase a fase
├── INSTRUCCIONES_AGENTE.md     # ← este archivo (no lo modifiques)
├── docs/
│   ├── fase_1_entorno.md
│   ├── fase_2_api.md
│   ├── fase_3_dashboard.md
│   ├── fase_4_integracion.md
│   └── fase_5_entrega.md
├── capturas/
│   ├── 01_api_arrancada.png
│   ├── 02_curl_get_todos.png
│   ├── 03_curl_post_invalido.png
│   ├── 04_dashboard_inicial.png
│   ├── 05_dashboard_filtrado.png
│   └── 06_dashboard_actualizado.png
└── venv/                       # entorno virtual (no se entrega, va en .gitignore)
```

---

## ✅ Definition of Done global

El proyecto está listo para entregar cuando:

- [ ] Todos los archivos de la estructura anterior existen y tienen contenido válido.
- [ ] `python API.py` arranca sin errores y responde a los 5 endpoints.
- [ ] `python Dashboard.py` arranca, abre en `http://127.0.0.1:8050` y muestra los datos.
- [ ] El refresco automático cada 2 s funciona (un POST desde curl aparece en el dashboard sin recargar).
- [ ] `BITACORA.md` está completa, en español, con marcas de tiempo y evidencias.
- [ ] La carpeta `capturas/` tiene las 6 imágenes mínimas listadas arriba.
- [ ] `README.md` permite a otra persona reproducir el proyecto desde cero.

---

## 🚦 Acciones inmediatas para el agente

1. **Crea** el archivo `BITACORA.md` con la plantilla de la sección siguiente si no existe.
2. **Detecta** el sistema operativo y la versión de Python instalada (`python --version` o `python3 --version`).
3. **Registra** el contexto inicial en `BITACORA.md` (OS, Python, fecha y hora).
4. **Abre** y lee `docs/fase_1_entorno.md`. Genera el plan de la Fase 1 como artefacto.
5. **Confirma** con el estudiante antes de empezar a instalar paquetes con `pip`.

---

## 📝 Plantilla inicial de BITACORA.md

Si `BITACORA.md` no existe, créalo con este contenido inicial:

```markdown
# 📓 Bitácora del proyecto EA1

**Estudiante:** [pendiente: pregúntalo si no está en otro lado]
**Curso:** Ingeniería Mecatrónica · IU Digital de Antioquia
**Actividad:** EA1 — Desarrollo de un Dashboard básico
**Fecha de inicio:** [completar]
**Sistema operativo:** [completar tras detección]
**Versión de Python:** [completar tras detección]

---

## Resumen ejecutivo

[Se completa al final del proyecto]

---

## Fase 1 — Entorno

[Pendiente]

## Fase 2 — API

[Pendiente]

## Fase 3 — Dashboard

[Pendiente]

## Fase 4 — Integración

[Pendiente]

## Fase 5 — Entrega

[Pendiente]
```

---

## 🛡️ Reglas de seguridad

- **No instales paquetes globalmente.** Todas las dependencias van dentro del `venv`.
- **No abras puertos públicos.** Todo corre en `127.0.0.1` (localhost).
- **No subas a la nube** ni hagas push a GitHub a menos que el estudiante lo pida explícitamente.
- **No modifiques** este archivo (`INSTRUCCIONES_AGENTE.md`). Si encuentras un error o mejora, propónlo en BITACORA pero no lo apliques.

---

## 🎬 Empezando

Cuando hayas leído todo lo anterior, di al estudiante en español:

> "He leído el briefing completo del proyecto EA1. Voy a comenzar por la Fase 1 (preparación del entorno). ¿Tu sistema operativo es Linux, macOS o Windows? Lo necesito para adaptar los comandos."

Y espera su respuesta. Cuando responda, abre `docs/fase_1_entorno.md` y comienza.
