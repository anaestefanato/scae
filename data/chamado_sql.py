CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS chamado (
id_duvida INTEGER PRIMARY KEY AUTOINCREMENT,
id_usuario_criador INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
id_administrador_responsavel INTEGER FOREIGN KEY REFERENCES administrador(id_usuario) ON DELETE CASCADE,
titulo TEXT NOT NULL,
descricao TEXT NOT NULL,
data_criacao DATE NOT NULL,
status TEXT NOT NULL CHECK (status IN ('em_andamento', 'concluído')))
"""

INSERIR = """
INSERT INTO chamado (id_usuario_criador, id_administrador_responsavel, titulo, descricao, data_criacao, status)
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_POR_PAGINA = """
SELECT
    c.id_duvida,
    c.id_usuario_criador,
    c.id_administrador_responsavel,
    c.titulo,
    c.descricao,
    c.data_criacao,
    c.status,
    u.nome AS nome_usuario_criador,
    a.nome AS nome_administrador_responsavel
FROM chamado c
INNER JOIN usuario u ON c.id_usuario_criador = u.id_usuario
INNER JOIN administrador a ON c.id_administrador_responsavel = a.id_usuario
ORDER BY n.data_criacao 
LIMIT ? OFFSET ?
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