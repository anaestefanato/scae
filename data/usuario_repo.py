from typing import Any, Optional
from data.usuario_model import Usuario
from data.usuario_sql import *
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
    
def inserir(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.tipo_usuario))
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
    
def obter_usuarios_por_pagina(pagina: int, limite: int) -> list[Usuario]:
    offset = (pagina - 1) * limite
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS + " LIMIT ? OFFSET ?", (limite, offset))
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
        if row:
            usuario = Usuario(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                tipo_usuario=row["tipo_usuario"])
            return usuario
        return None
    
def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                tipo_usuario=row["tipo_usuario"])
            return usuario
        return None

def atualizar(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (usuario.nome, usuario.email, usuario.tipo_usuario, usuario.id_usuario))
        return cursor.rowcount > 0

def atualizar_senha(id: int, senha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_SENHA, (senha, id))
        return cursor.rowcount > 0

def atualizar_tipo_usuario(id: int, tipo_usuario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_TIPO_USUARIO, (tipo_usuario, id))
        return cursor.rowcount > 0

def excluir(id: int, cursor=None) -> bool:
    if cursor is None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(EXCLUIR, (id,))
            return cursor.rowcount > 0
    else:
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0