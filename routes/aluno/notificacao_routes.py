from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/notificacoes")
@requer_autenticacao(["aluno"])
async def get_notificacoes(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)
    
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/notificacoes.html", {"request": request, "aluno": aluno})
    return response

