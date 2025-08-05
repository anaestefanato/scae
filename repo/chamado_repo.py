from typing import Optional, List
from model.chamado_model import Chamado
from data.chamado_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela recurso: {e}")
        return False
    
def inserir(chamado: Chamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            chamado.id_usuario_criador,
            chamado.id_administrador_responsavel,
            chamado.titulo,
            chamado.descricao,
            chamado.data_criacao,
            chamado.status
        ))
        return cursor.lastrowid

def obter_por_id(id: int) -> Optional[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Chamado(
                id_chamado=row["id_chamado"],
                id_usuario_criador=row["id_usuario_criador"],
                id_administrador_responsavel=row["id_administrador_responsavel"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_criacao=row["data_criacao"],
                status=row["status"]
            )
        return None

def obter_por_pagina(pagina: int, limit: int) -> List[Chamado]:
    offset = (pagina - 1) * limit
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limit, offset))
        rows = cursor.fetchall()
        return [
            Chamado(
                id_chamado=row["id_chamado"],
                id_usuario_criador=row["id_usuario_criador"],
                id_administrador_responsavel=row["id_administrador_responsavel"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_criacao=row["data_criacao"],
                status=row["status"]
            )
            for row in rows
        ]

def atualizar(chamado: Chamado) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            chamado.titulo,
            chamado.descricao,
            chamado.status,
            chamado.id_chamado
        ))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0
