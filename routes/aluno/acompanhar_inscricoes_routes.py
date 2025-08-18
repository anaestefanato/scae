from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/acompanhar-inscricoes")
async def get_acompanhar_inscricoes(request: Request):
    response = templates.TemplateResponse("/aluno/acompanhar_inscricoes.html", {"request": request})
    return response

