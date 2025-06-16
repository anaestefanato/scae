from typing import Optional
from data.auxilio_moradia_model import AuxilioMoradia
from data.auxilio_moradia_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(auxilioMoradia: AuxilioMoradia) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            auxilioMoradia.id_auxilio_moradia,
            auxilioMoradia.urlCompResidenciaAlugada,
            auxilioMoradia.urlComprovanteResidenciaFixa,
            auxilioMoradia.urlContratoAluguelCidCampus,
            auxilioMoradia.urlContratoAluguelCidNatal))
        return cursor.lastrowid

def obter_todos() -> list[AuxilioMoradia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            AuxilioMoradia(id_auxilio_moradia=row["id_auxilio_moradia"],
                           urlCompResidenciaAlugada=row["urlCompResidenciaAlugada"],
                           urlComprovanteResidenciaFixa=row["urlComprovanteResidenciaFixa"],
                           urlContratoAluguelCidCampus=row["urlContratoAluguelCidCampus"],
                           urlContratoAluguelCidNatal=row["urlContratoAluguelCidNatal"])
            for row in rows]
        return auxilios

def obter_por_id(self, id: int) -> Optional[AuxilioMoradia]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return AuxilioMoradia(**row)
        return None
    
def atualizar(self, auxilioMoradia: AuxilioMoradia) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            auxilioMoradia.urlCompResidenciaAlugada,
            auxilioMoradia.urlComprovanteResidenciaFixa,
            auxilioMoradia.urlContratoAluguelCidCampus,
            auxilioMoradia.urlContratoAluguelCidNatal))
        return cursor.rowcount > 0
    
def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0