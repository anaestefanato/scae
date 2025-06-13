CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS recurso (
id_recurso INTEGER PRIMARY KEY AUTOINCREMENT,
id_inscricao INTEGER FOREIGN KEY REFERENCES inscricao(id_inscricao) ON DELETE CASCADE,
id_assistente INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
descricao TEXT NOT NULL,
data_envio DATE NOT NULL,
data_resposta DATE NOT NULL,
status TEXT NOT NULL CHECK (status IN ('pendente', 'respondido', 'rejeitado')))
"""

INSERIR = """
INSERT INTO recurso (id_inscricao, id_assistente, descricao, data_envio, data_resposta, status)
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
id_recurso, id_inscricao, id_assistente, descricao, data_envio, data_resposta, status
FROM recurso
ORDER BY data_envio
"""

OBTER_POR_ID = """
SELECT
id_recurso, id_inscricao, id_assistente, descricao, data_envio, data_resposta, status
FROM recurso
WHERE id_recurso = ?
"""

ATUALIZAR = """
UPDATE recurso
SET descricao = ?, data_envio = ?, data_resposta = ?, status = ?
WHERE id_recurso = ?
"""