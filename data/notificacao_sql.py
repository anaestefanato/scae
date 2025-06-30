CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS notificacao (
id_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
id_usuario_destinatario INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
titulo TEXT NOT NULL,
data_envio DATE NOT NULL,
tipo TEXT NOT NULL)
"""

INSERIR = """
INSERT INTO notificacao (id_usuario_destinatario, titulo, data_envio, tipo)
VALUES (?, ?, ?, ?)
"""
#terminar
OBTER_POR_PAGINA = """
SELECT
    n.id_notificacao,
    n.id_usuario_destinatario, n.titulo, n.data_envio, n.tipo,
FROM inscricao i
INNER JOIN aluno al ON i.id_aluno = al.id_usuario
INNER JOIN edital e ON i.id_edital = e.id_edital
ORDER BY i.data_inscricao
LIMIT ? OFFSET ?
"""

OBTER_POR_ID = """
SELECT
id_notificacao, id_usuario_destinatario, titulo, data_envio, tipo
FROM notificacao n
INNER JOIN usuario u ON n.id_usuario_destinatario = u.id_usuario
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
