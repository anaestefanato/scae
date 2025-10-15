import sqlite3

conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Get any inscricao for the user (regardless of status)
cursor.execute('''
    SELECT i.id_inscricao, i.id_edital, i.status
    FROM inscricao i
    WHERE i.id_aluno = 2
    LIMIT 1
''')
inscricao = cursor.fetchone()

if inscricao:
    print(f'Inscricao ID: {inscricao[0]}, Edital ID: {inscricao[1]}, Status: {inscricao[2]}')
    
    # Create a transport auxilio
    cursor.execute('''
        INSERT INTO auxilio (id_edital, id_inscricao, tipo_auxilio, descricao, valor_mensal, data_inicio, data_fim)
        VALUES (?, ?, 'auxilio transporte', 'Auxílio transporte para teste', 150.00, '2025-11-01', '2025-12-31')
    ''', (inscricao[1], inscricao[0]))
    
    auxilio_id = cursor.lastrowid
    print(f'Auxilio transporte criado com ID: {auxilio_id}')
    
    # Create a pending recebimento for this transport auxilio
    cursor.execute('''
        INSERT INTO recebimento (id_auxilio, mes_referencia, ano_referencia, valor, data_recebimento, status, observacoes)
        VALUES (?, 'Novembro', 2025, 150.00, '2025-11-15', 'pendente', 'Recebimento transporte - teste')
    ''', (auxilio_id,))
    
    recebimento_id = cursor.lastrowid
    print(f'Recebimento transporte criado com ID: {recebimento_id}')
    
    conn.commit()
else:
    print('Nenhuma inscrição encontrada')

conn.close()
