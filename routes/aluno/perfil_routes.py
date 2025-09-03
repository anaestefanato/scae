from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from repo import aluno_repo, usuario_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

# TESTE COM USUARIO NO LUGAR DE ALUNO PORQUE A TABELA ALUNO NÃO ESTÁ FUNCIONANDO
@router.get("/inicio/{id}")
async def get_root(request: Request, id: int):
    usuario = usuario_repo.obter_por_id(id)
    response = templates.TemplateResponse("/aluno/dashboard.html", {"request": request, "usuario": usuario})
    return response

