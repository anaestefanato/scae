from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analise-inscricoes")
#@requer_autenticacao("assistente")
async def get_analise_inscricoes(request: Request):
    usuario_logado = obter_usuario_logado(request)
    if not usuario_logado:
        return RedirectResponse(url="/login", status_code=302)
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/analise_inscricoes.html", {"request": request, "assistente": assistente})
    return response

@router.get("/analise-inscricoes/detalhes")
#@requer_autenticacao("assistente")
async def get_analise_inscricoes_detalhes(request: Request):
    usuario_logado = obter_usuario_logado(request)
    if not usuario_logado:
        return RedirectResponse(url="/login", status_code=302)
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/detalhes_inscricoes.html", {"request": request, "assistente": assistente})
    return response