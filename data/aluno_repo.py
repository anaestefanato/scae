from typing import Optional
from data.aluno_model import Aluno
from data.aluno_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    
def inserir(aluno: Aluno) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            aluno.id_usuario, 
            aluno.matricula))
        return cursor.lastrowid
    
def obter_todos() -> list[Aluno]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        alunos = [
            Aluno(
                id_usuario=row["id_usuario"], 
                cpf=row["cpf"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                endereco=row["endereco"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                matricula=row["matricula"])
            for row in rows]
        return alunos
    
def obter_por_id(id: int) -> Optional[Aluno]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            aluno = Aluno(
                id_usuario=row["id_usuario"], 
                cpf=row["cpf"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                endereco=row["endereco"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                matricula=row["matricula"])
            return aluno(**row)
        return None
    
def atualizar(self, aluno: Aluno) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            aluno.cpf, 
            aluno.data_nascimento,
            aluno.filiacao,
            aluno.endereco,
            aluno.nome_banco,
            aluno.agencia_bancaria,
            aluno.numero_conta_bancaria,
            aluno.renda_familiar,
            aluno.matricula, 
            aluno.id_usuario))
        return cursor.rowcount > 0
    
def excluir(self, id: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0