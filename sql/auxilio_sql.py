CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS auxilio (
    id_auxilio INTEGER PRIMARY KEY AUTOINCREMENT,
    id_edital INTEGER,
    id_inscricao INTEGER,
    descricao TEXT NOT NULL,
    valor_mensal REAL NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    tipo_auxilio TEXT NOT NULL CHECK (
        tipo_auxilio IN ('auxilio alimentacao', 'auxilio material', 'auxilio moradia', 'auxilio transporte')
    ),
    status_auxilio TEXT DEFAULT 'pendente' CHECK (
        status_auxilio IN ('pendente', 'deferido', 'indeferido')
    ),
    FOREIGN KEY (id_edital) REFERENCES edital(id_edital) ON DELETE CASCADE,
    FOREIGN KEY (id_inscricao) REFERENCES inscricao(id_inscricao) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO auxilio (
    id_edital,
    id_inscricao,
    descricao,
    valor_mensal,
    data_inicio,
    data_fim,
    tipo_auxilio
) VALUES (?, ?, ?, ?, ?, ?, ?)
"""


OBTER_TODOS = """
SELECT
    a.id_auxilio,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio,
    a.status_auxilio
FROM auxilio a
INNER JOIN edital e ON a.id_edital = e.id_edital
INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao

"""

OBTER_POR_ID = """
SELECT
    a.id_auxilio, a.id_edital, a.id_inscricao, a.descricao,
    a.valor_mensal, a.data_inicio, a.data_fim, a.tipo_auxilio, a.status_auxilio
FROM auxilio a
LEFT JOIN edital e ON a.id_edital = e.id_edital
LEFT JOIN inscricao i ON a.id_inscricao = i.id_inscricao
WHERE a.id_auxilio = ?
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

ATUALIZAR_STATUS = """
UPDATE auxilio
SET status_auxilio = ?
WHERE id_auxilio = ?
"""

ATUALIZAR_VALOR = """
UPDATE auxilio
SET valor_mensal = ?
WHERE id_auxilio = ?
"""

OBTER_AUXILIOS_POR_INSCRICAO = """
SELECT
    a.id_auxilio,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio,
    a.status_auxilio
FROM auxilio a
WHERE a.id_inscricao = ?
ORDER BY a.tipo_auxilio
"""

OBTER_POR_ALUNO = """
SELECT
    a.id_auxilio,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio,
    a.status_auxilio,
    e.titulo as edital_titulo,
    i.status as status_inscricao
FROM auxilio a
INNER JOIN inscricao i ON a.id_inscricao = i.id_inscricao
INNER JOIN edital e ON a.id_edital = e.id_edital
WHERE i.id_aluno = ?
ORDER BY a.data_inicio DESC
"""