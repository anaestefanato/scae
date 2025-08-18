from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analisar-cadastro")
async def get_analisar_cadastro(request: Request):
    response = templates.TemplateResponse("/admin/analisar_cadastro.html", {"request": request})
    return response

