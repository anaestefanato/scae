from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/recebimentos")
async def get_recebimentos(request: Request):
    response = templates.TemplateResponse("/aluno/recebimentos.html", {"request": request})
    return response

