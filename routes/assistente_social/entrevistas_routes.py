from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/entrevistas")
@requer_autenticacao("assistente")
async def get_entrevistas(request: Request):
    response = templates.TemplateResponse("/assistente/entrevistas.html", {"request": request})
    return response

@router.get("/entrevistas/nova")
@requer_autenticacao("assistente")
async def get_entrevistas_nova(request: Request):
    response = templates.TemplateResponse("/assistente/nova_entrevista.html", {"request": request})
    return response
