CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
matricula TEXT UNIQUE NOT NULL,
email TEXT NOT NULL,
senha TEXT NOT NULL,
perfil TEXT NOT NULL DEFAULT 'aluno',
foto TEXT,
token_redefinicao TEXT,
data_token TIMESTAMP,
data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERIR = """
INSERT INTO usuario (nome, matricula, email, senha, perfil) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
id_usuario, nome, matricula, email, senha, perfil 
FROM usuario
ORDER BY nome
""" 

OBTER_POR_ID = """
SELECT 
id_usuario, nome, matricula, email, senha, perfil 
FROM usuario
WHERE id_usuario = ?
""" 

OBTER_POR_MATRICULA = """
SELECT
id_usuario, nome, matricula, email, senha, perfil
FROM usuario
WHERE matricula = ?
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT id_usuario, nome, matricula, email, senha, perfil
FROM usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

ATUALIZAR = """
UPDATE usuario
SET nome = ?, email = ?
WHERE id_usuario = ?
"""

ATUALIZAR_SENHA = """
UPDATE usuario
SET senha = ?
WHERE id_usuario = ?
"""
ATUALIZAR_TOKEN = """
UPDATE usuario
SET token_redefinicao=?, data_token=?
WHERE email=?
"""

ATUALIZAR_FOTO = """
UPDATE usuario
SET foto=?
WHERE id=?
"""

OBTER_POR_TOKEN = """
SELECT 
id, nome, matricula, email, senha, perfil, foto, token_redefinicao, data_token
FROM usuario
WHERE token_redefinicao=? AND data_token > datetime('now')
"""

EXCLUIR = """
DELETE FROM usuario
WHERE id_usuario = ?
"""