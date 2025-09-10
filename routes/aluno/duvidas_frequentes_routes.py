from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/duvidas")
@requer_autenticacao(["aluno"])
async def get_duvidas(request: Request):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dados-cadastrais", status_code=303)
    response = templates.TemplateResponse("/aluno/duvidas.html", {"request": request})
    return response

