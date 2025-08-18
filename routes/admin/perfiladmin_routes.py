from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/inicio")
async def get_perfil(request: Request):
    response = templates.TemplateResponse("/admin/dashboard.html", {"request": request})
    return response

