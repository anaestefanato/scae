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
            recurso.id_assistente,
            recurso.descricao,
            recurso.dataEnvio,
            recurso.dataResposta,
            recurso.status))
        return cursor.lastrowid

def obter_todos() -> list[Recurso]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        recursos = [
            Recurso(
                id_recurso=row["id_recurso"],
                id_inscricao=row["id_inscricao"],
                id_assistente=row["id_assistente"],
                descricao=row["descricao"],
                dataEnvio=row["dataEnvio"],
                dataResposta=row["dataResposta"],
                status=row["status"])
            for row in rows]
        return recursos

def obter_por_id(id: int) -> Optional[Recurso]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            recurso = Recurso(
                id_recurso=row["id_recurso"],
                id_inscricao=row["id_inscricao"],
                id_assistente=row["id_assistente"],
                descricao=row["descricao"],
                dataEnvio=row["dataEnvio"],
                dataResposta=row["dataResposta"],
                status=row["status"])
            return recurso
        return None

def atualizar(self, recurso: Recurso) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (recurso.descricao, recurso.status))
        return cursor.rowcount > 0

def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0