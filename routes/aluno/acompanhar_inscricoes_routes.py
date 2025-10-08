from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo, inscricao_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/acompanhar-inscricoes")
@requer_autenticacao(["aluno"])
async def get_acompanhar_inscricoes(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar todas as inscrições do aluno
    inscricoes = inscricao_repo.obter_por_aluno(usuario_logado['id'])
    
    response = templates.TemplateResponse("/aluno/acompanhar_inscricoes.html", {
        "request": request, 
        "aluno": aluno,
        "inscricoes": inscricoes
    })
    return response

@router.get("/acompanhar-inscricoes/recurso")
@requer_autenticacao(["aluno"])
async def get_acompanhar_inscricoes_recurso(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)
    
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/solicitar_recurso.html", {"request": request, "aluno": aluno})
    return response


