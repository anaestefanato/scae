from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo, aluno_repo
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
    
    context = {
        "request": request, 
        "admin": admin,
        "possiveis_alunos": possiveis_alunos,
        "total_cadastros_pendentes": len(possiveis_alunos_raw)
    }
    
    response = templates.TemplateResponse("/admin/dashboard_admin.html", context)
    return response

