import sqlite3

conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Get aluno ID (using id_usuario from usuario table)
cursor.execute('''
    SELECT u.id_usuario 
    FROM usuario u 
    WHERE u.matricula = ?
''', ('aluno123',))
aluno = cursor.fetchone()
print(f'ID Aluno: {aluno[0]}')

# Get auxilios for this aluno
cursor.execute('''
    SELECT a.id_auxilio, a.tipo_auxilio, i.id_inscricao 
    FROM auxilio a 
    INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao 
    WHERE i.id_aluno = ?
''', (aluno[0],))

auxilios = cursor.fetchall()
print('\nAuxílios:')
for aux in auxilios:
    print(f'  ID: {aux[0]}, Tipo: {aux[1]}, Inscrição: {aux[2]}')

# Also check existing recebimentos
cursor.execute('''
    SELECT r.id_recebimento, r.id_auxilio, r.mes_referencia, r.status, a.tipo_auxilio
    FROM recebimento r
    INNER JOIN auxilio a ON r.id_auxilio = a.id_auxilio
    INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
    WHERE i.id_aluno = ?
''', (aluno[0],))

recebimentos = cursor.fetchall()
print('\nRecebimentos do aluno:')
for rec in recebimentos:
    print(f'  ID: {rec[0]}, Auxílio ID: {rec[1]}, Mês: {rec[2]}, Status: {rec[3]}, Tipo: {rec[4]}')

conn.close()
