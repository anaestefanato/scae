from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analise-inscricoes")
@requer_autenticacao("assistente")
async def get_analise_inscricoes(request: Request):
    response = templates.TemplateResponse("/assistente/analise_inscricoes.html", {"request": request})
    return response

@router.get("/analise-inscricoes/detalhes")
@requer_autenticacao("assistente")
async def get_analise_inscricoes_detalhes(request: Request):
    response = templates.TemplateResponse("/assistente/detalhes_inscricoes.html", {"request": request})
    return response