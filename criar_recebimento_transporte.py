import sqlite3

conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Inserir recebimento de transporte pendente
cursor.execute("""
    INSERT INTO recebimento (id_auxilio, mes_referencia, ano_referencia, valor, data_recebimento, status, observacoes)
    VALUES (2, 'Novembro', 2025, 150.00, '2025-11-15', 'pendente', 'Recebimento teste para transporte')
""")

conn.commit()
print(f'Recebimento transporte criado com ID: {cursor.lastrowid}')
conn.close()
