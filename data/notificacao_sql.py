CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS notificacao (
    id_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario_destinatario INTEGER,
    titulo TEXT NOT NULL,
    data_envio DATE NOT NULL,
    tipo TEXT NOT NULL,
    FOREIGN KEY (id_usuario_destinatario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO notificacao (id_usuario_destinatario, titulo, data_envio, tipo)
VALUES (?, ?, ?, ?)
"""

OBTER_POR_PAGINA = """
SELECT
    n.id_notificacao,
    n.id_usuario_destinatario,
    n.titulo,
    n.data_envio,
    n.tipo
FROM notificacao n
ORDER BY n.data_envio
LIMIT ? OFFSET ?
"""

OBTER_POR_ID = """
SELECT
    id_notificacao, id_usuario_destinatario, titulo, data_envio, tipo
FROM notificacao
WHERE id_notificacao = ?
"""

ATUALIZAR = """
UPDATE notificacao
SET titulo = ?, tipo = ?
WHERE id_notificacao = ?
"""

EXCLUIR = """
DELETE FROM notificacao
WHERE id_notificacao = ?
"""
