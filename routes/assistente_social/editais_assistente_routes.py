from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/editais")
@requer_autenticacao("assistente")
async def get_editais_assistente(request: Request, usuario_logado: dict = None):
    """
    Página de gerenciamento de editais para assistentes sociais.
    Permite visualizar, publicar e gerenciar editais, cronogramas, anexos e resultados.
    """
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    context = {
        "request": request,
        "assistente": assistente
    }
    
    response = templates.TemplateResponse("/assistente/editais_assist.html", context)
    return response
