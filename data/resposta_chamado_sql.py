CRIAR_TABELA = """ 
CREATE TABLE IF NOT EXISTS resposta_chamado (
    id_resposta_chamado INTEGER PRIMARY KEY AUTOINCREMENT,
    id_chamado INTEGER,
    id_usuario_autor INTEGER,
    mensagem TEXT NOT NULL,
    data_resposta DATE NOT NULL,
    FOREIGN KEY (id_chamado) REFERENCES chamado(id_duvida) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario_autor) REFERENCES usuario(id_usuario) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO resposta_chamado (id_chamado, id_usuario_autor, mensagem, data_resposta)
VALUES (?, ?, ?, ?)
"""

OBTER_POR_PAGINA = """
SELECT
    rc.id_resposta_chamado,
    rc.id_chamado,
    rc.id_usuario_autor,
    rc.mensagem,
    rc.data_resposta
FROM resposta_chamado rc
INNER JOIN chamado c ON rc.id_chamado = c.id_chamado
INNER JOIN usuario u ON rc.id_usuario_autor = u.id_usuario
ORDER BY rc.data_resposta
LIMIT ? OFFSET ?
"""

OBTER_POR_ID = """
SELECT
    rc.id_resposta_chamado,
    rc.id_chamado,
    rc.id_usuario_autor,
    rc.mensagem,
    rc.data_resposta
FROM resposta_chamado rc
INNER JOIN chamado c ON rc.id_chamado = c.id_chamado
INNER JOIN usuario u ON rc.id_usuario_autor = u.id_usuario
WHERE rc.id_resposta_chamado = ?
"""

ATUALIZAR = """
UPDATE resposta_chamado
SET mensagem = ?
WHERE id_resposta_chamado = ?
"""

EXCLUIR = """
DELETE FROM resposta_chamado
WHERE id_resposta_chamado = ?
"""