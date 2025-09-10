from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/suporte")
async def get_suporte(request: Request):
    usuario = request.session.get("usuario")
    if not usuario.completo:
        return RedirectResponse("/aluno/dados-cadastrais", status_code=303)
    
    response = templates.TemplateResponse("/aluno/suporte.html", {"request": request})
    return response


