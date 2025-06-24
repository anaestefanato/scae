from typing import Optional
from data.usuario_model import Usuario
from data.usuario_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            usuario.id_usuario,
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.tipo_usuario,))
        return cursor.lastrowid

def obter_todos() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                tipo_usuario=row["tipo_usuario"])
            for row in rows]
        return usuarios

def obter_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        usuario = Usuario(
            id_usuario=row["id_usuario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            tipo_usuario=row["tipo_usuario"])
        return usuario

def atualizar(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (usuario.nome, usuario.email, usuario.senha, usuario.tipo_usuario))
        return cursor.rowcount > 0

def atualizar_senha(id: int, nova_senha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_SENHA, (nova_senha, id))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)