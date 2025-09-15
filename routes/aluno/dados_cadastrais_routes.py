from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from repo.aluno_repo import marcar_cadastro_completo, atualizar
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dadoscadastrais")
@requer_autenticacao(["aluno"])
async def get_dados_cadastrais(request: Request, usuario_logado: dict = None):
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])                 
    response = templates.TemplateResponse("/aluno/dadoscadastrais.html", {"request": request, "aluno": aluno})
    return response

@router.post("/aluno/dadoscadastrais")
@requer_autenticacao(["aluno"])
async def post_dados_cadastrais(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    curso: str = Form(...),
    cep: str = Form(...),
    cidade: str = Form(...),
    bairro: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    nome_banco: str = Form(...),
    agencia_bancaria: str = Form(...),
    numero_conta_bancaria: str = Form(...),
    renda_familiar: str = Form(...),
    qtd_membros_familia: int = Form(...),
    renda_per_capita: str = Form(None),
    situacao_moradia: str = Form(...)
):
    usuario = obter_usuario_logado(request)
    id_aluno = usuario["id"]
    dados = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "email": email,
        "telefone": telefone,
        "curso": curso,
        "cep": cep,
        "cidade": cidade,
        "bairro": bairro,
        "rua": rua,
        "numero": numero,
        "nome_banco": nome_banco,
        "agencia_bancaria": agencia_bancaria,
        "numero_conta_bancaria": numero_conta_bancaria,
        "renda_familiar": renda_familiar,
        "qtd_membros_familia": qtd_membros_familia,
        "renda_per_capita": renda_per_capita,
        "situacao_moradia": situacao_moradia
    }
    atualizar(id_aluno, dados)
    marcar_cadastro_completo(id_aluno)
    return RedirectResponse("/aluno/dadoscadastrais", status.HTTP_303_SEE_OTHER)