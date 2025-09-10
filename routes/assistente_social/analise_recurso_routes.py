from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analise-recursos")
@requer_autenticacao("assistente")
async def get_analise_recursos(request: Request):
    response = templates.TemplateResponse("/assistente/analise_recursos.html", {"request": request})
    return response

