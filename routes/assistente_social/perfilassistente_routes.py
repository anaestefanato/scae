from fastapi import APIRouter, Request, Formfrom fastapi import APIRouter, Request

from fastapi.responses import RedirectResponsefrom fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templatesfrom fastapi.templating import Jinja2Templates



from repo import usuario_repofrom repo import usuario_repo

from repo.inscricao_repo import obter_estatisticas_dashboard, obter_inscricoes_recentes_dashboardfrom repo.inscricao_repo import obter_estatisticas_dashboard, obter_inscricoes_recentes_dashboard

from util.auth_decorator import obter_usuario_logado, requer_autenticacaofrom util.auth_decorator import obter_usuario_logado, requer_autenticacao

from util.security import criptografar_senha, verificar_senha



router = APIRouter()

router = APIRouter()templates = Jinja2Templates(directory="templates")

templates = Jinja2Templates(directory="templates")



@router.get("/inicio")

@router.get("/inicio")@requer_autenticacao("assistente")

@requer_autenticacao("assistente")async def get_perfil(request: Request, usuario_logado: dict = None):

async def get_inicio(request: Request, usuario_logado: dict = None):    

        assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])

    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])    

        # Buscar estatísticas do dashboard

    # Buscar estatísticas do dashboard    estatisticas = obter_estatisticas_dashboard()

    estatisticas = obter_estatisticas_dashboard()    if not estatisticas:

    if not estatisticas:        estatisticas = {

        estatisticas = {            'editais_ativos': 0,

            'editais_ativos': 0,            'inscricoes_pendentes': 0,

            'inscricoes_pendentes': 0,            'alunos_beneficiados': 0,

            'alunos_beneficiados': 0,            'valor_total_mensal': 0.0

            'valor_total_mensal': 0.0        }

        }    

        # Buscar inscrições recentes com prioridade

    # Buscar inscrições recentes com prioridade    inscricoes_recentes = obter_inscricoes_recentes_dashboard()

    inscricoes_recentes = obter_inscricoes_recentes_dashboard()    

        context = {

    context = {        "request": request, 

        "request": request,         "assistente": assistente,

        "assistente": assistente,        "estatisticas": estatisticas,

        "estatisticas": estatisticas,        "inscricoes_recentes": inscricoes_recentes

        "inscricoes_recentes": inscricoes_recentes    }

    }    

        response = templates.TemplateResponse("/assistente/dashboard_assistente.html", context)

    response = templates.TemplateResponse("/assistente/dashboard_assistente.html", context)    return response

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
    nova_senha_criptografada = criptografar_senha(new_password)
    sucesso = usuario_repo.atualizar_senha(assistente.id_usuario, nova_senha_criptografada)
    
    if sucesso:
        return RedirectResponse(url="/assistente/perfil?sucesso=senha_alterada", status_code=302)
    else:
        return RedirectResponse(url="/assistente/perfil?erro=erro_servidor", status_code=302)