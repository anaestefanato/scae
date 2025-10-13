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
    
def inserir(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        # Primeiro insere o usuário
        id_usuario = usuario_repo.inserir(usuario)
        return id_usuario
    
def completar_cadastro(aluno: Aluno) -> Optional[bool]:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verificar se já existe um registro para este usuário
        cursor.execute("SELECT aprovado FROM aluno WHERE id_usuario = ?", (aluno.id_usuario,))
        registro_existente = cursor.fetchone()
        
        if registro_existente:
            # Se já existe, fazer UPDATE preservando o status de aprovação
            cursor.execute("""
                UPDATE aluno SET 
                    cpf = ?, telefone = ?, curso = ?, data_nascimento = ?, filiacao = ?, 
                    cep = ?, cidade = ?, bairro = ?, rua = ?, numero = ?, estado = ?, 
                    complemento = ?, nome_banco = ?, agencia_bancaria = ?, numero_conta_bancaria = ?, 
                    renda_familiar = ?, quantidade_pessoas = ?, renda_per_capita = ?, situacao_moradia = ?,
                    ano_ingresso = ?, ano_conclusao_previsto = ?, bolsa_pesquisa = ?, cad_unico = ?, bolsa_familia = ?
                WHERE id_usuario = ?
            """, (
                aluno.cpf, aluno.telefone, aluno.curso, aluno.data_nascimento, aluno.filiacao,
                aluno.cep, aluno.cidade, aluno.bairro, aluno.rua, aluno.numero, aluno.estado,
                aluno.complemento, aluno.nome_banco, aluno.agencia_bancaria, aluno.numero_conta_bancaria,
                aluno.renda_familiar, aluno.quantidade_pessoas, aluno.renda_per_capita, aluno.situacao_moradia,
                aluno.ano_ingresso, aluno.ano_conclusao_previsto, aluno.bolsa_pesquisa, aluno.cad_unico, aluno.bolsa_familia,
                aluno.id_usuario
            ))
        else:
            # Se não existe, inserir como aprovado (aprovado = 1)
            cursor.execute("""
                INSERT INTO aluno (id_usuario, cpf, telefone, curso, data_nascimento, filiacao, 
                                 cep, cidade, bairro, rua, numero, estado, complemento, 
                                 nome_banco, agencia_bancaria, numero_conta_bancaria, 
                                 renda_familiar, quantidade_pessoas, renda_per_capita, 
                                 situacao_moradia, aprovado, ano_ingresso, ano_conclusao_previsto, 
                                 bolsa_pesquisa, cad_unico, bolsa_familia) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?)
            """, (
                aluno.id_usuario, aluno.cpf, aluno.telefone, aluno.curso, aluno.data_nascimento, aluno.filiacao,
                aluno.cep, aluno.cidade, aluno.bairro, aluno.rua, aluno.numero, aluno.estado,
                aluno.complemento, aluno.nome_banco, aluno.agencia_bancaria, aluno.numero_conta_bancaria,
                aluno.renda_familiar, aluno.quantidade_pessoas, aluno.renda_per_capita, aluno.situacao_moradia,
                aluno.ano_ingresso, aluno.ano_conclusao_previsto, aluno.bolsa_pesquisa, aluno.cad_unico, aluno.bolsa_familia
            ))
        
        return cursor.rowcount > 0
    
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
                telefone=row["telefone"],
                curso=row["curso"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                cep=row["cep"],
                cidade=row["cidade"],
                bairro=row["bairro"],
                rua=row["rua"],
                numero=row["numero"],
                estado=row["estado"],
                complemento=row["complemento"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"],
                renda_per_capita=row["renda_per_capita"],
                situacao_moradia=row["situacao_moradia"],
                perfil="aluno",
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )
            alunos.append(aluno)
        return alunos

def obter_alunos_aprovados() -> list[dict]:
    """Obtém apenas alunos que foram aprovados (não pendentes) com informações organizadas para a interface"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_ALUNOS_APROVADOS)
            resultado = cursor.fetchall()
            
        alunos = []
        
        for row in resultado:
            auxilios_str = row[6] if row[6] else ""
            auxilios = auxilios_str.split(',') if auxilios_str else []
            
            aluno = {
                'id_usuario': row[0],
                'nome': row[1] or 'Nome não informado',
                'matricula': row[2] or 'Matrícula não informada',
                'email': row[3] or 'Email não informado',
                'curso': row[4] or 'Curso não informado',
                'situacao': row[5] or 'Inativo',
                'auxilios': auxilios,
                'valor_mensal': float(row[7]) if row[7] else 0.0
            }
            alunos.append(aluno)
            
        return alunos
        
    except Exception as e:
        print(f"Erro ao obter alunos aprovados: {e}")
        return []
    
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
                perfil=row["perfil"],
                foto=None,  # Não está na query atual
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                cpf=row["cpf"],
                telefone=row["telefone"],
                curso=row["curso"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                cep=row["cep"],
                cidade=row["cidade"],
                bairro=row["bairro"],
                rua=row["rua"],
                numero=row["numero"],
                estado=row["estado"],
                complemento=row["complemento"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"],
                renda_per_capita=row["renda_per_capita"],
                situacao_moradia=row["situacao_moradia"]
            )
        return None


def contar_todos() -> int:
    """Conta o total de alunos cadastrados"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_TODOS)
        return cursor.fetchone()["total"]

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
                perfil=row["perfil"],
                cpf=row["cpf"],
                telefone=row["telefone"],
                curso=row["curso"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                cep=row["cep"],
                cidade=row["cidade"],
                bairro=row["bairro"],
                rua=row["rua"],
                numero=row["numero"],
                estado=row["estado"],
                complemento=row["complemento"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"],
                renda_per_capita=row["renda_per_capita"],
                situacao_moradia=row["situacao_moradia"],
                auxilios=row["auxilios"] if row["auxilios"] else None,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )
            for row in rows]
        return alunos

def contar_beneficiados() -> int:
    """Conta o total de alunos beneficiados (com auxílios aprovados)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_BENEFICIADOS)
        return cursor.fetchone()["total"]

def obter_beneficiados_por_pagina(pagina: int, limite: int) -> list[Usuario]:
    """Obtém alunos beneficiados com paginação"""
    offset = (pagina - 1) * limite
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_BENEFICIADOS_POR_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        alunos = [
            Aluno(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                cpf=row["cpf"],
                telefone=row["telefone"],
                curso=row["curso"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                cep=row["cep"],
                cidade=row["cidade"],
                bairro=row["bairro"],
                rua=row["rua"],
                numero=row["numero"],
                estado=row["estado"],
                complemento=row["complemento"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"],
                renda_per_capita=row["renda_per_capita"],
                situacao_moradia=row["situacao_moradia"],
                auxilios=row["auxilios"] if row["auxilios"] else None,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )
            for row in rows]
        return alunos

def contar_nao_beneficiados() -> int:
    """Conta o total de alunos não beneficiados (sem auxílios aprovados)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_NAO_BENEFICIADOS)
        return cursor.fetchone()["total"]

def obter_nao_beneficiados_por_pagina(pagina: int, limite: int) -> list[Usuario]:
    """Obtém alunos não beneficiados com paginação"""
    offset = (pagina - 1) * limite
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_NAO_BENEFICIADOS_POR_PAGINA, (limite, offset))
        rows = cursor.fetchall()
        alunos = [
            Aluno(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                cpf=row["cpf"],
                telefone=row["telefone"],
                curso=row["curso"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                cep=row["cep"],
                cidade=row["cidade"],
                bairro=row["bairro"],
                rua=row["rua"],
                numero=row["numero"],
                estado=row["estado"],
                complemento=row["complemento"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"],
                renda_per_capita=row["renda_per_capita"],
                situacao_moradia=row["situacao_moradia"],
                auxilios=row["auxilios"] if row["auxilios"] else None,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )
            for row in rows]
        return alunos

def atualizar(aluno: Aluno) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            id_usuario=aluno.id_usuario,
            nome=aluno.nome,
            matricula=aluno.matricula,
            email=aluno.email,
            senha=aluno.senha,
            perfil=aluno.perfil,
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None
        )
        usuario_repo.atualizar(usuario)
        cursor.execute(ATUALIZAR, (
            aluno.cpf, 
            aluno.telefone,
            aluno.curso,
            aluno.data_nascimento,
            aluno.filiacao,
            aluno.cep,
            aluno.cidade,
            aluno.bairro,
            aluno.rua,
            aluno.numero,
            aluno.estado,
            aluno.complemento,
            aluno.nome_banco,
            aluno.agencia_bancaria,
            aluno.numero_conta_bancaria,
            aluno.renda_familiar,
            aluno.quantidade_pessoas,
            aluno.renda_per_capita,
            aluno.situacao_moradia,
            aluno.ano_ingresso,
            aluno.ano_conclusao_previsto,
            aluno.bolsa_pesquisa,
            aluno.cad_unico,
            aluno.bolsa_familia,
            aluno.id_usuario))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        # Primeiro exclui da tabela aluno
        cursor.execute(EXCLUIR, (id,))
        # Depois exclui da tabela usuario
        usuario_repo.excluir(id, cursor)
        return True
    
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
    
def obter_por_matricula(matricula: str) -> Optional[Aluno]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_MATRICULA, (matricula,))
        row = cursor.fetchone()
        if row:
            return Aluno(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                cpf=row["cpf"],
                telefone=row["telefone"],
                curso=row["curso"],
                data_nascimento=row["data_nascimento"],
                filiacao=row["filiacao"],
                cep=row["cep"],
                cidade=row["cidade"],
                bairro=row["bairro"],
                rua=row["rua"],
                numero=row["numero"],
                estado=row["estado"],
                complemento=row["complemento"],
                nome_banco=row["nome_banco"],
                agencia_bancaria=row["agencia_bancaria"],
                numero_conta_bancaria=row["numero_conta_bancaria"],
                renda_familiar=row["renda_familiar"],
                quantidade_pessoas=row["quantidade_pessoas"],
                renda_per_capita=row["renda_per_capita"],
                situacao_moradia=row["situacao_moradia"],
                ano_ingresso=row.get("ano_ingresso"),
                ano_conclusao_previsto=row.get("ano_conclusao_previsto"),
                bolsa_pesquisa=row.get("bolsa_pesquisa"),
                cad_unico=row.get("cad_unico"),
                bolsa_familia=row.get("bolsa_familia")
            )
        return None

