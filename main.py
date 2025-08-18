from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routes import public
from routes.aluno import perfil_routes
from repo import administrador_repo, aluno_repo, assistente_social_repo, auxilio_moradia_repo, auxilio_repo, auxilio_transporte_repo, chamado_repo, duvida_edital_repo, edital_repo, inscricao_repo, notificacao_repo, recurso_repo, resposta_chamado_repo, usuario_repo

usuario_repo.criar_tabela()
aluno_repo.criar_tabela()
administrador_repo.criar_tabela()
assistente_social_repo.criar_tabela()
auxilio_repo.criar_tabela()
chamado_repo.criar_tabela()
edital_repo.criar_tabela()
duvida_edital_repo.criar_tabela()
resposta_chamado_repo.criar_tabela()
inscricao_repo.criar_tabela()
notificacao_repo.criar_tabela()
recurso_repo.criar_tabela()
auxilio_moradia_repo.AuxilioMoradiaRepo.criar_tabela()
auxilio_transporte_repo.AuxilioTransporteRepo.criar_tabela()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public.router)
app.include_router(perfil_routes.router, prefix="/aluno")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)