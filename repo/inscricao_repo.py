from typing import Optional
from model.inscricao_model import Inscricao
from sql.inscricao_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            conn.commit()
        return True
    except Exception as e:
        print("Erro ao criar tabela:", e)
        return False

def inserir(inscricao: Inscricao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            inscricao.id_aluno,
            inscricao.id_edital,
            inscricao.data_inscricao,
            inscricao.status,
            inscricao.urlDocumentoIdentificacao,
            inscricao.urlDeclaracaoRenda,
            inscricao.urlTermoResponsabilidade
        ))
        conn.commit()  
        return cursor.lastrowid


def obter_por_pagina(pagina: int, limit: int) -> list[Inscricao]:
    offset = (pagina - 1) * limit
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limit, offset))
        rows = cursor.fetchall()
        inscricoes = []
        for row in rows:
            inscricao = Inscricao(
                id_inscricao=row["id_inscricao"],
                id_aluno=row["id_aluno"],
                id_edital=row["id_edital"],
                data_inscricao=row["data_inscricao"],
                status=row["status"],
                urlDocumentoIdentificacao=row["urlDocumentoIdentificacao"],
                urlDeclaracaoRenda=row["urlDeclaracaoRenda"],
                urlTermoResponsabilidade=row["urlTermoResponsabilidade"]
            )
            inscricoes.append(inscricao)
        return inscricoes

def obter_por_id(id: int) -> Optional[Inscricao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None  # <-- IMPORTANTE: retorna None se não achar nada
        return Inscricao(
            id_inscricao=row["id_inscricao"],
            id_aluno=row["id_aluno"],
            id_edital=row["id_edital"],
            data_inscricao=row["data_inscricao"],
            status=row["status"],
            urlDocumentoIdentificacao=row["urlDocumentoIdentificacao"],
            urlDeclaracaoRenda=row["urlDeclaracaoRenda"],
            urlTermoResponsabilidade=row["urlTermoResponsabilidade"]
        )
    

def atualizar(inscricao: Inscricao) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                inscricao.status,
                inscricao.urlDocumentoIdentificacao,
                inscricao.urlDeclaracaoRenda,
                inscricao.urlTermoResponsabilidade,
                inscricao.id_inscricao
            ))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar inscrição:", e)
        return False


def atualizar_status(id_inscricao: int, novo_status: str) -> bool:
    """Atualiza apenas o status de uma inscrição"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE inscricao SET status = ? WHERE id_inscricao = ?",
                (novo_status, id_inscricao)
            )
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar status da inscrição {id_inscricao}:", e)
        return False


def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)


def obter_por_aluno(id_aluno: int) -> list[dict]:
    """Obtém todas as inscrições de um aluno com informações relacionadas"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ALUNO, (id_aluno,))
        rows = cursor.fetchall()
        inscricoes = []
        for row in rows:
            inscricao = {
                'id_inscricao': row["id_inscricao"],
                'id_aluno': row["id_aluno"],
                'id_edital': row["id_edital"],
                'data_inscricao': row["data_inscricao"],
                'status': row["status"],
                'urlDocumentoIdentificacao': row["urlDocumentoIdentificacao"],
                'urlDeclaracaoRenda': row["urlDeclaracaoRenda"],
                'urlTermoResponsabilidade': row["urlTermoResponsabilidade"],
                'edital_titulo': row["edital_titulo"],
                'data_publicacao': row["data_publicacao"],
                'data_encerramento': row["data_encerramento"],
                'id_auxilio': row["id_auxilio"],
                'tipo_auxilio': row["tipo_auxilio"],
                'valor_mensal': row["valor_mensal"],
                'data_inicio': row["data_inicio"],
                'data_fim': row["data_fim"]
            }
            inscricoes.append(inscricao)
        return inscricoes


