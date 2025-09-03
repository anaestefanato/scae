from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/duvidas")
@requer_autenticacao(["aluno"])
async def get_duvidas(request: Request):
    response = templates.TemplateResponse("/aluno/duvidas.html", {"request": request})
    return response

