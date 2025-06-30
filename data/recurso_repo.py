from typing import Optional
from data.recurso_model import Recurso
from data.recurso_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(recurso: Recurso) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            recurso.id_recurso,
            recurso.id_inscricao,
            recurso.id_assistente_social,
            recurso.descricao,
            recurso.data_envio,
            recurso.data_resposta,
            recurso.status))
        return cursor.lastrowid

def obter_por_pagina(pagina: int, limit: int) -> list[Recurso]:
    offset = (pagina - 1) * limit
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limit, offset))
        rows = cursor.fetchall()
        recursos = []
        for row in rows:
            recurso = Recurso(
                id_recurso=row["id_recurso"],
                id_inscricao=row["id_inscricao"],
                id_assistente_social=row["id_assistente"],
                descricao=row["descricao"],
                data_envio=row["dataEnvio"],
                data_resposta=row["dataResposta"],
                status=row["status"]
            )
            recursos.append(recurso)
        return recursos

def obter_por_id(id: int) -> Optional[Recurso]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        recurso = Recurso(
            id_recurso=row["id_recurso"],
            id_inscricao=row["id_inscricao"],
            id_assistente_social=row["id_assistente"],
            descricao=row["descricao"],
            data_envio=row["dataEnvio"],
            data_resposta=row["dataResposta"],
            status=row["status"])
        return recurso

def atualizar(recurso: Recurso) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (recurso.descricao, recurso.status))
        return (cursor.rowcount > 0)

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)