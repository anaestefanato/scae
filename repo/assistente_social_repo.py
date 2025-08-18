from typing import Optional
from repo import usuario_repo
from model.assistente_social_model import AssistenteSocial
from sql.assistente_social_sql import *
from model.usuario_model import Usuario
from sql.util import get_connection

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

def inserir(assistenteSocial: AssistenteSocial) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            0,
            assistenteSocial.nome,
            assistenteSocial.email,
            assistenteSocial.senha,
            assistenteSocial.tipo_usuario
        )
        id_usuario = usuario_repo.inserir(usuario)
        if not id_usuario:
            return None
        cursor.execute(INSERIR, (
            id_usuario,  # usa o id retornado da inserção do usuário
            assistenteSocial.matricula
        ))
        conn.commit()
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
                tipo_usuario=row["tipo_usuario"],
                matricula=row["matricula"])
            for row in rows]
        return assistentes

def obter_por_id( id: int) -> Optional[AssistenteSocial]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        assistentes = AssistenteSocial(
            id_usuario=row["id_usuario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            tipo_usuario=row["tipo_usuario"],
            matricula=row["matricula"])
        return assistentes
    
def atualizar(assistenteSocial: AssistenteSocial) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(assistenteSocial.id_usuario,
                assistenteSocial.nome, 
                assistenteSocial.email, 
                assistenteSocial.senha, 
                assistenteSocial.tipo_usuario)
        usuario_repo.atualizar(usuario)
        cursor.execute(ATUALIZAR, (
            assistenteSocial.matricula,  # usa o id do usuário já existente
            assistenteSocial.id_usuario))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)