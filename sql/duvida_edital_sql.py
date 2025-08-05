CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS duvida_edital (
    id_duvida INTEGER PRIMARY KEY AUTOINCREMENT,
    id_edital INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    pergunta TEXT NOT NULL,
    resposta TEXT,
    data_pergunta TEXT NOT NULL,
    data_resposta TEXT,
    status TEXT NOT NULL,
    FOREIGN KEY (id_edital) REFERENCES edital(id_edital) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_aluno) REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

INSERIR = """
INSERT INTO duvida_edital (
    id_edital, id_aluno, pergunta, resposta, data_pergunta, data_resposta, status
) VALUES (?, ?, ?, ?, ?, ?, ?);
"""

OBTER_POR_ID = "SELECT * FROM duvida_edital WHERE id_duvida = ?;"

OBTER_POR_PAGINA = """
SELECT * FROM duvida_edital
ORDER BY data_pergunta DESC
LIMIT ? OFFSET ?;
"""

ATUALIZAR = """
UPDATE duvida_edital SET
    pergunta = ?,
    resposta = ?,
    data_pergunta = ?,
    data_resposta = ?,
    status = ?
WHERE id_duvida = ?;
"""

EXCLUIR = "DELETE FROM duvida_edital WHERE id_duvida = ?;"
