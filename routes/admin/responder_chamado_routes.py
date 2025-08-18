from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/responder-chamado")
async def get_responder_chamado(request: Request):
    response = templates.TemplateResponse("/admin/responder_chamado.html", {"request": request})
    return response

