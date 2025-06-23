CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS auxilio (
id_auxilio INTEGER PRIMARY KEY AUTOINCREMENT,
id_edital INTEGER FOREIGN KEY REFERENCES edital(id_edital) ON DELETE CASCADE,
id_inscricao INTEGER FOREIGN KEY REFERENCES inscricao(id_inscricao) ON DELETE CASCADE,
descricao TEXT NOT NULL,
valor_mensal REAL NOT NULL,
data_inicio DATE NOT NULL,
data_fim DATE NOT NULL,
tipo_auxilio TEXT NOT NULL CHECK (tipo_auxilio IN ("auxilio alimantacao, 'auxilio material', 'auxilio moradia', 'auxilio transporte')))
"""

INSERIR = """
INSERT INTO auxilio (id_edital, id_inscricao, descricao, valor_mensal, data_inicio, data_fim, tipo_auxilio)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
id_auxilio, id_edital, id_inscricao, descricao, valor_mensal, data_inicio, data_fim, tipo_auxilio
FROM auxilio
JOIN edital ON auxilio.id_edital = edital.id_edital
JOIN inscricao ON auxilio.id_inscricao = inscricao.id_inscricao
ORDER BY tipo_auxilio
"""

OBTER_POR_ID = """
SELECT
id_auxilio, id_edital, id_inscricao, descricao, valor_mensal, data_inicio, data_fim, tipo_auxilio
FROM auxilio
WHERE id_auxilio = ?
"""

ATUALIZAR = """
UPDATE auxilio
SET descricao = ?, valor_mensal = ?, data_fim = ?, tipo_auxilio = ?
WHERE id_auxilio = ?
"""

EXCLUIR = """
DELETE FROM auxilio
WHERE id_auxilio = ?
"""