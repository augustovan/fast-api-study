from typing import Optional

from pydantic import BaseModel


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int


cursos = [
    Curso(id=1, titulo="Programação para leigos", aulas=43, horas=56),
    Curso(id=2, titulo="Algoritimos e Logica de Programação", aulas=52, horas=66)
]
