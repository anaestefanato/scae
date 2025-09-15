from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/editais")
@requer_autenticacao(["aluno"])
async def get_editais(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/editais.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/detalhes")
@requer_autenticacao(["aluno"])
async def get_editais_detalhes(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/editais_detalhes.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/primeira-inscricao")
@requer_autenticacao(["aluno"])
async def get_editais_primeira_inscricao(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/editais_primeira_inscricao.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/renovacao")
@requer_autenticacao(["aluno"])
async def get_editais_renovacao(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/editais_renovacao.html", {"request": request, "aluno": aluno})
    return response
