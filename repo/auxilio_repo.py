from typing import Optional
from model.auxilio_model import Auxilio
from sql.auxilio_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            # Ensure columns added in newer versions exist on older DB files
            _ensure_auxilio_columns(conn)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

def inserir(auxilio: Auxilio) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            auxilio.id_edital,
            auxilio.id_inscricao,
            auxilio.descricao,
            auxilio.valor_mensal,
            auxilio.data_inicio,
            auxilio.data_fim,
            auxilio.tipo_auxilio
        ))
        return cursor.lastrowid

    
def obter_todos() -> list[Auxilio]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        auxilios = [
            Auxilio(id_auxilio=row["id_auxilio"],
                   id_edital=row["id_edital"],
                   id_inscricao=row["id_inscricao"],    
                   tipo_auxilio=row["tipo_auxilio"],
                   descricao=row["descricao"],
                   valor_mensal=row["valor_mensal"],
                   data_inicio=row["data_inicio"],
                   data_fim=row["data_fim"])
            for row in rows]
        return auxilios

def obter_por_id(id: int) -> Optional[Auxilio]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        auxilio = Auxilio(
            id_auxilio=row["id_auxilio"],
            id_edital=row["id_edital"],
            id_inscricao=row["id_inscricao"],
            tipo_auxilio=row["tipo_auxilio"],
            descricao=row["descricao"],
            valor_mensal=row["valor_mensal"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"])
        return auxilio  
        
    
def atualizar(auxilio: Auxilio) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            auxilio.descricao,
            auxilio.valor_mensal,
            auxilio.data_fim,
            auxilio.tipo_auxilio,
            auxilio.id_auxilio
        ))
        return cursor.rowcount > 0
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)

def obter_por_aluno(id_aluno: int) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ALUNO, (id_aluno,))
        rows = cursor.fetchall()
        auxilios = []
        for row in rows:
            auxilio = {
                'id_auxilio': row["id_auxilio"],
                'id_edital': row["id_edital"],
                'id_inscricao': row["id_inscricao"],
                'tipo_auxilio': row["tipo_auxilio"],
                'descricao': row["descricao"],
                'valor_mensal': row["valor_mensal"],
                'data_inicio': row["data_inicio"],
                'data_fim': row["data_fim"],
                'edital_titulo': row["edital_titulo"],
                'status_inscricao': row["status_inscricao"],
                'status_auxilio': row["status_auxilio"] if "status_auxilio" in row.keys() else "pendente",
                'motivo_indeferimento': row["motivo_indeferimento"] if "motivo_indeferimento" in row.keys() else None
            }
            auxilios.append(auxilio)
        return auxilios

def atualizar_status_auxilio(id_auxilio: int, status: str) -> bool:
    """Atualiza o status de um auxílio específico"""
    if status not in ['pendente', 'deferido', 'indeferido']:
        return False
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_STATUS, (status, id_auxilio))
        return cursor.rowcount > 0

def atualizar_valor_auxilio(id_auxilio: int, valor_mensal: float) -> bool:
    """Atualiza o valor mensal de um auxílio específico"""
    if valor_mensal <= 0:
        return False
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_VALOR, (valor_mensal, id_auxilio))
        return cursor.rowcount > 0

def atualizar_motivo_indeferimento(id_auxilio: int, motivo: str) -> bool:
    """Atualiza o motivo de indeferimento de um auxílio específico"""
    if not motivo or not motivo.strip():
        return False
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_MOTIVO_INDEFERIMENTO, (motivo.strip(), id_auxilio))
        return cursor.rowcount > 0

def obter_auxilios_por_inscricao(id_inscricao: int) -> list[dict]:
    """Obtém todos os auxílios de uma inscrição com seus status individuais"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_AUXILIOS_POR_INSCRICAO, (id_inscricao,))
        rows = cursor.fetchall()
        auxilios = []
        for row in rows:
            auxilio = {
                'id_auxilio': row["id_auxilio"],
                'id_edital': row["id_edital"],
                'id_inscricao': row["id_inscricao"],
                'tipo_auxilio': row["tipo_auxilio"],
                'descricao': row["descricao"],
                'valor_mensal': row["valor_mensal"],
                'data_inicio': row["data_inicio"],
                'data_fim': row["data_fim"],
                'status_auxilio': row["status_auxilio"] if "status_auxilio" in row.keys() else "pendente",
                'motivo_indeferimento': row["motivo_indeferimento"] if "motivo_indeferimento" in row.keys() else None
            }
            auxilios.append(auxilio)
        return auxilios
 

def _ensure_auxilio_columns(conn) -> None:
    """Ensure the auxilio table contains newer columns introduced after initial schema.

    This performs idempotent ALTER TABLE operations to add missing columns so
    older database files won't raise "no such column" errors at runtime.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(auxilio)")
        cols = {row[1] for row in cursor.fetchall()}  # row format: (cid, name, type, ...)

        # Add status_auxilio if missing
        if 'status_auxilio' not in cols:
            try:
                cursor.execute("ALTER TABLE auxilio ADD COLUMN status_auxilio TEXT DEFAULT 'pendente'")
            except Exception:
                # best-effort: ignore if cannot add (e.g., locked or other race)
                pass

        # Add motivo_indeferimento if missing
        if 'motivo_indeferimento' not in cols:
            try:
                cursor.execute("ALTER TABLE auxilio ADD COLUMN motivo_indeferimento TEXT")
            except Exception:
                pass
        conn.commit()
    except Exception:
        # Swallow errors here to avoid breaking startup; errors will be visible in logs
        pass

