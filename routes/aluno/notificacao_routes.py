from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/notificacoes")
async def get_notificacoes(request: Request):
    response = templates.TemplateResponse("/aluno/notificacoes.html", {"request": request})
    return response

