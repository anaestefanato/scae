from typing import Optional, List
from data.notificacao_model import Notificacao
from data.notificacao_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True  # criação não retorna rowcount confiável

def inserir(notificacao: Notificacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            notificacao.id_usuario_destinatario,
            notificacao.titulo,
            notificacao.data_envio,
            notificacao.tipo
        ))
        return cursor.lastrowid

def obter_por_pagina(pagina: int, limit: int) -> List[Notificacao]:
    offset = (pagina - 1) * limit
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limit, offset))
        rows = cursor.fetchall()
        notificacoes = []
        for row in rows:
            notificacao = Notificacao(
                id_notificacao=row["id_notificacao"],
                id_usuario_destinatario=row["id_usuario_destinatario"],
                titulo=row["titulo"],
                data_envio=row["data_envio"],
                tipo=row["tipo"]
            )
            notificacoes.append(notificacao)
        return notificacoes

def obter_por_id(id_notificacao: int) -> Optional[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_notificacao,))
        row = cursor.fetchone()
        if row is None:
            return None
        notificacao = Notificacao(
            id_notificacao=row["id_notificacao"],
            id_usuario_destinatario=row["id_usuario_destinatario"],
            titulo=row["titulo"],
            data_envio=row["data_envio"],
            tipo=row["tipo"]
        )
        return notificacao

def atualizar(notificacao: Notificacao) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            notificacao.titulo,
            notificacao.tipo,
            notificacao.id_notificacao
        ))
        return cursor.rowcount > 0

def excluir(id_notificacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_notificacao,))
        return cursor.rowcount > 0
