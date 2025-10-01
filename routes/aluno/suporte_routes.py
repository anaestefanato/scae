from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.chamado_model import Chamado
from repo import usuario_repo, chamado_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/suporte")
@requer_autenticacao(["aluno"])
async def get_suporte(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar chamados do usuário
    chamados = chamado_repo.obter_por_usuario(aluno.id_usuario)
    
    # Buscar estatísticas
    estatisticas = chamado_repo.obter_estatisticas_usuario(aluno.id_usuario)
    
    # Se não há chamados, criar dados de exemplo
    if not chamados:
        chamado_repo.inserir_dados_exemplo(aluno.id_usuario)
        chamados = chamado_repo.obter_por_usuario(aluno.id_usuario)
        estatisticas = chamado_repo.obter_estatisticas_usuario(aluno.id_usuario)
    
    # Verificar se há mensagem de sucesso
    sucesso = request.query_params.get("sucesso")
    mensagem_sucesso = "Chamado enviado com sucesso!" if sucesso == "1" else None
    
    response = templates.TemplateResponse("/aluno/suporte.html", {
        "request": request, 
        "aluno": aluno,
        "chamados": chamados,
        "estatisticas": estatisticas,
        "sucesso": mensagem_sucesso
    })
    return response

@router.post("/suporte/novo")
@requer_autenticacao(["aluno"])
async def post_novo_chamado(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    categoria: str = Form(...),
    usuario_logado: dict = None
):
    usuario = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    chamado = Chamado(
        id_chamado=None,   
        id_usuario_criador=usuario.id_usuario,
        id_administrador_responsavel=None,
        titulo=titulo,
        descricao=descricao,
        categoria=categoria,
        data_criacao="",
        data_ultima_atualizacao=None,
        status="aberto")

    id_chamado = chamado_repo.inserir(chamado)
    
    if not id_chamado:
        # Em caso de erro, recarregar a página com os dados necessários
        aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
        chamados = chamado_repo.obter_por_usuario(aluno.id_usuario)
        estatisticas = chamado_repo.obter_estatisticas_usuario(aluno.id_usuario)
        return templates.TemplateResponse(
            "aluno/suporte.html",
            {
                "request": request, 
                "aluno": aluno,
                "chamados": chamados,
                "estatisticas": estatisticas,
                "erro": "Erro ao enviar chamado. Tente novamente."
            }
        )

    # Redirecionar para a página de suporte com mensagem de sucesso
    return RedirectResponse("/aluno/suporte?sucesso=1", status_code=303)