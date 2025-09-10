from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/recebimentos")
@requer_autenticacao(["aluno"])
async def get_recebimentos(request: Request, matricula: str):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dadoscadastrais", status_code=303)
    aluno = usuario_repo.obter_usuario_por_matricula(matricula)
    response = templates.TemplateResponse("/aluno/recebimentos.html", {"request": request, "aluno": aluno})
    return response

