from typing import Optional
from data.administrador_model import Administrador
from data.administrador_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(administrador: Administrador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            administrador.id_usuario, 
            administrador.matricula))
        return cursor.lastrowid

def obter_todos() -> list[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        administradores = [
            Administrador(
                id_usuario=row["id_usuario"], 
                matricula=row["matricula"])
            for row in rows]
        return administradores

def obter_por_id(id: int) -> Optional[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        administrador = Administrador(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"])
        return administrador