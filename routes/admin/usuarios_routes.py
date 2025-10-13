from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from dtos.novo_admin_dto import CadastroAdminDTO
from dtos.novo_assist_dto import CadastroAssistDTO
from model.usuario_model import Usuario
from model.administrador_model import Administrador
from model.assistente_social_model import AssistenteSocial
from repo import administrador_repo, assistente_social_repo, usuario_repo, aluno_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao
from util.security import criar_hash_senha


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/usuarios/alunos")
@requer_autenticacao("admin")
async def get_usuario_aluno(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    alunos = aluno_repo.obter_todos()
    
    # Converter objetos para dicionários para serialização JSON com todos os campos
    alunos_dict = [
        {
            "id_usuario": a.id_usuario,
            "nome": a.nome,
            "matricula": a.matricula,
            "email": a.email,
            "cpf": a.cpf if a.cpf else "",
            "telefone": a.telefone if a.telefone else "",
            "curso": a.curso if a.curso else "",
            "data_nascimento": a.data_nascimento if a.data_nascimento else "",
            "filiacao": a.filiacao if a.filiacao else "",
            "cep": a.cep if a.cep else "",
            "cidade": a.cidade if a.cidade else "",
            "bairro": a.bairro if a.bairro else "",
            "rua": a.rua if a.rua else "",
            "numero": a.numero if a.numero else "",
            "estado": a.estado if a.estado else "",
            "complemento": a.complemento if a.complemento else "",
            "nome_banco": a.nome_banco if a.nome_banco else "",
            "agencia_bancaria": a.agencia_bancaria if a.agencia_bancaria else "",
            "numero_conta_bancaria": a.numero_conta_bancaria if a.numero_conta_bancaria else "",
            "renda_familiar": a.renda_familiar if a.renda_familiar else 0,
            "quantidade_pessoas": a.quantidade_pessoas if a.quantidade_pessoas else 0,
            "renda_per_capita": a.renda_per_capita if a.renda_per_capita else 0,
            "situacao_moradia": a.situacao_moradia if a.situacao_moradia else "",
            "aprovado": a.aprovado if hasattr(a, 'aprovado') else False,
            "perfil": a.perfil
        }
        for a in alunos
    ]
    
    response = templates.TemplateResponse("/admin/usuario_aluno.html", {
        "request": request, 
        "admin": admin,
        "alunos": alunos_dict,
        "total_alunos": len(alunos_dict)
    })
    return response

@router.get("/usuarios/assistente")
@requer_autenticacao("admin")
async def get_usuario_assistente(request: Request, usuario_logado: dict = None, sucesso: str = None):
    
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    assistentes = assistente_social_repo.obter_todos()
    
    # Converter objetos para dicionários para serialização JSON
    assistentes_dict = [
        {
            "id_usuario": a.id_usuario,
            "nome": a.nome,
            "matricula": a.matricula,
            "email": a.email,
            "siape": a.siape,
            "perfil": a.perfil
        }
        for a in assistentes
    ]
    
    context = {
        "request": request,
        "admin": admin,
        "assistentes": assistentes_dict
    }
    
    if sucesso:
        context["sucesso"] = sucesso
    
    response = templates.TemplateResponse("/admin/usuario_assist.html", context)
    return response

@router.get("/usuarios/admin")
@requer_autenticacao("admin")
async def get_usuario_administrador(request: Request, usuario_logado: dict = None, sucesso: str = None, erro: str = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    administradores_obj = administrador_repo.obter_todos()
    
    # Converter objetos Administrador para dicionários
    administradores = [
        {
            "id_usuario": a.id_usuario,
            "matricula": a.matricula,
            "nome": a.nome,
            "email": a.email,
            "perfil": a.perfil,
            "tipo_admin": a.tipo_admin,
            "data_cadastro": str(a.data_cadastro) if a.data_cadastro else None
        }
        for a in administradores_obj
    ]
    
    context = {
        "request": request, 
        "admin": admin,
        "administradores": administradores
    }
    
    # Adicionar mensagens se existirem
    if sucesso:
        context["sucesso"] = sucesso
    if erro:
        context["erro"] = erro
    
    response = templates.TemplateResponse("/admin/usuario_admin.html", context)
    return response

@router.post("/usuarios/admin/excluir/{id_usuario}")
@requer_autenticacao("admin")
async def post_excluir_administrador(
    request: Request,
    id_usuario: int,
    usuario_logado: dict = None
):
    try:
        # Verificar se o administrador existe
        administrador = administrador_repo.obter_por_id(id_usuario)
        
        if not administrador:
            return RedirectResponse(
                url="/admin/usuarios/admin?erro=Administrador não encontrado",
                status_code=303
            )
        
        # Verificar se não está tentando excluir a si mesmo
        usuario_atual = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
        if usuario_atual.id_usuario == id_usuario:
            return RedirectResponse(
                url="/admin/usuarios/admin?erro=Você não pode excluir sua própria conta",
                status_code=303
            )
        
        # Excluir do banco de dados
        sucesso = administrador_repo.excluir(id_usuario)
        
        if sucesso:
            return RedirectResponse(
                url="/admin/usuarios/admin?sucesso=Administrador excluído com sucesso!",
                status_code=303
            )
        else:
            return RedirectResponse(
                url="/admin/usuarios/admin?erro=Erro ao excluir administrador",
                status_code=303
            )
            
    except Exception as e:
        print(f"Erro ao excluir administrador: {e}")
        return RedirectResponse(
            url="/admin/usuarios/admin?erro=Erro interno ao excluir administrador",
            status_code=303
        )

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

@router.get("/usuarios/assistente/editar/{id_usuario}")
@requer_autenticacao("admin")
async def get_editar_assistente(request: Request, id_usuario: int, usuario_logado: dict = None):
    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    assistente = assistente_social_repo.obter_por_id(id_usuario)
    
    if not assistente:
        return RedirectResponse(url="/admin/usuarios/assistente?erro=Assistente não encontrado", status_code=303)
    
    return templates.TemplateResponse(
        "/admin/editar_assist.html",
        {"request": request, "admin": admin, "assistente": assistente}
    )

@router.post("/usuarios/assistente/editar/{id_usuario}")
@requer_autenticacao("admin")
async def post_editar_assistente(
    request: Request,
    id_usuario: int,
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    siape: str = Form(...),
    senha: str = Form(None),
    usuario_logado: dict = None
):
    try:
        admin_logado = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
        assistente_atual = assistente_social_repo.obter_por_id(id_usuario)
        
        if not assistente_atual:
            return RedirectResponse(url="/admin/usuarios/assistente?erro=Assistente não encontrado", status_code=303)
        
        # Validar com DTO (sem senha se não foi fornecida)
        try:
            # Se senha não foi fornecida, usar a atual
            senha_validar = senha if senha else "senha123"  # senha temporária só para validação
            
            dados_dto = CadastroAssistDTO(
                nome=nome,
                matricula=matricula,
                email=email,
                senha=senha_validar,
                siape=siape
            )
        except ValidationError as e:
            erro_info = e.errors()[0]
            erro_msg = erro_info['msg']
            if erro_msg.startswith('Value error, '):
                erro_msg = erro_msg.replace('Value error, ', '', 1)
            campo_erro = erro_info['loc'][0] if erro_info.get('loc') else ''
            
            return templates.TemplateResponse(
                "admin/editar_assist.html",
                {"request": request, "admin": admin_logado, "assistente": assistente_atual, "erro": erro_msg, "campo_erro": campo_erro}
            )
        
        # Atualizar senha apenas se foi fornecida
        if senha:
            try:
                senha_hash = criar_hash_senha(senha)
                assistente_atual.senha = senha_hash
            except Exception as e:
                print(f"Erro ao criar hash da senha: {e}")
                return templates.TemplateResponse(
                    "admin/editar_assist.html",
                    {"request": request, "admin": admin_logado, "assistente": assistente_atual, "erro": "Erro ao processar senha"}
                )
        
        # Atualizar dados
        assistente_atual.nome = nome.strip()
        assistente_atual.matricula = matricula.strip()
        assistente_atual.email = email.strip().lower()
        assistente_atual.siape = siape.strip()
        
        # Garantir que campos obrigatórios estejam presentes
        if not assistente_atual.foto:
            assistente_atual.foto = None
        if not assistente_atual.token_redefinicao:
            assistente_atual.token_redefinicao = None
        if not assistente_atual.data_token:
            assistente_atual.data_token = None
        if not assistente_atual.data_cadastro:
            assistente_atual.data_cadastro = None
        
        # Atualizar no banco
        try:
            sucesso = assistente_social_repo.atualizar(assistente_atual)
            if not sucesso:
                return templates.TemplateResponse(
                    "admin/editar_assist.html",
                    {"request": request, "admin": admin_logado, "assistente": assistente_atual, "erro": "Erro ao atualizar cadastro"}
                )
        except Exception as e:
            print(f"Erro ao atualizar assistente: {e}")
            return templates.TemplateResponse(
                "admin/editar_assist.html",
                {"request": request, "admin": admin_logado, "assistente": assistente_atual, "erro": "Erro interno do sistema"}
            )
        
        return RedirectResponse(url="/admin/usuarios/assistente?sucesso=Assistente atualizado com sucesso!", status_code=303)
        
    except Exception as e:
        print(f"Erro geral ao editar assistente: {e}")
        return RedirectResponse(url="/admin/usuarios/assistente?erro=Erro ao editar assistente", status_code=303)

@router.post("/usuarios/assistente/excluir/{id_usuario}")
@requer_autenticacao("admin")
async def post_excluir_assistente(
    request: Request,
    id_usuario: int,
    usuario_logado: dict = None
):
    try:
        # Verificar se o assistente existe
        assistente = assistente_social_repo.obter_por_id(id_usuario)
        
        if not assistente:
            return RedirectResponse(
                url="/admin/usuarios/assistente?erro=Assistente não encontrado",
                status_code=303
            )
        
        # Excluir do banco de dados
        sucesso = assistente_social_repo.excluir(id_usuario)
        
        if sucesso:
            return RedirectResponse(
                url="/admin/usuarios/assistente?sucesso=Assistente excluído com sucesso!",
                status_code=303
            )
        else:
            return RedirectResponse(
                url="/admin/usuarios/assistente?erro=Erro ao excluir assistente",
                status_code=303
            )
            
    except Exception as e:
        print(f"Erro ao excluir assistente: {e}")
        return RedirectResponse(
            url="/admin/usuarios/assistente?erro=Erro interno ao excluir assistente",
            status_code=303
        )

       