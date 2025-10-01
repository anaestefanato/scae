from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/entrevistas")
@requer_autenticacao("assistente")
async def get_entrevistas(request: Request, usuario_logado: dict = None):
    
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/entrevistas.html", {"request": request, "assistente": assistente})
    return response

@router.get("/entrevistas/nova")
@requer_autenticacao("assistente")
async def get_entrevistas_nova(request: Request, usuario_logado: dict = None):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/nova_entrevista.html", {"request": request, "assistente": assistente})
    return response

@router.get("/nova-entrevista")
@requer_autenticacao("assistente")
async def get_nova_entrevista(request: Request, usuario_logado: dict = None):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/assistente/nova_entrevista.html", {"request": request, "assistente": assistente})
    return response
