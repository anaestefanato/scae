from urllib import request
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo, aluno_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/alunos")
@requer_autenticacao("assistente")
async def get_alunos(request: Request, usuario_logado: dict = None):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar alunos aprovados
    try:
        alunos = aluno_repo.obter_alunos_aprovados()
    except Exception as e:
        print(f"Erro ao buscar alunos aprovados: {e}")
        alunos = []
    
    # Estatísticas básicas
    total_alunos = len(alunos)
    alunos_ativos = len([a for a in alunos if a.get('situacao') == 'Ativo'])
    
    context = {
        "request": request, 
        "assistente": assistente,
        "alunos": alunos,
        "total_alunos": total_alunos,
        "alunos_ativos": alunos_ativos
    }
    
    response = templates.TemplateResponse("/assistente/alunos.html", context)
    return response

@router.get("/alunos/detalhes")
@requer_autenticacao("assistente")
async def get_alunos_detalhes(request: Request, usuario_logado: dict = None):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/detalhes_alunos.html", {"request": request, "assistente": assistente})
    return response