def obter_estatisticas_analise() -> dict:
    """Obtém estatísticas das inscrições para análise"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ESTATISTICAS_ANALISE)
        row = cursor.fetchone()
        return {
            'pendentes': row["pendentes"] or 0,
            'em_analise': row["em_analise"] or 0,
            'analisadas_hoje': row["analisadas_hoje"] or 0,
            'total_analisadas': row["total_analisadas"] or 0
        }


def obter_inscricoes_para_analise(pagina: int = 1, limite: int = 10, filtro_edital: str = None, filtro_status: str = None, filtro_busca: str = None, ordenacao: str = None) -> tuple[list[dict], int]:
    """Obtém inscrições para análise com paginação e filtros"""
    offset = (pagina - 1) * limite
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Construir WHERE clause dinâmica
        where_clauses = []
        params_count = []
        params_list = []
        
        # Filtro de status (padrão é pendente se não especificado)
        if filtro_status:
            where_clauses.append("i.status = ?")
            params_count.append(filtro_status)
            params_list.append(filtro_status)
        else:
            where_clauses.append("i.status = ?")
            params_count.append('pendente')
            params_list.append('pendente')
        
        # Filtro de edital
        if filtro_edital:
            where_clauses.append("i.id_edital = ?")
            params_count.append(filtro_edital)
            params_list.append(filtro_edital)
        
        # Filtro de busca por nome
        if filtro_busca:
            where_clauses.append("LOWER(u.nome) LIKE ?")
            params_count.append(f"%{filtro_busca.lower()}%")
            params_list.append(f"%{filtro_busca.lower()}%")
        
        where_sql = " AND ".join(where_clauses)
        
        # Query de contagem
        sql_count = f"""
        SELECT COUNT(*) as total
        FROM inscricao i
        INNER JOIN edital e ON i.id_edital = e.id_edital
        INNER JOIN usuario u ON i.id_aluno = u.id_usuario
        WHERE {where_sql}
        """
        
        cursor.execute(sql_count, params_count)
        total = cursor.fetchone()["total"]
        
        # Ordenação
        if ordenacao == 'mais-antigas':
            order_sql = "i.data_inscricao ASC"
        else:
            order_sql = "i.data_inscricao DESC"
        
        # Query principal
        sql_list = f"""
        SELECT 
            i.id_inscricao,
            i.id_aluno,
            i.id_edital,
            i.data_inscricao,
            i.status,
            i.urlDocumentoIdentificacao,
            i.urlDeclaracaoRenda,
            i.urlTermoResponsabilidade,
            e.titulo as edital_titulo,
            e.data_encerramento,
            u.nome as aluno_nome,
            u.matricula as aluno_matricula,
            u.email as aluno_email,
            al.telefone as aluno_telefone,
            al.curso as aluno_curso,
            al.ano_ingresso as aluno_ano_ingresso,
            al.ano_conclusao_previsto as aluno_ano_conclusao,
            al.quantidade_pessoas as aluno_pessoas_residencia,
            al.renda_per_capita as aluno_renda_percapita,
            al.cad_unico as aluno_cad_unico,
            al.bolsa_familia as aluno_bolsa_familia,
            al.cpf as aluno_cpf,
            al.data_nascimento as aluno_data_nascimento,
            al.cep as aluno_cep,
            al.cidade as aluno_cidade,
            al.estado as aluno_estado,
            al.bairro as aluno_bairro,
            al.rua as aluno_rua,
            al.numero as aluno_numero,
            al.complemento as aluno_complemento,
            al.nome_banco as aluno_nome_banco,
            al.agencia_bancaria as aluno_agencia_bancaria,
            al.numero_conta_bancaria as aluno_numero_conta_bancaria,
            al.renda_familiar as aluno_renda_familiar,
            al.situacao_moradia as aluno_situacao_moradia,
            al.bolsa_pesquisa as aluno_bolsa_pesquisa,
            a.tipo_auxilio,
            a.valor_mensal,
            at.tipo_transporte as at_tipo_transporte,
            at.tipo_onibus as at_tipo_onibus,
            at.gasto_passagens_dia as at_gasto_passagens_dia,
            at.gasto_van_mensal as at_gasto_van_mensal,
            at.urlCompResidencia as at_urlCompResidencia,
            at.urlPasseEscolarFrente as at_urlPasseEscolarFrente,
            at.urlPasseEscolarVerso as at_urlPasseEscolarVerso,
            at.urlComprovanteRecarga as at_urlComprovanteRecarga,
            at.urlComprovantePassagens as at_urlComprovantePassagens,
            at.urlContratoTransporte as at_urlContratoTransporte,
            am.url_comp_residencia_fixa as am_url_comp_residencia_fixa,
            am.url_comp_residencia_alugada as am_url_comp_residencia_alugada,
            am.url_contrato_aluguel_cid_campus as am_url_contrato_aluguel_cid_campus,
            am.url_contrato_aluguel_cid_natal as am_url_contrato_aluguel_cid_natal,
            CASE 
                WHEN DATE(e.data_encerramento) <= DATE('now', '+7 days') THEN 'Alta'
                WHEN DATE(e.data_encerramento) <= DATE('now', '+15 days') THEN 'Média'
                ELSE 'Baixa'
            END as prioridade
        FROM inscricao i
        INNER JOIN edital e ON i.id_edital = e.id_edital
    INNER JOIN usuario u ON i.id_aluno = u.id_usuario
    LEFT JOIN aluno al ON u.id_usuario = al.id_usuario
        LEFT JOIN auxilio a ON i.id_inscricao = a.id_inscricao
        LEFT JOIN auxilio_transporte at ON at.id_auxilio_transporte = a.id_auxilio
        LEFT JOIN auxilio_moradia am ON am.id_auxilio_moradia = a.id_auxilio
        WHERE {where_sql}
        ORDER BY {order_sql}
        LIMIT ? OFFSET ?
        """
        
        params_list.extend([limite, offset])
        cursor.execute(sql_list, params_list)
        rows = cursor.fetchall()

        inscricoes = []
        inscricoes_dict = {}
        
        for row in rows:
            id_inscricao = row["id_inscricao"]
            
            # Se a inscrição já foi processada, adicionar o auxílio e atualizar campos específicos
            if id_inscricao in inscricoes_dict:
                if row["tipo_auxilio"] and row["tipo_auxilio"] not in inscricoes_dict[id_inscricao]['auxilios_lista']:
                    inscricoes_dict[id_inscricao]['auxilios_lista'].append(row["tipo_auxilio"])
                
                # Atualizar campos de transporte se não estiverem preenchidos e esta linha tem dados
                if row["at_tipo_transporte"] and not inscricoes_dict[id_inscricao].get("auxilio_transporte_tipo"):
                    inscricoes_dict[id_inscricao]["auxilio_transporte_tipo"] = row["at_tipo_transporte"]
                    inscricoes_dict[id_inscricao]["auxilio_transporte_tipo_onibus"] = row["at_tipo_onibus"] if "at_tipo_onibus" in row.keys() else None
                    inscricoes_dict[id_inscricao]["gasto_passagens_dia"] = row["at_gasto_passagens_dia"] if "at_gasto_passagens_dia" in row.keys() else None
                    inscricoes_dict[id_inscricao]["gasto_van_mensal"] = row["at_gasto_van_mensal"] if "at_gasto_van_mensal" in row.keys() else None
                    # Documentos de transporte
                    inscricoes_dict[id_inscricao]["at_urlCompResidencia"] = row["at_urlCompResidencia"] if "at_urlCompResidencia" in row.keys() else None
                    inscricoes_dict[id_inscricao]["at_urlPasseEscolarFrente"] = row["at_urlPasseEscolarFrente"] if "at_urlPasseEscolarFrente" in row.keys() else None
                    inscricoes_dict[id_inscricao]["at_urlPasseEscolarVerso"] = row["at_urlPasseEscolarVerso"] if "at_urlPasseEscolarVerso" in row.keys() else None
                    inscricoes_dict[id_inscricao]["at_urlComprovanteRecarga"] = row["at_urlComprovanteRecarga"] if "at_urlComprovanteRecarga" in row.keys() else None
                    inscricoes_dict[id_inscricao]["at_urlComprovantePassagens"] = row["at_urlComprovantePassagens"] if "at_urlComprovantePassagens" in row.keys() else None
                    inscricoes_dict[id_inscricao]["at_urlContratoTransporte"] = row["at_urlContratoTransporte"] if "at_urlContratoTransporte" in row.keys() else None
                
                # Atualizar campos de moradia se não estiverem preenchidos e esta linha tem dados
                if row["am_url_comp_residencia_fixa"] and not inscricoes_dict[id_inscricao].get("am_url_comp_residencia_fixa"):
                    inscricoes_dict[id_inscricao]["am_url_comp_residencia_fixa"] = row["am_url_comp_residencia_fixa"]
                    inscricoes_dict[id_inscricao]["am_url_comp_residencia_alugada"] = row["am_url_comp_residencia_alugada"] if "am_url_comp_residencia_alugada" in row.keys() else None
                    inscricoes_dict[id_inscricao]["am_url_contrato_aluguel_cid_campus"] = row["am_url_contrato_aluguel_cid_campus"] if "am_url_contrato_aluguel_cid_campus" in row.keys() else None
                    inscricoes_dict[id_inscricao]["am_url_contrato_aluguel_cid_natal"] = row["am_url_contrato_aluguel_cid_natal"] if "am_url_contrato_aluguel_cid_natal" in row.keys() else None
                
                continue
            # build documentos list from available urls
            documentos = []
            if "urlDocumentoIdentificacao" in row.keys() and row["urlDocumentoIdentificacao"]:
                documentos.append(row["urlDocumentoIdentificacao"])
            if "urlDeclaracaoRenda" in row.keys() and row["urlDeclaracaoRenda"]:
                documentos.append(row["urlDeclaracaoRenda"])
            if "urlTermoResponsabilidade" in row.keys() and row["urlTermoResponsabilidade"]:
                documentos.append(row["urlTermoResponsabilidade"])
            # auxilio_transporte documents
            if "at_urlCompResidencia" in row.keys() and row["at_urlCompResidencia"]:
                documentos.append(row["at_urlCompResidencia"])
            if "at_urlPasseEscolarFrente" in row.keys() and row["at_urlPasseEscolarFrente"]:
                documentos.append(row["at_urlPasseEscolarFrente"])
            if "at_urlPasseEscolarVerso" in row.keys() and row["at_urlPasseEscolarVerso"]:
                documentos.append(row["at_urlPasseEscolarVerso"])
            if "at_urlComprovanteRecarga" in row.keys() and row["at_urlComprovanteRecarga"]:
                documentos.append(row["at_urlComprovanteRecarga"])
            if "at_urlComprovantePassagens" in row.keys() and row["at_urlComprovantePassagens"]:
                documentos.append(row["at_urlComprovantePassagens"])
            if "at_urlContratoTransporte" in row.keys() and row["at_urlContratoTransporte"]:
                documentos.append(row["at_urlContratoTransporte"])
            # auxilio_moradia documents
            if "am_url_comp_residencia_fixa" in row.keys() and row["am_url_comp_residencia_fixa"]:
                documentos.append(row["am_url_comp_residencia_fixa"])
            if "am_url_comp_residencia_alugada" in row.keys() and row["am_url_comp_residencia_alugada"]:
                documentos.append(row["am_url_comp_residencia_alugada"])
            if "am_url_contrato_aluguel_cid_campus" in row.keys() and row["am_url_contrato_aluguel_cid_campus"]:
                documentos.append(row["am_url_contrato_aluguel_cid_campus"])
            if "am_url_contrato_aluguel_cid_natal" in row.keys() and row["am_url_contrato_aluguel_cid_natal"]:
                documentos.append(row["am_url_contrato_aluguel_cid_natal"])

            # Criar lista de auxílios
            auxilios_lista = []
            if row["tipo_auxilio"]:
                auxilios_lista.append(row["tipo_auxilio"])

            inscricao = {
                'id_inscricao': row["id_inscricao"],
                'id_aluno': row["id_aluno"],
                'id_edital': row["id_edital"],
                'data_inscricao': row["data_inscricao"],
                'status': row["status"],
                'urlDocumentoIdentificacao': row["urlDocumentoIdentificacao"],
                'urlDeclaracaoRenda': row["urlDeclaracaoRenda"],
                'urlTermoResponsabilidade': row["urlTermoResponsabilidade"],
                'edital_titulo': row["edital_titulo"],
                'data_encerramento': row["data_encerramento"],
                'aluno_nome': row["aluno_nome"],
                'aluno_matricula': row["aluno_matricula"],
                'aluno_email': row["aluno_email"] if "aluno_email" in row.keys() else None,
                'aluno_telefone': row["aluno_telefone"] if "aluno_telefone" in row.keys() else None,
                'aluno_curso': row["aluno_curso"] if "aluno_curso" in row.keys() else None,
                'aluno_ano_ingresso': row["aluno_ano_ingresso"] if "aluno_ano_ingresso" in row.keys() else None,
                'aluno_ano_conclusao': row["aluno_ano_conclusao"] if "aluno_ano_conclusao" in row.keys() else None,
                'aluno_pessoas_residencia': row["aluno_pessoas_residencia"] if "aluno_pessoas_residencia" in row.keys() else None,
                'aluno_renda_percapita': row["aluno_renda_percapita"] if "aluno_renda_percapita" in row.keys() else None,
                'aluno_cad_unico': row["aluno_cad_unico"] if "aluno_cad_unico" in row.keys() else None,
                'aluno_bolsa_familia': row["aluno_bolsa_familia"] if "aluno_bolsa_familia" in row.keys() else None,
                'aluno_bolsa_pesquisa': row["aluno_bolsa_pesquisa"] if "aluno_bolsa_pesquisa" in row.keys() else None,
                'aluno_cpf': row["aluno_cpf"] if "aluno_cpf" in row.keys() else None,
                'aluno_data_nascimento': row["aluno_data_nascimento"] if "aluno_data_nascimento" in row.keys() else None,
                'aluno_cep': row["aluno_cep"] if "aluno_cep" in row.keys() else None,
                'aluno_cidade': row["aluno_cidade"] if "aluno_cidade" in row.keys() else None,
                'aluno_estado': row["aluno_estado"] if "aluno_estado" in row.keys() else None,
                'aluno_bairro': row["aluno_bairro"] if "aluno_bairro" in row.keys() else None,
                'aluno_rua': row["aluno_rua"] if "aluno_rua" in row.keys() else None,
                'aluno_numero': row["aluno_numero"] if "aluno_numero" in row.keys() else None,
                'aluno_complemento': row["aluno_complemento"] if "aluno_complemento" in row.keys() else None,
                'aluno_auxilios': row["aluno_auxilios"] if "aluno_auxilios" in row.keys() else None,
                # aliases expected by the template
                'aluno_periodo': row["aluno_periodo"] if "aluno_periodo" in row.keys() else None,
                'renda_per_capita': row["aluno_renda_percapita"] if "aluno_renda_percapita" in row.keys() else (row["renda_per_capita"] if "renda_per_capita" in row.keys() else None),
                'composicao_familiar': row["composicao_familiar"] if "composicao_familiar" in row.keys() else None,
                'pessoas_residencia': row["aluno_pessoas_residencia"] if "aluno_pessoas_residencia" in row.keys() else (row["quantidade_pessoas"] if "quantidade_pessoas" in row.keys() else None),
                'quantidade_pessoas': row["aluno_pessoas_residencia"] if "aluno_pessoas_residencia" in row.keys() else (row["quantidade_pessoas"] if "quantidade_pessoas" in row.keys() else None),
                'renda_percapita': row["aluno_renda_percapita"] if "aluno_renda_percapita" in row.keys() else None,
                'ano_ingresso': row["aluno_ano_ingresso"] if "aluno_ano_ingresso" in row.keys() else None,
                'ano_conclusao_previsto': row["aluno_ano_conclusao"] if "aluno_ano_conclusao" in row.keys() else None,
                'cad_unico': row["aluno_cad_unico"] if "aluno_cad_unico" in row.keys() else None,
                'bolsa_familia': row["aluno_bolsa_familia"] if "aluno_bolsa_familia" in row.keys() else None,
                'auxilios': row["aluno_auxilios"] if "aluno_auxilios" in row.keys() else None,
                'tipo_auxilio': row["tipo_auxilio"] if "tipo_auxilio" in row.keys() else "Não especificado",
                'valor_mensal': row["valor_mensal"] if "valor_mensal" in row.keys() else 0,
                'prioridade': row["prioridade"],
                # transporte / auxilio_transporte fields
                'auxilio_transporte_tipo': row["at_tipo_transporte"] if "at_tipo_transporte" in row.keys() else None,
                'auxilio_transporte_tipo_onibus': row["at_tipo_onibus"] if "at_tipo_onibus" in row.keys() else None,
                'gasto_passagens_dia': row["at_gasto_passagens_dia"] if "at_gasto_passagens_dia" in row.keys() else None,
                'gasto_van_mensal': row["at_gasto_van_mensal"] if "at_gasto_van_mensal" in row.keys() else None,
                'at_urlCompResidencia': row["at_urlCompResidencia"] if "at_urlCompResidencia" in row.keys() else None,
                'at_urlPasseEscolarFrente': row["at_urlPasseEscolarFrente"] if "at_urlPasseEscolarFrente" in row.keys() else None,
                'at_urlPasseEscolarVerso': row["at_urlPasseEscolarVerso"] if "at_urlPasseEscolarVerso" in row.keys() else None,
                'at_urlComprovanteRecarga': row["at_urlComprovanteRecarga"] if "at_urlComprovanteRecarga" in row.keys() else None,
                'at_urlComprovantePassagens': row["at_urlComprovantePassagens"] if "at_urlComprovantePassagens" in row.keys() else None,
                'at_urlContratoTransporte': row["at_urlContratoTransporte"] if "at_urlContratoTransporte" in row.keys() else None,
                # moradia / auxilio_moradia fields
                'am_url_comp_residencia_fixa': row["am_url_comp_residencia_fixa"] if "am_url_comp_residencia_fixa" in row.keys() else None,
                'am_url_comp_residencia_alugada': row["am_url_comp_residencia_alugada"] if "am_url_comp_residencia_alugada" in row.keys() else None,
                'am_url_contrato_aluguel_cid_campus': row["am_url_contrato_aluguel_cid_campus"] if "am_url_contrato_aluguel_cid_campus" in row.keys() else None,
                'am_url_contrato_aluguel_cid_natal': row["am_url_contrato_aluguel_cid_natal"] if "am_url_contrato_aluguel_cid_natal" in row.keys() else None,
                # aggregated documentos
                'documentos': documentos,
                'auxilios_lista': auxilios_lista,
            }
            inscricoes_dict[id_inscricao] = inscricao

        # Converter dict para lista
        inscricoes = list(inscricoes_dict.values())
        
        return inscricoes, total
    


def obter_estatisticas_dashboard() -> Optional[dict]:
    """
    Obtém estatísticas gerais do dashboard para assistente social
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_ESTATISTICAS_DASHBOARD)
            row = cursor.fetchone()
            
            if row:
                return {
                    'editais_ativos': row[0] or 0,
                    'inscricoes_pendentes': row[1] or 0,
                    'alunos_beneficiados': row[2] or 0,
                    'valor_total_mensal': row[3] or 0.0
                }
            return None
    except Exception as e:
        print("Erro ao obter estatísticas do dashboard:", e)
        return None


def obter_inscricoes_recentes_dashboard() -> list[dict]:
    """
    Obtém inscrições recentes com prioridade para o dashboard
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_INSCRICOES_RECENTES_DASHBOARD)
            rows = cursor.fetchall()
            
            inscricoes = []
            for row in rows:
                inscricao = {
                    'id_inscricao': row[0],
                    'data_inscricao': row[1],
                    'aluno_nome': row[2],
                    'edital_titulo': row[3],
                    'tipo_auxilio': row[4] or 'Não definido',
                    'prioridade': row[5]
                }
                inscricoes.append(inscricao)
            
            return inscricoes
    except Exception as e:
        print("Erro ao obter inscrições recentes para dashboard:", e)
        return []