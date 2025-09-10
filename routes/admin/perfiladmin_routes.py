from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/inicio")
@requer_autenticacao("admin")
async def get_perfil(request: Request, matricula: str):
    admin = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/admin/dashboard.html", {"request": request, "admin": admin})
    return response

