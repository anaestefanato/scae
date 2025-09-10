from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/agenda")
@requer_autenticacao("assistente")
async def get_agenda(request: Request):
    response = templates.TemplateResponse("/assistente/agenda.html", {"request": request})
    return response

