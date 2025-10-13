from util.db_util import get_connection

conn = get_connection()
cursor = conn.cursor()

query = """
SELECT 
u.id_usuario, 
u.nome,
u.matricula,
al.cpf,
GROUP_CONCAT(DISTINCT CASE 
    WHEN i.status = 'aprovado' THEN aux.tipo_auxilio 
END) as auxilios
FROM aluno al
INNER JOIN usuario u ON al.id_usuario = u.id_usuario
LEFT JOIN inscricao i ON al.id_usuario = i.id_aluno
LEFT JOIN auxilio aux ON i.id_inscricao = aux.id_inscricao
GROUP BY u.id_usuario
LIMIT 3
"""

cursor.execute(query)
results = cursor.fetchall()

print("Total de resultados:", len(results))
for row in results:
    print("\n" + "="*50)
    print(f"ID: {row['id_usuario']}")
    print(f"Nome: {row['nome']}")
    print(f"Matrícula: {row['matricula']}")
    print(f"CPF: {row['cpf']}")
    print(f"Auxílios: {row['auxilios']}")
    print(f"Tipo do campo auxilios: {type(row['auxilios'])}")
    
conn.close()
