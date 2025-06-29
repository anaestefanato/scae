from typing import Optional
from data import usuario_repo
from data.aluno_model import Aluno
from data.aluno_sql import *
from data.usuario_model import Usuario
from data.util import get_connection

def criar_tabela() -> bool:
    usuario_repo.criar_tabela()  # <- garante que a tabela base exista primeiro
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    
def inserir(aluno: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0,
                aluno.nome,
                aluno.email,
                aluno.senha,
                aluno.tipo_usuario)
        id_usuario = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            aluno.id_usuario, 
            aluno.matricula))
        return id_usuario
    
def obter_todos() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        alunos = [
            Usuario(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                tipo_usuario=row["tipo"], 
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
    
def obter_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            aluno = Usuario(
                id_usuario=row["id_usuario"], 
                nome=row["nome"],
                email=row["email"], 
                senha=row["senha"],
                tipo_usuario=row["tipo"],
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

def obter_alunos_por_pagina(pagina: int, limite: int) -> list[Usuario]:
    offset = (pagina - 1) * limite
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        alunos = [
            Usuario(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                tipo_usuario=row["tipo"],
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

def atualizar(aluno: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(aluno.id_usuario,
                          aluno.nome, 
                          aluno.email, 
                          aluno.senha, 
                          aluno.tipo_usuario)
        usuario_repo.atualizar(usuario, cursor)
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
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)