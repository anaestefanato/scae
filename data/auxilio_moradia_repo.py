from typing import Optional
from data import auxilio_repo
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
        auxilio = AuxilioMoradia(0,
            auxilioMoradia.id_edital,
            auxilioMoradia.id_inscricao,
            auxilioMoradia.descricao,
            auxilioMoradia.valor_mensal,
            auxilioMoradia.data_inicio,
            auxilioMoradia.data_fim,
            auxilioMoradia.tipo_auxilio)
        id_auxilio = auxilio_repo.inserir(auxilio, cursor)
        cursor.execute(INSERIR, (
            auxilioMoradia.id_auxilio_moradia,
            auxilioMoradia.urlCompResidenciaAlugada,
            auxilioMoradia.urlCompResidenciaFixa,
            auxilioMoradia.urlContratoAluguelCidCampus,
            auxilioMoradia.urlContratoAluguelCidNatal))
        return id_auxilio

def obter_todos() -> list[AuxilioMoradia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            AuxilioMoradia(id_auxilio_moradia=row["id_auxilio_moradia"],
                        id_auxilio=row["id_auxilio"],
                        id_edital=row["id_edital"],
                        id_inscricao=row["id_inscricao"],
                        descricao=row["descricao"],
                        valor_mensal=row["valor_mensal"],
                        data_inicio=row["data_inicio"],
                        data_fim=row["data_fim"],
                        tipo_auxilio=row["tipo_auxilio"],
                        urlCompResidenciaAlugada=row["urlCompResidenciaAlugada"],
                        urlComprovanteResidenciaFixa=row["urlCompResidenciaFixa"],
                        urlContratoAluguelCidCampus=row["urlContratoAluguelCidCampus"],
                        urlContratoAluguelCidNatal=row["urlContratoAluguelCidNatal"])
            for row in rows]
        return auxilios

def obter_por_id(id: int) -> Optional[AuxilioMoradia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        auxilio = AuxilioMoradia(
            id_auxilio_moradia=row["id_auxilio_moradia"],
            id_auxilio=row["id_auxilio"],
            id_edital=row["id_edital"],
            id_inscricao=row["id_inscricao"],
            descricao=row["descricao"],
            valor_mensal=row["valor_mensal"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"],
            tipo_auxilio=row["tipo_auxilio"],
            urlCompResidenciaAlugada=row["urlCompResidenciaAlugada"],
            urlComprovanteResidenciaFixa=row["urlCompResidenciaFixa"],
            urlContratoAluguelCidCampus=row["urlContratoAluguelCidCampus"],
            urlContratoAluguelCidNatal=row["urlContratoAluguelCidNatal"])
        return auxilio
    
def atualizar(auxilioMoradia: AuxilioMoradia) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        auxilio = AuxilioMoradia(auxilioMoradia.id_auxilio_moradia,
            auxilioMoradia.id_edital,
            auxilioMoradia.id_inscricao,
            auxilioMoradia.descricao,
            auxilioMoradia.valor_mensal,
            auxilioMoradia.data_inicio,
            auxilioMoradia.data_fim,
            auxilioMoradia.tipo_auxilio)
        auxilio_repo.atualizar(auxilio, cursor)
        cursor.execute(ATUALIZAR, (
            auxilioMoradia.urlCompResidenciaAlugada,
            auxilioMoradia.urlCompResidenciaFixa,
            auxilioMoradia.urlContratoAluguelCidCampus,
            auxilioMoradia.urlContratoAluguelCidNatal))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        auxilio_repo.excluir(id, cursor)
        return cursor.rowcount > 0