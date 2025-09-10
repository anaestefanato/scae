from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import aluno_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/acompanhar-inscricoes")
async def get_acompanhar_inscricoes(request: Request):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dados-cadastrais", status_code=303)
        
    response = templates.TemplateResponse("/aluno/acompanhar_inscricoes.html", {"request": request})
    return response

@router.get("/acompanhar-inscricoes/recurso")
async def get_acompanhar_inscricoes_recurso(request: Request):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dados-cadastrais", status_code=303)
    
    response = templates.TemplateResponse("/aluno/solicitar_recurso.html", {"request": request})
    return response
