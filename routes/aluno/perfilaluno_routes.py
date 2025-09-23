from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import aluno_repo, usuario_repo, auxilio_repo, edital_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/inicio")
@requer_autenticacao(["aluno"])
async def get_root(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    auxilios = auxilio_repo.obter_por_aluno(aluno.id_usuario)
    editais_abertos = edital_repo.obter_editais_abertos()
    
    response = templates.TemplateResponse("/aluno/dashboard.html", {
        "request": request, 
        "aluno": aluno,
        "auxilios": auxilios,
        "editais_abertos": editais_abertos
    })
    return response

