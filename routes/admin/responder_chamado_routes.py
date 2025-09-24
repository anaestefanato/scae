from fastapi import APIRouter, Request, Query, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo, chamado_repo, resposta_chamado_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/chamados")
@requer_autenticacao(["admin"])
async def get_chamados(
    request: Request, 
    usuario_logado: dict = None,
    pagina: int = Query(1, ge=1),
    status: str = Query(None),
    categoria: str = Query(None),
    busca: str = Query(None)
):
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Obter chamados com filtros e paginação
    result = chamado_repo.obter_por_pagina_com_usuario(
        pagina=pagina, 
        limit=10,
        filtro_status=status,
        filtro_categoria=categoria
    )
    
    # Se não há chamados, criar dados de exemplo
    if result['total'] == 0:
        # Inserir dados de exemplo para usuário admin
        chamado_repo.inserir_dados_exemplo(admin.id_usuario)
        result = chamado_repo.obter_por_pagina_com_usuario(pagina=pagina, limit=10)
    
    # Obter estatísticas gerais
    estatisticas = chamado_repo.obter_estatisticas_gerais()
    
    response = templates.TemplateResponse("/admin/chamado.html", {
        "request": request, 
        "admin": admin,
        "chamados": result['chamados'],
        "pagination": {
            'current_page': result['current_page'],
            'total_pages': result['total_pages'],
            'has_next': result['has_next'],
            'has_prev': result['has_prev'],
            'total': result['total']
        },
        "estatisticas": estatisticas,
        "filtros": {
            'status': status,
            'categoria': categoria,
            'busca': busca
        }
    })
    return response

@router.post("/chamados/{id_chamado}/status")
@requer_autenticacao(["admin"])
async def atualizar_status_chamado(
    id_chamado: int,
    request: Request,
    status: str = Form(...),
    usuario_logado: dict = None
):
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    success = chamado_repo.atualizar_status(id_chamado, status, admin.id_usuario)
    
    if not success:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    
    return RedirectResponse("/admin/chamados", status_code=303)

@router.get("/chamados/{id_chamado}/detalhes")
@requer_autenticacao(["admin"])
async def get_detalhes_chamado(
    id_chamado: int,
    request: Request,
    usuario_logado: dict = None
):
    chamado = chamado_repo.obter_por_id(id_chamado)
    
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    
    # Buscar informações do usuário que criou o chamado
    usuario = usuario_repo.obter_usuario_por_id(chamado.id_usuario_criador)
    
    # Buscar respostas do chamado (se houver)
    respostas = resposta_chamado_repo.obter_por_chamado(id_chamado)
    
    return {
        "chamado": chamado.__dict__,
        "usuario": usuario.__dict__ if usuario else None,
        "respostas": [resposta.__dict__ for resposta in respostas] if respostas else []
    }

@router.post("/chamados/{id_chamado}/responder")
@requer_autenticacao(["admin"])
async def responder_chamado(
    id_chamado: int,
    request: Request,
    mensagem: str = Form(...),
    status: str = Form("em-andamento"),
    usuario_logado: dict = None
):
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Verificar se o chamado existe
    chamado = chamado_repo.obter_por_id(id_chamado)
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    
    # Criar resposta
    from model.resposta_chamado_model import RespostaChamado
    from datetime import datetime
    
    resposta = RespostaChamado(
        id_resposta=None,
        id_chamado=id_chamado,
        id_usuario=admin.id_usuario,
        mensagem=mensagem,
        data_resposta=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status=""
    )
    
    # Inserir resposta
    resposta_chamado_repo.inserir(resposta)
    
    # Atualizar status do chamado
    chamado_repo.atualizar_status(id_chamado, status, admin.id_usuario)
    
    return RedirectResponse("/admin/chamados", status_code=303)

