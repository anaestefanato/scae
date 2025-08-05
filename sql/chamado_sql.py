CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS chamado (
    id_chamado INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario_criador INTEGER NOT NULL,
    id_administrador_responsavel INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data_criacao DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('em_andamento', 'concluído')),
    FOREIGN KEY (id_usuario_criador) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_administrador_responsavel) REFERENCES administrador(id_usuario) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO chamado (
    id_usuario_criador,
    id_administrador_responsavel,
    titulo,
    descricao,
    data_criacao,
    status
)
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_POR_ID = """
SELECT
    id_chamado,
    id_usuario_criador,
    id_administrador_responsavel,
    titulo,
    descricao,
    data_criacao,
    status
FROM chamado
WHERE id_chamado = ?
"""

OBTER_POR_PAGINA = """
SELECT
    c.id_chamado,
    c.id_usuario_criador,
    c.id_administrador_responsavel,
    c.titulo,
    c.descricao,
    c.data_criacao,
    c.status
FROM chamado c
ORDER BY c.data_criacao
LIMIT ? OFFSET ?
"""

ATUALIZAR = """
UPDATE chamado
SET titulo = ?, descricao = ?, status = ?
WHERE id_chamado = ?
"""

EXCLUIR = """
DELETE FROM chamado
WHERE id_chamado = ?
"""
