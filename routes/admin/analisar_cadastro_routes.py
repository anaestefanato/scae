from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo, aluno_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analisar-cadastros")
@requer_autenticacao("admin")
async def get_analisar_cadastros(request: Request, usuario_logado: dict = None):
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    possiveis_alunos = aluno_repo.obter_possiveis_alunos()
    
    context = {
        "request": request, 
        "admin": admin,
        "possiveis_alunos": possiveis_alunos
    }
    
    response = templates.TemplateResponse("admin/analisar_cadastros.html", context)
    return response


@router.post("/aprovar-usuario/{id_usuario}")
@requer_autenticacao("admin")
async def aprovar_usuario(request: Request, id_usuario: int, usuario_logado: dict = None):
    sucesso = aluno_repo.aprovar_aluno(id_usuario)
    
    # Verificar se a requisição vem do dashboard
    referer = request.headers.get("referer", "")
    if "/admin/inicio" in referer:
        redirect_url = "/admin/inicio"
    else:
        redirect_url = "/admin/analisar-cadastros"
    
    if sucesso:
        return RedirectResponse(f"{redirect_url}?sucesso=Usuario aprovado com sucesso!", status_code=302)
    else:
        return RedirectResponse(f"{redirect_url}?erro=Erro ao aprovar usuário.", status_code=302)


@router.post("/rejeitar-usuario/{id_usuario}")
@requer_autenticacao("admin")
async def rejeitar_usuario(request: Request, id_usuario: int, usuario_logado: dict = None):
    sucesso = aluno_repo.rejeitar_aluno(id_usuario)
    
    # Verificar se a requisição vem do dashboard
    referer = request.headers.get("referer", "")
    if "/admin/inicio" in referer:
        redirect_url = "/admin/inicio"
    else:
        redirect_url = "/admin/analisar-cadastros"
    
    if sucesso:
        return RedirectResponse(f"{redirect_url}?sucesso=Usuario rejeitado com sucesso!", status_code=302)
    else:
        return RedirectResponse(f"{redirect_url}?erro=Erro ao rejeitar usuário.", status_code=302)


@router.get("/inscricoes")
@requer_autenticacao("admin")
async def get_analisar_inscricoes(request: Request, usuario_logado: dict = None):
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("admin/analisar_incricoes.html", {"request": request, "admin": admin})
    return response


