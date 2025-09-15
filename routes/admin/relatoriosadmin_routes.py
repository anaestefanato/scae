from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/relatorios")
@requer_autenticacao("admin")
async def get_relatorios(request: Request, usuario_logado: dict = None):
    
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/relatorios.html", {"request": request, "admin": admin})
    return response

