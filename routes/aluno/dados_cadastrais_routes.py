from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dadoscadastrais")
async def get_dados_cadastrais(request: Request):
    response = templates.TemplateResponse("/aluno/dadoscadastrais.html", {"request": request})
    return response

