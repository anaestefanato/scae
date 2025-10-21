from fastapi import APIRouter, Request, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import math
from datetime import datetime

from repo import usuario_repo, inscricao_repo, auxilio_repo
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

@router.post("/analise-inscricoes/deferir-auxilio")
@requer_autenticacao("assistente")
async def deferir_auxilio(request: Request, usuario_logado: dict = None):
    """Endpoint para deferir um auxílio específico"""
    try:
        data = await request.json()
        id_auxilio = data.get('id_auxilio')
        valor_mensal = data.get('valor_mensal')
        observacoes = data.get('observacoes', '')
        
        if not id_auxilio:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "ID do auxílio não fornecido"}
            )
        
        if not valor_mensal or float(valor_mensal) <= 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Valor mensal é obrigatório e deve ser maior que zero"}
            )
        
        # Atualizar status e valor do auxílio
        sucesso_status = auxilio_repo.atualizar_status_auxilio(id_auxilio, 'deferido')
        sucesso_valor = auxilio_repo.atualizar_valor_auxilio(id_auxilio, float(valor_mensal))
        
        # Obter a inscrição relacionada e atualizar seu status para 'analisado'
        auxilio = auxilio_repo.obter_por_id(id_auxilio)
        if auxilio and auxilio.id_inscricao:
            inscricao_repo.atualizar_status(auxilio.id_inscricao, 'analisado')
        
        if sucesso_status and sucesso_valor:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True, 
                    "message": "Auxílio deferido com sucesso",
                    "id_auxilio": id_auxilio,
                    "status": "deferido",
                    "valor_mensal": float(valor_mensal)
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Erro ao deferir auxílio"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Erro: {str(e)}"}
        )

@router.post("/analise-inscricoes/indeferir-auxilio")
@requer_autenticacao("assistente")
async def indeferir_auxilio(request: Request, usuario_logado: dict = None):
    """Endpoint para indeferir um auxílio específico"""
    try:
        data = await request.json()
        id_auxilio = data.get('id_auxilio')
        motivo = data.get('motivo', '')
        
        if not id_auxilio:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "ID do auxílio não fornecido"}
            )
        
        if not motivo:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Motivo do indeferimento é obrigatório"}
            )
        
        # Atualizar status do auxílio
        sucesso_status = auxilio_repo.atualizar_status_auxilio(id_auxilio, 'indeferido')
        sucesso_motivo = auxilio_repo.atualizar_motivo_indeferimento(id_auxilio, motivo)
        
        # Obter a inscrição relacionada e atualizar seu status para 'analisado'
        auxilio = auxilio_repo.obter_por_id(id_auxilio)
        if auxilio and auxilio.id_inscricao:
            inscricao_repo.atualizar_status(auxilio.id_inscricao, 'analisado')
        
        if sucesso_status and sucesso_motivo:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True, 
                    "message": "Auxílio indeferido com sucesso",
                    "id_auxilio": id_auxilio,
                    "status": "indeferido",
                    "motivo": motivo
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Erro ao indeferir auxílio"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Erro: {str(e)}"}
        )

@router.get("/analise-inscricoes/auxilios/{id_inscricao}")
@requer_autenticacao("assistente")
async def obter_auxilios_inscricao(id_inscricao: int, request: Request, usuario_logado: dict = None):
    """Endpoint para obter todos os auxílios de uma inscrição com seus status"""
    try:
        auxilios = auxilio_repo.obter_auxilios_por_inscricao(id_inscricao)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "auxilios": auxilios
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Erro: {str(e)}"}
        )
