CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS duvida_edital (
id_duvida INTEGER PRIMARY KEY AUTOINCREMENT,
id_edital INTEGER FOREIGN KEY REFERENCES edital(id_edital) ON DELETE CASCADE,
id_aluno INTEGER FOREIGN KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
pergunta TEXT NOT NULL,
resposta TEXT NOT NULL,
data_pergunta DATE NOT NULL,
data_resposta DATE NOT NULL,
status TEXT NOT NULL CHECK (status IN ('pendente', 'respondido', 'rejeitado')))
"""

INSERIR = """
INSERT INTO duvida_edital (id_edital, id_aluno, pergunta, resposta, data_pergunta, data_resposta, status)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
id_duvida, id_edital, id_aluno, pergunta, resposta, data_pergunta, data_resposta, status
FROM duvida_edital
ORDER BY status
"""

OBTER_POR_ID = """
SELECT
id_duvida, id_edital, id_aluno, pergunta, resposta, data_pergunta, data_resposta, status
FROM duvida_edital
WHERE id_duvida = ?
"""

ATUALIZAR = """
UPDATE duvida_edital
SET pergunta = ?, resposta = ?, status = ?
WHERE id_duvida = ?
"""

EXCLUIR = """
DELETE FROM duvida_edital
WHERE id_duvida = ?
"""