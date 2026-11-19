from typing import Literal

from pydantic import BaseModel

Estado = Literal["en_espera", "listo"]


class TurnoIn(BaseModel):
    boleta: str
    nombre: str


class TurnoOut(BaseModel):
    id: int
    numero: int
    posicion: int | None
    hora_estimada: str | None
    estado: Estado
