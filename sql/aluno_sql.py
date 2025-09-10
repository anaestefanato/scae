CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS aluno (
    id_usuario INTEGER PRIMARY KEY,
    cpf TEXT NOT NULL,
    rg TEXT NOT NULL,
    telefone TEXT NOT NULL,
    curso TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    filiacao TEXT NOT NULL,
    cep TEXT NOT NULL,
    cidade TEXT NOT NULL,
    bairro TEXT NOT NULL,
    rua TEXT NOT NULL,
    numero TEXT NOT NULL,
    nome_banco TEXT NOT NULL,
    agencia_bancaria TEXT NOT NULL,
    numero_conta_bancaria TEXT NOT NULL,
    renda_familiar REAL NOT NULL,
    quantidade_pessoas INTEGER NOT NULL,
    cadastro_completo BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO aluno (id_usuario, cpf, rg, telefone, curso, data_nascimento, filiacao, cep, cidade, bairro, rua, numero, nome_banco, agencia_bancaria, numero_conta_bancaria, renda_familiar, quantidade_pessoas) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
al.id_usuario, al.cpf, al.rg, al.telefone, al.curso, al.data_nascimento, al.filiacao, al.cep, al.cidade, al.bairro, al.rua, al.numero, al.nome_banco, al.agencia_bancaria, al.numero_conta_bancaria, al.renda_familiar, al.quantidade_pessoas, u.nome, u.matricula, u.email, u.senha
FROM aluno al 
INNER JOIN usuario u ON al.id_usuario = u.id_usuario    
ORDER BY al.matricula
""" 

OBTER_POR_ID = """
SELECT 
    al.id_usuario AS id_usuario,
    u.nome AS nome,
    u.matricula AS matricula
    u.email AS email,
    u.senha AS senha,
    u.tipo_usuario AS tipo_usuario,
    al.cpf AS cpf,
    al.rg AS rg,
    al.telefone AS telefone,
    al.curso AS curso,
    al.data_nascimento AS data_nascimento,
    al.filiacao AS filiacao,
    al.cep AS cep,
    al.cidade AS cidade,
    al.bairro AS bairro,
    al.rua AS rua,
    al.numero AS numero,
    al.nome_banco AS nome_banco,
    al.agencia_bancaria AS agencia_bancaria,
    al.numero_conta_bancaria AS numero_conta_bancaria,
    al.renda_familiar AS renda_familiar,
    al.quantidade_pessoas AS quantidade_pessoas
FROM aluno al
JOIN usuario u ON al.id_usuario = u.id_usuario
WHERE al.id_usuario = ?
""" 

OBTER_POR_PAGINA = """
SELECT
u.id_usuario,
u.matricula,
u.nome,
u.email,
u.senha,
u.tipo_usuario,
al.cpf,
al.rg,
al.telefone,
al.curso,
al.data_nascimento,
al.filiacao,
al.cep,
al.cidade,
al.bairro,
al.rua,
al.numero,
al.nome_banco,
al.agencia_bancaria,
al.numero_conta_bancaria,
al.renda_familiar,
al.quantidade_pessoas
FROM aluno al
INNER JOIN usuario u ON al.id_usuario = u.id_usuario
ORDER BY u.matricula
LIMIT ? OFFSET ?
"""

ATUALIZAR = """
UPDATE aluno
SET cpf = ?, rg = ?, telefone = ?, data_nascimento = ?, filiacao = ?, cep = ?, cidade = ?, bairro = ?, rua = ?, numero = ?, nome_banco = ?, agencia_bancaria = ?, numero_conta_bancaria = ?, renda_familiar = ?, quantidade_pessoas = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM aluno
WHERE id_usuario = ?
"""

POSSUI_CADASTRO_COMPLETO = """
SELECT cadastro_completo
FROM aluno
WHERE id_usuario = ?
"""

MARCAR_CADASTRO_COMPLETO = """
UPDATE aluno
SET cadastro_completo = 1
WHERE id_usuario = ?
"""