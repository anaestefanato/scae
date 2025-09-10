from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import aluno_repo
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/acompanhar-inscricoes")
@requer_autenticacao(["aluno"])
async def get_acompanhar_inscricoes(request: Request, matricula: str):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dados-cadastrais", status_code=303)

    aluno = aluno_repo.obter_aluno_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/acompanhar_inscricoes.html", {"request": request, "aluno": aluno})
    return response

@router.get("/acompanhar-inscricoes/recurso")
async def get_acompanhar_inscricoes_recurso(request: Request, matricula: str):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dados-cadastrais", status_code=303)
    aluno = aluno_repo.obter_aluno_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/solicitar_recurso.html", {"request": request, "aluno": aluno})
    return response
