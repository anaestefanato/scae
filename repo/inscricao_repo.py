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
            a.tipo_auxilio,
            a.valor_mensal,
            CASE 
                WHEN DATE(e.data_encerramento) <= DATE('now', '+7 days') THEN 'Alta'
                WHEN DATE(e.data_encerramento) <= DATE('now', '+15 days') THEN 'Média'
                ELSE 'Baixa'
            END as prioridade
        FROM inscricao i
        INNER JOIN edital e ON i.id_edital = e.id_edital
        INNER JOIN usuario u ON i.id_aluno = u.id_usuario
        LEFT JOIN auxilio a ON i.id_inscricao = a.id_inscricao
        WHERE {where_sql}
        ORDER BY {order_sql}
        LIMIT ? OFFSET ?
        """
        
        params_list.extend([limite, offset])
        cursor.execute(sql_list, params_list)
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
                'data_encerramento': row["data_encerramento"],
                'aluno_nome': row["aluno_nome"],
                'aluno_matricula': row["aluno_matricula"],
                'tipo_auxilio': row["tipo_auxilio"] if "tipo_auxilio" in row else "Não especificado",
                'valor_mensal': row["valor_mensal"] if "valor_mensal" in row else 0,
                'prioridade': row["prioridade"]
            }
            inscricoes.append(inscricao)
        
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