CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS inscricao (
    id_inscricao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_aluno INTEGER,
    id_edital INTEGER,
    data_inscricao DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pendente', 'deferido', 'indeferido')),
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
    e.data_encerramento,
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