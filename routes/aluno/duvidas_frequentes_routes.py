from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/duvidas")
async def get_duvidas(request: Request):
    response = templates.TemplateResponse("/aluno/duvidas.html", {"request": request})
    return response

