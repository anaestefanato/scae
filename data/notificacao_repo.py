from typing import Optional
from data.notificacao_model import Notificacao
from data.notificacao_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(notificacao: Notificacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            notificacao.id_notificacao,
            notificacao.id_usuario_destinatario,
            notificacao.titulo,
            notificacao.dataEnvio,
            notificacao.tipo))
        return cursor.lastrowid

def obter_todos() -> list[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        notificacoes = [
            Notificacao(
                id_notificacao=row["id_notificacao"],
                id_usuario_destinatario=row["id_usuario_destinatario"],
                titulo=row["titulo"],
                dataEnvio=row["dataEnvio"],
                tipo=row["tipo"])
            for row in rows]
        return notificacoes

def obter_por_id(id: int) -> Optional[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            notificacao = Notificacao(
                id_notificacao=row["id_notificacao"],
                id_usuario_destinatario=row["id_usuario_destinatario"],
                titulo=row["titulo"],
                dataEnvio=row["dataEnvio"],
                tipo=row["tipo"])
            return notificacao
        return None

def atualizar(self, notificacao: Notificacao) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (notificacao.titulo, notificacao.tipo))
        return cursor.rowcount > 0

def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0
                