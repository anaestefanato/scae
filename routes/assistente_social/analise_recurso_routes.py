from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analise-recursos")
#@requer_autenticacao("assistente")
async def get_analise_recursos(request: Request):
    usuario_logado = obter_usuario_logado(request)
    if not usuario_logado:
        return RedirectResponse(url="/login", status_code=302)
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/analise_recursos.html", {"request": request, "assistente": assistente})
    return response

