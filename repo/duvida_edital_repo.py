from typing import Optional, List
from model.duvida_edital_model import DuvidaEdital
from data.duvida_edital_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print("Erro ao criar tabela duvida_edital:", e)
        return False

def inserir(duvida: DuvidaEdital) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            duvida.id_edital,
            duvida.id_aluno,
            duvida.pergunta,
            duvida.resposta,
            duvida.data_pergunta,
            duvida.data_resposta,
            duvida.status
        ))
        conn.commit()
        return cursor.lastrowid

def obter_por_id(id_duvida: int) -> Optional[DuvidaEdital]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_duvida,))
        row = cursor.fetchone()
        if row is None:
            return None
        return DuvidaEdital(
            id_duvida=row["id_duvida"],
            id_edital=row["id_edital"],
            id_aluno=row["id_aluno"],
            pergunta=row["pergunta"],
            resposta=row["resposta"],
            data_pergunta=row["data_pergunta"],
            data_resposta=row["data_resposta"],
            status=row["status"]
        )

def obter_por_pagina(pagina: int, limite: int) -> List[DuvidaEdital]:
    offset = (pagina - 1) * limite
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        duvidas = []
        for row in rows:
            duvida = DuvidaEdital(
                id_duvida=row["id_duvida"],
                id_edital=row["id_edital"],
                id_aluno=row["id_aluno"],
                pergunta=row["pergunta"],
                resposta=row["resposta"],
                data_pergunta=row["data_pergunta"],
                data_resposta=row["data_resposta"],
                status=row["status"]
            )
            duvidas.append(duvida)
        return duvidas

def atualizar(duvida: DuvidaEdital) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            duvida.pergunta,
            duvida.resposta,
            duvida.data_pergunta,
            duvida.data_resposta,
            duvida.status,
            duvida.id_duvida
        ))
        conn.commit()
        return cursor.rowcount > 0

def excluir(id_duvida: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_duvida,))
        conn.commit()
        return cursor.rowcount > 0
