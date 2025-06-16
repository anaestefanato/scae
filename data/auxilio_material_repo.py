from typing import Optional
from data.auxilio_material_model import AuxilioMaterial
from data.auxilio_material_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(auxilioMaterial: AuxilioMaterial) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (auxilioMaterial.id_auxilio_alimentacao,))
        return cursor.lastrowid

def obter_todos() -> list[AuxilioMaterial]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            AuxilioMaterial(id_auxilio_material=row["id_auxilio_material"])
            for row in rows]
        return auxilios

def obter_por_id(self, id: int) -> Optional[AuxilioMaterial]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return AuxilioMaterial(**row)
        return None
    
def atualizar(self, auxilioMaterial: AuxilioMaterial) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            auxilioMaterial.id_auxilio_material,))
        return cursor.rowcount > 0
    
def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0