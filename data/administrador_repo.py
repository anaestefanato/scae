from typing import Optional
from data import usuario_repo
from data.administrador_model import Administrador
from data.administrador_sql import *
from data.usuario_model import Usuario
from data.util import get_connection

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
            0,
            administrador.nome, 
            administrador.email, 
            administrador.senha, 
            administrador.tipo_usuario
        )
        id_usuario = usuario_repo.inserir(usuario)
        
        cursor.execute(INSERIR, (
            id_usuario,  
            administrador.matricula
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
                tipo_usuario=row["tipo"])
            for row in rows]
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
            email=row["email"],
            senha=row["senha"],
            tipo_usuario=row["tipo_usuario"],
            matricula=row["matricula"]
        )
    
def atualizar(administrador: Administrador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(administrador.id_usuario,
                          administrador.matricula)
        usuario.repo.atualizar(usuario, cursor)
        cursor.execute(ATUALIZAR, (
            administrador.matricula, 
            administrador.id_usuario))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)