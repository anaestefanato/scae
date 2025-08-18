from typing import Optional, List
from repo import auxilio_repo
from model.auxilio_model import Auxilio
from model.auxilio_moradia_model import AuxilioMoradia
from sql.auxilio_moradia_sql import *
from sql.util import get_connection

class AuxilioMoradiaRepo:

    @staticmethod
    def criar_tabela() -> bool:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(CRIAR_TABELA)
            return True
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")
            return False

    @staticmethod
    def inserir(auxilioMoradia: AuxilioMoradia) -> Optional[int]:
        with get_connection() as conn:
            cursor = conn.cursor()
            auxilio = Auxilio(
                id_auxilio=0,
                id_edital=auxilioMoradia.id_edital,
                id_inscricao=auxilioMoradia.id_inscricao,
                descricao=auxilioMoradia.descricao,
                valor_mensal=auxilioMoradia.valor_mensal,
                data_inicio=auxilioMoradia.data_inicio,
                data_fim=auxilioMoradia.data_fim,
                tipo_auxilio=auxilioMoradia.tipo_auxilio
            )
            id_auxilio = auxilio_repo.inserir(auxilio)
            if id_auxilio is None:
                return None
            cursor.execute(INSERIR, (
                id_auxilio,
                auxilioMoradia.url_comp_residencia_fixa,
                auxilioMoradia.url_comp_residencia_alugada,
                auxilioMoradia.url_contrato_aluguel_cid_campus,
                auxilioMoradia.url_contrato_aluguel_cid_natal
            ))
            return id_auxilio

    @staticmethod
    def obter_todos() -> List[AuxilioMoradia]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            return [
                AuxilioMoradia(
                    id_auxilio=row["id_auxilio_moradia"],
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
                    url_contrato_aluguel_cid_natal=row["url_contrato_aluguel_cid_natal"]
                ) for row in rows
            ]

    @staticmethod
    def obter_por_id(id: int) -> Optional[AuxilioMoradia]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return AuxilioMoradia(
                id_auxilio=row["id_auxilio_moradia"],
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
                url_contrato_aluguel_cid_natal=row["url_contrato_aluguel_cid_natal"]
            )

    @staticmethod
    def atualizar(auxilioMoradia: AuxilioMoradia) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                auxilioMoradia.url_comp_residencia_fixa,
                auxilioMoradia.url_comp_residencia_alugada,
                auxilioMoradia.url_contrato_aluguel_cid_campus,
                auxilioMoradia.url_contrato_aluguel_cid_natal,
                auxilioMoradia.id_auxilio
            ))
            return cursor.rowcount > 0

    @staticmethod
    def excluir(id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM auxilio_moradia WHERE id_auxilio_moradia = ?", (id,))
            if cursor.rowcount == 0:
                return False
            cursor.execute("DELETE FROM auxilio WHERE id_auxilio = ?", (id,))
            conn.commit()
            return True
