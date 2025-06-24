from typing import Optional
from data.chamado_model import Chamado
from data.chamado_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(chamado: Chamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            chamado.id_duvida,
            chamado.id_usuario_criador,
            chamado.id_administrador_responsavel,
            chamado.titulo,
            chamado.descricao,
            chamado.data_criacao,
            chamado.status))
        return cursor.lastrowid

def obter_todos() -> list[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        chamados = [
            Chamado(
                id_duvida=row["id_duvida"],
                id_usuario_criador=row["id_usuario_criador"],
                id_administrador_responsavel=row["id_administrador_responsavel"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_criacao=row["data_criacao"],
                status=row["status"])
            for row in rows]
        return chamados

def obter_por_id(id: int) -> Optional[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        chamado = Chamado(
            id_duvida=row["id_duvida"],
            id_usuario_criador=row["id_usuario_criador"],
            id_administrador_responsavel=row["id_administrador_responsavel"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            data_criacao=row["data_criacao"],
            status=row["status"])
        return chamado

def atualizar(chamado: Chamado) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (chamado.titulo, chamado.descricao, chamado.status))
        return (cursor.rowcount > 0)

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)