import os
from fastapi import APIRouter, Form, Request, UploadFile, File, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.aluno_model import Aluno
from repo import usuario_repo
from repo import aluno_repo
from repo.aluno_repo import marcar_cadastro_completo, atualizar
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/perfil")
@requer_autenticacao(["aluno"])
async def get_dados_cadastrais(request: Request, usuario_logado: dict = None, sucesso: str = None):
    # Busca dados completos do aluno
    aluno = aluno_repo.obter_por_matricula(usuario_logado['matricula'])
    
    # Se não encontrar dados completos, busca dados básicos do usuário
    if not aluno:
        usuario = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
        aluno = usuario
    
    context = {"request": request, "aluno": aluno}
    if sucesso:
        context["mensagem_sucesso"] = "Informações salvas com sucesso!"
    
    response = templates.TemplateResponse("/aluno/perfil.html", context)
    return response

@router.post("/perfil")
@requer_autenticacao()
async def post_perfil(
    request: Request,
    usuario_logado: dict = None,
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    telefone: str = Form(...),
    curso: str = Form(...),
    data_nascimento: str = Form(...),
    filiacao: str = Form(...),
    cep: str = Form(...),
    cidade: str = Form(...),
    bairro: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    nome_banco: str = Form(...),
    agencia_bancaria: str = Form(...),
    numero_conta_bancaria: str = Form(...),
    renda_familiar: str = Form(...),
    quantidade_pessoas: str = Form(...),
    renda_per_capita: str = Form(...),
    situacao_moradia: str = Form(...)
):
    usuario = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    
    if not aluno_repo.possui_cadastro_completo(usuario.id_usuario):
        aluno = Aluno(
            id_usuario=usuario.id_usuario,
            nome=usuario.nome,
            matricula=usuario.matricula,
            email=usuario.email,
            senha=usuario.senha,
            perfil=usuario.perfil,
            foto=getattr(usuario, 'foto', None),
            token_redefinicao=getattr(usuario, 'token_redefinicao', None),
            data_token=getattr(usuario, 'data_token', None),
            data_cadastro=getattr(usuario, 'data_cadastro', None),
            cpf=cpf,
            telefone=telefone,
            curso=curso,
            data_nascimento=data_nascimento,
            filiacao=filiacao,
            cep=cep,
            cidade=cidade,
            bairro=bairro,
            rua=rua,
            numero=numero,
            nome_banco=nome_banco,
            agencia_bancaria=agencia_bancaria,
            numero_conta_bancaria=numero_conta_bancaria,
            renda_familiar=float(renda_familiar),
            quantidade_pessoas=int(quantidade_pessoas),
            renda_per_capita=float(renda_per_capita),
            situacao_moradia=situacao_moradia
        )
        sucesso = aluno_repo.completar_cadastro(aluno)

        if sucesso:
            aluno_repo.marcar_cadastro_completo(usuario.id_usuario)
            # Atualiza a sessão para refletir cadastro completo
            if hasattr(request, 'session'):
                request.session['usuario']['completo'] = True
            return RedirectResponse("/aluno/inicio?sucesso=1", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "aluno/perfil.html",
        {"request": request, "aluno": usuario, "erro": "Erro ao completar cadastro."}
    )
    
    # # Atualizar dados do usuário
    # usuario.nome = nome
    # usuario.email = email
    # usuario_repo.alterar(usuario)

    # # Se for aluno, atualizar dados adicionais
    # if usuario.perfil == 'aluno' and cpf  and telefone and curso and data_nascimento and filiacao and cep and cidade and bairro and rua and numero and nome_banco and agencia_bancaria and numero_conta_bancaria and renda_familiar and quantidade_pessoas:
    #     try:
    #         from util.db_util import get_connection
    #         with get_connection() as conn:
    #             cursor = conn.cursor()
    #             cursor.execute(
    #                 ATUALIZAR,
    #                 (cpf, rg, telefone, data_nascimento, filiacao, cep, cidade, bairro, rua, numero, nome_banco, agencia_bancaria, numero_conta_bancaria, renda_familiar, quantidade_pessoas, usuario.matricula)
    #             )
    #             conn.commit()
    #     except:
    #         pass
    
    # # Atualizar sessão
    # from util.auth_decorator import criar_sessao
    # usuario_dict = {
    #     "id": usuario.id,
    #     "nome": nome,
    #     "email": email,
    #     "perfil": usuario.perfil,
    #     "foto": usuario.foto
    # }
    # criar_sessao(request, usuario_dict)
    
    # return RedirectResponse("/perfil?sucesso=1", status.HTTP_303_SEE_OTHER)

@router.post("/perfil/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),  # ← Recebe arquivo de foto
    usuario_logado: dict = None
):
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

    # 2. Criar diretório se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)

    # 3. Gerar nome único para evitar conflitos
    import secrets
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # 4. Salvar arquivo no sistema
    try:
        conteudo = await foto.read()  # ← Lê conteúdo do arquivo
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # 5. Salvar caminho no banco de dados
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        usuario_repo.atualizar_foto(usuario_logado['id'], caminho_relativo)

        # 6. Atualizar sessão do usuário
        usuario_logado['foto'] = caminho_relativo
        from util.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)

    except Exception as e:
        return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)