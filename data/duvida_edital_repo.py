from typing import Optional
from data.duvida_edital_model import DuvidaEdital
from data.duvida_edital_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(duvida: DuvidaEdital) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            duvida.id_duvida,
            duvida.id_edital,
            duvida.id_aluno,
            duvida.pergunta,
            duvida.resposta,
            duvida.dataPergunta,
            duvida.dataResposta,
            duvida.status))
        return cursor.lastrowid
    
def obter_todos() -> list[DuvidaEdital]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        duvidas = [
            DuvidaEdital(
                id_duvida=row["id_duvida"],
                id_edital=row["id_edital"],
                id_aluno=row["id_aluno"],
                pergunta=row["pergunta"],
                resposta=row["resposta"],
                dataPergunta=row["dataPergunta"],
                dataResposta=row["dataResposta"],
                status=row["status"])
            for row in rows]
        return duvidas

def obter_por_id(id: int) -> Optional[DuvidaEdital]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            duvida = DuvidaEdital(
                id_duvida=row["id_duvida"],
                id_edital=row["id_edital"],
                id_aluno=row["id_aluno"],
                pergunta=row["pergunta"],
                resposta=row["resposta"],
                dataPergunta=row["dataPergunta"],
                dataResposta=row["dataResposta"],
                status=row["status"])
            return duvida
        return None

def atualizar(self, duvida: DuvidaEdital) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (duvida.pergunta, duvida.resposta, duvida.status))
        return cursor.rowcount > 0

def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0