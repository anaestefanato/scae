from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/relatorios")
async def get_relatorios(request: Request):
    response = templates.TemplateResponse("/assistente/relatorios.html", {"request": request})
    return response

