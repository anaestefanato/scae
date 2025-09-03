from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/suporte")
async def get_suporte(request: Request):
    response = templates.TemplateResponse("/aluno/suporte.html", {"request": request})
    return response


