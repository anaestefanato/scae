from typing import Optional
from data import usuario_repo
from data.administrador_model import Administrador
from data.administrador_sql import *
from data.usuario_model import Usuario
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

def obter_por_id(self, id: int) -> Optional[Administrador]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Administrador(**row)
        return None
    
def atualizar(self, administrador: Administrador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(administrador.id_usuario,
                          administrador.matricula)
        usuario.repo.atualizar(usuario, cursor)
        cursor.execute(ATUALIZAR, (
            administrador.matricula, 
            administrador.id_usuario))
        return (cursor.rowcount > 0)
    
def excluir(self, id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario_repo.excluir(id, cursor)
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)