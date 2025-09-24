from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from repo.inscricao_repo import obter_estatisticas_dashboard, obter_inscricoes_recentes_dashboard
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/inicio")
@requer_autenticacao("assistente")
async def get_perfil(request: Request, usuario_logado: dict = None):
    
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar estatísticas do dashboard
    estatisticas = obter_estatisticas_dashboard()
    if not estatisticas:
        estatisticas = {
            'editais_ativos': 0,
            'inscricoes_pendentes': 0,
            'alunos_beneficiados': 0,
            'valor_total_mensal': 0.0
        }
    
    # Buscar inscrições recentes com prioridade
    inscricoes_recentes = obter_inscricoes_recentes_dashboard()
    
    context = {
        "request": request, 
        "assistente": assistente,
        "estatisticas": estatisticas,
        "inscricoes_recentes": inscricoes_recentes
    }
    
    response = templates.TemplateResponse("/assistente/dashboard_assistente.html", context)
    return response

