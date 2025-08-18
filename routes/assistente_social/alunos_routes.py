from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/alunos")
async def get_alunos(request: Request):
    response = templates.TemplateResponse("/assistente/alunos.html", {"request": request})
    return response

@router.get("/alunos/detalhes")
async def get_alunos_detalhes(request: Request):
    response = templates.TemplateResponse("/assistente/detalhes_alunos.html", {"request": request})
    return response


