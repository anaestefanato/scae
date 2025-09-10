from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/responder-chamado")
@requer_autenticacao("admin")
async def get_responder_chamado(request: Request, matricula: str):
    admin = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/admin/responder_chamado.html", {"request": request, "admin": admin})
    return response

