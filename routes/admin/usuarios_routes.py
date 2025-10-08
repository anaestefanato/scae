from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from dtos.novo_admin_dto import CadastroAdminDTO
from dtos.novo_assist_dto import CadastroAssistDTO
from model.usuario_model import Usuario
from model.administrador_model import Administrador
from model.assistente_social_model import AssistenteSocial
from repo import administrador_repo, assistente_social_repo, usuario_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao
from util.security import criar_hash_senha


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/usuarios/alunos")
@requer_autenticacao("admin")
async def get_usuario_aluno(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/usuario_aluno.html", {"request": request, "admin": admin})
    return response

@router.get("/usuarios/assistente")
@requer_autenticacao("admin")
async def get_usuario_assistente(request: Request, usuario_logado: dict = None):
    
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/usuario_assist.html", {"request": request, "admin": admin})
    return response

@router.get("/usuarios/admin")
@requer_autenticacao("admin")
async def get_usuario_administrador(request: Request, usuario_logado: dict = None, sucesso: str = None, erro: str = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    context = {
        "request": request, 
        "admin": admin
    }
    
    # Adicionar mensagens se existirem
    if sucesso:
        context["sucesso"] = sucesso
    if erro:
        context["erro"] = erro
    
    response = templates.TemplateResponse("/admin/usuario_admin.html", context)
    return response

@router.get("/usuarios/admin/novo")
@requer_autenticacao("admin")
async def get_usuario_administrador_novo(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/novo_admin.html", {"request": request, "admin": admin})
    return response

@router.post("/usuarios/admin/novo")
@requer_autenticacao("admin")
async def post_criar_admin(
    request: Request,
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    tipo_admin: str = Form(...),
    usuario_logado: dict = None
):
    
    try:
        # Obter dados do admin logado para retornar em caso de erro
        admin_logado = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
        
        # Validar com DTO
        try:
            dados_dto = CadastroAdminDTO(
                nome=nome,
                matricula=matricula,
                email=email,
                senha=senha,
                tipo_admin=tipo_admin
            )
        except ValidationError as e:
            erro_info = e.errors()[0]
            erro_msg = erro_info['msg']
            # Remover o prefixo "Value error, " se existir
            if erro_msg.startswith('Value error, '):
                erro_msg = erro_msg.replace('Value error, ', '', 1)
            # Pegar o nome do campo com erro
            campo_erro = erro_info['loc'][0] if erro_info.get('loc') else ''
            
            return templates.TemplateResponse(
                "admin/novo_admin.html",
                {"request": request, "admin": admin_logado, "erro": erro_msg, "campo_erro": campo_erro}
            )
        
        # Validar tipo_admin
        tipos_validos = ["geral", "sistema", "assistencia"]
        if tipo_admin not in tipos_validos:
            return templates.TemplateResponse(
                "admin/novo_admin.html",
                {"request": request, "admin": admin_logado, "erro": "Tipo de administrador inválido"}
            )
        
        # Validar tamanho da senha para bcrypt (máximo 72 bytes)
        if len(senha.encode('utf-8')) > 72:
            return templates.TemplateResponse(
                "admin/novo_admin.html",
                {"request": request, "admin": admin_logado, "erro": "Senha muito longa. Máximo 72 caracteres."}
            )
        
        # Verificar se matrícula já existe
        usuario = usuario_repo.obter_usuario_por_matricula(matricula)
        if usuario:
            return templates.TemplateResponse(
                "admin/novo_admin.html",
                {"request": request, "admin": admin_logado, "erro": "Matrícula já cadastrada"}
            )
            
        # Verificar se email já existe
        usuario = usuario_repo.obter_usuario_por_email(email)
        if usuario:
            return templates.TemplateResponse(
                "admin/novo_admin.html",
                {"request": request, "admin": admin_logado, "erro": "Email já cadastrado"}
            )  
        
        # Criar hash da senha
        try:
            senha_hash = criar_hash_senha(senha)
        except Exception as e:
            print(f"Erro ao criar hash da senha: {e}")
            return templates.TemplateResponse(
                "admin/novo_admin.html",
                {"request": request, "admin": admin_logado, "erro": "Erro ao processar senha"}
            )
        
        # Criar objeto Administrador
        admin = Administrador(
            id_usuario=None,
            nome=nome.strip(),
            matricula=matricula.strip(),
            email=email.strip().lower(),
            senha=senha_hash,
            perfil="admin",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            tipo_admin=tipo_admin
        )

        # Inserir no banco
        try:
            id_admin = administrador_repo.inserir(admin)
            if not id_admin:
                print("Erro: administrador_repo.inserir() retornou None/False")
                return templates.TemplateResponse(
                    "admin/novo_admin.html",
                    {"request": request, "admin": admin_logado, "erro": "Erro ao criar cadastro. Tente novamente."}
                )
        except Exception as e:
            print(f"Erro ao inserir administrador no banco: {e}")
            return templates.TemplateResponse(
                "admin/novo_admin.html",
                {"request": request, "admin": admin_logado, "erro": "Erro interno do sistema. Tente novamente."}
            )
            
        # Sucesso - redirecionar com mensagem
        return RedirectResponse(url="/admin/usuarios/admin?sucesso=Administrador cadastrado com sucesso!", status_code=303)
        
    except Exception as e:
        print(f"Erro geral na rota post_criar_admin: {e}")
        admin_logado = None
        try:
            admin_logado = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
        except:
            pass
        return templates.TemplateResponse(
            "admin/novo_admin.html",
            {"request": request, "admin": admin_logado, "erro": "Erro interno do sistema"}
        )

@router.get("/usuarios/assistente/novo")
@requer_autenticacao("admin")
async def get_usuario_assistente_novo(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/admin/novo_assist.html", {"request": request, "admin": admin})
    return response

@router.post("/usuarios/assistente/novo")
@requer_autenticacao("admin")
async def post_criar_assistente(
    request: Request,
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    siape: str = Form(...),
    usuario_logado: dict = None
):
    try:
        # Obter dados do admin logado
        admin_logado = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
        
        # Validar com DTO
        try:
            dados_dto = CadastroAssistDTO(
                nome=nome,
                matricula=matricula,
                email=email,
                senha=senha,
                siape=siape
            )
        except ValidationError as e:
            erro_info = e.errors()[0]
            erro_msg = erro_info['msg']
            # Remover o prefixo "Value error, " se existir
            if erro_msg.startswith('Value error, '):
                erro_msg = erro_msg.replace('Value error, ', '', 1)
            # Pegar o nome do campo com erro
            campo_erro = erro_info['loc'][0] if erro_info.get('loc') else ''
            
            return templates.TemplateResponse(
                "admin/novo_assist.html",
                {"request": request, "admin": admin_logado, "erro": erro_msg, "campo_erro": campo_erro}
            )
        
        # Validar tamanho da senha para bcrypt (máximo 72 bytes)
        if len(senha.encode('utf-8')) > 72:
            return templates.TemplateResponse(
                "admin/novo_assist.html",
                {"request": request, "admin": admin_logado, "erro": "Senha muito longa. Máximo 72 caracteres."}
            )
        
        # Verificar se matrícula já existe
        usuario = usuario_repo.obter_usuario_por_matricula(matricula)
        if usuario:
            return templates.TemplateResponse(
                "admin/novo_assist.html",
                {"request": request, "admin": admin_logado, "erro": "Matrícula já cadastrada"}
            )
            
        # Verificar se email já existe
        usuario = usuario_repo.obter_usuario_por_email(email)
        if usuario:
            return templates.TemplateResponse(
                "admin/novo_assist.html",
                {"request": request, "admin": admin_logado, "erro": "Email já cadastrado"}
            )

        # Criar hash da senha
        try:
            senha_hash = criar_hash_senha(senha)
        except Exception as e:
            print(f"Erro ao criar hash da senha: {e}")
            return templates.TemplateResponse(
                "admin/novo_assist.html",
                {"request": request, "admin": admin_logado, "erro": "Erro ao processar senha"}
            )

        # Criar objeto AssistenteSocial
        assistente = AssistenteSocial(
            id_usuario=None,
            nome=nome.strip(),
            matricula=matricula.strip(),
            email=email.strip().lower(),
            senha=senha_hash,
            perfil="assistente",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            siape=siape.strip()
        )

        # Inserir no banco
        try:
            id_assistente = assistente_social_repo.inserir(assistente)
            if not id_assistente:
                print("Erro: assistente_social_repo.inserir() retornou None/False")
                return templates.TemplateResponse(
                    "admin/novo_assist.html",
                    {"request": request, "admin": admin_logado, "erro": "Erro ao criar cadastro. Tente novamente."}
                )
        except Exception as e:
            print(f"Erro ao inserir assistente no banco: {e}")
            return templates.TemplateResponse(
                "admin/novo_assist.html",
                {"request": request, "admin": admin_logado, "erro": "Erro interno do sistema. Tente novamente."}
            )

        # Sucesso - redirecionar com mensagem
        return RedirectResponse(url="/admin/usuarios/assistente?sucesso=Assistente cadastrado com sucesso!", status_code=303)
        
    except Exception as e:
        print(f"Erro geral na rota post_criar_assistente: {e}")
        admin_logado = None
        try:
            admin_logado = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
        except:
            pass
        return templates.TemplateResponse(
            "admin/novo_assist.html",
            {"request": request, "admin": admin_logado, "erro": "Erro interno do sistema"}
        )

       