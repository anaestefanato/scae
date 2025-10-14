from typing import Optional
from model.recebimento_model import Recebimento
from sql.recebimento_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

def inserir(recebimento: Recebimento) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            recebimento.id_auxilio,
            recebimento.mes_referencia,
            recebimento.ano_referencia,
            recebimento.valor,
            recebimento.data_recebimento,
            recebimento.status,
            recebimento.observacoes
        ))
        return cursor.lastrowid

def obter_todos() -> list[Recebimento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        recebimentos = [
            Recebimento(
                id_recebimento=row["id_recebimento"],
                id_auxilio=row["id_auxilio"],
                mes_referencia=row["mes_referencia"],
                ano_referencia=row["ano_referencia"],
                valor=row["valor"],
                data_recebimento=row["data_recebimento"],
                status=row["status"],
                observacoes=row["observacoes"])
            for row in rows]
        return recebimentos

def obter_por_id(id: int) -> Optional[Recebimento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        recebimento = Recebimento(
            id_recebimento=row["id_recebimento"],
            id_auxilio=row["id_auxilio"],
            mes_referencia=row["mes_referencia"],
            ano_referencia=row["ano_referencia"],
            valor=row["valor"],
            data_recebimento=row["data_recebimento"],
            status=row["status"],
            observacoes=row["observacoes"])
        return recebimento

def atualizar(recebimento: Recebimento) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            recebimento.valor,
            recebimento.data_recebimento,
            recebimento.status,
            recebimento.observacoes,
            recebimento.id_recebimento
        ))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)

def confirmar_recebimento(id_recebimento: int, comprovante_transporte: Optional[str] = None, comprovante_moradia: Optional[str] = None) -> bool:
    """Confirma um recebimento e salva os comprovantes se fornecidos"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONFIRMAR_RECEBIMENTO, (comprovante_transporte, comprovante_moradia, id_recebimento))
        return cursor.rowcount > 0

def obter_por_aluno(id_aluno: int) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ALUNO, (id_aluno,))
        rows = cursor.fetchall()
        recebimentos = []
        for row in rows:
            recebimento = {
                'id_recebimento': row["id_recebimento"],
                'id_auxilio': row["id_auxilio"],
                'mes_referencia': row["mes_referencia"],
                'ano_referencia': row["ano_referencia"],
                'valor': row["valor"],
                'data_recebimento': row["data_recebimento"],
                'status': row["status"],
                'observacoes': row["observacoes"],
                'tipo_auxilio': row["tipo_auxilio"],
                'edital_titulo': row["edital_titulo"]
            }
            recebimentos.append(recebimento)
        return recebimentos

def obter_estatisticas_aluno(id_aluno: int) -> dict:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ESTATISTICAS_ALUNO, (id_aluno,))
        row = cursor.fetchone()
        if row is None:
            return {
                'total_recebimentos': 0,
                'total_valor': 0.0,
                'tipos_auxilio': 0,
                'valor_medio': 0.0
            }
        return {
            'total_recebimentos': row["total_recebimentos"] or 0,
            'total_valor': row["total_valor"] or 0.0,
            'tipos_auxilio': row["tipos_auxilio"] or 0,
            'valor_medio': row["valor_medio"] or 0.0
        }

def inserir_dados_exemplo() -> bool:
    """Insere dados de exemplo na tabela de recebimentos"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Primeiro, obtém um ID de aluno que tenha auxílio deferido
            cursor.execute("""
                SELECT DISTINCT i.id_aluno 
                FROM inscricao i 
                INNER JOIN auxilio a ON i.id_inscricao = a.id_inscricao
                WHERE i.status = 'deferido' 
                LIMIT 1
            """)
            result = cursor.fetchone()
            if not result:
                print("Nenhum aluno com auxílio deferido encontrado para inserir dados de exemplo")
                return True
            
            id_aluno = result[0]
            
            # Executar cada comando SQL separadamente com o ID do aluno
            comandos = INSERIR_DADOS_EXEMPLO.split(';')
            for comando in comandos:
                comando = comando.strip()
                if comando and not comando.startswith('--') and comando != '':
                    cursor.execute(comando, (id_aluno,))
            conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir dados de exemplo: {e}")
        return False
