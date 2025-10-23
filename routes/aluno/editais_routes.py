from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List
import os
from datetime import datetime
from pydantic import ValidationError
import traceback

def log_debug(mensagem):
    """Escreve logs de debug em arquivo"""
    with open("debug_auxilios.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {mensagem}\n")

from repo import usuario_repo, inscricao_repo, aluno_repo, auxilio_repo, edital_repo
from repo.auxilio_transporte_repo import AuxilioTransporteRepo
from repo.auxilio_moradia_repo import AuxilioMoradiaRepo
from model.inscricao_model import Inscricao
from model.aluno_model import Aluno
from model.auxilio_model import Auxilio
from model.auxilio_transporte_model import AuxilioTransporte
from model.auxilio_moradia_model import AuxilioMoradia
from dtos.primeira_inscricao_dto import PrimeiraInscricaoDTO
from dtos.renovação_dto import RenovacaoDTO
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/editais")
@requer_autenticacao(["aluno"])
async def get_editais(request: Request, usuario_logado: dict = None):
    if not usuario_logado.get('completo', True):
        return RedirectResponse("/aluno/perfil", status_code=303)

    from repo import edital_repo
    from datetime import date
    
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    
    # Obter todos os editais visíveis (publicados e ativos)
    todos_editais = edital_repo.obter_editais_visiveis_alunos()
    
    # Determinar se cada edital está dentro do período de inscrição
    hoje = date.today()
    editais_com_status = []
    
    for edital in todos_editais:
        edital_dict = {
            'id_edital': edital.id_edital,
            'titulo': edital.titulo,
            'descricao': edital.descricao,
            'data_publicacao': edital.data_publicacao,
            'arquivo': edital.arquivo,
            'status': edital.status,
            'data_inicio_inscricao': edital.data_inicio_inscricao,
            'data_fim_inscricao': edital.data_fim_inscricao,
            'data_inicio_vigencia': edital.data_inicio_vigencia,
            'data_fim_vigencia': edital.data_fim_vigencia,
            'inscricoes_abertas': False,
            'inscricoes_futuras': False,
            'inscricoes_encerradas': False
        }
        
        # Verificar se está no período de inscrição
        if edital.data_inicio_inscricao and edital.data_fim_inscricao:
            try:
                data_inicio = datetime.strptime(edital.data_inicio_inscricao, '%Y-%m-%d').date()
                data_fim = datetime.strptime(edital.data_fim_inscricao, '%Y-%m-%d').date()
                
                if hoje < data_inicio:
                    edital_dict['inscricoes_futuras'] = True
                elif hoje > data_fim:
                    edital_dict['inscricoes_encerradas'] = True
                else:
                    edital_dict['inscricoes_abertas'] = True
            except:
                edital_dict['inscricoes_abertas'] = False
        
        editais_com_status.append(edital_dict)
    
    # Ordenar editais: primeiro os com inscrições abertas, depois futuros, depois encerrados
    def ordenar_editais(edital):
        if edital['inscricoes_abertas']:
            return (0, edital['data_fim_inscricao'])  # Inscrições abertas primeiro, ordenados por data fim
        elif edital['inscricoes_futuras']:
            return (1, edital['data_inicio_inscricao'])  # Inscrições futuras em segundo, ordenados por data início
        else:
            return (2, edital['data_publicacao'])  # Encerradas por último, ordenados por data publicação
    
    editais_com_status.sort(key=ordenar_editais)
    
    response = templates.TemplateResponse(
        "/aluno/editais.html", 
        {
            "request": request, 
            "aluno": aluno, 
            "editais": editais_com_status
        }
    )
    return response

@router.get("/editais/detalhes")
@requer_autenticacao(["aluno"])
async def get_editais_detalhes(request: Request, usuario_logado: dict = None):
    if not usuario_logado.get('completo', True):
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    response = templates.TemplateResponse("/aluno/editais_detalhes.html", {"request": request, "aluno": aluno})
    return response

@router.get("/editais/primeira-inscricao")
@requer_autenticacao(["aluno"])
async def get_editais_primeira_inscricao(request: Request, usuario_logado: dict = None):
    if not usuario_logado.get('completo', True):
        return RedirectResponse("/aluno/perfil", status_code=303)

    aluno = aluno_repo.obter_por_matricula(usuario_logado['matricula'])
    
    # Buscar edital ativo para inscrição
    editais_visiveis = edital_repo.obter_editais_visiveis_alunos()
    edital_ativo = editais_visiveis[0] if editais_visiveis else None
    
    if not edital_ativo:
        return RedirectResponse("/aluno/editais?erro=Não há editais abertos para inscrição no momento.", status_code=303)
    
    # Buscar inscrição existente (se houver)
    inscricoes = inscricao_repo.obter_por_aluno(aluno.id_usuario)
    inscricao_existente = inscricoes[0] if inscricoes else None
    
    # Pegar campo com erro da query string (se houver)
    campo_erro = request.query_params.get('campo_erro', None)
    
    response = templates.TemplateResponse(
        "/aluno/editais_primeira_inscricao.html", 
        {
            "request": request, 
            "aluno": aluno,
            "campo_erro": campo_erro,
            "inscricao": inscricao_existente,
            "edital": edital_ativo
        }
    )
    return response


