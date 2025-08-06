from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from repo import edital_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/aluno/editais")
async def get_root(request: Request):
    editais = edital_repo.obter_todos()
    response = templates.TemplateResponse("/editais/editais.html", {"request": request, "editais": editais})
    return response
   
