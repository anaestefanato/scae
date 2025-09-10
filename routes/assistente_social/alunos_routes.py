from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/alunos")
@requer_autenticacao("assistente")
async def get_alunos(request: Request):
    response = templates.TemplateResponse("/assistente/alunos.html", {"request": request})
    return response

@router.get("/alunos/detalhes")
@requer_autenticacao("assistente")
async def get_alunos_detalhes(request: Request):
    response = templates.TemplateResponse("/assistente/detalhes_alunos.html", {"request": request})
    return response