@router.post("/editais/primeira-inscricao/validar")
@requer_autenticacao(["aluno"])
async def validar_dados_primeira_inscricao(
    request: Request,
    usuario_logado: dict = None,
    # Dados Pessoais
    nome: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    telefone: str = Form(...),
    email: str = Form(...),
    logradouro: str = Form(...),
    numero: str = Form(...),
    complemento: Optional[str] = Form(None),
    bairro: str = Form(...),
    cidade: str = Form(...),
    estado: str = Form(...),
    cep: str = Form(...),
    # Dados Acadêmicos
    curso: str = Form(...),
    matricula: str = Form(...),
    ano_ingresso: int = Form(...),
    ano_conclusao_previsto: int = Form(...),
    # Dados Financeiros
    pessoas_residencia: int = Form(...),
    renda_percapita: str = Form(...),
    bolsa_pesquisa: str = Form(...),
    cad_unico: str = Form(...),
    bolsa_familia: str = Form(...)
):
    """
    Endpoint para validar dados da Etapa 1 usando o DTO Pydantic.
    Retorna JSON com os erros de validação (se houver).
    """
    from fastapi.responses import JSONResponse
    
    try:
        # Tentar criar o DTO apenas com os dados da Etapa 1
        # Os campos de auxílios serão None/vazios pois não são obrigatórios
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
            renda_percapita=renda_percapita,
            bolsa_pesquisa=bolsa_pesquisa,
            cad_unico=cad_unico,
            bolsa_familia=bolsa_familia,
            # Campos opcionais de auxílios (não validados nesta etapa)
            auxilios_selecionados=[],
            tipo_transporte=None,
            tipo_onibus=None,
            gasto_passagens_dia=None,
            gasto_van_mensal=None,
            tipo_moradia=None,
            gasto_aluguel=None
        )
        
        # Se chegou aqui, os dados são válidos
        return JSONResponse(
            content={"valido": True, "mensagem": "Dados válidos!"},
            status_code=200
        )
        
    except ValidationError as e:
        # Extrair erros de validação
        erros = []
        for erro in e.errors():
            campo = erro['loc'][0] if erro['loc'] else 'campo'
            mensagem = erro['msg']
            tipo = erro['type']
            
            # Traduzir nomes de campos para português
            traducao_campos = {
                'nome': 'Nome Completo',
                'cpf': 'CPF',
                'data_nascimento': 'Data de Nascimento',
                'telefone': 'Telefone',
                'email': 'E-mail',
                'logradouro': 'Logradouro',
                'numero': 'Número',
                'bairro': 'Bairro',
                'cidade': 'Cidade',
                'estado': 'Estado',
                'cep': 'CEP',
                'curso': 'Curso',
                'matricula': 'Matrícula',
                'ano_ingresso': 'Ano de Ingresso',
                'ano_conclusao_previsto': 'Ano Previsto para Conclusão',
                'pessoas_residencia': 'Quantas pessoas residem com você',
                'renda_percapita': 'Renda Familiar Per Capita',
                'bolsa_pesquisa': 'Bolsa de Pesquisa/Estágio',
                'cad_unico': 'CAD Único',
                'bolsa_familia': 'Bolsa Família'
            }
            
            campo_traduzido = traducao_campos.get(str(campo), str(campo))
            
            # Personalizar mensagens de erro
            if 'cpf' in str(campo).lower():
                mensagem_amigavel = "CPF inválido. Por favor, verifique se digitou corretamente."
            elif 'email' in str(campo).lower():
                mensagem_amigavel = "E-mail inválido. Por favor, verifique o formato."
            elif 'telefone' in str(campo).lower():
                mensagem_amigavel = "Telefone inválido. Use o formato (00) 00000-0000."
            elif 'cep' in str(campo).lower():
                mensagem_amigavel = "CEP inválido. Use o formato 00000-000."
            else:
                mensagem_amigavel = mensagem
            
            erros.append({
                'campo': str(campo),
                'campo_traduzido': campo_traduzido,
                'mensagem': mensagem_amigavel,
                'tipo': tipo
            })
        
        return JSONResponse(
            content={
                "valido": False, 
                "erros": erros,
                "mensagem": f"Foram encontrados {len(erros)} erro(s) de validação."
            },
            status_code=400
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "valido": False,
                "mensagem": f"Erro ao validar dados: {str(e)}"
            },
            status_code=500
        )


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
    # Dados de transporte (opcionais) - receber como string para tratar valores vazios
    tipo_transporte: Optional[str] = Form(None),
    tipo_onibus: Optional[List[str]] = Form([]),
    gasto_passagens_dia: Optional[str] = Form(None),
    gasto_van_mensal: Optional[str] = Form(None),
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
        # 1. Mapear renda_percapita de categoria para valor numérico
        mapa_renda = {
            "menor_1": 1412.0,      # 1 salário mínimo
            "ate_1_5": 2118.0,      # 1,5 salário mínimo
            "maior_1_5": 2500.0     # Valor representativo acima de 1,5
        }
        renda_valor = mapa_renda.get(renda_percapita, 0.0)
        
        # Tratar campos float opcionais (converter string vazia ou inválida em None)
        def converter_para_float(valor_str):
            if valor_str in [None, "", "0", 0]:
                return None
            try:
                valor_float = float(valor_str)
                return valor_float if valor_float > 0 else None
            except (ValueError, TypeError):
                return None
        
        gasto_passagens_dia_tratado = converter_para_float(gasto_passagens_dia)
        gasto_van_mensal_tratado = converter_para_float(gasto_van_mensal)
        
        # 2. Validar dados do formulário usando o DTO
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
                renda_percapita=renda_valor,
                bolsa_pesquisa=bolsa_pesquisa,
                cad_unico=cad_unico,
                bolsa_familia=bolsa_familia,
                auxilios=auxilios,
                tipo_transporte=tipo_transporte,
                tipo_onibus=tipo_onibus,
                gasto_passagens_dia=gasto_passagens_dia_tratado,
                gasto_van_mensal=gasto_van_mensal_tratado
            )
        except ValidationError as e:
            # Extrair primeira mensagem de erro com detalhes
            primeiro_erro = e.errors()[0]
            mensagem_erro = primeiro_erro['msg']
            campo_erro = primeiro_erro['loc'][0] if primeiro_erro['loc'] else 'campo'
            
            # Traduzir nomes de campos para português
            traducao_campos = {
                'nome': 'Nome Completo',
                'cpf': 'CPF',
                'data_nascimento': 'Data de Nascimento',
                'telefone': 'Telefone',
                'email': 'E-mail',
                'logradouro': 'Logradouro',
                'numero': 'Número',
                'bairro': 'Bairro',
                'cidade': 'Cidade',
                'estado': 'Estado',
                'cep': 'CEP',
                'curso': 'Curso',
                'matricula': 'Matrícula',
                'ano_ingresso': 'Ano de Ingresso',
                'ano_conclusao_previsto': 'Ano Previsto para Conclusão',
                'pessoas_residencia': 'Quantas pessoas residem com você',
                'renda_percapita': 'Renda Familiar Per Capita',
                'bolsa_pesquisa': 'Bolsa de Pesquisa/Estágio',
                'cad_unico': 'CAD Único',
                'bolsa_familia': 'Bolsa Família',
                'tipo_transporte': 'Tipo de Transporte',
                'gasto_passagens_dia': 'Gasto com Passagens por Dia',
                'gasto_van_mensal': 'Gasto Mensal com Van'
            }
            
            campo_traduzido = traducao_campos.get(str(campo_erro), str(campo_erro))
            
            # Personalizar mensagem de erro
            if 'cpf' in str(campo_erro).lower():
                mensagem_amigavel = "CPF inválido. Por favor, verifique se digitou corretamente."
            elif 'email' in str(campo_erro).lower():
                mensagem_amigavel = "E-mail inválido. Por favor, verifique o formato."
            elif 'telefone' in str(campo_erro).lower():
                mensagem_amigavel = "Telefone inválido. Use o formato (00) 00000-0000."
            elif 'cep' in str(campo_erro).lower():
                mensagem_amigavel = "CEP inválido. Use o formato 00000-000."
            else:
                mensagem_amigavel = mensagem_erro
            
            return RedirectResponse(
                f"/aluno/editais/primeira-inscricao?erro={campo_traduzido}: {mensagem_amigavel}&campo_erro={campo_erro}", 
                status_code=303
            )
        
        # 3. Validar documentos obrigatórios - verificar se foram enviados
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
        
        # 5. Buscar edital ativo para inscrição
        editais_visiveis = edital_repo.obter_editais_visiveis_alunos()
        edital_ativo = editais_visiveis[0] if editais_visiveis else None
        
        if not edital_ativo:
            return RedirectResponse(
                "/aluno/editais?erro=Não há editais abertos para inscrição no momento.", 
                status_code=303
            )
        
        id_edital_ativo = edital_ativo.id_edital
        
        # 6. Criar diretório para upload de arquivos
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
        nova_inscricao = Inscricao(
            id_inscricao=0,
            id_aluno=aluno.id_usuario,
            id_edital=id_edital_ativo,  # Usando edital ativo encontrado
            data_inscricao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="pendente",
            urlDocumentoIdentificacao=doc_identificacao_path,
            urlDeclaracaoRenda=anexo_1_path,
            urlTermoResponsabilidade=anexo_3_path
        )
        id_inscricao = inscricao_repo.inserir(nova_inscricao)
        print(f"[DEBUG] Inscrição criada com ID: {id_inscricao} para edital {id_edital_ativo}")
        print(f"[DEBUG] Auxílios selecionados: {auxilios}")
        
        # 9. Processar auxílio de transporte (se selecionado)
        if "transporte" in auxilios:
            try:
                print(f"[DEBUG] Processando auxílio transporte para inscrição {id_inscricao}")
                # Salvar documentos de transporte usando a função auxiliar
                url_comp_residencia = await salvar_arquivo(comprovante_residencia_transporte, "comp_residencia_transporte")
                url_passe_frente = await salvar_arquivo(passe_escolar_frente, "passe_escolar_frente")
                url_passe_verso = await salvar_arquivo(passe_escolar_verso, "passe_escolar_verso")
                url_comp_recarga = await salvar_arquivo(comprovante_recarga, "comp_recarga")
                url_comp_passagens = await salvar_arquivo(comprovante_passagens, "comp_passagens")
                url_contrato_transp = await salvar_arquivo(contrato_transporte, "contrato_transporte")
                
                # Processar tipo de ônibus (pode ser múltiplo)
                tipos_onibus_str = ",".join(tipo_onibus) if tipo_onibus else None
                
                print(f"[DEBUG] Criando objeto AuxilioTransporte com tipo_transporte={tipo_transporte}")
                # Criar registro de auxílio transporte
                auxilio_transporte = AuxilioTransporte(
                    id_auxilio=0,
                    id_edital=id_edital_ativo,
                    id_inscricao=id_inscricao,
                    descricao=f"Auxílio Transporte - {tipo_transporte if tipo_transporte else 'Não especificado'}",
                    valor_mensal=300.0,  # Valor padrão
                    data_inicio=datetime.now().strftime("%Y-%m-%d"),
                    data_fim="",
                    tipo_auxilio="auxilio transporte",
                    tipo_transporte=tipo_transporte if tipo_transporte else "nao_informado",
                    tipo_onibus=tipos_onibus_str,
                    gasto_passagens_dia=gasto_passagens_dia_tratado,
                    gasto_van_mensal=gasto_van_mensal_tratado,
                    urlCompResidencia=url_comp_residencia,
                    urlPasseEscolarFrente=url_passe_frente,
                    urlPasseEscolarVerso=url_passe_verso,
                    urlComprovanteRecarga=url_comp_recarga,
                    urlComprovantePassagens=url_comp_passagens,
                    urlContratoTransporte=url_contrato_transp
                )
                print(f"[DEBUG] Inserindo auxílio transporte no banco...")
                log_debug(f"Tentando inserir auxílio transporte para inscrição {id_inscricao}")
                id_aux_transp = AuxilioTransporteRepo.inserir(auxilio_transporte)
                print(f"[DEBUG] Auxílio transporte inserido com ID: {id_aux_transp}")
                log_debug(f"Auxílio transporte inserido com ID: {id_aux_transp}")
            except Exception as e_transp:
                erro_msg = f"Erro ao processar auxílio transporte: {e_transp}"
                print(f"[ERRO] {erro_msg}")
                print(f"[ERRO] Traceback: {traceback.format_exc()}")
                log_debug(erro_msg)
                log_debug(f"Traceback completo:\n{traceback.format_exc()}")
                # Continua mesmo com erro no auxílio transporte
        
        # 10. Processar auxílio de moradia (se selecionado)
        if "moradia" in auxilios:
            try:
                print(f"[DEBUG] Processando auxílio moradia para inscrição {id_inscricao}")
                # Salvar documentos de moradia usando a função auxiliar
                comp_res_anterior = await salvar_arquivo(comprovante_residencia_anterior, "comp_res_anterior") or "nao_enviado"
                comp_res_atual = await salvar_arquivo(comprovante_residencia_atual, "comp_res_atual") or "nao_enviado"
                contrato_alug = await salvar_arquivo(contrato_aluguel, "contrato_aluguel") or "nao_enviado"
                decl_prop = await salvar_arquivo(declaracao_proprietario, "declaracao_proprietario") or "nao_enviado"
                
                # Criar registro de auxílio moradia
                auxilio_moradia = AuxilioMoradia(
                    id_auxilio=0,
                    id_edital=id_edital_ativo,
                    id_inscricao=id_inscricao,
                    descricao="Auxílio Moradia",
                    valor_mensal=400.0,  # Valor padrão
                    data_inicio=datetime.now().strftime("%Y-%m-%d"),
                    data_fim="",
                    tipo_auxilio="auxilio moradia",
                    url_comp_residencia_fixa=comp_res_anterior,
                    url_comp_residencia_alugada=comp_res_atual,
                    url_contrato_aluguel_cid_campus=contrato_alug,
                    url_contrato_aluguel_cid_natal=decl_prop
                )
                print(f"[DEBUG] Inserindo auxílio moradia no banco...")
                id_aux_morad = AuxilioMoradiaRepo.inserir(auxilio_moradia)
                print(f"[DEBUG] Auxílio moradia inserido com ID: {id_aux_morad}")
            except Exception as e_moradia:
                print(f"[ERRO] Erro ao processar auxílio moradia: {e_moradia}")
                print(f"[ERRO] Traceback: {traceback.format_exc()}")
                log_debug(f"Erro auxílio moradia: {e_moradia}")
                log_debug(f"Traceback:\n{traceback.format_exc()}")
                # Continua mesmo com erro no auxílio moradia
        
        # 11. Processar auxílio de alimentação (se selecionado)
        if "alimentacao" in auxilios:
            try:
                print(f"[DEBUG] Processando auxílio alimentação para inscrição {id_inscricao}")
                auxilio_alimentacao = Auxilio(
                    id_auxilio=0,
                    id_edital=id_edital_ativo,
                    id_inscricao=id_inscricao,
                    descricao="Auxílio Alimentação",
                    valor_mensal=600.0,  # Valor padrão
                    data_inicio=datetime.now().strftime("%Y-%m-%d"),
                    data_fim="",
                    tipo_auxilio="auxilio alimentacao"
                )
                print(f"[DEBUG] Inserindo auxílio alimentação no banco...")
                id_aux_alim = auxilio_repo.inserir(auxilio_alimentacao)
                print(f"[DEBUG] Auxílio alimentação inserido com ID: {id_aux_alim}")
            except Exception as e_alim:
                print(f"[ERRO] Erro ao processar auxílio alimentação: {e_alim}")
                print(f"[ERRO] Traceback: {traceback.format_exc()}")
                log_debug(f"Erro auxílio alimentação: {e_alim}")
                log_debug(f"Traceback:\n{traceback.format_exc()}")
                # Continua mesmo com erro no auxílio alimentação
        
        # 12. Processar auxílio material didático (se selecionado)
        if "material" in auxilios:
            try:
                print(f"[DEBUG] Processando auxílio material para inscrição {id_inscricao}")
                auxilio_material = Auxilio(
                    id_auxilio=0,
                    id_edital=id_edital_ativo,
                    id_inscricao=id_inscricao,
                    descricao="Auxílio Material Didático",
                    valor_mensal=200.0,  # Valor padrão (por semestre, mas representado mensalmente)
                    data_inicio=datetime.now().strftime("%Y-%m-%d"),
                    data_fim="",
                    tipo_auxilio="auxilio material"
                )
                print(f"[DEBUG] Inserindo auxílio material no banco...")
                id_aux_mat = auxilio_repo.inserir(auxilio_material)
                print(f"[DEBUG] Auxílio material inserido com ID: {id_aux_mat}")
            except Exception as e_mat:
                print(f"[ERRO] Erro ao processar auxílio material: {e_mat}")
                print(f"[ERRO] Traceback: {traceback.format_exc()}")
                log_debug(f"Erro auxílio material: {e_mat}")
                log_debug(f"Traceback:\n{traceback.format_exc()}")
                # Continua mesmo com erro no auxílio material
        
        # 13. Redirecionar com mensagem de sucesso
        return RedirectResponse(
            "/aluno/editais?msg=✓ Primeira inscrição enviada com sucesso! Sua solicitação foi registrada e está em análise. Acompanhe as atualizações no sistema.", 
            status_code=303
        )
        
    except ValidationError as ve:
        # Erro de validação do Pydantic - já tratado acima, mas capturado aqui por segurança
        print(f"Erro de validação: {ve}")
        primeiro_erro = ve.errors()[0]
        mensagem_erro = primeiro_erro.get('msg', 'Dados inválidos')
        return RedirectResponse(
            f"/aluno/editais/primeira-inscricao?erro=Erro de validação: {mensagem_erro}", 
            status_code=303
        )
    except Exception as e:
        # Log detalhado do erro
        print(f"Erro ao processar inscrição: {e}")
        print(f"Traceback completo: {traceback.format_exc()}")
        log_debug(f"ERRO GERAL na submissão: {e}")
        log_debug(f"Traceback:\n{traceback.format_exc()}")
        
        # Verificar se a inscrição foi criada (para evitar duplicação)
        erro_msg = str(e)
        if "UNIQUE constraint failed" in erro_msg or "duplicate" in erro_msg.lower():
            return RedirectResponse(
                "/aluno/editais/primeira-inscricao?erro=Você já possui uma inscrição ativa neste edital.", 
                status_code=303
            )
        
        return RedirectResponse(
            f"/aluno/editais/primeira-inscricao?erro=Erro ao processar inscrição: {str(e)[:100]}. Por favor, tente novamente.", 
            status_code=303
        )


