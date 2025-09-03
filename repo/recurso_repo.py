from typing import Optional
from model.recurso_model import Recurso
from sql.recurso_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela recurso: {e}")
        return False

def inserir(recurso: Recurso) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            recurso.id_inscricao,
            recurso.id_assistente,
            recurso.descricao,
            recurso.data_envio,
            recurso.data_resposta,
            recurso.status
        ))
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
                id_assistente=row["id_assistente"],
                descricao=row["descricao"],
                data_envio=row["data_envio"],
                data_resposta=row["data_resposta"],
                status=row["status"]
            )
            recursos.append(recurso)
        return recursos

def obter_por_id(id: int) -> Optional[Recurso]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Recurso(
                id_recurso=row["id_recurso"],
                id_inscricao=row["id_inscricao"],
                id_assistente=row["id_assistente"],
                descricao=row["descricao"],
                data_envio=row["data_envio"],
                data_resposta=row["data_resposta"],
                status=row["status"]
            )
        return None

    def obter_por_id(id: int) -> Optional[Recurso]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (id,))
            row = cursor.fetchone()
            if row:
                return Recurso(
                    id_recurso=row["id_recurso"],
                    id_inscricao=row["id_inscricao"],
                    id_assistente=row["id_assistente"],
                    descricao=row["descricao"],
                    data_envio=row["data_envio"],
                    data_resposta=row["data_resposta"],
                    status=row["status"]
                )
            return None

def atualizar(recurso: Recurso) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                recurso.descricao,
                recurso.status,
                recurso.id_recurso
            ))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar recurso:", e)
        return False

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0