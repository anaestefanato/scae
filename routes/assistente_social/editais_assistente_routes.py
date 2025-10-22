from fastapi import APIRouter, Request, Form, UploadFile, File, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pydantic import ValidationError
import os

from repo import usuario_repo, edital_repo
from model.edital_model import Edital
from dtos.edital_dto import EditalDTO
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/editais")
@requer_autenticacao("assistente")
async def get_editais_assistente(request: Request, usuario_logado: dict = None):
    """
    Página de gerenciamento de editais para assistentes sociais.
    Permite visualizar, publicar e gerenciar editais, cronogramas, anexos e resultados.
    """
    assistente = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    editais = edital_repo.obter_todos()
    
    context = {
        "request": request,
        "assistente": assistente,
        "editais": editais
    }
    
    response = templates.TemplateResponse("/assistente/editais_assist.html", context)
    return response


@router.post("/editais/publicar")
@requer_autenticacao("assistente")
async def publicar_edital(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    data_publicacao: str = Form(...),
    data_inicio_inscricao: str = Form(...),
    data_fim_inscricao: str = Form(...),
    data_inicio_vigencia: str = Form(...),
    data_fim_vigencia: str = Form(...),
    arquivo: UploadFile = File(...),
    usuario_logado: dict = None
):
    """
    Processa o formulário de publicação de edital.
    Salva o arquivo PDF e registra o edital no banco de dados.
    Segue o padrão da primeira inscrição do aluno.
    """
    try:
        # 1. Validar dados do formulário usando o DTO (seguindo padrão da primeira inscrição)
        try:
            # Edital sempre será publicado como ativo
            dados_validados = EditalDTO(
                titulo=titulo,
                descricao=descricao,
                data_publicacao=data_publicacao,
                data_inicio_inscricao=data_inicio_inscricao,
                data_fim_inscricao=data_fim_inscricao,
                data_inicio_vigencia=data_inicio_vigencia,
                data_fim_vigencia=data_fim_vigencia,
                status="ativo"
            )
        except ValidationError as e:
            # Pegar primeira mensagem de erro e limpar o prefixo "Value error,"
            erro_msg = e.errors()[0]['msg']
            if erro_msg.startswith('Value error, '):
                erro_msg = erro_msg.replace('Value error, ', '')
            from urllib.parse import quote
            return RedirectResponse(
                f"/assistente/editais?erro={quote(erro_msg)}&modal=abrir&titulo={quote(titulo)}&descricao={quote(descricao)}&data_publicacao={data_publicacao}&data_inicio_inscricao={data_inicio_inscricao}&data_fim_inscricao={data_fim_inscricao}&data_inicio_vigencia={data_inicio_vigencia}&data_fim_vigencia={data_fim_vigencia}",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        # 2. Validar arquivo
        if not arquivo or not arquivo.filename:
            from urllib.parse import quote
            return RedirectResponse(
                f"/assistente/editais?erro=Nenhum arquivo foi enviado&modal=abrir&titulo={quote(titulo)}&descricao={quote(descricao)}&data_publicacao={data_publicacao}&data_inicio_inscricao={data_inicio_inscricao}&data_fim_inscricao={data_fim_inscricao}&data_inicio_vigencia={data_inicio_vigencia}&data_fim_vigencia={data_fim_vigencia}",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        # 3. Validar tipo de arquivo
        tipos_permitidos = ["application/pdf"]
        if arquivo.content_type not in tipos_permitidos:
            from urllib.parse import quote
            return RedirectResponse(
                f"/assistente/editais?erro=Apenas arquivos PDF são permitidos&modal=abrir&titulo={quote(titulo)}&descricao={quote(descricao)}&data_publicacao={data_publicacao}&data_inicio_inscricao={data_inicio_inscricao}&data_fim_inscricao={data_fim_inscricao}&data_inicio_vigencia={data_inicio_vigencia}&data_fim_vigencia={data_fim_vigencia}",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        # 4. Validar tamanho
        conteudo_arquivo = await arquivo.read()
        tamanho_max = 10 * 1024 * 1024  # 10MB
        if len(conteudo_arquivo) > tamanho_max:
            from urllib.parse import quote
            return RedirectResponse(
                f"/assistente/editais?erro=Arquivo excede o tamanho máximo de 10MB&modal=abrir&titulo={quote(titulo)}&descricao={quote(descricao)}&data_publicacao={data_publicacao}&data_inicio_inscricao={data_inicio_inscricao}&data_fim_inscricao={data_fim_inscricao}&data_inicio_vigencia={data_inicio_vigencia}&data_fim_vigencia={data_fim_vigencia}",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        # 5. Criar diretório para upload (seguindo padrão do sistema)
        ano = datetime.now().year
        upload_dir = os.path.join("static", "uploads", "editais", str(ano))
        os.makedirs(upload_dir, exist_ok=True)
        
        # 6. Gerar nome único para o arquivo (seguindo padrão do sistema)
        import secrets
        extensao = arquivo.filename.split(".")[-1]
        nome_arquivo = f"edital_{secrets.token_hex(8)}.{extensao}"
        caminho_completo = os.path.join(upload_dir, nome_arquivo)
        
        # 7. Salvar arquivo no sistema
        with open(caminho_completo, "wb") as f:
            f.write(conteudo_arquivo)
        
        # 8. Criar objeto Edital usando dados validados do DTO
        novo_edital = Edital(
            id_edital=0,
            titulo=dados_validados.titulo,
            descricao=dados_validados.descricao,
            data_publicacao=dados_validados.data_publicacao,
            arquivo=f"/static/uploads/editais/{ano}/{nome_arquivo}",
            status=dados_validados.status,
            data_inicio_inscricao=dados_validados.data_inicio_inscricao,
            data_fim_inscricao=dados_validados.data_fim_inscricao,
            data_inicio_vigencia=dados_validados.data_inicio_vigencia,
            data_fim_vigencia=dados_validados.data_fim_vigencia
        )
        
        # 9. Inserir no banco de dados
        id_edital = edital_repo.inserir(novo_edital)
        
        if id_edital:
            # Sucesso - redirecionar com mensagem
            return RedirectResponse(
                "/assistente/editais?sucesso=Edital publicado com sucesso",
                status_code=status.HTTP_303_SEE_OTHER
            )
        else:
            # Erro no banco - remover arquivo e redirecionar
            if os.path.exists(caminho_completo):
                os.remove(caminho_completo)
            return RedirectResponse(
                "/assistente/editais?erro=Erro ao salvar edital no banco de dados",
                status_code=status.HTTP_303_SEE_OTHER
            )
    
    except Exception as e:
        import traceback
        print(f"Erro ao publicar edital: {e}")
        print(f"Traceback completo:\n{traceback.format_exc()}")
        return RedirectResponse(
            f"/assistente/editais?erro=Erro ao processar publicação: {str(e)}",
            status_code=status.HTTP_303_SEE_OTHER
        )
