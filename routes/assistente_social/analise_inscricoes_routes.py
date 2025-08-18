from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analise-inscricoes")
async def get_analise_inscricoes(request: Request):
    response = templates.TemplateResponse("/assistente/analise_inscricoes.html", {"request": request})
    return response

