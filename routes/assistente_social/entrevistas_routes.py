from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/entrevistas")
async def get_entrevistas(request: Request):
    response = templates.TemplateResponse("/assistente/entrevistas.html", {"request": request})
    return response

@router.get("/entrevistas/nova")
async def get_entrevistas_nova(request: Request):
    response = templates.TemplateResponse("/assistente/nova_entrevista.html", {"request": request})
    return response
