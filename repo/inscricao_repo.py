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


def obter_inscricoes_para_analise(pagina: int = 1, limite: int = 10) -> tuple[list[dict], int]:
    """Obtém inscrições pendentes para análise com paginação"""
    offset = (pagina - 1) * limite
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Buscar total de registros
        cursor.execute(CONTAR_INSCRICOES_PARA_ANALISE)
        total = cursor.fetchone()["total"]
        
        # Buscar registros da página
        cursor.execute(OBTER_INSCRICOES_PARA_ANALISE, (limite, offset))
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
    except Exception as e:
        print("Erro ao obter inscrições para análise:", e)
        return [], 0


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