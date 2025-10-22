CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS edital (
id_edital INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT NOT NULL,
descricao TEXT NOT NULL,
data_publicacao DATE NOT NULL,
arquivo TEXT NOT NULL,
status TEXT NOT NULL CHECK (status IN ('ativo', 'inativo')),
data_inicio_inscricao DATE,
data_fim_inscricao DATE,
data_inicio_vigencia DATE,
data_fim_vigencia DATE)
"""

INSERIR = """
INSERT INTO edital (titulo, descricao, data_publicacao, arquivo, status, 
data_inicio_inscricao, data_fim_inscricao, data_inicio_vigencia, data_fim_vigencia) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
id_edital, titulo, descricao, data_publicacao, arquivo, status,
data_inicio_inscricao, data_fim_inscricao, data_inicio_vigencia, data_fim_vigencia
FROM edital
ORDER BY data_publicacao DESC
""" 

OBTER_POR_ID = """
SELECT 
id_edital, titulo, descricao, data_publicacao, arquivo, status,
data_inicio_inscricao, data_fim_inscricao, data_inicio_vigencia, data_fim_vigencia
FROM edital
WHERE id_edital = ?
""" 

ATUALIZAR = """
UPDATE edital
SET titulo = ?, descricao = ?, arquivo = ?, status = ?,
data_inicio_inscricao = ?, data_fim_inscricao = ?, data_inicio_vigencia = ?, data_fim_vigencia = ?
WHERE id_edital = ?
"""

EXCLUIR = """
DELETE FROM edital
WHERE id_edital = ?
"""

OBTER_EDITAIS_ABERTOS = """
SELECT 
    e.id_edital, e.titulo, e.descricao, e.data_publicacao, e.arquivo, e.status,
    e.data_inicio_inscricao, e.data_fim_inscricao, e.data_inicio_vigencia, e.data_fim_vigencia,
    (SELECT ROUND(AVG(a.valor_mensal), 2) FROM auxilio a 
     INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao 
     WHERE i.id_edital = e.id_edital) as valor_medio
FROM edital e
WHERE e.status = 'ativo' 
    AND date('now') BETWEEN e.data_inicio_inscricao AND e.data_fim_inscricao
ORDER BY e.data_fim_inscricao ASC
"""

OBTER_EDITAIS_VISIVEIS_ALUNOS = """
SELECT 
    id_edital, titulo, descricao, data_publicacao, arquivo, status,
    data_inicio_inscricao, data_fim_inscricao, data_inicio_vigencia, data_fim_vigencia
FROM edital
WHERE status = 'ativo' 
    AND data_publicacao <= ?
ORDER BY data_publicacao DESC
"""