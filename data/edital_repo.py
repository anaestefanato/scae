from typing import Optional
from data.edital_model import Edital
from data.edital_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(edital: Edital) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            edital.id_edital,
            edital.titulo,
            edital.descricao,
            edital.data_publicacao,
            edital.data_encerramento,
            edital.arquivo,
            edital.status))
        return cursor.lastrowid

def obter_todos() -> list[Edital]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        editais = [
            Edital(
                id_edital=row["id_edital"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_publicacao=row["data_publicacao"],
                data_encerramento=row["data_encerramento"],
                arquivo=row["arquivo"],
                status=row["status"])
            for row in rows]
        return editais

def obter_por_id(id: int) -> Optional[Edital]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        edital = Edital(
            id_edital=row["id_edital"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            data_publicacao=row["data_publicacao"],
            data_encerramento=row["data_encerramento"],
            arquivo=row["arquivo"],
            status=row["status"])
        return edital

def atualizar(edital: Edital) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (edital.titulo, edital.descricao, edital.data_encerramento, edital.arquivo, edital.status))
        return (cursor.rowcount > 0)

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)