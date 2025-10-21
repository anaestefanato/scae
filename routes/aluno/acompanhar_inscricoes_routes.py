from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from repo import usuario_repo, inscricao_repo, auxilio_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Adicionar filtro personalizado para formatar datas
def formatar_data(data_str):
    """Formata string de data para padrão DD/MM/YYYY"""
    if not data_str:
        return 'N/A'
    
    try:
        # Tenta formatos comuns
        for formato in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']:
            try:
                data_obj = datetime.strptime(str(data_str), formato)
                return data_obj.strftime('%d/%m/%Y')
            except ValueError:
                continue
        # Se nenhum formato funcionar, retorna a string original
        return str(data_str)
    except:
        return str(data_str)

templates.env.filters['formatar_data'] = formatar_data


@router.get("/acompanhar-inscricoes")
@requer_autenticacao(["aluno"])
async def get_acompanhar_inscricoes(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar todas as inscrições do aluno
    inscricoes = inscricao_repo.obter_por_aluno(usuario_logado['id'])
    
    # Buscar os auxílios de cada inscrição
    auxilios_por_aluno = auxilio_repo.obter_por_aluno(usuario_logado['id'])
    
    # Agrupar auxílios por inscrição, começando com todas as inscrições
    inscricoes_com_auxilios = {}
    for inscricao in inscricoes:
        id_inscricao = inscricao['id_inscricao']
        inscricoes_com_auxilios[id_inscricao] = {
            'edital_titulo': inscricao.get('edital_titulo', 'Edital sem título'),
            'status': inscricao['status'],
            'data_inscricao': inscricao['data_inscricao'],
            'auxilios': []
        }
    
    # Adicionar auxílios às inscrições correspondentes
    for auxilio in auxilios_por_aluno:
        id_inscricao = auxilio['id_inscricao']
        if id_inscricao in inscricoes_com_auxilios:
            inscricoes_com_auxilios[id_inscricao]['auxilios'].append(auxilio)
    
    response = templates.TemplateResponse("/aluno/acompanhar_inscricoes.html", {
        "request": request, 
        "aluno": aluno,
        "inscricoes": inscricoes,
        "inscricoes_com_auxilios": inscricoes_com_auxilios
    })
    return response

@router.get("/acompanhar-inscricoes/recurso")
@requer_autenticacao(["aluno"])
async def get_acompanhar_inscricoes_recurso(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)
    
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/solicitar_recurso.html", {"request": request, "aluno": aluno})
    return response


