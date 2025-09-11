from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/suporte")
#@requer_autenticacao(["aluno"])
async def get_suporte(request: Request, matricula: str):
    usuario_logado = obter_usuario_logado(request)
    if not usuario_logado:
        return RedirectResponse(url="/login", status_code=302)
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)
    aluno = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/suporte.html", {"request": request, "aluno": aluno})
    return response


