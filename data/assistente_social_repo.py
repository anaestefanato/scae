from typing import Optional
from data.assistente_social_model import AssistenteSocial
from data.assistente_social_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(assistenteSocial: AssistenteSocial) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            assistenteSocial.id_usuario, 
            assistenteSocial.matricula))
        return cursor.lastrowid

def obter_todos() -> list[AssistenteSocial]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        assistentes = [
            AssistenteSocial(
                id_usuario=row["id_usuario"], 
                matricula=row["matricula"])
            for row in rows]
        return assistentes

def obter_por_id(self, id: int) -> Optional[AssistenteSocial]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return AssistenteSocial(**row)
        return None
    
def atualizar(self, assistenteSocial: AssistenteSocial) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            assistenteSocial.matricula, 
            assistenteSocial.id_usuario))
        return cursor.rowcount > 0
    
def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0