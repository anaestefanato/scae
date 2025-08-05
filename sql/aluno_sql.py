CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS aluno (
    id_usuario INTEGER,
    cpf TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    filiacao TEXT NOT NULL,
    endereco TEXT NOT NULL,
    nome_banco TEXT NOT NULL,
    agencia_bancaria TEXT NOT NULL,
    numero_conta_bancaria TEXT NOT NULL,
    renda_familiar REAL NOT NULL,
    matricula TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO aluno (id_usuario, cpf, data_nascimento, filiacao, endereco, nome_banco, agencia_bancaria, numero_conta_bancaria, renda_familiar, matricula) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    aluno.id_usuario AS id_usuario,
    usuario.nome AS nome,
    usuario.email AS email,
    usuario.senha AS senha,
    usuario.tipo_usuario AS tipo_usuario,
    aluno.cpf AS cpf,
    aluno.data_nascimento AS data_nascimento,
    aluno.filiacao AS filiacao,
    aluno.endereco AS endereco,
    aluno.nome_banco AS nome_banco,
    aluno.agencia_bancaria AS agencia_bancaria,
    aluno.numero_conta_bancaria AS numero_conta_bancaria,
    aluno.renda_familiar AS renda_familiar,
    aluno.matricula AS matricula
FROM aluno
JOIN usuario ON aluno.id_usuario = usuario.id_usuario
WHERE aluno.id_usuario = ?
""" 

OBTER_POR_PAGINA = """
SELECT
u.id_usuario,
u.nome,
u.email,
u.senha,
u.tipo_usuario,
al.cpf,
al.data_nascimento,
al.filiacao,
al.endereco,
al.nome_banco,
al.agencia_bancaria,
al.numero_conta_bancaria,
al.renda_familiar,
al.matricula
FROM aluno al
INNER JOIN usuario u ON al.id_usuario = u.id_usuario
ORDER BY al.matricula
LIMIT ? OFFSET ?
"""

ATUALIZAR = """
UPDATE aluno
SET cpf = ?, data_nascimento = ?, filiacao = ?, endereco = ?, nome_banco = ?, agencia_bancaria = ?, numero_conta_bancaria = ?, renda_familiar = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM aluno
WHERE id_usuario = ?
"""