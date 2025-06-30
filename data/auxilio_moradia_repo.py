from typing import Optional
from data import auxilio_repo
from data.auxilio_moradia_model import AuxilioMoradia
from data.auxilio_moradia_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(auxilio_moradia: AuxilioMoradia) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        auxilio = AuxilioMoradia(
            id_auxilio=0,
            id_edital=auxilio_moradia.id_edital,
            id_inscricao=auxilio_moradia.id_inscricao,
            descricao=auxilio_moradia.descricao,
            valor_mensal=auxilio_moradia.valor_mensal,
            data_inicio=auxilio_moradia.data_inicio,
            data_fim=auxilio_moradia.data_fim,
            tipo_auxilio=auxilio_moradia.tipo_auxilio,
            url_comp_residencia_fixa="",
            url_comp_residencia_alugada="",
            url_contrato_aluguel_cid_campus="",
            url_contrato_aluguel_cid_natal=""
        )
        id_auxilio = auxilio_repo.inserir(auxilio, cursor)
        cursor.execute(INSERIR, (
            id_auxilio,
            auxilio_moradia.url_comp_residencia_fixa,
            auxilio_moradia.url_comp_residencia_alugada,
            auxilio_moradia.url_contrato_aluguel_cid_campus,
            auxilio_moradia.url_contrato_aluguel_cid_natal
        ))
        return id_auxilio

def obter_todos() -> list[AuxilioMoradia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            AuxilioMoradia(
                id_auxilio=row["id_auxilio"],
                id_edital=row["id_edital"],
                id_inscricao=row["id_inscricao"],
                descricao=row["descricao"],
                valor_mensal=row["valor_mensal"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                tipo_auxilio=row["tipo_auxilio"],
                url_comp_residencia_fixa=row["url_comp_residencia_fixa"],
                url_comp_residencia_alugada=row["url_comp_residencia_alugada"],
                url_contrato_aluguel_cid_campus=row["url_contrato_aluguel_cid_campus"],
                url_contrato_aluguel_cid_natal=row["url_contrato_aluguel_cid_natal"],
                id_auxilio= row["id_auxilio_moradia"]
            )
            for row in rows
        ]
        return auxilios

def obter_por_id(id: int) -> Optional[AuxilioMoradia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        auxilio = AuxilioMoradia(
            id_auxilio=row["id_auxilio"],
            id_edital=row["id_edital"],
            id_inscricao=row["id_inscricao"],
            descricao=row["descricao"],
            valor_mensal=row["valor_mensal"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"],
            tipo_auxilio=row["tipo_auxilio"],
            url_comp_residencia_fixa=row["url_comp_residencia_fixa"],
            url_comp_residencia_alugada=row["url_comp_residencia_alugada"],
            url_contrato_aluguel_cid_campus=row["url_contrato_aluguel_cid_campus"],
            url_contrato_aluguel_cid_natal=row["url_contrato_aluguel_cid_natal"],
            id_auxilio=row["id_auxilio_moradia"]
        )
        return auxilio

def atualizar(auxilio_moradia: AuxilioMoradia) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        auxilio = AuxilioMoradia(
            id_auxilio=auxilio_moradia.id_auxilio,
            id_edital=auxilio_moradia.id_edital,
            id_inscricao=auxilio_moradia.id_inscricao,
            descricao=auxilio_moradia.descricao,
            valor_mensal=auxilio_moradia.valor_mensal,
            data_inicio=auxilio_moradia.data_inicio,
            data_fim=auxilio_moradia.data_fim,
            tipo_auxilio=auxilio_moradia.tipo_auxilio,
            url_comp_residencia_fixa="",
            url_comp_residencia_alugada="",
            url_contrato_aluguel_cid_campus="",
            url_contrato_aluguel_cid_natal=""
        )
        auxilio_repo.atualizar(auxilio, cursor)
        cursor.execute(ATUALIZAR, (
            auxilio_moradia.url_comp_residencia_fixa,
            auxilio_moradia.url_comp_residencia_alugada,
            auxilio_moradia.url_contrato_aluguel_cid_campus,
            auxilio_moradia.url_contrato_aluguel_cid_natal,
            auxilio_moradia.id_auxilio
        ))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        auxilio_repo.excluir(id, cursor)
        return cursor.rowcount > 0
