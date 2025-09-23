CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS recebimento (
    id_recebimento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_auxilio INTEGER NOT NULL,
    mes_referencia TEXT NOT NULL,
    ano_referencia INTEGER NOT NULL,
    valor REAL NOT NULL,
    data_recebimento DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('confirmado', 'pendente', 'cancelado')),
    observacoes TEXT DEFAULT '',
    FOREIGN KEY (id_auxilio) REFERENCES auxilio(id_auxilio) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO recebimento (
    id_auxilio,
    mes_referencia,
    ano_referencia,
    valor,
    data_recebimento,
    status,
    observacoes
) VALUES (?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
    r.id_recebimento,
    r.id_auxilio,
    r.mes_referencia,
    r.ano_referencia,
    r.valor,
    r.data_recebimento,
    r.status,
    r.observacoes
FROM recebimento r
ORDER BY r.ano_referencia DESC, r.mes_referencia DESC
"""

OBTER_POR_ID = """
SELECT
    r.id_recebimento,
    r.id_auxilio,
    r.mes_referencia,
    r.ano_referencia,
    r.valor,
    r.data_recebimento,
    r.status,
    r.observacoes
FROM recebimento r
WHERE r.id_recebimento = ?
"""

ATUALIZAR = """
UPDATE recebimento
SET valor = ?, data_recebimento = ?, status = ?, observacoes = ?
WHERE id_recebimento = ?
"""

EXCLUIR = """
DELETE FROM recebimento
WHERE id_recebimento = ?
"""

OBTER_POR_ALUNO = """
SELECT
    r.id_recebimento,
    r.id_auxilio,
    r.mes_referencia,
    r.ano_referencia,
    r.valor,
    r.data_recebimento,
    r.status,
    r.observacoes,
    a.tipo_auxilio,
    e.titulo as edital_titulo
FROM recebimento r
INNER JOIN auxilio a ON r.id_auxilio = a.id_auxilio
INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
INNER JOIN edital e ON a.id_edital = e.id_edital
WHERE i.id_aluno = ?
ORDER BY r.ano_referencia DESC, 
    CASE r.mes_referencia
        WHEN 'Janeiro' THEN 1
        WHEN 'Fevereiro' THEN 2
        WHEN 'Março' THEN 3
        WHEN 'Abril' THEN 4
        WHEN 'Maio' THEN 5
        WHEN 'Junho' THEN 6
        WHEN 'Julho' THEN 7
        WHEN 'Agosto' THEN 8
        WHEN 'Setembro' THEN 9
        WHEN 'Outubro' THEN 10
        WHEN 'Novembro' THEN 11
        WHEN 'Dezembro' THEN 12
    END DESC
"""

OBTER_ESTATISTICAS_ALUNO = """
SELECT
    COUNT(*) as total_recebimentos,
    ROUND(SUM(r.valor), 2) as total_valor,
    COUNT(DISTINCT a.tipo_auxilio) as tipos_auxilio,
    ROUND(AVG(r.valor), 2) as valor_medio
FROM recebimento r
INNER JOIN auxilio a ON r.id_auxilio = a.id_auxilio
INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
WHERE i.id_aluno = ? AND r.status = 'confirmado'
"""

