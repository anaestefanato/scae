from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


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
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.obter_por_email(email)
    
    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Email ou senha inválidos"}
        )
    
    # Criar sessão
    usuario_dict = {
        "id": usuario.id,
        "nome": usuario.nome,
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

# @router.post("/login")
# async def post_login(request: Request):
#     # fazer checagens antes do redirecionamento
#     response = RedirectResponse(url="/aluno/inicio", status_code=303)
#     return response


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