from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
import secrets
from routes import public
from routes.admin import analisar_cadastro_routes, editaisadmin_routes, pagamentos_routes, perfiladmin_routes, responder_chamado_routes, usuarios_routes
from routes.aluno import acompanhar_inscricoes_routes, dados_cadastrais_routes, duvidas_frequentes_routes, editais_routes, notificacao_routes, perfilaluno_routes, recebimentos_routes, suporte_routes
from repo import administrador_repo, aluno_repo, assistente_social_repo, auxilio_moradia_repo, auxilio_repo, auxilio_transporte_repo, chamado_repo, duvida_edital_repo, edital_repo, inscricao_repo, notificacao_repo, recurso_repo, resposta_chamado_repo, usuario_repo, recebimento_repo
from routes.assistente_social import alunos_routes, analise_inscricoes_routes, analise_recurso_routes, perfilassistente_routes, entrevistas_routes, relatorios_routes, agenda_routes, editais_assistente_routes
from util import seed_db

usuario_repo.criar_tabela()
aluno_repo.criar_tabela()
administrador_repo.criar_tabela()
assistente_social_repo.criar_tabela()
auxilio_repo.criar_tabela()
recebimento_repo.criar_tabela()
chamado_repo.criar_tabela()
edital_repo.criar_tabela()
duvida_edital_repo.criar_tabela()
resposta_chamado_repo.criar_tabela()
inscricao_repo.criar_tabela()
notificacao_repo.criar_tabela()
recurso_repo.criar_tabela()
auxilio_moradia_repo.AuxilioMoradiaRepo.criar_tabela()
auxilio_transporte_repo.AuxilioTransporteRepo.criar_tabela()
seed_db.criar_admin_padrao()
seed_db.criar_aluno_padrao()
seed_db.criar_assistente_padrao()
recebimento_repo.inserir_dados_exemplo()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# Gerar chave secreta (em produção, use variável de ambiente!)
SECRET_KEY = "f0983404657523e010e3c1cafb3e61be"

# Adicionar middleware de sessão
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600,  # Sessão expira em 1 hora
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)

app.include_router(public.router)
app.include_router(perfilaluno_routes.router, prefix="/aluno")
app.include_router(editais_routes.router, prefix="/aluno")
app.include_router(recebimentos_routes.router, prefix="/aluno")
app.include_router(dados_cadastrais_routes.router, prefix="/aluno")
app.include_router(suporte_routes.router, prefix="/aluno")
app.include_router(notificacao_routes.router, prefix="/aluno")
app.include_router(duvidas_frequentes_routes.router, prefix="/aluno")
app.include_router(acompanhar_inscricoes_routes.router, prefix="/aluno")

app.include_router(analisar_cadastro_routes.router, prefix="/admin")
app.include_router(responder_chamado_routes.router, prefix="/admin")
app.include_router(perfiladmin_routes.router, prefix="/admin")
app.include_router(editaisadmin_routes.router, prefix="/admin")
app.include_router(pagamentos_routes.router, prefix="/admin")
app.include_router(usuarios_routes.router, prefix="/admin")
app.include_router(relatorios_routes.router, prefix="/admin")

app.include_router(perfilassistente_routes.router, prefix="/assistente")
app.include_router(analise_inscricoes_routes.router, prefix="/assistente")
app.include_router(analise_recurso_routes.router, prefix="/assistente")
app.include_router(alunos_routes.router, prefix="/assistente")
app.include_router(entrevistas_routes.router, prefix="/assistente")
app.include_router(relatorios_routes.router, prefix="/assistente")
app.include_router(agenda_routes.router, prefix="/assistente")
app.include_router(editais_assistente_routes.router, prefix="/assistente")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)