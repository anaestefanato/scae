CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS administrador (
id_usuario INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
matricula TEXT NOT NULL)
"""

INSERIR = """
INSERT INTO administrador (matricula) 
VALUES (?)
"""

OBTER_TODOS = """
SELECT 
id_usuario, matricula 
FROM administrador
ORDER BY matricula
""" 

OBTER_POR_ID = """
SELECT 
id_usuario, matricula 
FROM administrador
WHERE id_usuario = ?
""" 

ATUALIZAR = """
UPDATE administrador
SET matricula = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM administrador
WHERE id_usuario = ?
"""