@router.get("/editais/renovacao")
@requer_autenticacao(["aluno"])
async def get_editais_renovacao(request: Request, usuario_logado: dict = None):
    if not usuario_logado.get('completo', True):
        return RedirectResponse("/aluno/perfil", status_code=303)

    # Buscar dados completos do aluno
    aluno = aluno_repo.obter_por_matricula(usuario_logado['matricula'])
    
    # Buscar inscrições anteriores do aluno
    inscricoes = inscricao_repo.obter_por_aluno(aluno.id_usuario)
    inscricao_anterior = inscricoes[0] if inscricoes else None
    
    # Buscar auxílios atuais do aluno (se houver inscrição anterior)
    auxilios_atuais = []
    auxilio_transporte = None
    auxilio_moradia = None
    
    if inscricao_anterior:
        # Buscar todos os auxílios da inscrição anterior
        id_inscricao = inscricao_anterior['id_inscricao']
        
        # Tentar buscar auxílio transporte
        try:
            auxilio_transporte_list = AuxilioTransporteRepo.obter_todos()
            for aux in auxilio_transporte_list:
                if aux.id_inscricao == id_inscricao:
                    auxilio_transporte = aux
                    auxilios_atuais.append('transporte')
                    break
        except:
            pass
        
        # Tentar buscar auxílio moradia
        try:
            auxilio_moradia_list = AuxilioMoradiaRepo.obter_todos()
            for aux in auxilio_moradia_list:
                if aux.id_inscricao == id_inscricao:
                    auxilio_moradia = aux
                    auxilios_atuais.append('moradia')
                    break
        except:
            pass
        
        # Verificar outros auxílios através do tipo
        if inscricao_anterior.get('tipo_auxilio'):
            tipo = inscricao_anterior['tipo_auxilio'].lower()
            if 'alimentacao' in tipo or 'alimentação' in tipo:
                auxilios_atuais.append('alimentacao')
            if 'material' in tipo:
                auxilios_atuais.append('material')
    
    response = templates.TemplateResponse(
        "/aluno/editais_renovacao.html", 
        {
            "request": request, 
            "aluno": aluno,
            "inscricao_anterior": inscricao_anterior,
            "auxilios_atuais": auxilios_atuais,
            "auxilio_transporte": auxilio_transporte,
            "auxilio_moradia": auxilio_moradia,
            "quantidade_pessoas_residencia": aluno.quantidade_pessoas if aluno else 0
        }
    )
    return response


