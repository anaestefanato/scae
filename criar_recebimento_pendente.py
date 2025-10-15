from util.db_util import get_connection
from datetime import datetime

# Inserir um recebimento pendente para o aluno padrão
with get_connection() as conn:
    cursor = conn.cursor()
    
    # Buscar um auxílio do aluno padrão
    cursor.execute("""
        SELECT a.id_auxilio, a.tipo_auxilio
        FROM auxilio a
        INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
        INNER JOIN usuario u ON i.id_aluno = u.id_usuario
        WHERE u.matricula = 'aluno123'
        LIMIT 1
    """)
    
    auxilio = cursor.fetchone()
    
    if auxilio:
        id_auxilio = auxilio['id_auxilio']
        tipo_auxilio = auxilio['tipo_auxilio']
        
        # Inserir recebimento pendente para Outubro/2025
        cursor.execute("""
            INSERT INTO recebimento (id_auxilio, mes_referencia, ano_referencia, valor, data_recebimento, status, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_auxilio, 'Outubro', 2025, 200.00, datetime.now().strftime('%Y-%m-%d'), 'pendente', 'Recebimento pendente de confirmação'))
        
        conn.commit()
        print(f"Recebimento pendente criado com sucesso para {tipo_auxilio}!")
        print(f"ID do auxílio: {id_auxilio}")
    else:
        print("Nenhum auxílio encontrado para o aluno padrão")
