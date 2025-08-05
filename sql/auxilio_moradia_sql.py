CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS auxilio_moradia (
    id_auxilio_moradia INTEGER PRIMARY KEY,
    url_comp_residencia_fixa TEXT NOT NULL,
    url_comp_residencia_alugada TEXT NOT NULL,
    url_contrato_aluguel_cid_campus TEXT NOT NULL,
    url_contrato_aluguel_cid_natal TEXT NOT NULL,
    FOREIGN KEY (id_auxilio_moradia) REFERENCES auxilio(id_auxilio) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO auxilio_moradia (
    id_auxilio_moradia,
    url_comp_residencia_fixa,
    url_comp_residencia_alugada,
    url_contrato_aluguel_cid_campus,
    url_contrato_aluguel_cid_natal
) VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
    am.id_auxilio_moradia,
    am.url_comp_residencia_fixa,
    am.url_comp_residencia_alugada,
    am.url_contrato_aluguel_cid_campus,
    am.url_contrato_aluguel_cid_natal,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio
FROM auxilio_moradia am
INNER JOIN auxilio a ON am.id_auxilio_moradia = a.id_auxilio
ORDER BY am.id_auxilio_moradia
"""

OBTER_POR_ID = """
SELECT
    am.id_auxilio_moradia,
    am.url_comp_residencia_fixa,
    am.url_comp_residencia_alugada,
    am.url_contrato_aluguel_cid_campus,
    am.url_contrato_aluguel_cid_natal,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio
FROM auxilio_moradia am
INNER JOIN auxilio a ON am.id_auxilio_moradia = a.id_auxilio
WHERE am.id_auxilio_moradia = ?
"""

ATUALIZAR = """
UPDATE auxilio_moradia
SET
    url_comp_residencia_fixa = ?,
    url_comp_residencia_alugada = ?,
    url_contrato_aluguel_cid_campus = ?,
    url_contrato_aluguel_cid_natal = ?
WHERE id_auxilio_moradia = ?
"""

EXCLUIR = """
DELETE FROM auxilio_moradia
WHERE id_auxilio_moradia = ?
"""