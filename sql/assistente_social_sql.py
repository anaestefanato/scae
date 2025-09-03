CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS assistente_social (
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO assistente_social (id_usuario, matricula) VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT 
a.id_usuario, u.nome, u.email, u.senha, u.tipo_usuario, a.matricula
FROM assistente_social a
INNER JOIN usuario u ON a.id_usuario = u.id_usuario
ORDER BY a.matricula
""" 

OBTER_POR_ID = """
SELECT 
a.id_usuario, u.nome, u.email, u.senha, u.tipo_usuario, a.matricula
FROM assistente_social a
INNER JOIN usuario u ON a.id_usuario = u.id_usuario
WHERE a.id_usuario = ?
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