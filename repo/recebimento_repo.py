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

def confirmar_recebimentos_mes(id_aluno: int, mes_referencia: str, ano_referencia: int, 
                                comprovante_transporte: Optional[str] = None, 
                                comprovante_moradia: Optional[str] = None) -> bool:
    """Confirma todos os recebimentos de um aluno em um determinado mês"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Confirmar todos os recebimentos do mês
        cursor.execute(CONFIRMAR_RECEBIMENTOS_MES, (id_aluno, mes_referencia, ano_referencia))
        
        # Atualizar comprovante de transporte se fornecido
        if comprovante_transporte:
            cursor.execute(ATUALIZAR_COMPROVANTE_TRANSPORTE, (comprovante_transporte, id_aluno, mes_referencia, ano_referencia))
        
        # Atualizar comprovante de moradia se fornecido
        if comprovante_moradia:
            cursor.execute(ATUALIZAR_COMPROVANTE_MORADIA, (comprovante_moradia, id_aluno, mes_referencia, ano_referencia))
        
        return cursor.rowcount > 0

def obter_por_aluno(id_aluno: int) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ALUNO, (id_aluno,))
        rows = cursor.fetchall()
        recebimentos = []
        for row in rows:
            # Processar a string de detalhes dos auxílios
            auxilios = []
            if row["auxilios_detalhes"]:
                for aux_info in row["auxilios_detalhes"].split('|'):
                    tipo, valor, id_rec = aux_info.split(':')
                    auxilios.append({
                        'tipo_auxilio': tipo,
                        'valor': float(valor),
                        'id_recebimento': int(id_rec)
                    })
            
            recebimento = {
                'mes_referencia': row["mes_referencia"],
                'ano_referencia': row["ano_referencia"],
                'valor_total': row["valor_total"],
                'data_recebimento': row["data_recebimento"],
                'status': row["status"],
                'auxilios': auxilios
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

def gerar_recebimentos_auxilio_deferido(id_auxilio: int, valor_mensal: float, data_deferimento: str) -> bool:
    """
    Gera recebimentos automaticamente quando um auxílio é deferido.
    Cria recebimentos do mês seguinte ao deferimento até o fim da vigência do auxílio.
    """
    try:
        from datetime import datetime
        
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Obter informações do auxílio
            cursor.execute("""
                SELECT a.data_fim, a.id_inscricao, i.id_aluno
                FROM auxilio a
                INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
                WHERE a.id_auxilio = ?
            """, (id_auxilio,))
            
            result = cursor.fetchone()
            if not result:
                print(f"Auxílio {id_auxilio} não encontrado")
                return False
            
            data_fim_str = result[0]
            
            # Converter data de deferimento para datetime
            data_def = datetime.strptime(data_deferimento[:10], '%Y-%m-%d')
            
            # Primeiro recebimento é no mês seguinte ao deferimento
            mes_inicio = data_def.month + 1
            ano_inicio = data_def.year
            if mes_inicio > 12:
                mes_inicio = 1
                ano_inicio += 1
            
            # Converter data_fim para datetime
            if data_fim_str:
                data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d')
            else:
                # Se não tem data fim, gerar até o final do ano
                data_fim = datetime(ano_inicio, 12, 31)
            
            # Gerar recebimentos mensais
            mes_atual = mes_inicio
            ano_atual = ano_inicio
            recebimentos_criados = 0
            
            while (ano_atual < data_fim.year) or (ano_atual == data_fim.year and mes_atual <= data_fim.month):
                mes_ref = str(mes_atual).zfill(2)
                
                # Data de recebimento é dia 5 do mês
                data_recebimento = f"{ano_atual}-{mes_ref}-05"
                
                # Verificar se já existe recebimento para este mês
                cursor.execute("""
                    SELECT COUNT(*) FROM recebimento 
                    WHERE id_auxilio = ? AND mes_referencia = ? AND ano_referencia = ?
                """, (id_auxilio, mes_ref, ano_atual))
                
                if cursor.fetchone()[0] == 0:
                    # Inserir recebimento
                    cursor.execute("""
                        INSERT INTO recebimento (
                            id_auxilio, mes_referencia, ano_referencia, 
                            valor, data_recebimento, status, observacoes
                        ) VALUES (?, ?, ?, ?, ?, 'pendente', 'Gerado automaticamente')
                    """, (id_auxilio, mes_ref, ano_atual, valor_mensal, data_recebimento))
                    recebimentos_criados += 1
                
                # Próximo mês
                mes_atual += 1
                if mes_atual > 12:
                    mes_atual = 1
                    ano_atual += 1
            
            conn.commit()
            print(f"Gerados {recebimentos_criados} recebimentos para o auxílio {id_auxilio}")
            return True
            
    except Exception as e:
        print(f"Erro ao gerar recebimentos: {e}")
        import traceback
        traceback.print_exc()
        return False

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