@router.post("/editais/renovacao/validar")
@requer_autenticacao(["aluno"])
async def validar_dados_renovacao(
    request: Request,
    usuario_logado: dict = None,
    # Dados Pessoais
    nome: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    telefone: str = Form(...),
    email: str = Form(...),
    logradouro: str = Form(...),
    numero: str = Form(...),
    complemento: Optional[str] = Form(None),
    bairro: str = Form(...),
    cidade: str = Form(...),
    estado: str = Form(...),
    cep: str = Form(...),
    # Dados Acadêmicos
    curso: str = Form(...),
    matricula: str = Form(...),
    ano_ingresso: int = Form(...),
    ano_conclusao_previsto: int = Form(...),
    # Dados Financeiros
    pessoas_residencia: int = Form(...),
    renda_percapita: str = Form(...),
    bolsa_pesquisa: str = Form(...),
    cad_unico: str = Form(...),
    bolsa_familia: str = Form(...)
):
    """
    Endpoint para validar dados da Etapa 1 de Renovação usando o DTO Pydantic.
    Retorna JSON com os erros de validação (se houver).
    """
    from fastapi.responses import JSONResponse
    
    try:
        # 1. Mapear renda_percapita de categoria para valor numérico
        mapa_renda = {
            "menor_1": 1412.0,      # 1 salário mínimo
            "ate_1_5": 2118.0,      # 1,5 salário mínimo
            "maior_1_5": 2500.0     # Valor representativo acima de 1,5
        }
        renda_valor = mapa_renda.get(renda_percapita, 0.0)
        
        # Tentar criar o DTO apenas com os dados da Etapa 1
        # Os campos de auxílios serão vazios pois não são obrigatórios
        dados_validados = RenovacaoDTO(
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
            renda_percapita=renda_valor,
            bolsa_pesquisa=bolsa_pesquisa,
            cad_unico=cad_unico,
            bolsa_familia=bolsa_familia,
            # Campos opcionais de auxílios (não validados nesta etapa)
            auxilios=[],
            tipo_transporte=None,
            tipo_onibus=None,
            gasto_passagens_dia=None,
            gasto_van_mensal=None
        )
        
        # Se chegou aqui, os dados são válidos
        return JSONResponse(
            content={"valido": True, "mensagem": "Dados válidos!"},
            status_code=200
        )
        
    except ValidationError as e:
        # Extrair erros de validação
        erros = []
        for erro in e.errors():
            campo = erro['loc'][0] if erro['loc'] else 'campo'
            mensagem = erro['msg']
            tipo = erro['type']
            
            # Traduzir nomes de campos para português
            traducao_campos = {
                'nome': 'Nome Completo',
                'cpf': 'CPF',
                'data_nascimento': 'Data de Nascimento',
                'telefone': 'Telefone',
                'email': 'E-mail',
                'logradouro': 'Logradouro',
                'numero': 'Número',
                'bairro': 'Bairro',
                'cidade': 'Cidade',
                'estado': 'Estado',
                'cep': 'CEP',
                'curso': 'Curso',
                'matricula': 'Matrícula',
                'ano_ingresso': 'Ano de Ingresso',
                'ano_conclusao_previsto': 'Ano Previsto para Conclusão',
                'pessoas_residencia': 'Quantas pessoas residem com você',
                'renda_percapita': 'Renda Familiar Per Capita',
                'bolsa_pesquisa': 'Bolsa de Pesquisa/Estágio',
                'cad_unico': 'CAD Único',
                'bolsa_familia': 'Bolsa Família'
            }
            
            campo_traduzido = traducao_campos.get(str(campo), str(campo))
            
            # Personalizar mensagens de erro
            if 'cpf' in str(campo).lower():
                mensagem_amigavel = "CPF inválido. Por favor, verifique se digitou corretamente."
            elif 'email' in str(campo).lower():
                mensagem_amigavel = "E-mail inválido. Por favor, verifique o formato."
            elif 'telefone' in str(campo).lower():
                mensagem_amigavel = "Telefone inválido. Use o formato (00) 00000-0000."
            elif 'cep' in str(campo).lower():
                mensagem_amigavel = "CEP inválido. Use o formato 00000-000."
            else:
                mensagem_amigavel = mensagem
            
            erros.append({
                'campo': str(campo),
                'campo_traduzido': campo_traduzido,
                'mensagem': mensagem_amigavel,
                'tipo': tipo
            })
        
        return JSONResponse(
            content={
                "valido": False, 
                "erros": erros,
                "mensagem": f"Foram encontrados {len(erros)} erro(s) de validação."
            },
            status_code=400
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "valido": False,
                "mensagem": f"Erro ao validar dados: {str(e)}"
            },
            status_code=500
        )


