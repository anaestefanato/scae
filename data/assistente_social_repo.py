from typing import Optional
from data import usuario_repo
from data.assistente_social_model import AssistenteSocial
from data.assistente_social_sql import *
from data.usuario_model import Usuario
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(assistenteSocial: AssistenteSocial) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0,
                assistenteSocial.nome, 
                assistenteSocial.email, 
                assistenteSocial.senha, 
                assistenteSocial.tipo)
        id_usuario = usuario.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            assistenteSocial.id_usuario, 
            assistenteSocial.matricula))
        return id_usuario

def obter_todos() -> list[AssistenteSocial]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        assistentes = [
            AssistenteSocial(
                id_usuario=row["id_usuario"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                tipo=row["tipo"],
                matricula=row["matricula"])
            for row in rows]
        return assistentes

def obter_por_id( id: int) -> Optional[AssistenteSocial]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        assistentes = AssistenteSocial(
            id_usuario=row["id_usuario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            tipo=row["tipo"],
            matricula=row["matricula"])
        return assistentes
    
def atualizar(assistenteSocial: AssistenteSocial) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(assistenteSocial.id_usuario,
                assistenteSocial.nome, 
                assistenteSocial.email, 
                assistenteSocial.senha, 
                assistenteSocial.tipo)
        usuario.repo.atualizar(usuario, cursor)
        cursor.execute(ATUALIZAR, (
            assistenteSocial.matricula))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)