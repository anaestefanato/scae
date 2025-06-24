from typing import Optional
from data import auxilio_repo
from data.auxilio_model import Auxilio
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
        auxilio = Auxilio(0,
            auxilioTransporte.id_edital,
            auxilioTransporte.id_inscricao,
            auxilioTransporte.descricao,
            auxilioTransporte.valor_mensal,
            auxilioTransporte.data_inicio,
            auxilioTransporte.data_fim,
            auxilioTransporte.tipo_auxilio)
        id_auxilio = auxilio.inserir(auxilio, cursor)
        cursor.execute(INSERIR, (
            auxilioTransporte.id_auxilio_transporte,
            auxilioTransporte.urlCompTransporte,
            auxilioTransporte.urlCompResidencia))
        return id_auxilio

def obter_todos() -> list[AuxilioTransporte]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            AuxilioTransporte(
                id_auxilio_transporte=row["id_auxilio_transporte"],
                id_edital=row["id_edital"],
                id_inscricao=row["id_inscricao"],
                descricao=row["descricao"],
                valor_mensal=row["valor_mensal"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                tipo_auxilio=row["tipo_auxilio"],
                url_CompTransporte=row["url_CompTransporte"],   
                url_CompResidencia=row["url_CompResidencia"])
            for row in rows]
        return auxilios

def obter_por_id(id: int) -> Optional[AuxilioTransporte]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        auxilio = AuxilioTransporte(
            id_auxilio_transporte=row["id_auxilio_transporte"],
            id_edital=row["id_edital"],
            id_inscricao=row["id_inscricao"],
            descricao=row["descricao"],
            valor_mensal=row["valor_mensal"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"],
            tipo_auxilio=row["tipo_auxilio"],
            url_CompTransporte=row["url_CompTransporte"],
            url_CompResidencia=row["url_CompResidencia"])
        return auxilio
    
def atualizar(auxilioTransporte: AuxilioTransporte) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        auxilio = AuxilioTransporte(auxilioTransporte.id_auxilio_transporte,
            auxilioTransporte.id_edital,
            auxilioTransporte.id_inscricao,
            auxilioTransporte.descricao,
            auxilioTransporte.valor_mensal,
            auxilioTransporte.data_inicio,
            auxilioTransporte.data_fim,
            auxilioTransporte.tipo_auxilio)
        auxilio.atualizar(auxilio, cursor)
        cursor.execute(ATUALIZAR, (
            auxilioTransporte.id_auxilio_transporte,
            auxilioTransporte.urlCompTransporte,
            auxilioTransporte.urlCompResidencia))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        auxilio_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)