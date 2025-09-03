from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from model.usuario_model import Usuario
from model.cliente_model import Cliente
from repo import usuario_repo, cliente_repo
from util.security import criar_hash_senha, verificar_senha, gerar_token_redefinicao, obter_data_expiracao_token, validar_forca_senha
from util.auth_decorator import criar_sessao, destruir_sessao, obter_usuario_logado, esta_logado
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates/auth")

@router.post("/login")
async def post_login(
    request: Request,
    matricula: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.OBTER_POR_MATRICULA(matricula) 
    
    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Email ou senha inválidos"}
        )
    
    # Criar sessão
    usuario_dict = {
        "id": usuario.id_usuario,
        "nome": usuario.nome,
        "matricula": usuario.matricula,
        "email": usuario.email,
        "perfil": usuario.perfil,
        "foto": usuario.foto
    }
    criar_sessao(request, usuario_dict)
    
    # Redirecionar
    if redirect:
        return RedirectResponse(redirect, status.HTTP_303_SEE_OTHER)
    
    if usuario.perfil == "admin":
        return RedirectResponse("/admin", status.HTTP_303_SEE_OTHER)
    elif usuario.perfil == "assistente":
        return RedirectResponse("/assistente", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)