CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
senha TEXT NOT NULL,
tipo TEXT NOT NULL
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, tipo_usuario) 
VALUES (?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
id_usuario, nome, email, senha, tipo_usuario 
FROM usuario
ORDER BY nome
""" 

OBTER_POR_ID = """
SELECT 
id_usuario, nome, email, senha, tipo_usuario 
FROM usuario
WHERE id_usuario = ?
""" 

OBTER_POR_EMAIL = """
SELECT
id_usuario, nome, email, senha, tipo_usuario
FROM usuario
WHERE email = ?
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT id_usuario, nome, email, senha, tipo_usuario
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

ATUALIZAR = """
UPDATE usuario
SET nome = ?, email = ?, tipo_usuario = ?
WHERE id_usuario = ?
"""

ATUALIZAR_SENHA = """
UPDATE usuario
SET senha = ?
WHERE id_usuario = ?
"""
ATUALIZAR_TIPO_USUARIO = """
UPDATE usuario
SET tipo_usuario = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM usuario
WHERE id_usuario = ?
"""