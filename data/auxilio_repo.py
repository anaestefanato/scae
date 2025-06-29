from typing import Optional
from data.auxilio_model import Auxilio
from data.auxilio_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

def inserir(auxilio: Auxilio) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            auxilio.id_edital,
            auxilio.id_inscricao,
            auxilio.descricao,
            auxilio.valor_mensal,
            auxilio.data_inicio,
            auxilio.data_fim,
            auxilio.tipo_auxilio
        ))
        return cursor.lastrowid

    
def obter_todos() -> list[Auxilio]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            Auxilio(id_auxilio=row["id_auxilio"],
                   id_edital=row["id_edital"],
                   id_inscricao=row["id_inscricao"],    
                   tipo_auxilio=row["tipo_auxilio"],
                   descricao=row["descricao"],
                   valor_mensal=row["valor_mensal"],
                   data_inicio=row["data_inicio"],
                   data_fim=row["data_fim"])
            for row in rows]
        return auxilios

def obter_por_id(id: int) -> Optional[Auxilio]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        auxilio = Auxilio(
            id_auxilio=row["id_auxilio"],
            id_edital=row["id_edital"],
            id_inscricao=row["id_inscricao"],
            tipo_auxilio=row["tipo_auxilio"],
            descricao=row["descricao"],
            valor_mensal=row["valor_mensal"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"])
        return auxilio  
        
    
def atualizar(auxilio: Auxilio) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            auxilio.descricao,
            auxilio.valor_mensal,
            auxilio.data_fim,
            auxilio.tipo_auxilio,
            auxilio.id_auxilio
        ))
        return cursor.rowcount > 0
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)