# TASKS · backlog sin estado

El estado vive en la rama `claims` (`uak status`); este archivo solo guarda tareas. Revisa el grafo con `uak graph`.

> **Supuestos (corrida headless, nadie pudo responder):**
> - Evento corto: 3 h × 1 persona → presupuesto de 3 × 1 ÷ 1,5 = 2 tareas en total. Setup + contrato + API van en una sola tarea (HACK-001) y la UI en otra (HACK-002), cada una de ≤45 min. Sin design lock, landing ni spike: no hay API externa y el evento dura menos de 24 h.
> - Rúbrica tomada de IDEA.md, porque la tabla de `.uak/PROJECT.md` sigue vacía: C1 Funciona de punta a punta (40), C2 Utilidad real (30), C3 Diseño (20), C4 Presentación (10). Un humano debe copiarla a PROJECT.md.
> - Stack: FastAPI + SQLite (Python, `uv`) para la API; Vite + React + TypeScript en `web/`. Deploy: Dockerfile + Render Blueprint, generados con `uak deploy --write` dentro de HACK-001.
> - Alcance: solo turnos (apartar, ver posición, marcar listo y atendido). El menú, los pagos y los pedidos de comida quedan fuera. Sin autenticación: el alumno se identifica con su boleta.
> - No queda presupuesto para una tarea de demo: HACK-002 escribe `README.md` (el pitch en una línea + el guion de demo de 90 s) para C4.
> - HACK-002 aplica una receta de estilo simple y es dueña de los tokens (`web/DESIGN.md`, `web/src/index.css`, `web/src/lib/ui/`); la dirección visual no se fija en este plan.
> - **Aviso de freeze:** `Freeze-Epoch` (1795096800) cae unos 21 min después del inicio de esta corrida. Si es correcto, ninguna tarea se podrá tomar sin `Freeze-Allowed`. Lo decide el humano (`uak clock … --write` o `uak allow`); este plan no lo cambia.

## HACK-001 · Setup + contrato + API de turnos (apartar, posición, marcar listo)

- **Type:** setup
- **Priority:** P0
- **Estimate:** 45 min
- **Rubric / Spec:** C1 · IDEA.md
- **Depends on:** None
- **Uses contract:** None
- **Related:** HACK-002
- **Paths:** pyproject.toml, uv.lock, app/, web/package.json, web/package-lock.json, web/vite.config.ts, web/tsconfig.json, web/index.html, web/src/main.tsx, web/src/fixtures/, Dockerfile, render.yaml, .gitignore
- **Freeze-Allowed:** no
- **Acceptance:**
  - Dependencias completas de una vez: Python `fastapi`, `uvicorn`, `pytest`, `httpx`; web `react`, `react-dom`, `vite`, `typescript`, `vitest`, `@testing-library/react`, `jsdom`, con scripts `dev`, `build` y `test` en `web/package.json`.
  - Contrato en `app/schemas/turnos.py`: `POST /api/turnos` con `{boleta, nombre}` → 201 `{id, numero, posicion, hora_estimada, estado: "en_espera"}`; `GET /api/turnos` → la cola en orden; `GET /api/turnos/{id}` → turno con su posición actual; `POST /api/turnos/{id}/listo` → `estado: "listo"`, y sale de la cola.
  - Un mismo alumno (boleta) no puede tener dos turnos activos: 409 con mensaje claro.
  - Marcar un turno inexistente responde 404.
  - `hora_estimada` usa un reloj inyectable (minutos por turno configurables), así los tests son deterministas.
  - Fixtures en `web/src/fixtures/turnos.json` con `demo_data: true`, para que HACK-002 trabaje sin la API.
  - Dockerfile y `render.yaml` generados con `bash .uak/bin/uak deploy --write`; FastAPI sirve el build de `web/`.
  - `bash .uak/bin/smoke` sale con 0.
- **Tests:** aparta_turno_y_devuelve_numero_y_posicion, rechaza_segundo_turno_activo_del_mismo_alumno, marcar_listo_avanza_la_posicion_de_los_demas, responde_404_al_marcar_turno_inexistente
- **Verify:** `uv run pytest -q app/tests/test_turnos.py`
- **Next step:** Crear `pyproject.toml` y `app/tests/test_turnos.py` con los 4 tests + un stub en `app/routers/turnos.py`, correr `uak red HACK-001`, implementar el resto y luego `bash .uak/bin/uak deploy --write`.

## HACK-002 · Pantalla del alumno + panel de cafetería + README

- **Type:** feature
- **Priority:** P0
- **Estimate:** 45 min
- **Rubric / Spec:** C1, C2, C3, C4 · IDEA.md
- **Depends on:** HACK-001
- **Uses contract:** HACK-001
- **Related:** HACK-001
- **Paths:** web/DESIGN.md, web/src/index.css, web/src/lib/ui/, web/src/App.tsx, web/src/features/turnos/, web/src/features/panel/, README.md
- **Freeze-Allowed:** no
- **Acceptance:**
  - Alumno: `Recipe: flow · Hero: el número de turno y la posición en la cola`. Captura boleta y nombre, aparta el turno y ve número, posición y hora estimada, que se actualizan solos (polling cada 5 s).
  - Si el alumno ya tiene un turno activo (409), lo ve como un mensaje de error claro, no como pantalla en blanco.
  - Panel de cafetería: `Recipe: list · Hero: la cola de turnos en espera`. Lista la cola en orden; "Marcar listo" quita el turno de la cola.
  - Cada pantalla tiene estados vacío, cargando, error y datos de ejemplo (etiqueta `demo_data` visible cuando se usan los fixtures).
  - El flujo cabe en 1280×720 sin scroll; foco visible, operable con teclado y contraste AA.
  - `web/DESIGN.md` con una receta de estilo simple; todos los colores salen de tokens CSS en `web/src/index.css`.
  - `bash .uak/bin/design-lint` pasa; capturas a 1280×720 y 390×844 en `.uak-shots/HACK-002/` y veredicto `SHIP` del `design-critic`.
  - `README.md` con el pitch en una línea, cómo correrlo y el guion de demo de 90 s (alumno aparta → panel marca listo → la posición del alumno avanza).
- **Tests:** muestra_numero_y_posicion_tras_apartar, muestra_error_si_ya_tiene_turno_activo, panel_marca_listo_y_lo_quita_de_la_cola, muestra_estado_vacio_sin_turnos
- **Verify:** `npm --prefix web test -- --run && npm --prefix web run build && bash .uak/bin/design-lint`
- **Next step:** Escribir los 4 tests en `web/src/features/turnos/turnos.test.tsx` y `web/src/features/panel/panel.test.tsx` contra `web/src/fixtures/turnos.json`, correr `uak red HACK-002` y luego construir las pantallas.
