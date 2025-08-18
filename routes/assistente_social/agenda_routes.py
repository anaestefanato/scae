from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/agenda")
async def get_agenda(request: Request):
    response = templates.TemplateResponse("/assistente/agenda.html", {"request": request})
    return response

