from typing import Optional
from model.resposta_chamado_model import RespostaChamado
from sql.resposta_chamado_sql import *
from sql.util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela resposta chamado: {e}")
        return False

def inserir(resposta: RespostaChamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            resposta.id_chamado,
            resposta.id_usuario,
            resposta.mensagem,
            resposta.data_resposta))
        return cursor.lastrowid

def obter_por_pagina(pagina: int, limit: int) -> list[RespostaChamado]:
    offset = (pagina - 1) * limit
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limit, offset))
        rows = cursor.fetchall()
        respostas = []
        for row in rows:
            resposta = RespostaChamado(
                id_resposta=row["id_resposta_chamado"],
                id_chamado=row["id_chamado"],
                id_usuario=row["id_usuario_autor"],
                mensagem=row["mensagem"],
                data_resposta=row["data_resposta"],
                status=""
            )
            respostas.append(resposta)
        return respostas

def obter_por_id(id: int) -> Optional[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return RespostaChamado(
                id_resposta=row["id_resposta_chamado"],
                id_chamado=row["id_chamado"],
                id_usuario=row["id_usuario_autor"],
                mensagem=row["mensagem"],
                data_resposta=row["data_resposta"],
                status=""
            )
        return None

def atualizar(resposta: RespostaChamado) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (resposta.mensagem, resposta.id_resposta))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0