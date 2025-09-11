from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dadoscadastrais")
# @requer_autenticacao(["aluno"])
async def get_dados_cadastrais(request: Request):
    usuario_logado = obter_usuario_logado(request)
    if not usuario_logado:
        return RedirectResponse(url="/login", status_code=302)
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])                 
    response = templates.TemplateResponse("/aluno/dadoscadastrais.html", {"request": request, "aluno": aluno})
    return response

