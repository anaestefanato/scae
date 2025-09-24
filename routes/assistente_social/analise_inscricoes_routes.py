from fastapi import APIRouter, Request, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import math

from repo import usuario_repo, inscricao_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analise-inscricoes")
@requer_autenticacao("assistente")
async def get_analise_inscricoes(request: Request, usuario_logado: dict = None, pagina: int = Query(1, ge=1)):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar estatísticas
    estatisticas = inscricao_repo.obter_estatisticas_analise()
    
    # Buscar inscrições para análise com paginação
    limite = 10
    inscricoes, total = inscricao_repo.obter_inscricoes_para_analise(pagina, limite)
    
    # Calcular informações de paginação
    total_paginas = math.ceil(total / limite)
    tem_anterior = pagina > 1
    tem_proximo = pagina < total_paginas
    
    response = templates.TemplateResponse("/assistente/analise_inscricoes.html", {
        "request": request, 
        "assistente": assistente,
        "estatisticas": estatisticas,
        "inscricoes": inscricoes,
        "pagina_atual": pagina,
        "total_paginas": total_paginas,
        "tem_anterior": tem_anterior,
        "tem_proximo": tem_proximo,
        "total_inscricoes": total
    })
    return response

@router.get("/analise-inscricoes/detalhes")
@requer_autenticacao("assistente")
async def get_analise_inscricoes_detalhes(request: Request, usuario_logado: dict = None):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/detalhes_inscricoes.html", {"request": request, "assistente": assistente})
    return response