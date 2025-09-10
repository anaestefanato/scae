import os
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import Optional

from model.usuario_model import Usuario
from repo import aluno_repo, usuario_repo
from sql.usuario_sql import obter_por_matricula
from sql.aluno_sql import ATUALIZAR
from util.security import criar_hash_senha, verificar_senha, validar_forca_senha
from util.auth_decorator import requer_autenticacao, obter_usuario_logado
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates/dadoscadastrais")


@router.get("/dadoscadastrais")
@requer_autenticacao()
async def get_perfil(request: Request):
    usuario_logado = obter_usuario_logado(request)
    # Buscar dados completos do usuário
    usuario = usuario_repo.obter_por_matricula(usuario_logado['matricula'])
    if not usuario:
        return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)
    
    # Se for aluno, buscar dados adicionais
    aluno_dados = None
    if usuario.perfil == 'aluno':
        aluno = aluno_repo.obter_por_id(usuario.id)       
    
    return templates.TemplateResponse(
        "dados_cadastrais.html",
        {
            "request": request,
            "usuario": usuario,
            "aluno_dados": aluno_dados
        }
    )


@router.post("/dadoscadastrais")
@requer_autenticacao()
async def post_perfil(
    request: Request,
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(None),
    rg: str = Form(None),
    telefone: str = Form(None),
    curso: str = Form(None),
    data_nascimento: str = Form(None),
    filiacao: str = Form(None),
    cep: str = Form(None),
    cidade: str = Form(None),
    bairro: str = Form(None),
    rua: str = Form(None),
    numero: str = Form(None),
    nome_banco: str = Form(None),
    agencia_bancaria: str = Form(None),
    numero_conta_bancaria: str = Form(None),
    renda_familiar: str = Form(None),
    quantidade_pessoas: str = Form(None)
):
    usuario_logado = obter_usuario_logado(request)
    usuario = usuario_repo.obter_por_matricula(usuario_logado['matricula'])
    
    # Verificar se o email já está em uso por outro usuário
    usuario_existente = usuario_repo.obter_por_matricula(matricula)
    if usuario_existente and usuario_existente.id != usuario.id:
        aluno = None
        if usuario.perfil == 'aluno':
            try:
                from util.db_util import get_connection
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(obter_por_matricula, (usuario.matricula,))
                    row = cursor.fetchone()
                    if row:
                        aluno = {
                            'cpf': row["cpf"],
                            'rg': row["rg"],
                            'telefone': row["telefone"],
                            'curso': row["curso"],
                            'data_nascimento': row["data_nascimento"],
                            'filiacao': row["filiacao"],
                            'cep': row["cep"],
                            'cidade': row["cidade"],
                            'bairro': row["bairro"],
                            'rua': row["rua"],
                            'numero': row["numero"],
                            'nome_banco': row["nome_banco"],
                            'agencia_bancaria': row["agencia_bancaria"],
                            'numero_conta_bancaria': row["numero_conta_bancaria"],
                            'renda_familiar': row["renda_familiar"],
                            'quantidade_pessoas': row["quantidade_pessoas"]
                        }
            except:
                pass
        
        return templates.TemplateResponse(
            "dados_cadastrais.html",
            {
                "request": request,
                "usuario": usuario,
                "aluno_dados": aluno,
                "erro": "Esta matrícula já está em uso"
            }
        )
    
    # Atualizar dados do usuário
    usuario.nome = nome
    usuario.email = email
    usuario_repo.alterar(usuario)

    # Se for aluno, atualizar dados adicionais
    if usuario.perfil == 'aluno' and cpf and rg and telefone and curso and data_nascimento and filiacao and cep and cidade and bairro and rua and numero and nome_banco and agencia_bancaria and numero_conta_bancaria and renda_familiar and quantidade_pessoas:
        try:
            from util.db_util import get_connection
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    ATUALIZAR,
                    (cpf, rg, telefone, data_nascimento, filiacao, cep, cidade, bairro, rua, numero, nome_banco, agencia_bancaria, numero_conta_bancaria, renda_familiar, quantidade_pessoas, usuario.matricula)
                )
                conn.commit()
        except:
            pass
    
    # Atualizar sessão
    from util.auth_decorator import criar_sessao
    usuario_dict = {
        "id": usuario.id,
        "nome": nome,
        "email": email,
        "perfil": usuario.perfil,
        "foto": usuario.foto
    }
    criar_sessao(request, usuario_dict)
    
    return RedirectResponse("/perfil?sucesso=1", status.HTTP_303_SEE_OTHER)

#MEXER daqui pra baixo
@router.get("/perfil/alterar-senha")
@requer_autenticacao()
async def get_alterar_senha(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "alterar_senha.html",
        {"request": request, "usuario_logado": usuario_logado}
    )


@router.post("/perfil/alterar-senha")
@requer_autenticacao()
async def post_alterar_senha(
    request: Request,
    senha_atual: str = Form(...),
    senha_nova: str = Form(...),
    confirmar_senha: str = Form(...)
):
    usuario_logado = obter_usuario_logado(request)
    usuario = usuario_repo.obter_por_id(usuario_logado['id'])
    
    # Verificar senha atual
    if not verificar_senha(senha_atual, usuario.senha):
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": "Senha atual incorreta"
            }
        )
    
    # Verificar se as novas senhas coincidem
    if senha_nova != confirmar_senha:
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": "As novas senhas não coincidem"
            }
        )
    
    # Validar força da nova senha
    senha_valida, msg_erro = validar_forca_senha(senha_nova)
    if not senha_valida:
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": msg_erro
            }
        )
    
    # Atualizar senha
    senha_hash = criar_hash_senha(senha_nova)
    usuario_repo.atualizar_senha(usuario.id, senha_hash)
    
    return templates.TemplateResponse(
        "alterar_senha.html",
        {
            "request": request,
            "sucesso": "Senha alterada com sucesso!"
        }
    )


@router.post("/perfil/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...)
):
    usuario_logado = obter_usuario_logado(request)
    # Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)
    
    # Criar diretório de upload se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Gerar nome único para o arquivo
    import secrets
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)
    
    # Salvar arquivo
    try:
        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)
        
        # Atualizar caminho no banco
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        usuario_repo.atualizar_foto(usuario_logado['id'], caminho_relativo)
        
        # Atualizar sessão
        usuario_logado['foto'] = caminho_relativo
        from util.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)
        
    except Exception as e:
        return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)
    
    return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)