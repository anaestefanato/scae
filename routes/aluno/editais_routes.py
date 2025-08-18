from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/editais")
async def get_editais(request: Request):
    response = templates.TemplateResponse("/aluno/editais.html", {"request": request})
    return response

@router.get("/editais/detalhes")
async def get_editais_detalhes(request: Request):
    response = templates.TemplateResponse("/aluno/editais_detalhes.html", {"request": request})
    return response

