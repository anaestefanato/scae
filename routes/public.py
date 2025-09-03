from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import criar_sessao
from util.security import verificar_senha


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("/publicas/index.html", {"request": request})
    return response


@router.get("/login")
async def get_login(request: Request):
    response = templates.TemplateResponse("/publicas/login.html", {"request": request})
    return response



# @router.post("/login")
# async def post_login(request: Request):
#     # fazer checagens antes do redirecionamento
#     response = RedirectResponse(url="/aluno/inicio", status_code=303)
#     return response



@router.get("/cadastro")
async def get_cadastro(request: Request):
    response = templates.TemplateResponse("/publicas/cadastro.html", {"request": request})
    return response

@router.get("/sobre")
async def get_sobre(request: Request):
    response = templates.TemplateResponse("/publicas/sobre.html", {"request": request})
    return response

@router.get("/contato")
async def get_contato(request: Request):
    response = templates.TemplateResponse("/publicas/contato.html", {"request": request})
    return response