@router.post("/editais/renovacao/validar-etapa2")
@requer_autenticacao(["aluno"])
async def validar_auxilios_renovacao(
    request: Request,
    usuario_logado: dict = None,
    auxilios_renovacao: List[str] = Form([]),
    auxilios_novos: List[str] = Form([])
):
    """
    Endpoint para validar dados da Etapa 2 de Renovação (Auxílios).
    Verifica se pelo menos um auxílio foi selecionado (renovação ou novo).
    """
    from fastapi.responses import JSONResponse
    
    try:
        # Verificar se pelo menos um auxílio foi selecionado
        total_auxilios = len(auxilios_renovacao) + len(auxilios_novos)
        
        if total_auxilios == 0:
            return JSONResponse(
                content={
                    "valido": False,
                    "mensagem": "Você precisa selecionar pelo menos um auxílio para continuar com a renovação."
                },
                status_code=400
            )
        
        # Validação bem-sucedida
        return JSONResponse(
            content={
                "valido": True,
                "mensagem": "Auxílios validados com sucesso!",
                "total_selecionados": total_auxilios,
                "auxilios_renovacao": auxilios_renovacao,
                "auxilios_novos": auxilios_novos
            },
            status_code=200
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "valido": False,
                "mensagem": f"Erro ao validar auxílios: {str(e)}"
            },
            status_code=500
        )


