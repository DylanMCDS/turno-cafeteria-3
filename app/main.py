from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.schemas.turnos import TurnoIn, TurnoOut

WEB_DIST = Path(__file__).resolve().parent.parent / "web" / "dist"


def create_app(clock=datetime.now, minutos_por_turno: int = 5) -> FastAPI:
    app = FastAPI(title="Turno Cafetería")
    turnos: dict[int, dict] = {}

    def cola() -> list[dict]:
        return [t for t in turnos.values() if t["estado"] == "en_espera"]

    def serializa(t: dict) -> TurnoOut:
        if t["estado"] == "en_espera":
            pos = cola().index(t) + 1
            hora = (clock() + timedelta(minutes=minutos_por_turno * pos)).isoformat()
        else:
            pos, hora = None, None
        return TurnoOut(id=t["id"], numero=t["numero"], posicion=pos,
                        hora_estimada=hora, estado=t["estado"])

    @app.post("/api/turnos", status_code=201, response_model=TurnoOut)
    def crea(body: TurnoIn):
        if any(t["boleta"] == body.boleta for t in cola()):
            raise HTTPException(409, "Esta boleta ya tiene un turno activo")
        n = len(turnos) + 1
        turnos[n] = {"id": n, "numero": n, "boleta": body.boleta,
                     "nombre": body.nombre, "estado": "en_espera"}
        return serializa(turnos[n])

    @app.get("/api/turnos", response_model=list[TurnoOut])
    def lista():
        return [serializa(t) for t in cola()]

    @app.get("/api/turnos/{turno_id}", response_model=TurnoOut)
    def uno(turno_id: int):
        if turno_id not in turnos:
            raise HTTPException(404, "Turno no encontrado")
        return serializa(turnos[turno_id])

    @app.post("/api/turnos/{turno_id}/listo", response_model=TurnoOut)
    def listo(turno_id: int):
        if turno_id not in turnos:
            raise HTTPException(404, "Turno no encontrado")
        turnos[turno_id]["estado"] = "listo"
        return serializa(turnos[turno_id])

    if WEB_DIST.is_dir():
        app.mount("/assets", StaticFiles(directory=WEB_DIST / "assets"), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def spa(path: str):
            f = WEB_DIST / path
            return FileResponse(f if path and f.is_file() else WEB_DIST / "index.html")

    return app


app = create_app()
