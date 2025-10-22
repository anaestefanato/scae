from typing import Optional
from model.edital_model import Edital
from sql.edital_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print("Erro ao criar tabela aluno:", e)
        return False

def inserir(edital: Edital) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            edital.id_edital,
            edital.titulo,
            edital.descricao,
            edital.data_publicacao,
            edital.arquivo,
            edital.status,
            edital.data_inicio_inscricao,
            edital.data_fim_inscricao,
            edital.data_inicio_vigencia,
            edital.data_fim_vigencia))
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
                arquivo=row["arquivo"],
                status=row["status"],
                data_inicio_inscricao=row["data_inicio_inscricao"],
                data_fim_inscricao=row["data_fim_inscricao"],
                data_inicio_vigencia=row["data_inicio_vigencia"],
                data_fim_vigencia=row["data_fim_vigencia"])
            for row in rows]
        return editais

def obter_por_id(id: int) -> Optional[Edital]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None  # Não encontrou o edital
        edital = Edital(
            id_edital=row["id_edital"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            data_publicacao=row["data_publicacao"],
            arquivo=row["arquivo"],
            status=row["status"],
            data_inicio_inscricao=row["data_inicio_inscricao"],
            data_fim_inscricao=row["data_fim_inscricao"],
            data_inicio_vigencia=row["data_inicio_vigencia"],
            data_fim_vigencia=row["data_fim_vigencia"]
        )
        return edital

def atualizar(edital: Edital) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            edital.titulo,
            edital.descricao,
            edital.arquivo,
            edital.status,
            edital.data_inicio_inscricao,
            edital.data_fim_inscricao,
            edital.data_inicio_vigencia,
            edital.data_fim_vigencia,
            edital.id_edital
        ))
        conn.commit()
        return cursor.rowcount > 0


def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)

def obter_editais_abertos() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_EDITAIS_ABERTOS)
        rows = cursor.fetchall()
        editais = []
        for row in rows:
            edital = {
                'id_edital': row["id_edital"],
                'titulo': row["titulo"],
                'descricao': row["descricao"],
                'data_publicacao': row["data_publicacao"],
                'arquivo': row["arquivo"],
                'status': row["status"],
                'data_inicio_inscricao': row["data_inicio_inscricao"],
                'data_fim_inscricao': row["data_fim_inscricao"],
                'data_inicio_vigencia': row["data_inicio_vigencia"],
                'data_fim_vigencia': row["data_fim_vigencia"],
                'valor_medio': row["valor_medio"] or 0.0
            }
            editais.append(edital)
        return editais

def obter_editais_visiveis_alunos() -> list[Edital]:
    """
    Retorna apenas editais que devem ser visíveis para alunos.
    Critérios: status ativo e data de publicação <= data atual
    """
    from datetime import date
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_EDITAIS_VISIVEIS_ALUNOS, (date.today().strftime('%Y-%m-%d'),))
        rows = cursor.fetchall()
        editais = [
            Edital(
                id_edital=row["id_edital"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_publicacao=row["data_publicacao"],
                arquivo=row["arquivo"],
                status=row["status"],
                data_inicio_inscricao=row["data_inicio_inscricao"],
                data_fim_inscricao=row["data_fim_inscricao"],
                data_inicio_vigencia=row["data_inicio_vigencia"],
                data_fim_vigencia=row["data_fim_vigencia"])
            for row in rows]
        return editais