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

@router.get("/editais/primeira-inscricao")
async def get_editais_primeira_inscricao(request: Request):
    response = templates.TemplateResponse("/aluno/editais_primeira_inscricao.html", {"request": request})
    return response

@router.get("/editais/renovacao")
async def get_editais_renovacao(request: Request):
    response = templates.TemplateResponse("/aluno/editais_renovacao.html", {"request": request})
    return response
