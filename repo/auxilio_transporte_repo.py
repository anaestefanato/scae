from typing import Optional, List
from repo import auxilio_repo
from model.auxilio_model import Auxilio
from model.auxilio_transporte_model import AuxilioTransporte
from data.auxilio_transporte_sql import *
from data.util import get_connection

class AuxilioTransporteRepo:

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
    def inserir(auxilioTransporte: AuxilioTransporte) -> Optional[int]:
        with get_connection() as conn:
            cursor = conn.cursor()
            auxilio = Auxilio(
                id_auxilio=0,
                id_edital=auxilioTransporte.id_edital,
                id_inscricao=auxilioTransporte.id_inscricao,
                descricao=auxilioTransporte.descricao,
                valor_mensal=auxilioTransporte.valor_mensal,
                data_inicio=auxilioTransporte.data_inicio,
                data_fim=auxilioTransporte.data_fim,
                tipo_auxilio=auxilioTransporte.tipo_auxilio
            )
            id_auxilio = auxilio_repo.inserir(auxilio)
            if id_auxilio is None:
                return None
            cursor.execute(INSERIR, (
                id_auxilio,
                auxilioTransporte.urlCompResidencia,
                auxilioTransporte.urlCompTransporte
            ))
            return id_auxilio

    @staticmethod
    def obter_todos() -> List[AuxilioTransporte]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            return [
                AuxilioTransporte(
                    id_auxilio=row["id_auxilio_transporte"],
                    id_edital=row["id_edital"],
                    id_inscricao=row["id_inscricao"],
                    descricao=row["descricao"],
                    valor_mensal=row["valor_mensal"],
                    data_inicio=row["data_inicio"],
                    data_fim=row["data_fim"],
                    tipo_auxilio=row["tipo_auxilio"],
                    urlCompResidencia=row["urlCompResidencia"],
                    urlCompTransporte=row["urlCompTransporte"]
                ) for row in rows
            ]

    @staticmethod
    def obter_por_id(id: int) -> Optional[AuxilioTransporte]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return AuxilioTransporte(
                id_auxilio=row["id_auxilio_transporte"],
                id_edital=row["id_edital"],
                id_inscricao=row["id_inscricao"],
                descricao=row["descricao"],
                valor_mensal=row["valor_mensal"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                tipo_auxilio=row["tipo_auxilio"],
                urlCompResidencia=row["urlCompResidencia"],
                urlCompTransporte=row["urlCompTransporte"]
            )

    @staticmethod
    def atualizar(auxilioTransporte: AuxilioTransporte) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                auxilioTransporte.urlCompResidencia,
                auxilioTransporte.urlCompTransporte,
                auxilioTransporte.id_auxilio
            ))
            return cursor.rowcount > 0

    @staticmethod
    def excluir(id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Primeiro exclui da tabela derivada
            cursor.execute("DELETE FROM auxilio_transporte WHERE id_auxilio_transporte = ?", (id,))
            if cursor.rowcount == 0:
                return False            
            # Agora exclui da tabela base
            cursor.execute("DELETE FROM auxilio WHERE id_auxilio = ?", (id,))           
            conn.commit()  # força commit para liberar lock
            return True
