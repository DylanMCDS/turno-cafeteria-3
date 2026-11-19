from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

AHORA = datetime(2026, 1, 1, 12, 0, 0)


@pytest.fixture
def client():
    return TestClient(create_app(clock=lambda: AHORA, minutos_por_turno=5))


def test_aparta_turno_y_devuelve_numero_y_posicion(client):
    r = client.post("/api/turnos", json={"boleta": "2023000001", "nombre": "Ana"})
    assert r.status_code == 201
    t = r.json()
    assert t["numero"] == 1 and t["posicion"] == 1 and t["estado"] == "en_espera"
    assert t["hora_estimada"] == "2026-01-01T12:05:00"
    r2 = client.post("/api/turnos", json={"boleta": "2023000002", "nombre": "Beto"})
    assert r2.json()["posicion"] == 2
    assert r2.json()["hora_estimada"] == "2026-01-01T12:10:00"
    assert [x["id"] for x in client.get("/api/turnos").json()] == [t["id"], r2.json()["id"]]
    assert client.get(f"/api/turnos/{r2.json()['id']}").json()["posicion"] == 2


def test_rechaza_segundo_turno_activo_del_mismo_alumno(client):
    body = {"boleta": "2023000001", "nombre": "Ana"}
    assert client.post("/api/turnos", json=body).status_code == 201
    r = client.post("/api/turnos", json=body)
    assert r.status_code == 409
    assert "turno activo" in r.json()["detail"]


def test_marcar_listo_avanza_la_posicion_de_los_demas(client):
    a = client.post("/api/turnos", json={"boleta": "1", "nombre": "A"}).json()
    b = client.post("/api/turnos", json={"boleta": "2", "nombre": "B"}).json()
    r = client.post(f"/api/turnos/{a['id']}/listo")
    assert r.status_code == 200 and r.json()["estado"] == "listo"
    assert [x["id"] for x in client.get("/api/turnos").json()] == [b["id"]]
    assert client.get(f"/api/turnos/{b['id']}").json()["posicion"] == 1
    # tras quedar listo, el alumno puede apartar otro turno
    assert client.post("/api/turnos", json={"boleta": "1", "nombre": "A"}).status_code == 201


def test_responde_404_al_marcar_turno_inexistente(client):
    assert client.post("/api/turnos/999/listo").status_code == 404
