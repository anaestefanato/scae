CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS assistente_social (
id_usuario INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
matricula TEXT NOT NULL)
"""

INSERIR = """
INSERT INTO assistente_social (matricula) 
VALUES (?)
"""

OBTER_TODOS = """
SELECT 
id_usuario, matricula 
FROM assistente_social as
INNER JOIN usuario u ON as.id_usuario = u.id_usuario
ORDER BY matricula
""" 

OBTER_POR_ID = """
SELECT 
id_usuario, matricula 
FROM assistente_social as
INNER JOIN usuario u ON as.id_usuario = u.id_usuario
WHERE id_usuario = ?
""" 

ATUALIZAR = """
UPDATE assistente_social
SET matricula = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM assistente_social
WHERE id_usuario = ?
"""