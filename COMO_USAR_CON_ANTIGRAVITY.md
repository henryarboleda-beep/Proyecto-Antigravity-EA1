# 🚀 Cómo ejecutar este proyecto con Google Antigravity

Esta guía es para **ti, el estudiante**. Te explica qué hacer en la interfaz de Antigravity para que el agente construya, pruebe y documente todo el proyecto EA1 por ti.

---

## 1. Instalar Antigravity (si no lo tienes)

1. Ve a **https://antigravity.google/**
2. Descarga el instalador para tu sistema operativo (Windows, macOS o Linux).
3. Instálalo como cualquier aplicación.
4. La primera vez que lo abras te pedirá:
   - Iniciar sesión con tu cuenta de Google.
   - Elegir tema (claro/oscuro, da igual).
   - Elegir modo de desarrollo → **selecciona "Agent-driven" o "Agent-assisted"**.
   - Importar configuración de VS Code → **omite** (Skip).

> 💰 Antigravity es **gratis en preview** con cuotas generosas. No necesitas tarjeta de crédito.

---

## 2. Abrir la carpeta del proyecto

1. En Antigravity, ve a **File → Open Folder** (o `Ctrl + K Ctrl + O`).
2. Selecciona la carpeta `proyecto_dashboard/` (la que contiene este archivo).
3. Acepta cuando pregunte "Do you trust the authors of this folder?".

---

## 3. Decirle al agente qué hacer

Antigravity tiene dos vistas principales:
- **Editor View** — el editor estilo VS Code.
- **Manager View** — el orquestador de agentes.

Para este proyecto, usa la **Editor View**. En el panel lateral derecho (donde está el chat con el agente) escribe **exactamente** este prompt:

```
Lee el archivo INSTRUCCIONES_AGENTE.md de este proyecto y síguelo
al pie de la letra. Comienza por la Fase 1 y avanza secuencialmente
hasta la Fase 5, actualizando BITACORA.md tras cada fase.
Confirma conmigo antes de instalar paquetes con pip o de abrir
puertos de red. Mi sistema operativo es: [WINDOWS / MACOS / LINUX].
```

> Reemplaza `[WINDOWS / MACOS / LINUX]` con tu OS real.

---

## 4. Qué esperar mientras el agente trabaja

### Modo Plan
Antes de empezar cada fase, el agente generará un **Task List** (un artefacto). Lo verás como un panel a la derecha. Te muestra qué piensa hacer.

**Tu trabajo aquí:** revisarlo y aprobar. Si algo te llama la atención (p.ej. quiere cambiar puertos, instalar algo raro), puedes comentar como en Google Docs.

### Modo Execute
El agente comenzará a:
- Crear archivos.
- Ejecutar comandos en la terminal integrada.
- Mostrarte los outputs.

**Tu trabajo aquí:** observar y responder cuando te pregunte algo (p.ej. "tu OS es Windows, ¿confirmas que instale las dependencias?").

### Artefactos que producirá
- `BITACORA.md` actualizado con cada paso.
- Capturas en `capturas/` (sí, Antigravity puede tomar capturas del navegador con Browser-in-the-loop).
- Plan de implementación.
- Walkthrough final.

---

## 5. Cuándo intervenir

El agente seguirá el contrato definido en `INSTRUCCIONES_AGENTE.md`. **Tu intervención humana es necesaria en estos momentos:**

| Situación                                            | Qué hacer                                                       |
|------------------------------------------------------|-----------------------------------------------------------------|
| Te pregunta tu OS                                    | Respóndele "Windows" / "macOS" / "Linux"                        |
| Pide confirmación antes de `pip install`             | Responde "sí, adelante"                                         |
| El navegador interno pide permiso (Browser MCP)      | Otórgaselo (es para tomar capturas del dashboard)               |
| Una fase falla y el agente pide ayuda                | Lee el error, copia el mensaje, dile "intenta otra vez con X"   |
| El agente termina la Fase 5                          | Revisa la BITACORA y `RESUMEN_ENTREGA.md`                       |

---

## 6. Si Antigravity no tiene Browser-in-the-loop disponible

Si el agente no puede tomar capturas automáticamente del dashboard:

1. Cuando te diga "el dashboard está corriendo en `http://127.0.0.1:8050`", **abre tú mismo** ese link en tu navegador.
2. Toma capturas con la herramienta de captura de tu OS (`Win + Shift + S` en Windows, `Cmd + Shift + 4` en macOS).
3. Guárdalas en `capturas/` con los nombres exactos que dice cada fase (p.ej. `04_dashboard_inicial.png`).
4. Avísale al agente: "ya guardé las capturas en capturas/, continúa".

---

## 7. Cuando termine

El agente te dirá algo como:

> "He completado las 5 fases del proyecto EA1. ¿Quieres que prepare un .zip listo para entregar?"

Responde "sí" y guardará un comprimido sin las carpetas innecesarias.

---

## 8. Si quieres re-ejecutar todo desde cero

Borra estas carpetas/archivos:
- `venv/`
- `__pycache__/`
- `*.log`

Y vuelve a darle el prompt del paso 3. El agente detectará lo que ya existe y rehará lo que haga falta.

---

## 9. Si algo se rompe a medio camino

Antigravity guarda el historial de la sesión. Puedes:
- Pedirle al agente "revisa qué fase quedó incompleta y retómala".
- Mirar `BITACORA.md` para saber dónde quedó.
- Pedirle "muéstrame los últimos errores que encontraste".

---

## 10. ¿Por qué tantos archivos `.md`?

Cada `docs/fase_X_*.md` es una **especificación técnica detallada** para el agente. La estructura modular permite:

- Que el agente no tenga que mantener todo en su contexto a la vez.
- Que tú puedas leer una fase específica si quieres entender qué hace.
- Que si una fase falla, el agente pueda re-leer ese archivo concreto sin distraerse.

`INSTRUCCIONES_AGENTE.md` es el "índice" y las reglas globales. Las fases son los detalles.

---

## 11. Flujo resumido en una imagen mental

```
Tú: abres Antigravity
 ↓
Tú: abres carpeta proyecto_dashboard
 ↓
Tú: escribes el prompt del paso 3
 ↓
Agente: lee INSTRUCCIONES_AGENTE.md
 ↓
Agente: hace plan de Fase 1 → ejecuta → actualiza BITACORA
 ↓
Agente: hace plan de Fase 2 → ejecuta → actualiza BITACORA
 ↓
... (fases 3, 4, 5) ...
 ↓
Agente: te entrega proyecto listo + .zip
 ↓
Tú: subes el .zip a la plataforma de IU Digital ✅
```

---

¡Y eso es todo! Si Antigravity te falla por algo ajeno al proyecto (login, cuota, etc.), siempre puedes ejecutar el proyecto manualmente siguiendo el `TUTORIAL.md` paso a paso (es la versión humana de las mismas instrucciones).
