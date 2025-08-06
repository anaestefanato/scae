from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/aluno/perfil")
async def get_root(request: Request):
    response = templates.TemplateResponse("/perfil/perfil.html", {"request": request})
    return response

