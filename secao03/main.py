from fastapi import FastAPI


app = FastAPI()

cursos = {
  1: {
    "título": "Programação para leigos",
    "aulas": 112,
    "horas": 58
  },
  2: {
    "título": "Algoritimos e Logica de Programação",
    "aulas": 87,
    "horas": 67

  }
}


@app.get('/cursos')
async def get_cursos():
  return cursos

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)