from fastapi import APIRouter, Request, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import math
from datetime import datetime

from repo import usuario_repo, inscricao_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Adicionar filtro personalizado para formatar datas
def formatar_data(data_str):
    """Formata string de data para padrão DD/MM/YYYY"""
    if not data_str:
        return 'N/A'
    
    try:
        # Tenta formatos comuns
        for formato in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']:
            try:
                data_obj = datetime.strptime(str(data_str), formato)
                return data_obj.strftime('%d/%m/%Y')
            except ValueError:
                continue
        # Se nenhum formato funcionar, retorna a string original
        return str(data_str)
    except:
        return str(data_str)

templates.env.filters['formatar_data'] = formatar_data


@router.get("/analise-inscricoes")
@requer_autenticacao("assistente")
async def get_analise_inscricoes(
    request: Request, 
    usuario_logado: dict = None, 
    pagina: int = Query(1, ge=1),
    edital: str = Query(None),
    status: str = Query(None),
    ordenacao: str = Query(None),
    busca: str = Query(None)
):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar estatísticas
    estatisticas = inscricao_repo.obter_estatisticas_analise()
    
    # Buscar inscrições para análise com paginação e filtros
    limite = 10
    inscricoes, total = inscricao_repo.obter_inscricoes_para_analise(
        pagina=pagina, 
        limite=limite,
        filtro_edital=edital,
        filtro_status=status,
        filtro_busca=busca,
        ordenacao=ordenacao
    )
    
    # Calcular informações de paginação
    total_paginas = math.ceil(total / limite) if total > 0 else 1
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
        "total_inscricoes": total,
        "filtro_edital": edital,
        "filtro_status": status,
        "filtro_ordenacao": ordenacao,
        "filtro_busca": busca
    })
    return response

@router.get("/analise-inscricoes/detalhes")
@requer_autenticacao("assistente")
async def get_analise_inscricoes_detalhes(request: Request, usuario_logado: dict = None):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/detalhes_inscricoes.html", {"request": request, "assistente": assistente})
    return response