@router.post("/editais/renovacao")
@requer_autenticacao(["aluno"])
async def post_editais_renovacao(
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
    # Auxílios para renovação (já possui) e novos auxílios (não possui ainda)
    auxilios_renovacao: List[str] = Form([]),
    auxilios_novos: List[str] = Form([]),
    # Dados de transporte (opcionais)
    tipo_transporte: Optional[str] = Form(None),
    tipo_onibus: Optional[List[str]] = Form([]),
    gasto_passagens_dia: Optional[str] = Form(None),
    gasto_van_mensal: Optional[str] = Form(None),
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
        # 1. Mapear renda_percapita de categoria para valor numérico
        mapa_renda = {
            "menor_1": 1412.0,      # 1 salário mínimo
            "ate_1_5": 2118.0,      # 1,5 salário mínimo
            "maior_1_5": 2500.0     # Valor representativo acima de 1,5
        }
        renda_valor = mapa_renda.get(renda_percapita, 0.0)
        
        # Tratar campos float opcionais (converter string vazia ou inválida em None)
        def converter_para_float(valor_str):
            if valor_str in [None, "", "0", 0]:
                return None
            try:
                valor_float = float(valor_str)
                return valor_float if valor_float > 0 else None
            except (ValueError, TypeError):
                return None
        
        gasto_passagens_dia_tratado = converter_para_float(gasto_passagens_dia)
        gasto_van_mensal_tratado = converter_para_float(gasto_van_mensal)
        
        # 2. Buscar edital ativo para renovação
        editais_visiveis = edital_repo.obter_editais_visiveis_alunos()
        edital_ativo = editais_visiveis[0] if editais_visiveis else None
        
        if not edital_ativo:
            return RedirectResponse(
                "/aluno/editais?erro=Não há editais abertos para renovação no momento.", 
                status_code=303
            )
        
        id_edital_ativo = edital_ativo.id_edital
        
        # 3. Combinar auxílios de renovação e novos
        auxilios_total = list(set(auxilios_renovacao + auxilios_novos))
        
        # 3. Validar dados do formulário usando o DTO
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
                renda_percapita=renda_valor,
                bolsa_pesquisa=bolsa_pesquisa,
                cad_unico=cad_unico,
                bolsa_familia=bolsa_familia,
                auxilios=auxilios_total,
                tipo_transporte=tipo_transporte,
                tipo_onibus=tipo_onibus,
                gasto_passagens_dia=gasto_passagens_dia_tratado,
                gasto_van_mensal=gasto_van_mensal_tratado
            )
        except ValidationError as e:
            # Extrair primeira mensagem de erro com detalhes
            primeiro_erro = e.errors()[0]
            mensagem_erro = primeiro_erro['msg']
            campo_erro = primeiro_erro['loc'][0] if primeiro_erro['loc'] else 'campo'
            
            # Traduzir nomes de campos para português
            traducao_campos = {
                'nome': 'Nome Completo',
                'cpf': 'CPF',
                'data_nascimento': 'Data de Nascimento',
                'telefone': 'Telefone',
                'email': 'E-mail',
                'logradouro': 'Logradouro',
                'numero': 'Número',
                'bairro': 'Bairro',
                'cidade': 'Cidade',
                'estado': 'Estado',
                'cep': 'CEP',
                'curso': 'Curso',
                'matricula': 'Matrícula',
                'ano_ingresso': 'Ano de Ingresso',
                'ano_conclusao_previsto': 'Ano Previsto para Conclusão',
                'pessoas_residencia': 'Quantas pessoas residem com você',
                'renda_percapita': 'Renda Familiar Per Capita',
                'bolsa_pesquisa': 'Bolsa de Pesquisa/Estágio',
                'cad_unico': 'CAD Único',
                'bolsa_familia': 'Bolsa Família',
                'tipo_transporte': 'Tipo de Transporte',
                'gasto_passagens_dia': 'Gasto com Passagens por Dia',
                'gasto_van_mensal': 'Gasto Mensal com Van'
            }
            
            campo_traduzido = traducao_campos.get(str(campo_erro), str(campo_erro))
            
            # Personalizar mensagem de erro
            if 'cpf' in str(campo_erro).lower():
                mensagem_amigavel = "CPF inválido. Por favor, verifique se digitou corretamente."
            elif 'email' in str(campo_erro).lower():
                mensagem_amigavel = "E-mail inválido. Por favor, verifique o formato."
            elif 'telefone' in str(campo_erro).lower():
                mensagem_amigavel = "Telefone inválido. Use o formato (00) 00000-0000."
            elif 'cep' in str(campo_erro).lower():
                mensagem_amigavel = "CEP inválido. Use o formato 00000-000."
            else:
                mensagem_amigavel = mensagem_erro
            
            return RedirectResponse(
                f"/aluno/editais/renovacao?erro={campo_traduzido}: {mensagem_amigavel}&campo_erro={campo_erro}", 
                status_code=303
            )
        
        # 4. Validar documentos obrigatórios
        if not anexo_documentos or not anexo_documentos.filename:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Documento de Identificação é obrigatório", 
                status_code=303
            )
        
        if not anexo_1 or not anexo_1.filename:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Anexo I (Termo Comprobatório de Declaração de Renda) é obrigatório", 
                status_code=303
            )
        
        if not anexo_3 or not anexo_3.filename:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Anexo III (Termo de Responsabilidade) é obrigatório", 
                status_code=303
            )
        
        # 5. Validar tipos de arquivo e tamanho
        tipos_permitidos = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
        tamanho_max = 10 * 1024 * 1024  # 10MB
        
        # Validar Documento de Identificação
        if anexo_documentos.content_type not in tipos_permitidos:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Documento de Identificação: tipo de arquivo inválido. Use PDF ou imagens (JPG, PNG).", 
                status_code=303
            )
        
        conteudo_doc = await anexo_documentos.read()
        await anexo_documentos.seek(0)
        if len(conteudo_doc) > tamanho_max:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Documento de Identificação excede o tamanho máximo de 10MB", 
                status_code=303
            )
        
        # Validar Anexo I
        if anexo_1.content_type not in tipos_permitidos:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Anexo I: tipo de arquivo inválido. Use PDF ou imagens (JPG, PNG).", 
                status_code=303
            )
        
        conteudo_anexo1 = await anexo_1.read()
        await anexo_1.seek(0)
        if len(conteudo_anexo1) > tamanho_max:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Anexo I excede o tamanho máximo de 10MB", 
                status_code=303
            )
        
        # Validar Anexo III
        if anexo_3.content_type not in tipos_permitidos:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Anexo III: tipo de arquivo inválido. Use PDF ou imagens (JPG, PNG).", 
                status_code=303
            )
        
        conteudo_anexo3 = await anexo_3.read()
        await anexo_3.seek(0)
        if len(conteudo_anexo3) > tamanho_max:
            return RedirectResponse(
                "/aluno/editais/renovacao?erro=Anexo III excede o tamanho máximo de 10MB", 
                status_code=303
            )
        
        # 6. Atualizar dados do aluno
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
        
        # 7. Criar diretório para upload
        upload_dir = os.path.join("static", "uploads", "inscricoes", str(aluno.id_usuario))
        os.makedirs(upload_dir, exist_ok=True)
        
        # 8. Função auxiliar para salvar arquivo
        import secrets
        async def salvar_arquivo(arquivo: UploadFile, prefixo: str) -> str:
            if not arquivo or not arquivo.filename:
                return ""
            
            if arquivo.content_type not in tipos_permitidos:
                return ""
            
            extensao = arquivo.filename.split(".")[-1]
            nome_arquivo = f"{prefixo}_{secrets.token_hex(8)}.{extensao}"
            caminho_completo = os.path.join(upload_dir, nome_arquivo)
            
            conteudo = await arquivo.read()
            with open(caminho_completo, "wb") as f:
                f.write(conteudo)
            
            return f"/static/uploads/inscricoes/{aluno.id_usuario}/{nome_arquivo}"
        
        # 9. Salvar documentos obrigatórios
        doc_identificacao_path = await salvar_arquivo(anexo_documentos, "doc_identificacao")
        anexo_1_path = await salvar_arquivo(anexo_1, "anexo_1")
        anexo_3_path = await salvar_arquivo(anexo_3, "anexo_3")
        
        # 10. Criar inscrição de renovação
        nova_inscricao = Inscricao(
            id_inscricao=0,
            id_aluno=aluno.id_usuario,
            id_edital=id_edital_ativo,  # Usando edital ativo encontrado
            data_inscricao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="pendente",
            urlDocumentoIdentificacao=doc_identificacao_path,
            urlDeclaracaoRenda=anexo_1_path,
            urlTermoResponsabilidade=anexo_3_path
        )
        id_inscricao = inscricao_repo.inserir(nova_inscricao)
        
        # 11. Processar auxílio de transporte (renovação ou novo)
        if "transporte" in auxilios_total:
            # Salvar documentos de transporte
            url_comp_residencia = await salvar_arquivo(comprovante_residencia_transporte, "comp_residencia_transporte")
            url_passe_frente = await salvar_arquivo(passe_escolar_frente, "passe_escolar_frente")
            url_passe_verso = await salvar_arquivo(passe_escolar_verso, "passe_escolar_verso")
            url_comp_recarga = await salvar_arquivo(comprovante_recarga, "comp_recarga")
            url_comp_passagens = await salvar_arquivo(comprovante_passagens, "comp_passagens")
            url_contrato_transp = await salvar_arquivo(contrato_transporte, "contrato_transporte")
            
            tipos_onibus_str = ",".join(tipo_onibus) if tipo_onibus else None
            
            auxilio_transporte = AuxilioTransporte(
                id_auxilio=0,
                id_edital=id_edital_ativo,
                id_inscricao=id_inscricao,
                descricao=f"Auxílio Transporte - Renovação - {tipo_transporte if tipo_transporte else 'Não especificado'}",
                valor_mensal=300.0,
                data_inicio=datetime.now().strftime("%Y-%m-%d"),
                data_fim="",
                tipo_auxilio="transporte",
                tipo_transporte=tipo_transporte if tipo_transporte else "",
                tipo_onibus=tipos_onibus_str,
                gasto_passagens_dia=gasto_passagens_dia_tratado,
                gasto_van_mensal=gasto_van_mensal_tratado,
                urlCompResidencia=url_comp_residencia,
                urlPasseEscolarFrente=url_passe_frente,
                urlPasseEscolarVerso=url_passe_verso,
                urlComprovanteRecarga=url_comp_recarga,
                urlComprovantePassagens=url_comp_passagens,
                urlContratoTransporte=url_contrato_transp
            )
            AuxilioTransporteRepo.inserir(auxilio_transporte)
        
        # 12. Processar auxílio de moradia (renovação ou novo)
        if "moradia" in auxilios_total:
            comp_res_anterior = await salvar_arquivo(comprovante_residencia_anterior, "comp_res_anterior")
            comp_res_atual = await salvar_arquivo(comprovante_residencia_atual, "comp_res_atual")
            contrato_alug = await salvar_arquivo(contrato_aluguel, "contrato_aluguel")
            decl_prop = await salvar_arquivo(declaracao_proprietario, "declaracao_proprietario")
            
            auxilio_moradia = AuxilioMoradia(
                id_auxilio=0,
                id_edital=id_edital_ativo,
                id_inscricao=id_inscricao,
                descricao="Auxílio Moradia - Renovação",
                valor_mensal=400.0,
                data_inicio=datetime.now().strftime("%Y-%m-%d"),
                data_fim="",
                tipo_auxilio="moradia",
                url_comp_residencia_fixa=comp_res_anterior,
                url_comp_residencia_alugada=comp_res_atual,
                url_contrato_aluguel_cid_campus=contrato_alug,
                url_contrato_aluguel_cid_natal=decl_prop
            )
            AuxilioMoradiaRepo.inserir(auxilio_moradia)
        
        # 13. Processar auxílio de alimentação (renovação ou novo)
        if "alimentacao" in auxilios_total:
            auxilio_alimentacao = Auxilio(
                id_auxilio=0,
                id_edital=id_edital_ativo,
                id_inscricao=id_inscricao,
                descricao="Auxílio Alimentação",
                valor_mensal=600.0,
                data_inicio=datetime.now().strftime("%Y-%m-%d"),
                data_fim="",
                tipo_auxilio="alimentacao"
            )
            auxilio_repo.inserir(auxilio_alimentacao)
        
        # 14. Processar auxílio material didático (renovação ou novo)
        if "material" in auxilios_total:
            auxilio_material = Auxilio(
                id_auxilio=0,
                id_edital=id_edital_ativo,
                id_inscricao=id_inscricao,
                descricao="Auxílio Material Didático",
                valor_mensal=200.0,
                data_inicio=datetime.now().strftime("%Y-%m-%d"),
                data_fim="",
                tipo_auxilio="material"
            )
            auxilio_repo.inserir(auxilio_material)
        
        # 15. Redirecionar com mensagem de sucesso
        return RedirectResponse(
            "/aluno/editais?msg=✓ Renovação enviada com sucesso! Sua solicitação de renovação foi registrada e está em análise. Acompanhe as atualizações no sistema.", 
            status_code=303
        )
        
    except Exception as e:
        print(f"Erro ao processar renovação: {e}")
        return RedirectResponse(
            "/aluno/editais/renovacao?erro=Erro ao processar renovação. Tente novamente.", 
            status_code=303
        )
