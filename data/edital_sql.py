CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS edital (
id_edital INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT NOT NULL,
descricao TEXT NOT NULL,
data_publicacao DATE NOT NULL,
data_encerramento DATE NOT NULL,
arquivo TEXT NOT NULL,
status TEXT NOT NULL CHECK (status IN ('ativo', 'inativo')))
"""

INSERIR = """
INSERT INTO edital (titulo, descricao, data_publicacao, data_encerramento, arquivo, status) 
VALUES (?, ?, ?, ?,? ?)
"""

OBTER_TODOS = """
SELECT 
id_edital, titulo, descricao, data_publicacao, data_encerramento, arquivo, status 
FROM edital
ORDER BY data_publicacao
""" 

OBTER_POR_ID = """
SELECT 
id_edital, titulo, descricao, data_publicacao, data_encerramento, arquivo, status 
FROM edital
WHERE id_edital = ?
""" 

ATUALIZAR = """
UPDATE edital
SET titulo = ?, descricao = ?, data_publicacao = ?, data_encerramento = ?, arquivo = ?, status = ?
WHERE id_edital = ?
"""

EXCLUIR = """
DELETE FROM edital
WHERE id_edital = ?
"""