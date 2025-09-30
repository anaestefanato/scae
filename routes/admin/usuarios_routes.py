from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/usuarios/alunos")
@requer_autenticacao("admin")
async def get_usuario_aluno(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/usuario_aluno.html", {"request": request, "admin": admin})
    return response

@router.get("/usuarios/assistente")
@requer_autenticacao("admin")
async def get_usuario_assistente(request: Request, usuario_logado: dict = None):
    
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/usuario_assist.html", {"request": request, "admin": admin})
    return response

@router.get("/usuarios/admin")
@requer_autenticacao("admin")
async def get_usuario_administrador(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/usuario_admin.html", {"request": request, "admin": admin})
    return response

@router.get("/usuarios/admin/novo")
@requer_autenticacao("admin")
async def get_usuario_administrador_novo(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/novo_admin.html", {"request": request, "admin": admin})
    return response

@router.get("/usuarios/assistente/novo")
@requer_autenticacao("admin")
async def get_usuario_assistente_novo(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/novo_assist.html", {"request": request, "admin": admin})
    return response