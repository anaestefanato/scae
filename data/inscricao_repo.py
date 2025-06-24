from typing import Optional
from data.inscricao_model import Inscricao
from data.inscricao_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(inscricao: Inscricao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            inscricao.id_inscricao,
            inscricao.id_aluno,
            inscricao.id_edital,
            inscricao.data_inscricao,
            inscricao.status,
            inscricao.url_Documento_Identificacao,
            inscricao.urlDeclaracaoRenda,
            inscricao.url_Termo_Responsabilidade))
        return cursor.lastrowid

def obter_todos() -> list[Inscricao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        inscricoes = [
            Inscricao(
                id_inscricao=row["id_inscricao"],
                id_aluno=row["id_aluno"],
                id_edital=row["id_edital"],
                data_inscricao=row["data_inscricao"],
                status=row["status"],
                url_Documento_Identificacao=row["url_Documento_Identificacao"],
                urlDeclaracaoRenda=row["urlDeclaracaoRenda"],
                url_Termo_Responsabilidade=row["url_Termo_Responsabilidade"])
            for row in rows]
        return inscricoes

def obter_por_id(id: int) -> Optional[Inscricao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        inscricao = Inscricao(
            id_inscricao=row["id_inscricao"],
            id_aluno=row["id_aluno"],
            id_edital=row["id_edital"],
            data_inscricao=row["data_inscricao"],
            status=row["status"],
            url_Documento_Identificacao=row["url_Documento_Identificacao"],
            urlDeclaracaoRenda=row["urlDeclaracaoRenda"],
            url_Termo_Responsabilidade=row["url_Termo_Responsabilidade"])
        return inscricao

def atualizar(inscricao: Inscricao) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (inscricao.status, inscricao.url_Documento_Identificacao, inscricao.urlDeclaracaoRenda, inscricao.url_Termo_Responsabilidade))
        return (cursor.rowcount > 0)

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)