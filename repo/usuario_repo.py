from typing import Any, Optional
from model.usuario_model import Usuario
from sql.usuario_sql import *
from util.db_util import get_connection

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
            usuario.matricula,
            usuario.email,
            usuario.senha,
            usuario.perfil))
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
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"])
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
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"])
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
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"])
            return usuario
        return None
    
def obter_todos_por_perfil(perfil: str) -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_POR_PERFIL, (perfil,))
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None)
            for row in rows]
        return usuarios
    

def obter_usuario_por_matricula(matricula: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_MATRICULA, (matricula,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None)
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
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None)
            return usuario
        return None

def atualizar_token(email: str, token: str, data_expiracao: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_TOKEN, (token, data_expiracao, email))
        return (cursor.rowcount > 0)

def atualizar_foto(id: int, caminho_foto: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return (cursor.rowcount > 0)

def obter_por_token(token: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_TOKEN, (token,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id_usuario=row["id_usuario"], 
                    nome=row["nome"],
                    matricula=row["matricula"],
                    email=row["email"],
                    senha=row["senha"],
                    perfil=row["perfil"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"])
            return usuario
        return None

def limpar_token(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET token_redefinicao=NULL, data_token=NULL WHERE id=?", (id,))
        return (cursor.rowcount > 0)

def atualizar(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (usuario.nome, usuario.email, usuario.matricula, usuario.id_usuario))
        return cursor.rowcount > 0

def atualizar_senha(id: int, senha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_SENHA, (senha, id))
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

def atualizar_foto(id: int, caminho_foto: str) -> bool:
    """Atualiza apenas a foto do usuário"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return cursor.rowcount > 0