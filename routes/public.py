from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import aluno_repo, usuario_repo
from util.auth_decorator import criar_sessao
from util.security import verificar_senha


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("/publicas/index.html", {"request": request})
    return response


@router.get("/login")
async def get_login(request: Request):
    response = templates.TemplateResponse("/publicas/login.html", {"request": request})
    return response


@router.post("/login")
async def post_login(
    request: Request,
    matricula: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.obter_usuario_por_matricula(matricula) 
    
    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            "publicas/login.html",
            {"request": request, "erro": "Matrícula ou senha inválidos"}
        )
    
    # Criar sessão
    usuario_dict = {
        "id": usuario.id_usuario,
        "nome": usuario.nome,
        "matricula": usuario.matricula,
        "email": usuario.email,
        "perfil": usuario.perfil,
        "foto": usuario.foto,
        "completo": aluno_repo.possui_cadastro_completo(usuario.id_usuario)
    }
    criar_sessao(request, usuario_dict)
    
    # Redirecionar
    if redirect:
        return RedirectResponse(redirect, status.HTTP_303_SEE_OTHER)
    
    if usuario.perfil == "admin":
        return RedirectResponse("/admin", status.HTTP_303_SEE_OTHER)
    elif usuario.perfil == "assistente":
        return RedirectResponse("/assistente", status.HTTP_303_SEE_OTHER)
    elif usuario.perfil == "aluno":
        return RedirectResponse("/aluno/inicio", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro")
async def get_cadastro(request: Request):
    response = templates.TemplateResponse("/publicas/cadastro.html", {"request": request})
    return response

@router.get("/sobre")
async def get_sobre(request: Request):
    response = templates.TemplateResponse("/publicas/sobre.html", {"request": request})
    return response

@router.get("/contato")
async def get_contato(request: Request):
    response = templates.TemplateResponse("/publicas/contato.html", {"request": request})
    return response