from typing import Optional
from data.resposta_chamado_model import RespostaChamado
from data.resposta_chamado_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(resposta: RespostaChamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            resposta.id_resposta_chamado,
            resposta.id_chamado,
            resposta.id_usuario_autor,
            resposta.mensagem,
            resposta.data_resposta))
        return cursor.lastrowid

def obter_todos() -> list[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        respostas = [
            RespostaChamado(
                id_resposta_chamado=row["id_resposta_chamado"],
                id_chamado=row["id_chamado"],
                id_usuario_autor=row["id_usuario_autor"],
                mensagem=row["mensagem"],
                data_resposta=row["data_resposta"])
            for row in rows]
        return respostas

def obter_por_id(id: int) -> Optional[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        resposta = RespostaChamado(
            id_resposta_chamado=row["id_resposta_chamado"],
            id_chamado=row["id_chamado"],
            id_usuario_autor=row["id_usuario_autor"],
            mensagem=row["mensagem"],
            data_resposta=row["data_resposta"])
        return resposta

def atualizar(resposta: RespostaChamado) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (resposta.mensagem,))
        return (cursor.rowcount > 0)

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)