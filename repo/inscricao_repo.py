from typing import Optional
from model.inscricao_model import Inscricao
from data.inscricao_sql import *
from data.util import get_connection

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