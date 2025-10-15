from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo, aluno_repo, assistente_social_repo, inscricao_repo, chamado_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao
from util.date_util import calcular_tempo_relativo, formatar_data_brasileira


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/inicio")
@requer_autenticacao("admin")
async def get_perfil(request: Request, usuario_logado: dict = None):

    admin = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar solicitações de cadastro pendentes (limitado a 3 para o dashboard)
    possiveis_alunos_raw = aluno_repo.obter_possiveis_alunos()
    
    # Adicionar formatação de data aos usuários
    possiveis_alunos = []
    for usuario in possiveis_alunos_raw[:3]:  # Mostrar apenas os 3 mais recentes
        usuario_dict = {
            'id_usuario': usuario.id_usuario,
            'nome': usuario.nome,
            'matricula': usuario.matricula,
            'email': usuario.email,
            'data_cadastro': usuario.data_cadastro,
            'tempo_relativo': calcular_tempo_relativo(usuario.data_cadastro) if usuario.data_cadastro else "Data não informada",
            'data_formatada': formatar_data_brasileira(usuario.data_cadastro) if usuario.data_cadastro else "Data não informada"
        }
        possiveis_alunos.append(usuario_dict)
    
    # Estatísticas para os cartões do dashboard
    try:
        total_alunos = aluno_repo.contar_todos()
    except Exception:
        total_alunos = 0

    try:
        # assistente_social_repo não possui contador simples, usar len(obter_todos())
        total_assistentes = len(assistente_social_repo.obter_todos())
    except Exception:
        total_assistentes = 0

    try:
        estatisticas_inscricoes = inscricao_repo.obter_estatisticas_analise()
        # Mostrar o número de possíveis alunos como cadastros pendentes
        total_cadastros_pendentes = len(possiveis_alunos_raw)
    except Exception:
        total_cadastros_pendentes = len(possiveis_alunos_raw)

    try:
        estatisticas_chamados = chamado_repo.obter_estatisticas_gerais()
        total_chamados_pendentes = estatisticas_chamados.get('abertos', 0) if estatisticas_chamados else 0
    except Exception:
        total_chamados_pendentes = 0

    context = {
        "request": request,
        "admin": admin,
        "possiveis_alunos": possiveis_alunos,
        "total_cadastros_pendentes": total_cadastros_pendentes,
        "total_alunos": total_alunos,
        "total_assistentes": total_assistentes,
        "total_chamados_pendentes": total_chamados_pendentes
    }
    
    response = templates.TemplateResponse("/admin/dashboard_admin.html", context)
    return response

