from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/relatorios")
@requer_autenticacao("assistente")
async def get_relatorios(request: Request):
    response = templates.TemplateResponse("/assistente/relatorios.html", {"request": request})
    return response

