from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/editais")
@requer_autenticacao(["aluno"])
async def get_editais(request: Request, matricula: str):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)
    
    aluno = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/editais.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/detalhes")
@requer_autenticacao(["aluno"])
async def get_editais_detalhes(request: Request, matricula: str):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/editais_detalhes.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/primeira-inscricao")
@requer_autenticacao(["aluno"])
async def get_editais_primeira_inscricao(request: Request, matricula: str):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/editais_primeira_inscricao.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/renovacao")
@requer_autenticacao(["aluno"])
async def get_editais_renovacao(request: Request, matricula: str):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/editais_renovacao.html", {"request": request, "aluno": aluno})
    return response
