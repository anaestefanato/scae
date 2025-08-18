from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routes import public
from routes.aluno import perfil_routes
from repo import usuario_repo

usuario_repo.criar_tabela()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public.router)
app.include_router(perfil_routes.router, prefix="/aluno")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)