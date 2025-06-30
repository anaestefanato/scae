CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS auxilio_transporte (
    id_auxilio_transporte INTEGER PRIMARY KEY,
    urlCompResidencia TEXT NOT NULL,
    urlCompTransporte TEXT NOT NULL,
    FOREIGN KEY (id_auxilio_transporte) REFERENCES auxilio(id_auxilio) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO auxilio_transporte (id_auxilio_transporte, urlCompResidencia, urlCompTransporte)
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT
    at.id_auxilio_transporte,
    at.urlCompResidencia,
    at.urlCompTransporte,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio
FROM auxilio_transporte at
INNER JOIN auxilio a ON at.id_auxilio_transporte = a.id_auxilio
ORDER BY at.id_auxilio_transporte
"""

OBTER_POR_ID = """
SELECT
    at.id_auxilio_transporte,
    at.urlCompResidencia,
    at.urlCompTransporte,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio
FROM auxilio_transporte at
INNER JOIN auxilio a ON at.id_auxilio_transporte = a.id_auxilio
WHERE at.id_auxilio_transporte = ?
"""

ATUALIZAR = """
UPDATE auxilio_transporte
SET urlCompResidencia = ?, urlCompTransporte = ?
WHERE id_auxilio_transporte = ?
"""

EXCLUIR = """
DELETE FROM auxilio_transporte
WHERE id_auxilio_transporte = ?
"""
