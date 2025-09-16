from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.aluno_model import Aluno
from repo import usuario_repo
from repo import aluno_repo
from repo.aluno_repo import marcar_cadastro_completo, atualizar
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dadoscadastrais")
@requer_autenticacao(["aluno"])
async def get_dados_cadastrais(request: Request, usuario_logado: dict = None, sucesso: str = None):
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    context = {"request": request, "aluno": aluno}
    if sucesso:
        context["sucesso"] = "Informações salvas com sucesso!"
    
    response = templates.TemplateResponse("/aluno/dadoscadastrais.html", context)
    return response

@router.post("/dadoscadastrais")
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
            return RedirectResponse("/aluno/inicio?sucesso=1", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "aluno/dadoscadastrais.html",
        {"request": request, "aluno": usuario, "erro": "Erro ao completar cadastro."}
    )

