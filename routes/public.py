from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("/home/index.html", {"request": request})
    return response


@router.get("/login")
async def get_root(request: Request):
    response = templates.TemplateResponse("/login/login.html", {"request": request})
    return response




