CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL,
senha TEXT NOT NULL,
tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('administrador', 'aluno', 'assistente')))
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

ATUALIZAR = """
UPDATE usuario
SET nome = ?, email = ?, senha = ?, tipo_usuario = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM usuario
WHERE id_usuario = ?
"""