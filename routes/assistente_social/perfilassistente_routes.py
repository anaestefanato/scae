from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repo import usuario_repo
from repo.inscricao_repo import obter_estatisticas_dashboard, obter_inscricoes_recentes_dashboard
from repo.recurso_repo import contar_pendentes
from util.auth_decorator import obter_usuario_logado, requer_autenticacao
from util.security import criar_hash_senha, verificar_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/inicio")
@requer_autenticacao("assistente")
async def get_inicio(request: Request, usuario_logado: dict = None):
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Buscar estatísticas do dashboard
    try:
        estatisticas = obter_estatisticas_dashboard()
        if not estatisticas:
            estatisticas = {
                'editais_ativos': 0,
                'inscricoes_pendentes': 0,
                'alunos_beneficiados': 0,
                'valor_total_mensal': 0.0
            }
    except Exception as e:
        print(f"Erro ao buscar estatísticas: {e}")
        estatisticas = {
            'editais_ativos': 0,
            'inscricoes_pendentes': 0,
            'alunos_beneficiados': 0,
            'valor_total_mensal': 0.0
        }

    # Buscar quantidade de recursos pendentes
    try:
        recursos_pendentes = contar_pendentes()
    except Exception as e:
        print(f"Erro ao contar recursos pendentes: {e}")
        recursos_pendentes = 0

    # Buscar inscrições para análise (primeiros 5)
    try:
        from repo.inscricao_repo import obter_inscricoes_para_analise
        inscricoes_analise, _ = obter_inscricoes_para_analise(pagina=1, limite=5)
    except Exception as e:
        print(f"Erro ao buscar inscrições para análise: {e}")
        inscricoes_analise = []

    context = {
        "request": request,
        "assistente": assistente,
        "estatisticas": estatisticas,
        "recursos_pendentes": recursos_pendentes,
        "inscricoes_analise": inscricoes_analise
    }

    response = templates.TemplateResponse("/assistente/dashboard_assistente.html", context)
    return response



@router.get("/perfil")
@requer_autenticacao("assistente")
async def get_perfil_assistente(request: Request, usuario_logado: dict = None):
    
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    context = {
        "request": request, 
        "assistente": assistente
    }
    
    response = templates.TemplateResponse("/assistente/perfil_assist.html", context)
    return response


@router.post("/alterar-senha")
@requer_autenticacao("assistente")
async def alterar_senha_assistente(request: Request, 
                                  current_password: str = Form(...),
                                  new_password: str = Form(...),
                                  confirm_password: str = Form(...),
                                  usuario_logado: dict = None):
    
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Verificar se a senha atual está correta
    if not verificar_senha(current_password, assistente.senha):
        # Em uma implementação real, você retornaria uma mensagem de erro
        return RedirectResponse(url="/assistente/perfil?erro=senha_incorreta", status_code=302)
    
    # Verificar se as novas senhas coincidem
    if new_password != confirm_password:
        return RedirectResponse(url="/assistente/perfil?erro=senhas_diferentes", status_code=302)
    
    # Verificar tamanho mínimo da senha
    if len(new_password) < 6:
        return RedirectResponse(url="/assistente/perfil?erro=senha_pequena", status_code=302)
    
    # Atualizar a senha
    nova_senha_criptografada = criar_hash_senha(new_password)
    sucesso = usuario_repo.atualizar_senha(assistente.id_usuario, nova_senha_criptografada)
    
    if sucesso:
        return RedirectResponse(url="/assistente/perfil?sucesso=senha_alterada", status_code=302)
    else:
        return RedirectResponse(url="/assistente/perfil?erro=erro_servidor", status_code=302)