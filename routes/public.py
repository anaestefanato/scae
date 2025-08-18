from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("/home/index.html", {"request": request})
    return response


@router.get("/login")
async def get_login(request: Request):
    response = templates.TemplateResponse("/login/login.html", {"request": request})
    return response

@router.post("/login")
async def post_login(request: Request):
    # fazer checagens antes do redirecionamento
    response = RedirectResponse(url="/aluno/inicio", status_code=303)
    return response


@router.get("/cadastro")
async def get_cadastro(request: Request):
    response = templates.TemplateResponse("/cadastro/cadastro.html", {"request": request})
    return response

@router.get("/sobre")
async def get_sobre(request: Request):
    response = templates.TemplateResponse("/sobre/sobre.html", {"request": request})
    return response