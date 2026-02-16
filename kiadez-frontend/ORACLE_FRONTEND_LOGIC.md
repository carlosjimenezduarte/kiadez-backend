# Oracle Frontend Logic (Estado Actual)

## Alcance
- Este documento cubre solo la lógica actual del Oráculo en frontend.
- Ruta SPA activa: `/oracle` y `/oracle.html` en `src/App.svelte`.
- Archivo principal: `src/pages/Oracle.svelte`.
- Estilos principales: `public/css/styles.css` (sección Oracle).

## Ubicación y Enrutamiento
- Componente Oracle registrado en:
  - `src/App.svelte:73`
  - `src/App.svelte:74`
- Vista y lógica en:
  - `src/pages/Oracle.svelte:1`
- Estilos Oracle en:
  - `public/css/styles.css:6233`

## Estructura UI del Oráculo
- Barra superior social (topbar): `src/pages/Oracle.svelte:589`
- Portada y propósito visual: `src/pages/Oracle.svelte:643`
- Contenedor Oracle:
  - Introducción: `src/pages/Oracle.svelte:759`
  - Cartas no reveladas (deck): `src/pages/Oracle.svelte:773`
  - Cartas reveladas: `src/pages/Oracle.svelte:787`
- Modal de carta:
  - Overlay/modal: `src/pages/Oracle.svelte:855`
  - Acciones de respuesta: `src/pages/Oracle.svelte:881`
  - Historial de respuestas: `src/pages/Oracle.svelte:897`

## Estado y Persistencia (Local)
- Clave en localStorage:
  - `ORACLE_STATE_KEY = "oracle_state_v1"` en `src/pages/Oracle.svelte:222`
- Estado persistido:
  - `cycle`: ciclo actual (inicia en `1`)
  - `cycleStartAt`: timestamp inicio de ciclo
  - `lastPickAt`: timestamp última carta revelada
  - `revealedThisCycle`: array de IDs ya revelados en el ciclo
  - `history`: diccionario por carta con respuestas históricas
- Carga/guardado:
  - `loadState`: `src/pages/Oracle.svelte:255`
  - `saveState`: `src/pages/Oracle.svelte:278`

## Catálogo de Cartas
- Definidas en `oracleCards`:
  - `id`, `name`, `question`, `context`
  - Fuente: `src/pages/Oracle.svelte:8`
- Total calculado:
  - `TOTAL_CARDS = oracleCards.length` en `src/pages/Oracle.svelte:224`

## Reglas de Negocio Implementadas
- Cooldown global:
  - `COOLDOWN_MS = 72h` (`72 * 60 * 60 * 1000`) en `src/pages/Oracle.svelte:223`
- Mensaje de cooldown y bloqueo:
  - `updateCooldownStatus`: `src/pages/Oracle.svelte:332`
- Durante cooldown:
  - No se permite seleccionar carta nueva (`oracle-deck-card` bloqueada)
- Una vez se revelan las 30 cartas del ciclo:
  - Se espera a que no haya cooldown para iniciar nuevo ciclo
  - Reset de `revealedThisCycle` e incremento de `cycle`
  - Lógica: `src/pages/Oracle.svelte:337`

## Flujo Funcional Actual
- Inicialización:
  - `onMount` configura referencias DOM y render inicial con `renderAll()`
  - `renderAll`: `src/pages/Oracle.svelte:555`
- Deck:
  - Se baraja en cada render (`shuffleCards`)
  - Solo muestra cartas no reveladas del ciclo
  - Render: `renderOracleDeck` en `src/pages/Oracle.svelte:361`
- Carta revelada:
  - Al click abre modal (`openOracleModal`)
  - Función: `src/pages/Oracle.svelte:464`
- Respuesta del usuario (3 tipos):
  - `public`
  - `secret`
  - `heart` (reposar en el corazón)
  - Confirmación previa en `triggerConfirm`: `src/pages/Oracle.svelte:509`
  - Persistencia en `finalizeResponse`: `src/pages/Oracle.svelte:523`
- Historial:
  - Ordenado por fecha descendente
  - `renderHistory`: `src/pages/Oracle.svelte:430`

## Modelo de Historial por Carta
- Estructura por entrada:
  - `type`: `"public" | "secret" | "heart"`
  - `text`: respuesta (vacío en `heart`)
  - `date`: ISO string
  - `cycle`: número de ciclo
- Escritura:
  - `oracleState.history[selectedCard.id].push(entry)` en `src/pages/Oracle.svelte:542`

## Comportamientos Importantes
- Si una carta ya fue respondida en el ciclo (`public` o `secret`):
  - El textarea queda deshabilitado
  - Se ocultan acciones de respuesta
  - Lógica: `src/pages/Oracle.svelte:469` y `src/pages/Oracle.svelte:481`
- Si solo quedó en `heart`:
  - Permite responder luego en el mismo ciclo
  - Nota contextual en modal

## Hallazgos Técnicos (Importantes para Integración BD)
- No hay integración backend en Oracle:
  - Este componente no hace `fetch` ni consume endpoints.
  - Todo está en localStorage.
- Estado no está aislado por usuario:
  - `oracle_state_v1` es global al navegador.
- "Respuesta secreta" no está cifrada actualmente:
  - Se guarda igual en texto plano dentro de localStorage, solo cambia la etiqueta `type`.
- Mapeo de imágenes inconsistente con 30 cartas:
  - `getCardImage` usa una excepción para carta 1 (`Oracle9.png`) y luego módulo 13.
  - Implementación: `src/pages/Oracle.svelte:293`
  - Esto no representa un mapeo 1:1 de 30 cartas a 30 imágenes.
- Marcado legado no utilizado:
  - `openOracleModal(cardId, true)` se invoca con segundo parámetro, pero la función no lo usa.
  - Llamada: `src/pages/Oracle.svelte:425`

## Estado de Estilos Oracle
- Grilla de deck y tarjetas reveladas:
  - `public/css/styles.css:6333`
  - `public/css/styles.css:6385`
- Modal Oracle:
  - `public/css/styles.css:6428`
- Historial:
  - `public/css/styles.css:6494`

## Checklist de Preparación para Backend Real (Oracle)
- Definir entidad persistente de sesión Oracle por usuario (no localStorage global).
- Reemplazar `loadState/saveState` por API:
  - `GET /oracle/state`
  - `POST /oracle/reveal` o equivalente transaccional
  - `POST /oracle/respond`
- Encriptar realmente respuestas `secret` (si aplica política de producto).
- Corregir mapeo de imágenes a 30 cartas (1:1).
- Decidir si el barajado debe persistir por ciclo o ser solo visual por render.
- Mantener lógica de cooldown/ciclo en backend como fuente de verdad.

