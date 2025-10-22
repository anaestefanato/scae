import sqlite3
from datetime import date

# Conectar ao banco
conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Verificar todos os editais
cursor.execute('SELECT id_edital, titulo, data_publicacao, status FROM edital ORDER BY data_publicacao DESC')
editais = cursor.fetchall()

print('\n=== TODOS OS EDITAIS ===')
for e in editais:
    print(f'ID: {e[0]} | Título: {e[1]} | Data: {e[2]} | Status: {e[3]}')

# Verificar editais visíveis para alunos (data_publicacao <= hoje)
hoje = date.today().strftime('%Y-%m-%d')
print(f'\n=== EDITAIS VISÍVEIS PARA ALUNOS (data <= {hoje}) ===')
cursor.execute('''
    SELECT id_edital, titulo, data_publicacao, status 
    FROM edital 
    WHERE status = 'ativo' AND data_publicacao <= ?
    ORDER BY data_publicacao DESC
''', (hoje,))
editais_visiveis = cursor.fetchall()

if editais_visiveis:
    for e in editais_visiveis:
        print(f'ID: {e[0]} | Título: {e[1]} | Data: {e[2]} | Status: {e[3]}')
else:
    print('Nenhum edital visível para alunos')

# Verificar editais futuros (data_publicacao > hoje)
print(f'\n=== EDITAIS FUTUROS (data > {hoje}) ===')
cursor.execute('''
    SELECT id_edital, titulo, data_publicacao, status 
    FROM edital 
    WHERE status = 'ativo' AND data_publicacao > ?
    ORDER BY data_publicacao DESC
''', (hoje,))
editais_futuros = cursor.fetchall()

if editais_futuros:
    for e in editais_futuros:
        print(f'ID: {e[0]} | Título: {e[1]} | Data: {e[2]} | Status: {e[3]}')
else:
    print('Nenhum edital futuro')

conn.close()
print('\n')
