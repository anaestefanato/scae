from typing import Optional
from repo import usuario_repo
from model.aluno_model import Aluno
from sql.aluno_sql import *
from model.usuario_model import Usuario
from util.db_util import get_connection

def criar_tabela() -> bool:
    usuario_repo.criar_tabela()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print("Erro ao criar tabela aluno:", e)
        return False
    
def inserir(aluno: Aluno) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        # Primeiro insere o usuário
        id_usuario = usuario_repo.inserir(Usuario(
            id_usuario=0,
            nome=aluno.nome,
            matricula=aluno.matricula,
            email=aluno.email,
            senha=aluno.senha
        ))
        # Depois insere na tabela aluno
        cursor.execute(INSERIR, (
            aluno.id_usuario if aluno.id_usuario else id_usuario,
            aluno.cpf ,
            aluno.rg,
            aluno.telefone,
            aluno.curso,
            aluno.data_nascimento,
            aluno.filiacao,
            aluno.endereco,
            aluno.nome_banco,
            aluno.agencia_bancaria,
            aluno.numero_conta_bancaria,
            aluno.renda_familiar
        ))
        return id_usuario
    
def obter_todos() -> list[Aluno]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        alunos = []
        for row in rows:
            aluno = Aluno(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                cpf=row["cpf"],
                rg=row["rg"],
                telefone=row["telefone"],
                curso=row["curso"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                endereco=row["endereco"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"]
            )
            alunos.append(aluno)
        return alunos
    
def obter_por_id(id: int) -> Optional[Aluno]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Aluno(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                cpf=row["cpf"],
                rg=row["rg"],
                telefone=row["telefone"],
                curso=row["curso"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                endereco=row["endereco"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"])
        return None


def obter_alunos_por_pagina(pagina: int, limite: int) -> list[Usuario]:
    offset = (pagina - 1) * limite
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        alunos = [
            Aluno(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                tipo_usuario=row["tipo_usuario"],
                cpf=row["cpf"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                endereco=row["endereco"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"])
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
        usuario_repo.atualizar(usuario)
        cursor.execute(ATUALIZAR, (
            aluno.cpf, 
            aluno.data_nascimento,
            aluno.filiacao,
            aluno.endereco,
            aluno.nome_banco,
            aluno.agencia_bancaria,
            aluno.numero_conta_bancaria,
            aluno.renda_familiar,
            aluno.quantidade_pessoas,
            aluno.id_usuario))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)
    
def possui_cadastro_completo(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(POSSUI_CADASTRO_COMPLETO, (id,))
        row = cursor.fetchone()
        if row:
            return bool(row["cadastro_completo"])
        return False
    
def marcar_cadastro_completo(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(MARCAR_CADASTRO_COMPLETO, (id,))
        return (cursor.rowcount > 0)