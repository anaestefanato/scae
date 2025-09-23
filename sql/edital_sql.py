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
INSERT INTO edital (id_edital, titulo, descricao, data_publicacao, data_encerramento, arquivo, status) 
VALUES (?, ?, ?, ?, ?, ?, ?)
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
SET titulo = ?, descricao = ?, data_encerramento = ?, arquivo = ?, status = ?
WHERE id_edital = ?
"""

EXCLUIR = """
DELETE FROM edital
WHERE id_edital = ?
"""

OBTER_EDITAIS_ABERTOS = """
SELECT 
    e.id_edital, e.titulo, e.descricao, e.data_publicacao, e.data_encerramento, e.arquivo, e.status,
    (SELECT ROUND(AVG(a.valor_mensal), 2) FROM auxilio a 
     INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao 
     WHERE i.id_edital = e.id_edital) as valor_medio
FROM edital e
WHERE e.status = 'ativo' 
    AND date('now') <= e.data_encerramento
ORDER BY e.data_encerramento ASC
"""