CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS chamado (
id_duvida INTEGER PRIMARY KEY AUTOINCREMENT,
id_usuario_criador INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
id_administrador_responsavel INTEGER FOREIGN KEY REFERENCES administrador(id_usuario) ON DELETE CASCADE,
titulo TEXT NOT NULL,
descricao TEXT NOT NULL,
data_criacao DATE NOT NULL,
status TEXT NOT NULL CHECK (status IN ('em_andamento', 'concluìdo')))
"""

INSERIR = """
INSERT INTO chamado (id_usuario_criador, id_administrador_responsavel, titulo, descricao, data_criacao, status)
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
id_duvida, id_usuario_criador, id_administrador_responsavel, titulo, descricao, data_criacao, status
FROM chamado c
INNER JOIN usuario u ON c.id_usuario_criador = u.id_usuario
INNER JOIN administrador ad ON c.id_administrador_responsavel = ad.id_usuario
ORDER BY id_usuario_criador
"""

OBTER_POR_ID = """
SELECT
id_duvida, id_usuario_criador, id_administrador_responsavel, titulo, descricao, data_criacao, status
FROM chamado
WHERE id_duvida = ?
"""

ATUALIZAR = """
UPDATE chamado
SET titulo = ?, descricao = ?, status = ?
WHERE id_duvida = ?
"""

EXCLUIR = """
DELETE FROM chamado
WHERE id_duvida = ?
"""