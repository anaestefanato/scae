from typing import Optional
from data.auxilio_transporte_model import AuxilioTransporte
from data.auxilio_transporte_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(auxilioTransporte: AuxilioTransporte) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            auxilioTransporte.id_auxilio_transporte,
            auxilioTransporte.url_CompTransporte,
            auxilioTransporte.url_CompResidencia))
        return cursor.lastrowid

def obter_todos() -> list[AuxilioTransporte]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            AuxilioTransporte(
                id_auxilio_transporte=row["id_auxilio_transporte"],
                url_CompTransporte=row["url_CompTransporte"],   
                url_CompResidencia=row["url_CompResidencia"])
            for row in rows]
        return auxilios

def obter_por_id(self, id: int) -> Optional[AuxilioTransporte]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return AuxilioTransporte(**row)
        return None
    
def atualizar(self, auxilioTransporte: AuxilioTransporte) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            auxilioTransporte.id_auxilio_transporte,
            auxilioTransporte.url_CompTransporte,
            auxilioTransporte.url_CompResidencia))
        return cursor.rowcount > 0
    
def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0