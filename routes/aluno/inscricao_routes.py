from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from repo import inscricao_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/aluno/inscricao/listar")
async def get_inscricoes():
    inscricoes = inscricao_repo.inserir()
    response = templates.TemplateResponse("aluno/listar_inscricoes.html", {"request": {}, "inscricoes": inscricoes})
    return response