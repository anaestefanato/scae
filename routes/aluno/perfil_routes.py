from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/inicio")
async def get_root(request: Request):
    response = templates.TemplateResponse("/aluno/dashboard.html", {"request": request})
    return response

