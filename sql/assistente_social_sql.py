CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS assistente_social (
    id_usuario INTEGER,
    siape TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO assistente_social (id_usuario, siape) VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT 
a.id_usuario, u.nome, u.matricula, u.email, u.senha, u.perfil, u.foto, u.token_redefinicao, u.data_token, u.data_cadastro, a.siape
FROM assistente_social a
INNER JOIN usuario u ON a.id_usuario = u.id_usuario
ORDER BY a.siape
""" 

OBTER_POR_ID = """
SELECT 
a.id_usuario, u.nome, u.matricula, u.email, u.senha, u.perfil, u.foto, u.token_redefinicao, u.data_token, u.data_cadastro, a.siape
FROM assistente_social a
INNER JOIN usuario u ON a.id_usuario = u.id_usuario
WHERE a.id_usuario = ?
"""

ATUALIZAR = """
UPDATE assistente_social
SET siape = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM assistente_social
WHERE id_usuario = ?
"""