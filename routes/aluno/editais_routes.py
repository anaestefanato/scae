from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List
import os
from datetime import datetime
from pydantic import ValidationError

from repo import usuario_repo, inscricao_repo, aluno_repo
from repo.auxilio_transporte_repo import AuxilioTransporteRepo
from repo.auxilio_moradia_repo import AuxilioMoradiaRepo
from model.inscricao_model import Inscricao
from model.aluno_model import Aluno
from model.auxilio_transporte_model import AuxilioTransporte
from model.auxilio_moradia_model import AuxilioMoradia
from dtos.primeira_inscricao_dto import PrimeiraInscricaoDTO
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/editais")
@requer_autenticacao(["aluno"])
async def get_editais(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/editais.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/detalhes")
@requer_autenticacao(["aluno"])
async def get_editais_detalhes(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/editais_detalhes.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/primeira-inscricao")
@requer_autenticacao(["aluno"])
async def get_editais_primeira_inscricao(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = aluno_repo.obter_por_matricula(usuario_logado['matricula'])
    
    # Buscar inscrição existente (se houver)
    inscricoes = inscricao_repo.obter_por_aluno(aluno.id_usuario)
    inscricao_existente = inscricoes[0] if inscricoes else None
    
    response = templates.TemplateResponse(
        "/aluno/editais_primeira_inscricao.html", 
        {
            "request": request, 
            "aluno": aluno,
            "inscricao": inscricao_existente
        }
    )
    return response


@router.post("/editais/primeira-inscricao")
@requer_autenticacao(["aluno"])
async def post_editais_primeira_inscricao(
    request: Request,
    usuario_logado: dict = None,
    # Dados pessoais
    nome: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    telefone: str = Form(...),
    email: str = Form(...),
    logradouro: str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(""),
    bairro: str = Form(...),
    cidade: str = Form(...),
    estado: str = Form(...),
    cep: str = Form(...),
    # Dados acadêmicos
    curso: str = Form(...),
    matricula: str = Form(...),
    ano_ingresso: int = Form(...),
    ano_conclusao_previsto: int = Form(...),
    # Dados financeiros
    pessoas_residencia: int = Form(...),
    renda_percapita: str = Form(...),
    bolsa_pesquisa: str = Form(...),
    cad_unico: str = Form(...),
    bolsa_familia: str = Form(...),
    # Auxílios selecionados
    auxilios: List[str] = Form([]),
    # Dados de transporte (opcionais)
    tipo_transporte: Optional[str] = Form(None),
    tipo_onibus: Optional[List[str]] = Form([]),
    gasto_passagens_dia: Optional[float] = Form(None),
    gasto_van_mensal: Optional[float] = Form(None),
    # Documentos obrigatórios
    anexo_documentos: UploadFile = File(...),
    anexo_1: UploadFile = File(...),
    anexo_3: UploadFile = File(...),
    # Documentos de transporte (opcionais)
    comprovante_residencia_transporte: Optional[UploadFile] = File(None),
    passe_escolar_frente: Optional[UploadFile] = File(None),
    passe_escolar_verso: Optional[UploadFile] = File(None),
    comprovante_recarga: Optional[UploadFile] = File(None),
    comprovante_passagens: Optional[UploadFile] = File(None),
    contrato_transporte: Optional[UploadFile] = File(None),
    # Documentos de moradia (opcionais)
    comprovante_residencia_anterior: Optional[UploadFile] = File(None),
    comprovante_residencia_atual: Optional[UploadFile] = File(None),
    contrato_aluguel: Optional[UploadFile] = File(None),
    declaracao_proprietario: Optional[UploadFile] = File(None)
):
    try:
        # 1. Validar dados do formulário usando o DTO
        try:
            dados_validados = PrimeiraInscricaoDTO(
                nome=nome,
                cpf=cpf,
                data_nascimento=data_nascimento,
                telefone=telefone,
                email=email,
                logradouro=logradouro,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cep=cep,
                curso=curso,
                matricula=matricula,
                ano_ingresso=ano_ingresso,
                ano_conclusao_previsto=ano_conclusao_previsto,
                pessoas_residencia=pessoas_residencia,
                renda_percapita=float(renda_percapita) if renda_percapita else 0.0,
                bolsa_pesquisa=bolsa_pesquisa,
                cad_unico=cad_unico,
                bolsa_familia=bolsa_familia,
                auxilios=auxilios,
                tipo_transporte=tipo_transporte,
                tipo_onibus=tipo_onibus,
                gasto_passagens_dia=gasto_passagens_dia,
                gasto_van_mensal=gasto_van_mensal
            )
        except ValidationError as e:
            # Extrair primeira mensagem de erro
            primeiro_erro = e.errors()[0]
            mensagem_erro = primeiro_erro['msg']
            campo_erro = primeiro_erro['loc'][0] if primeiro_erro['loc'] else 'campo'
            
            return RedirectResponse(
                f"/aluno/editais/primeira-inscricao?erro=Erro no campo '{campo_erro}': {mensagem_erro}", 
                status_code=303
            )
        
        # 2. Validar documentos obrigatórios - verificar se foram enviados
        if not anexo_documentos or not anexo_documentos.filename:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Documento de Identificação é obrigatório", 
                status_code=303
            )
        
        if not anexo_1 or not anexo_1.filename:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Anexo I (Termo Comprobatório de Declaração de Renda) é obrigatório", 
                status_code=303
            )
        
        if not anexo_3 or not anexo_3.filename:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Anexo III (Termo de Responsabilidade) é obrigatório", 
                status_code=303
            )
        
        # 3. Validar tipos de arquivo e tamanho dos documentos obrigatórios
        tipos_permitidos = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
        tamanho_max = 10 * 1024 * 1024  # 10MB em bytes
        
        # Validar Documento de Identificação
        if anexo_documentos.content_type not in tipos_permitidos:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Documento de Identificação: tipo de arquivo inválido. Use PDF ou imagens (JPG, PNG).", 
                status_code=303
            )
        
        conteudo_doc = await anexo_documentos.read()
        await anexo_documentos.seek(0)  # Reset para ler novamente depois
        if len(conteudo_doc) > tamanho_max:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Documento de Identificação excede o tamanho máximo de 10MB", 
                status_code=303
            )
        
        # Validar Anexo I
        if anexo_1.content_type not in tipos_permitidos:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Anexo I: tipo de arquivo inválido. Use PDF ou imagens (JPG, PNG).", 
                status_code=303
            )
        
        conteudo_anexo1 = await anexo_1.read()
        await anexo_1.seek(0)
        if len(conteudo_anexo1) > tamanho_max:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Anexo I excede o tamanho máximo de 10MB", 
                status_code=303
            )
        
        # Validar Anexo III
        if anexo_3.content_type not in tipos_permitidos:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Anexo III: tipo de arquivo inválido. Use PDF ou imagens (JPG, PNG).", 
                status_code=303
            )
        
        conteudo_anexo3 = await anexo_3.read()
        await anexo_3.seek(0)
        if len(conteudo_anexo3) > tamanho_max:
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Anexo III excede o tamanho máximo de 10MB", 
                status_code=303
            )
        
        # 4. Atualizar dados do aluno com os dados validados
        aluno = aluno_repo.obter_por_matricula(usuario_logado['matricula'])
        
        aluno.nome = dados_validados.nome
        aluno.cpf = dados_validados.cpf
        aluno.data_nascimento = dados_validados.data_nascimento
        aluno.telefone = dados_validados.telefone
        aluno.email = dados_validados.email
        aluno.rua = dados_validados.logradouro
        aluno.numero = dados_validados.numero
        aluno.complemento = dados_validados.complemento
        aluno.bairro = dados_validados.bairro
        aluno.cidade = dados_validados.cidade
        aluno.estado = dados_validados.estado
        aluno.cep = dados_validados.cep
        aluno.curso = dados_validados.curso
        aluno.matricula = dados_validados.matricula
        aluno.quantidade_pessoas = dados_validados.pessoas_residencia
        aluno.ano_ingresso = dados_validados.ano_ingresso
        aluno.ano_conclusao_previsto = dados_validados.ano_conclusao_previsto
        aluno.bolsa_pesquisa = dados_validados.bolsa_pesquisa
        aluno.cad_unico = dados_validados.cad_unico
        aluno.bolsa_familia = dados_validados.bolsa_familia
        aluno.renda_per_capita = dados_validados.renda_percapita
        
        aluno_repo.atualizar(aluno)
        
        # 5. Criar diretório para upload de arquivos
        upload_dir = os.path.join("static", "uploads", "inscricoes", str(aluno.id_usuario))
        os.makedirs(upload_dir, exist_ok=True)
        
        # 6. Função auxiliar para salvar arquivo (seguindo padrão da foto de perfil)
        import secrets
        async def salvar_arquivo(arquivo: UploadFile, prefixo: str) -> str:
            """
            Salva arquivo com nome único e retorna o caminho relativo
            Retorna string vazia se o arquivo não existir
            """
            if not arquivo or not arquivo.filename:
                return ""
            
            # Validar tipo de arquivo
            if arquivo.content_type not in tipos_permitidos:
                return ""
            
            # Gerar nome único para evitar conflitos
            extensao = arquivo.filename.split(".")[-1]
            nome_arquivo = f"{prefixo}_{secrets.token_hex(8)}.{extensao}"
            caminho_completo = os.path.join(upload_dir, nome_arquivo)
            
            # Salvar arquivo no sistema
            conteudo = await arquivo.read()
            with open(caminho_completo, "wb") as f:
                f.write(conteudo)
            
            # Retornar caminho relativo para o banco de dados
            return f"/static/uploads/inscricoes/{aluno.id_usuario}/{nome_arquivo}"
        
        # 7. Salvar documentos obrigatórios
        doc_identificacao_path = await salvar_arquivo(anexo_documentos, "doc_identificacao")
        anexo_1_path = await salvar_arquivo(anexo_1, "anexo_1")
        anexo_3_path = await salvar_arquivo(anexo_3, "anexo_3")
        
        # 8. Criar inscrição
        # TODO: Buscar edital ativo - por enquanto usando id_edital = 1
        nova_inscricao = Inscricao(
            id_inscricao=0,
            id_aluno=aluno.id_usuario,
            id_edital=1,  # Ajustar para buscar edital ativo
            data_inscricao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="em_analise",
            urlDocumentoIdentificacao=doc_identificacao_path,
            urlDeclaracaoRenda=anexo_1_path,
            urlTermoResponsabilidade=anexo_3_path
        )
        id_inscricao = inscricao_repo.inserir(nova_inscricao)
        
        # 9. Processar auxílio de transporte (se selecionado)
        if "transporte" in auxilios:
            # Salvar documentos de transporte usando a função auxiliar
            url_comp_residencia = await salvar_arquivo(comprovante_residencia_transporte, "comp_residencia_transporte")
            url_passe_frente = await salvar_arquivo(passe_escolar_frente, "passe_escolar_frente")
            url_passe_verso = await salvar_arquivo(passe_escolar_verso, "passe_escolar_verso")
            url_comp_recarga = await salvar_arquivo(comprovante_recarga, "comp_recarga")
            url_comp_passagens = await salvar_arquivo(comprovante_passagens, "comp_passagens")
            url_contrato_transp = await salvar_arquivo(contrato_transporte, "contrato_transporte")
            
            # Processar tipo de ônibus (pode ser múltiplo)
            tipos_onibus_str = ",".join(tipo_onibus) if tipo_onibus else None
            
            # Criar registro de auxílio transporte
            auxilio_transporte = AuxilioTransporte(
                id_auxilio=0,
                id_edital=1,
                id_inscricao=id_inscricao,
                descricao=f"Auxílio Transporte - {tipo_transporte if tipo_transporte else 'Não especificado'}",
                valor_mensal=300.0,  # Valor padrão
                data_inicio=datetime.now().strftime("%Y-%m-%d"),
                data_fim="",
                tipo_auxilio="transporte",
                tipo_transporte=tipo_transporte if tipo_transporte else "",
                tipo_onibus=tipos_onibus_str,
                gasto_passagens_dia=gasto_passagens_dia,
                gasto_van_mensal=gasto_van_mensal,
                urlCompResidencia=url_comp_residencia,
                urlPasseEscolarFrente=url_passe_frente,
                urlPasseEscolarVerso=url_passe_verso,
                urlComprovanteRecarga=url_comp_recarga,
                urlComprovantePassagens=url_comp_passagens,
                urlContratoTransporte=url_contrato_transp
            )
            AuxilioTransporteRepo.inserir(auxilio_transporte)
        
        # 10. Processar auxílio de moradia (se selecionado)
        if "moradia" in auxilios:
            # Salvar documentos de moradia usando a função auxiliar
            comp_res_anterior = await salvar_arquivo(comprovante_residencia_anterior, "comp_res_anterior")
            comp_res_atual = await salvar_arquivo(comprovante_residencia_atual, "comp_res_atual")
            contrato_alug = await salvar_arquivo(contrato_aluguel, "contrato_aluguel")
            decl_prop = await salvar_arquivo(declaracao_proprietario, "declaracao_proprietario")
            
            # Criar registro de auxílio moradia
            auxilio_moradia = AuxilioMoradia(
                id_auxilio=0,
                id_edital=1,
                id_inscricao=id_inscricao,
                descricao="Auxílio Moradia",
                valor_mensal=400.0,  # Valor padrão
                data_inicio=datetime.now().strftime("%Y-%m-%d"),
                data_fim="",
                tipo_auxilio="moradia",
                url_comp_residencia_fixa=comp_res_anterior,
                url_comp_residencia_alugada=comp_res_atual,
                url_contrato_aluguel_cid_campus=contrato_alug,
                url_contrato_aluguel_cid_natal=decl_prop
            )
            AuxilioMoradiaRepo.inserir(auxilio_moradia)
        
        # 11. Redirecionar com mensagem de sucesso
        return RedirectResponse(
            "/aluno/editais?msg=Inscrição enviada com sucesso!", 
            status_code=303
        )
        
    except Exception as e:
        print(f"Erro ao processar inscrição: {e}")
        return RedirectResponse(
            "/aluno/editais/primeira-inscricao?erro=Erro ao processar inscrição. Tente novamente.", 
            status_code=303
        )


@router.get("/editais/renovacao")
@requer_autenticacao(["aluno"])
async def get_editais_renovacao(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/editais_renovacao.html", {"request": request, "aluno": aluno})
    return response
