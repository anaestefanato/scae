from fastapi import APIRouter, Query, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
import logging

from dtos.cadastro_dto import CadastroUsuarioDTO
from dtos.login_dto import LoginDTO
from model.aluno_model import Aluno
from model.usuario_model import Usuario
from repo import aluno_repo, usuario_repo
from util.auth_decorator import criar_sessao
from util.security import criar_hash_senha, verificar_senha

logger = logging.getLogger(__name__)


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("/publicas/index.html", {"request": request})
    return response


@router.get("/login")
async def get_login(request: Request, matricula: str = Query(None)):
    response = templates.TemplateResponse("/publicas/login.html", {"request": request, "matricula": matricula})
    return response


@router.post("/login")
async def post_login(
    request: Request,
    matricula: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    dados_formulario = {"matricula": matricula}
    try:
        login_dto = LoginDTO(matricula=matricula, senha=senha)
    
        usuario = usuario_repo.obter_usuario_por_matricula(login_dto.matricula) 
        
        if not usuario or not verificar_senha(login_dto.senha, usuario.senha):
            return templates.TemplateResponse(
                "publicas/login.html",
                {"request": request, "erro": "Matrícula ou senha inválidos"}
            )
        
        # Verificar se o usuário é aluno e se está na lista de possíveis alunos (não aprovados)
        if usuario.perfil == "aluno":
            aluno_aprovado = aluno_repo.existe_aluno_aprovado_por_matricula(matricula)
            if not aluno_aprovado:
                return templates.TemplateResponse(
                    "publicas/login.html",
                    {"request": request, "erro": "Seu cadastro ainda está pendente de aprovação pelo administrador."}
                )
        
        # Criar sessão
        usuario_dict = {
            "id": usuario.id_usuario,
            "nome": usuario.nome,
            "matricula": usuario.matricula,
            "email": usuario.email,
            "perfil": usuario.perfil,
            "foto": usuario.foto,
            "completo": aluno_repo.possui_cadastro_completo(usuario.id_usuario) if usuario.perfil == "aluno" else True
        }
        criar_sessao(request, usuario_dict)
        
        # Redirecionar
        if redirect:
            return RedirectResponse(redirect, status.HTTP_303_SEE_OTHER)
        
        if usuario.perfil == "admin":
            return RedirectResponse("/admin/inicio", status.HTTP_303_SEE_OTHER)
        elif usuario.perfil == "assistente":
            return RedirectResponse("/assistente/inicio", status.HTTP_303_SEE_OTHER)
        elif usuario.perfil == "aluno":
            return RedirectResponse("/aluno/inicio", status.HTTP_303_SEE_OTHER)

        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
        
    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        for erro in e.errors():
            campo = erro['loc'][0] if erro['loc'] else 'campo'
            mensagem = erro['msg']
            erros.append(f"{campo.capitalize()}: {mensagem}")

        erro_msg = " | ".join(erros)
        
        # Retornar template com dados preservados e erro
        return templates.TemplateResponse("/publicas/login.html", {
            "request": request,
            "erro": erro_msg,
            "dados": dados_formulario  # Preservar dados digitados
        })
    
    except Exception as e:
        return templates.TemplateResponse(
            "publicas/login.html",
            {"request": request, "erro": str(e), **dados_formulario}
        )
       

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro")
async def get_cadastro(request: Request):
    response = templates.TemplateResponse("/publicas/cadastro.html", {"request": request})
    return response

    
@router.post("/cadastro")
async def processar_cadastro(
    request: Request,
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    conf_senha: str = Form(...),
):
    usuario = usuario_repo.obter_usuario_por_matricula(matricula)
    if usuario:
        return templates.TemplateResponse(
                "publicas/cadastro.html",
                {"request": request, "erro": "Matrícula já cadastrada"}
        )
        
    usuario = usuario_repo.obter_usuario_por_email(email)
    if usuario:
            return templates.TemplateResponse(
                    "publicas/cadastro.html",
                    {"request": request, "erro": "E-mail já cadastrado"}
            )
             
    
    # Verificar se a senha é muito longa (limite do bcrypt: 72 bytes)
    if len(senha.encode('utf-8')) > 72:
        return templates.TemplateResponse(
                "publicas/cadastro.html",
                {"request": request, "erro": "Senha muito longa. Use no máximo 72 caracteres."}
        )

    # Criar dicionário com dados do formulário (para preservar)
    dados_formulario = {
        "nome": nome,
        "matricula": matricula,
        "email": email
        # Não inclua senhas aqui (segurança)
    }

    try:
        # Validar dados com Pydantic
        dados = CadastroUsuarioDTO(
            nome=nome,
            email=email,
            matricula=matricula,
            senha=senha,
            conf_senha=conf_senha
        )

        # Criar objeto Usuario
        usuario = Usuario(
            id_usuario=None,
            nome=dados.nome,
            matricula=dados.matricula,
            email=dados.email,
            senha=criar_hash_senha(dados.senha),
            perfil="aluno",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None
        )

        # Processar cadastro
        id_aluno = aluno_repo.inserir(usuario)

        # Sucesso - Redirecionar com mensagem flash
        return templates.TemplateResponse(
        "publicas/cadastro.html",
        {"request": request, "sucesso": "Cadastro realizado com sucesso! Aguarde aprovação do administrador para fazer login."}
    )

    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        for erro in e.errors():
            campo = erro['loc'][0] if erro['loc'] else 'campo'
            mensagem = erro['msg']
            erros.append(f"{campo.capitalize()}: {mensagem}")

        erro_msg = " | ".join(erros)
        logger.warning(f"Erro de validação no cadastro: {erro_msg}")

        # Retornar template com dados preservados e erro
        return templates.TemplateResponse("publicas/cadastro.html", {
            "request": request,
            "erro": erro_msg,
            "dados": dados_formulario  # Preservar dados digitados
        })

    except Exception as e:
        logger.error(f"Erro ao processar cadastro: {e}")

        return templates.TemplateResponse("publicas/cadastro.html", {
            "request": request,
            "erro": "Erro ao processar cadastro. Tente novamente.",
            "dados": dados_formulario
        })
    
@router.get("/sobre")
async def get_sobre(request: Request):
    response = templates.TemplateResponse("/publicas/sobre.html", {"request": request})
    return response

@router.get("/contato")
async def get_contato(request: Request):
    response = templates.TemplateResponse("/publicas/contato.html", {"request": request})
    return response