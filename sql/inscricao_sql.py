CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS inscricao (
    id_inscricao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_aluno INTEGER,
    id_edital INTEGER,
    data_inscricao DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pendente', 'analisado', 'deferido', 'indeferido')),
    urlDocumentoIdentificacao TEXT NOT NULL,
    urlDeclaracaoRenda TEXT NOT NULL,
    urlTermoResponsabilidade TEXT NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_edital) REFERENCES edital(id_edital) ON DELETE CASCADE
);
"""


INSERIR = """
INSERT INTO inscricao (
    id_aluno,
    id_edital,
    data_inscricao,
    status,
    urlDocumentoIdentificacao,
    urlDeclaracaoRenda,
    urlTermoResponsabilidade
) VALUES (?, ?, ?, ?, ?, ?, ?)
"""


OBTER_POR_PAGINA = """
SELECT
    i.id_inscricao,
    i.id_aluno,
    i.id_edital,
    i.data_inscricao,
    i.status,
    i.urlDocumentoIdentificacao,
    i.urlDeclaracaoRenda,
    i.urlTermoResponsabilidade
FROM inscricao i
INNER JOIN aluno al ON i.id_aluno = al.id_usuario
INNER JOIN edital e ON i.id_edital = e.id_edital
ORDER BY i.data_inscricao
LIMIT ? OFFSET ?
"""

OBTER_POR_ID = """
SELECT
    i.id_inscricao,
    i.id_aluno,
    i.id_edital,
    i.data_inscricao,
    i.status,
    i.urlDocumentoIdentificacao,
    i.urlDeclaracaoRenda,
    i.urlTermoResponsabilidade
FROM inscricao i
INNER JOIN aluno al ON i.id_aluno = al.id_usuario
INNER JOIN edital e ON i.id_edital = e.id_edital
WHERE i.id_inscricao = ?
"""

ATUALIZAR = """
UPDATE inscricao
SET status = ?, urlDocumentoIdentificacao = ?, urlDeclaracaoRenda = ?, urlTermoResponsabilidade = ?
WHERE id_inscricao = ?
"""

EXCLUIR = """
DELETE FROM inscricao
WHERE id_inscricao = ?
"""

OBTER_POR_ALUNO = """
SELECT
    i.id_inscricao,
    i.id_aluno,
    i.id_edital,
    i.data_inscricao,
    i.status,
    i.urlDocumentoIdentificacao,
    i.urlDeclaracaoRenda,
    i.urlTermoResponsabilidade,
    e.titulo as edital_titulo,
    e.data_publicacao,
    e.data_fim_inscricao,
    a.id_auxilio,
    a.tipo_auxilio,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim
FROM inscricao i
INNER JOIN edital e ON i.id_edital = e.id_edital
LEFT JOIN auxilio a ON i.id_inscricao = a.id_inscricao
WHERE i.id_aluno = ?
ORDER BY i.data_inscricao DESC
"""

OBTER_ESTATISTICAS_ANALISE = """
SELECT 
    COUNT(CASE WHEN status = 'pendente' THEN 1 END) as pendentes,
    COUNT(CASE WHEN status = 'em_analise' THEN 1 END) as em_analise,
    COUNT(CASE WHEN status IN ('deferido', 'indeferido') AND DATE(data_inscricao) = DATE('now') THEN 1 END) as analisadas_hoje,
    COUNT(*) as total_analisadas
FROM inscricao
"""

OBTER_INSCRICOES_PARA_ANALISE = """
SELECT 
    i.id_inscricao,
    i.id_aluno,
    i.id_edital,
    i.data_inscricao,
    i.status,
    i.urlDocumentoIdentificacao,
    i.urlDeclaracaoRenda,
    i.urlTermoResponsabilidade,
    e.titulo as edital_titulo,
    e.data_encerramento,
    u.nome as aluno_nome,
    u.matricula as aluno_matricula,
    a.tipo_auxilio,
    a.valor_mensal,
    CASE 
        WHEN DATE(e.data_encerramento) <= DATE('now', '+7 days') THEN 'Alta'
        WHEN DATE(e.data_encerramento) <= DATE('now', '+15 days') THEN 'Média'
        ELSE 'Baixa'
    END as prioridade
FROM inscricao i
INNER JOIN edital e ON i.id_edital = e.id_edital
INNER JOIN usuario u ON i.id_aluno = u.id_usuario
LEFT JOIN auxilio a ON i.id_inscricao = a.id_inscricao
WHERE i.status = 'pendente'
ORDER BY 
    CASE 
        WHEN DATE(e.data_encerramento) <= DATE('now', '+7 days') THEN 1
        WHEN DATE(e.data_encerramento) <= DATE('now', '+15 days') THEN 2
        ELSE 3
    END,
    i.data_inscricao ASC
LIMIT ? OFFSET ?
"""

CONTAR_INSCRICOES_PARA_ANALISE = """
SELECT COUNT(*) as total
FROM inscricao i
INNER JOIN edital e ON i.id_edital = e.id_edital
WHERE i.status = 'pendente'
"""

OBTER_ESTATISTICAS_DASHBOARD = """
SELECT 
    (SELECT COALESCE(COUNT(*), 0) FROM edital WHERE status = 'ativo') as editais_ativos,
    (SELECT COALESCE(COUNT(*), 0) 
     FROM inscricao i
     INNER JOIN edital e ON i.id_edital = e.id_edital
     INNER JOIN usuario u ON i.id_aluno = u.id_usuario
     WHERE i.status = 'pendente') as inscricoes_pendentes,
    (SELECT COALESCE(COUNT(DISTINCT i.id_aluno), 0) FROM inscricao i WHERE i.status = 'deferido') as alunos_beneficiados,
    (SELECT COALESCE(SUM(a.valor_mensal), 0.0) FROM auxilio a 
     INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao 
     WHERE i.status = 'deferido') as valor_total_mensal
"""

OBTER_INSCRICOES_RECENTES_DASHBOARD = """
SELECT 
    i.id_inscricao,
    i.data_inscricao,
    u.nome as aluno_nome,
    e.titulo as edital_titulo,
    a.tipo_auxilio,
    CASE 
        WHEN DATE(e.data_encerramento) <= DATE('now', '+7 days') THEN 'Alta'
        WHEN DATE(e.data_encerramento) <= DATE('now', '+15 days') THEN 'Média'
        ELSE 'Baixa'
    END as prioridade
FROM inscricao i
INNER JOIN edital e ON i.id_edital = e.id_edital
INNER JOIN usuario u ON i.id_aluno = u.id_usuario
LEFT JOIN auxilio a ON i.id_inscricao = a.id_inscricao
WHERE i.status IN ('pendente', 'em_analise')
ORDER BY 
    CASE 
        WHEN DATE(e.data_encerramento) <= DATE('now', '+7 days') THEN 1
        WHEN DATE(e.data_encerramento) <= DATE('now', '+15 days') THEN 2
        ELSE 3
    END,
    i.data_inscricao ASC
LIMIT 5
"""