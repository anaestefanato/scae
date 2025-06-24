CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS aluno (
id_usuario INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
cpf TEXT NOT NULL,
data_nascimento TEXT NOT NULL,
filiacao TEXT NOT NULL,
endereco TEXT NOT NULL,
nome_banco TEXT NOT NULL,
numero_conta_bancaria TEXT NOT NULL,
renda_familiar REAL NOT NULL,
matricula TEXT NOT NULL)
"""

INSERIR = """
INSERT INTO aluno (cpf, data_nascimento, filiacao, endereco, nome_banco, numero_conta_bancaria, renda_familiar, matricula) 
VALUES (?,?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
id_usuario, cpf, data_nascimento, filiacao, endereco, nome_banco, numero_conta_bancaria, renda_familiar, matricula 
FROM aluno al 
INNER JOIN usuario u ON al.id_usuario = u.id_usuario    
ORDER BY matricula
""" 

OBTER_POR_ID = """
SELECT 
id_usuario, cpf, data_nascimento, filiacao, endereco, nome_banco, numero_conta_bancaria, renda_familiar, matricula
FROM aluno al
INNER JOIN usuario u ON al.id_usuario = u.id_usuario
WHERE id_usuario = ?
""" 

ATUALIZAR = """
UPDATE aluno
SET cpf = ?, data_nascimento = ?, filiacao = ?, endereco = ?, nome_banco = ?, numero_conta_bancaria = ?, renda_familiar = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM aluno
WHERE id_usuario = ?
"""