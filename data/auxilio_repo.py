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
            auxilio.id_auxilio,
            auxilio.tipo_auxilio,
            auxilio.descricao,
            auxilio.valor_mensal,
            auxilio.data_inicio,
            auxilio.data_fim))
        return cursor.lastrowid
    
def obter_todos() -> list[Auxilio]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            Auxilio(id_auxilio=row["id_auxilio"],
                   tipo_auxilio=row["tipo_auxilio"],
                   descricao=row["descricao"],
                   valor=row["valor"],
                   data_inicio=row["data_inicio"],
                   data_fim=row["data_fim"])
            for row in rows]
        return auxilios

def obter_por_id(id: int) -> Optional[Auxilio]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        auxilio = Auxilio(
            id_auxilio=row["id_auxilio"],
            tipo_auxilio=row["tipo_auxilio"],
            descricao=row["descricao"],
            valor=row["valor_mensal"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"])
        return auxilio  
        
    
def atualizar(auxilio: Auxilio) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            auxilio.tipo_auxilio,
            auxilio.descricao,
            auxilio.valor_mensal,
            auxilio.data_fim))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)