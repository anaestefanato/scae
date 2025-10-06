CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS aluno (
    id_usuario INTEGER PRIMARY KEY,
    cpf TEXT NOT NULL,
    telefone TEXT NOT NULL,
    curso TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    filiacao TEXT NOT NULL,
    cep TEXT NOT NULL,
    cidade TEXT NOT NULL,
    bairro TEXT NOT NULL,
    rua TEXT NOT NULL,
    numero TEXT NOT NULL,
    estado TEXT NOT NULL,
    complemento TEXT,
    nome_banco TEXT NOT NULL,
    agencia_bancaria TEXT NOT NULL,
    numero_conta_bancaria TEXT NOT NULL,
    renda_familiar REAL NOT NULL,
    quantidade_pessoas INTEGER NOT NULL,
    renda_per_capita REAL NOT NULL,
    situacao_moradia TEXT NOT NULL,
    cadastro_completo BOOLEAN DEFAULT 0,
    aprovado BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO aluno (id_usuario, cpf, telefone, curso, data_nascimento, filiacao, cep, cidade, bairro, rua, numero, estado, complemento, nome_banco, agencia_bancaria, numero_conta_bancaria, renda_familiar, quantidade_pessoas, renda_per_capita, situacao_moradia) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
al.id_usuario, al.cpf, al.telefone, al.curso, al.data_nascimento, al.filiacao, al.cep, al.cidade, al.bairro, al.rua, al.numero, al.estado, al.complemento, al.nome_banco, al.agencia_bancaria, al.numero_conta_bancaria, al.renda_familiar, al.quantidade_pessoas, al.renda_per_capita, al.situacao_moradia, u.nome, u.matricula, u.email, u.senha
FROM aluno al 
INNER JOIN usuario u ON al.id_usuario = u.id_usuario    
ORDER BY u.nome
""" 

# Obter apenas alunos aprovados (não pendentes) com seus auxílios
OBTER_ALUNOS_APROVADOS = """
    SELECT 
        u.id_usuario,
        u.nome,
        u.matricula,
        u.email,
        a.curso,
        CASE 
            WHEN i.status = 'aprovado' THEN 'Ativo'
            WHEN i.status = 'suspenso' THEN 'Suspenso'
            ELSE 'Inativo'
        END as situacao,
        GROUP_CONCAT(DISTINCT e.titulo) as auxilios,
        COALESCE(SUM(DISTINCT 
            CASE 
                WHEN e.titulo LIKE '%Transporte%' THEN 150.00
                WHEN e.titulo LIKE '%Alimentação%' OR e.titulo LIKE '%Alimentacao%' THEN 300.00  
                WHEN e.titulo LIKE '%Moradia%' THEN 400.00
                WHEN e.titulo LIKE '%Material%' THEN 200.00
                ELSE 100.00
            END), 0) as valor_mensal
    FROM usuario u
    INNER JOIN aluno a ON u.id_usuario = a.id_usuario  
    LEFT JOIN inscricao i ON a.id_usuario = i.id_aluno AND i.status = 'aprovado'
    LEFT JOIN edital e ON i.id_edital = e.id_edital
    WHERE a.aprovado = 1
    GROUP BY u.id_usuario, u.nome, u.matricula, u.email, a.curso
    ORDER BY u.nome
""" 

OBTER_POR_ID = """
SELECT 
    al.id_usuario AS id_usuario,
    u.nome AS nome,
    u.matricula AS matricula,
    u.email AS email,
    u.senha AS senha,
    u.perfil AS perfil,
    al.cpf AS cpf,
    al.telefone AS telefone,
    al.curso AS curso,
    al.data_nascimento AS data_nascimento,
    al.filiacao AS filiacao,
    al.cep AS cep,
    al.cidade AS cidade,
    al.bairro AS bairro,
    al.rua AS rua,
    al.numero AS numero,
    al.estado AS estado,
    al.complemento AS complemento,
    al.nome_banco AS nome_banco,
    al.agencia_bancaria AS agencia_bancaria,
    al.numero_conta_bancaria AS numero_conta_bancaria,
    al.renda_familiar AS renda_familiar,
    al.quantidade_pessoas AS quantidade_pessoas,
    al.renda_per_capita AS renda_per_capita,
    al.situacao_moradia AS situacao_moradia
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
u.perfil,
al.cpf,
al.telefone,
al.curso,
al.data_nascimento,
al.filiacao,
al.cep,
al.cidade,
al.bairro,
al.rua,
al.numero,
al.estado,
al.complemento,
al.nome_banco,
al.agencia_bancaria,
al.numero_conta_bancaria,
al.renda_familiar,
al.quantidade_pessoas,
al.renda_per_capita,
al.situacao_moradia
FROM aluno al
INNER JOIN usuario u ON al.id_usuario = u.id_usuario
ORDER BY u.matricula
LIMIT ? OFFSET ?
"""

ATUALIZAR = """
UPDATE aluno
SET cpf = ?, telefone = ?, curso = ?, data_nascimento = ?, filiacao = ?, cep = ?, cidade = ?, bairro = ?, rua = ?, numero = ?, estado = ?, complemento = ?, nome_banco = ?, agencia_bancaria = ?, numero_conta_bancaria = ?, renda_familiar = ?, quantidade_pessoas = ?, renda_per_capita = ?, situacao_moradia = ?
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
OBTER_POR_MATRICULA = """
SELECT
    al.id_usuario AS id_usuario,
    u.nome AS nome,
    u.matricula AS matricula,
    u.email AS email,
    u.senha AS senha,
    u.perfil AS perfil,
    u.foto AS foto,
    al.cpf AS cpf,
    al.telefone AS telefone,
    al.curso AS curso,
    al.data_nascimento AS data_nascimento,
    al.filiacao AS filiacao,
    al.cep AS cep,
    al.cidade AS cidade,
    al.bairro AS bairro,
    al.rua AS rua,
    al.numero AS numero,
    al.estado AS estado,
    al.complemento AS complemento,
    al.nome_banco AS nome_banco,
    al.agencia_bancaria AS agencia_bancaria,
    al.numero_conta_bancaria AS numero_conta_bancaria,
    al.renda_familiar AS renda_familiar,
    al.quantidade_pessoas AS quantidade_pessoas,
    al.renda_per_capita AS renda_per_capita,
    al.situacao_moradia AS situacao_moradia
FROM aluno al
JOIN usuario u ON al.id_usuario = u.id_usuario
WHERE u.matricula = ?
"""
ADICIONAR_COLUNA_ESTADO = """
ALTER TABLE aluno ADD COLUMN estado TEXT NOT NULL
"""
ADICIONAR_COLUNA_COMPLEMENTO = """
ALTER TABLE aluno ADD COLUMN complemento TEXT NOT NULL
"""

# Queries para sistema de aprovação
OBTER_POSSIVEIS_ALUNOS = """
SELECT 
    u.id_usuario, u.nome, u.matricula, u.email, u.data_cadastro
FROM usuario u
LEFT JOIN aluno al ON u.id_usuario = al.id_usuario
WHERE u.perfil = 'aluno' AND (al.aprovado=0 OR al.id_usuario IS NULL)
ORDER BY u.data_cadastro DESC
"""

APROVAR_ALUNO = """
UPDATE aluno
SET aprovado = 1
WHERE id_usuario = ?
"""

REJEITAR_ALUNO = """
DELETE FROM aluno
WHERE id_usuario = ? AND aprovado=0
"""

EXISTE_ALUNO_APROVADO_POR_MATRICULA = """
SELECT 1
FROM aluno al
INNER JOIN usuario u ON al.id_usuario = u.id_usuario
WHERE u.matricula = ? AND al.aprovado = 1
"""