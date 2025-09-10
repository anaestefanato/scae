from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/inicio")
@requer_autenticacao("admin")
async def get_perfil(request: Request):
    usuario_logado = obter_usuario_logado(request)
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/dashboard.html", {"request": request, "admin": admin})
    return response

