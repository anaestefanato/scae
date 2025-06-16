from typing import Optional
from data.auxilio_alimentacao_model import AuxilioAlimentacao
from data.auxilio_alimentacao_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(auxilioAlimentacao: AuxilioAlimentacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (auxilioAlimentacao.id_auxilio_alimentacao,))
        return cursor.lastrowid

def obter_todos() -> list[AuxilioAlimentacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            AuxilioAlimentacao(id_auxilio_alimentacao=row["id_auxilio_alimentacao"])
            for row in rows]
        return auxilios

def obter_por_id(self, id: int) -> Optional[AuxilioAlimentacao]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return AuxilioAlimentacao(**row)
        return None

def atualizar(self, auxilioAlimentacao: AuxilioAlimentacao) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            auxilioAlimentacao.id_auxilio_alimentacao,))
        return cursor.rowcount > 0
    
def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0