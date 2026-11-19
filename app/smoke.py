"""Smoke de punta a punta: API real + build de web servido por FastAPI."""
from fastapi.testclient import TestClient

from app.main import create_app

c = TestClient(create_app())
t = c.post("/api/turnos", json={"boleta": "smoke", "nombre": "Smoke"})
assert t.status_code == 201, t.text
assert c.get(f"/api/turnos/{t.json()['id']}").json()["posicion"] == 1
assert c.post(f"/api/turnos/{t.json()['id']}/listo").json()["estado"] == "listo"
home = c.get("/")
assert home.status_code == 200 and "root" in home.text, "web/dist no se sirve"
print("SMOKE_OK")
