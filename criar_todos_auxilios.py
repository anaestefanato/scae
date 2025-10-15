import sqlite3

conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Get the user's inscricao
cursor.execute('''
    SELECT i.id_inscricao, i.id_edital
    FROM inscricao i
    WHERE i.id_aluno = 2
    LIMIT 1
''')
inscricao = cursor.fetchone()

if inscricao:
    id_inscricao = inscricao[0]
    id_edital = inscricao[1]
    print(f'Inscricao ID: {id_inscricao}, Edital ID: {id_edital}')
    
    # Check what auxilios already exist
    cursor.execute('''
        SELECT tipo_auxilio FROM auxilio 
        WHERE id_inscricao = ?
    ''', (id_inscricao,))
    auxilios_existentes = [row[0] for row in cursor.fetchall()]
    print(f'Auxílios existentes: {auxilios_existentes}')
    
    # Tipos de auxílio para criar
    tipos_auxilios = {
        'auxilio moradia': 300.00,
        'auxilio material': 100.00
    }
    
    auxilios_criados = []
    
    for tipo, valor in tipos_auxilios.items():
        if tipo not in auxilios_existentes:
            cursor.execute('''
                INSERT INTO auxilio (id_edital, id_inscricao, tipo_auxilio, descricao, valor_mensal, data_inicio, data_fim)
                VALUES (?, ?, ?, ?, ?, '2025-10-01', '2025-12-31')
            ''', (id_edital, id_inscricao, tipo, f'{tipo.title()} para teste', valor))
            
            auxilio_id = cursor.lastrowid
            auxilios_criados.append((auxilio_id, tipo, valor))
            print(f'Auxilio {tipo} criado com ID: {auxilio_id}')
    
    # Get all auxilios for this student
    cursor.execute('''
        SELECT id_auxilio, tipo_auxilio, valor_mensal 
        FROM auxilio 
        WHERE id_inscricao = ?
    ''', (id_inscricao,))
    todos_auxilios = cursor.fetchall()
    
    print(f'\nTodos os auxílios do aluno:')
    for aux in todos_auxilios:
        print(f'  ID: {aux[0]}, Tipo: {aux[1]}, Valor: R$ {aux[2]}')
    
    # Criar recebimentos para Outubro/2025 (se não existir)
    print('\n--- Criando recebimentos para Outubro/2025 ---')
    for aux in todos_auxilios:
        id_auxilio, tipo, valor = aux
        
        # Check if recebimento already exists
        cursor.execute('''
            SELECT id_recebimento FROM recebimento 
            WHERE id_auxilio = ? AND mes_referencia = 'Outubro' AND ano_referencia = 2025
        ''', (id_auxilio,))
        
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO recebimento (id_auxilio, mes_referencia, ano_referencia, valor, data_recebimento, status, observacoes)
                VALUES (?, 'Outubro', 2025, ?, '2025-10-15', 'pendente', 'Recebimento consolidado')
            ''', (id_auxilio, valor))
            print(f'Recebimento Outubro criado para {tipo} - R$ {valor}')
        else:
            print(f'Recebimento Outubro já existe para {tipo}')
    
    # Criar recebimentos para Novembro/2025
    print('\n--- Criando recebimentos para Novembro/2025 ---')
    for aux in todos_auxilios:
        id_auxilio, tipo, valor = aux
        
        # Check if recebimento already exists
        cursor.execute('''
            SELECT id_recebimento FROM recebimento 
            WHERE id_auxilio = ? AND mes_referencia = 'Novembro' AND ano_referencia = 2025
        ''', (id_auxilio,))
        
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO recebimento (id_auxilio, mes_referencia, ano_referencia, valor, data_recebimento, status, observacoes)
                VALUES (?, 'Novembro', 2025, ?, '2025-11-15', 'pendente', 'Recebimento consolidado')
            ''', (id_auxilio, valor))
            print(f'Recebimento Novembro criado para {tipo} - R$ {valor}')
        else:
            print(f'Recebimento Novembro já existe para {tipo}')
    
    conn.commit()
    print('\n✅ Todos os auxílios e recebimentos foram criados com sucesso!')
else:
    print('Nenhuma inscrição encontrada')

conn.close()
