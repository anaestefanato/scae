CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS administrador (
matricula TEXT PRIMARY KEY,
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario))
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