# from fastapi.responses import JSONResponse
from typing import Optional, Dict, List, Any
from fastapi import Response
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

from pydantic import BaseModel

from fastapi import Query
from fastapi import Path
from fastapi import Header
from fastapi import Depends

from time import sleep

from models import Curso
from models import cursos


def fake_db():
    try:
        print('Abrindo conexão com banco de dados')
        sleep(1)
    finally:
        print('Fechando conexão com banco de dados')
        sleep(1)


app = FastAPI(
    title="API Mimir",
    version="0.0.1",
    description="Api para consulta aplicação SaaS"

)


@app.get('/cursos',
         description='Retorna tds os cursos ou uma lista vazia',
         summary='Pipoca Retorna Lista',
         response_model=List[Curso],
         response_description='Cursos encontrados com sucesso')
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(title='ID do Curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Curso não encontrado !')


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int


@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id

        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com id {curso_id}'
                            )


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com id {curso_id}'
                            )


@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None), c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c

    print(f'X-GEEK: {x_geek}')

    return {"resultado": soma}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8000,
                reload=True
                )