def obter_possiveis_alunos() -> list[Usuario]:
    """Obtém todos os usuários que se cadastraram mas ainda não foram aprovados"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POSSIVEIS_ALUNOS)
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id_usuario=row["id_usuario"],
                nome=row["nome"],
                matricula=row["matricula"],
                email=row["email"],
                senha="",  # Não retorna senha por segurança
                perfil="aluno",
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=row["data_cadastro"])
            for row in rows]
        return usuarios
    
def existe_aluno_aprovado_por_matricula(matricula: str) -> bool:
    """Obtém um aluno aprovado (não pendente) por matrícula"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXISTE_ALUNO_APROVADO_POR_MATRICULA, (matricula,))
        row = cursor.fetchone()
        if row:
            return True
        return False                

def aprovar_aluno(id_usuario: int) -> bool:
    """Aprova um aluno (define aprovado como True)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Se o aluno ainda não tem registro na tabela aluno, cria um básico
        cursor.execute("SELECT id_usuario FROM aluno WHERE id_usuario = ?", (id_usuario,))
        if not cursor.fetchone():
            # Cria registro básico na tabela aluno com aprovado = True
            cursor.execute("""
                INSERT INTO aluno (id_usuario, cpf, telefone, curso, data_nascimento, filiacao, 
                                 cep, cidade, bairro, rua, numero, estado, complemento, 
                                 nome_banco, agencia_bancaria, numero_conta_bancaria, 
                                 renda_familiar, quantidade_pessoas, renda_per_capita, 
                                 situacao_moradia, aprovado) 
                VALUES (?, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 0, 0, 0, '', 1)
            """, (id_usuario,))
        else:
            # Atualiza registro existente
            cursor.execute(APROVAR_ALUNO, (id_usuario,))
        return cursor.rowcount > 0

def rejeitar_aluno(id_usuario: int) -> bool:
    """Rejeita um aluno (exclui tanto da tabela usuario quanto aluno se existir)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Primeiro exclui da tabela aluno se existir
        cursor.execute("DELETE FROM aluno WHERE id_usuario = ?", (id_usuario,))
        # Depois exclui da tabela usuario
        cursor.execute("DELETE FROM usuario WHERE id_usuario = ? AND perfil = 'aluno'", (id_usuario,))
        return cursor.rowcount > 0
    