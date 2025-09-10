from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import aluno_repo, usuario_repo
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")

# TESTE COM USUARIO NO LUGAR DE ALUNO PORQUE A TABELA ALUNO NÃO ESTÁ FUNCIONANDO
@router.get("/inicio/{matricula}")
@requer_autenticacao(["aluno"])
async def get_root(request: Request, matricula: str):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dados-cadastrais", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/dashboard.html", {"request": request, "aluno": aluno})
    return response

