CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS recurso (
    id_recurso INTEGER PRIMARY KEY AUTOINCREMENT,
    id_inscricao INTEGER NOT NULL,
    id_assistente INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    data_envio DATE NOT NULL,
    data_resposta DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pendente', 'respondido', 'rejeitado')),
    FOREIGN KEY (id_inscricao) REFERENCES inscricao(id_inscricao) ON DELETE CASCADE,
    FOREIGN KEY (id_assistente) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO recurso (id_inscricao, id_assistente, descricao, data_envio, data_resposta, status)
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_POR_PAGINA = """
SELECT
    r.id_recurso,
    r.id_inscricao,
    r.id_assistente,
    r.descricao,
    r.data_envio,
    r.data_resposta,
    r.status
FROM recurso r
INNER JOIN inscricao i ON r.id_inscricao = i.id_inscricao
INNER JOIN usuario u ON r.id_assistente = u.id_usuario
ORDER BY r.data_envio
LIMIT ? OFFSET ?
"""

OBTER_POR_ID = """
SELECT
    r.id_recurso,
    r.id_inscricao,
    r.id_assistente,
    r.descricao,
    r.data_envio,
    r.data_resposta,
    r.status
FROM recurso r
INNER JOIN inscricao i ON r.id_inscricao = i.id_inscricao
INNER JOIN usuario u ON r.id_assistente = u.id_usuario
WHERE r.id_recurso = ?
"""

ATUALIZAR = """
UPDATE recurso
SET descricao = ?, status = ?
WHERE id_recurso = ?
"""

EXCLUIR = """
DELETE FROM recurso
WHERE id_recurso = ?
"""