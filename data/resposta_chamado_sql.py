CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS resposta_chamado (
id_resposta_chamado INTEGER PRIMARY KEY AUTOINCREMENT,
id_chamado INTEGER FOREIGN KEY REFERENCES chamado(id_duvida) ON DELETE CASCADE,
id_usuario_autor INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
mensagem TEXT NOT NULL,
data_resposta DATE NOT NULL)
"""

INSERIR = """
INSERT INTO resposta_chamado (id_chamado, id_usuario_autor, mensagem, data_resposta)
VALUES (?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
id_resposta_chamado, id_chamado, id_usuario_autor, mensagem, data_resposta
FROM resposta_chamado
ORDER BY data_resposta
"""

OBTER_POR_ID = """
SELECT
id_resposta_chamado, id_chamado, id_usuario_autor, mensagem, data_resposta
FROM resposta_chamado
WHERE id_resposta_chamado = ?
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