from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo, chamado_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/suporte")
@requer_autenticacao(["aluno"])
async def get_suporte(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar chamados do usuário
    chamados = chamado_repo.obter_por_usuario(aluno.id_usuario)
    
    # Buscar estatísticas
    estatisticas = chamado_repo.obter_estatisticas_usuario(aluno.id_usuario)
    
    # Se não há chamados, criar dados de exemplo
    if not chamados:
        chamado_repo.inserir_dados_exemplo(aluno.id_usuario)
        chamados = chamado_repo.obter_por_usuario(aluno.id_usuario)
        estatisticas = chamado_repo.obter_estatisticas_usuario(aluno.id_usuario)
    
    response = templates.TemplateResponse("/aluno/suporte.html", {
        "request": request, 
        "aluno": aluno,
        "chamados": chamados,
        "estatisticas": estatisticas
    })
    return response


