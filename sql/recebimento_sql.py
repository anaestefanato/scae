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
    data_confirmacao DATE,
    comprovante_transporte TEXT,
    comprovante_moradia TEXT,
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

CONFIRMAR_RECEBIMENTO = """
UPDATE recebimento
SET status = 'confirmado',
    data_confirmacao = datetime('now'),
    comprovante_transporte = ?,
    comprovante_moradia = ?
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

INSERIR_DADOS_EXEMPLO = """
-- Dados de exemplo inseridos pela função inserir_dados_exemplo() no repositório
INSERT INTO recebimento (id_auxilio, mes_referencia, ano_referencia, valor, data_recebimento, status, observacoes) 
SELECT a.id_auxilio, 'Janeiro', 2025, 200.00, datetime('now', '-60 days'), 'confirmado', 'Primeiro recebimento'
FROM auxilio a
INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
WHERE i.status = 'deferido' AND i.id_aluno = ?
LIMIT 1;

INSERT INTO recebimento (id_auxilio, mes_referencia, ano_referencia, valor, data_recebimento, status, observacoes) 
SELECT a.id_auxilio, 'Fevereiro', 2025, 200.00, datetime('now', '-30 days'), 'confirmado', 'Segundo recebimento'
FROM auxilio a
INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
WHERE i.status = 'deferido' AND i.id_aluno = ?
LIMIT 1;

INSERT INTO recebimento (id_auxilio, mes_referencia, ano_referencia, valor, data_recebimento, status, observacoes) 
SELECT a.id_auxilio, 'Março', 2025, 200.00, datetime('now', '-5 days'), 'pendente', 'Terceiro recebimento - aguardando confirmação'
FROM auxilio a
INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
WHERE i.status = 'deferido' AND i.id_aluno = ?
LIMIT 1
"""

