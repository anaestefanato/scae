from typing import Optional
from repo import usuario_repo
from model.administrador_model import Administrador
from sql.administrador_sql import *
from model.usuario_model import Usuario
from util.db_util import get_connection

def criar_tabela() -> bool:
    usuario_repo.criar_tabela()  # <- garante que a tabela base exista primeiro
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

def inserir(administrador: Administrador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            id_usuario=0,
            nome=administrador.nome, 
            matricula=administrador.matricula,
            email=administrador.email, 
            senha=administrador.senha,
            perfil="admin",
            foto=administrador.foto,
            token_redefinicao=administrador.token_redefinicao,
            data_token=administrador.data_token,
            data_cadastro=administrador.data_cadastro
        )
        id_usuario = usuario_repo.inserir(usuario)
        
        cursor.execute(INSERIR, (
            id_usuario,  
            administrador.tipo_admin
        ))
        
        conn.commit()
        return id_usuario

def obter_todos() -> list[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        administradores = [
            Administrador(
                id_usuario=row["id_usuario"], 
                matricula=row["matricula"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"],
                tipo_admin=row["tipo_admin"]
            )
            for row in rows
        ]
        return administradores

def obter_por_id(id_usuario: int) -> Optional[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Administrador(
            id_usuario=row["id_usuario"],
            nome=row["nome"],
            matricula=row["matricula"],
            email=row["email"],
            senha=row["senha"],
            perfil=row["perfil"],
            foto=row["foto"],
            token_redefinicao=row["token_redefinicao"],
            data_token=row["data_token"],
            data_cadastro=row["data_cadastro"],
            tipo_admin=row["tipo_admin"]
        )
    
def atualizar(administrador: Administrador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            id_usuario=administrador.id_usuario, 
            nome=administrador.nome, 
            matricula=administrador.matricula,
            email=administrador.email, 
            senha=administrador.senha, 
            perfil=administrador.perfil,
            foto=administrador.foto,
            token_redefinicao=administrador.token_redefinicao,
            data_token=administrador.data_token,
            data_cadastro=administrador.data_cadastro
            )
        usuario_repo.atualizar(usuario)
        cursor.execute(ATUALIZAR, (
            administrador.tipo_admin, 
            administrador.id_usuario))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)