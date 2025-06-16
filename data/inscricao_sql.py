CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS inscricao (
id_inscricao INTEGER PRIMARY KEY AUTOINCREMENT,
id_aluno INTEGER FOREIGN KEY REFERENCES aluno(id_usuario) ON DELETE CASCADE,
id_edital INTEGER FOREIGN KEY REFERENCES edital(id_edital) ON DELETE CASCADE,
data_inscricao DATE NOT NULL,
status TEXT NOT NULL CHECK (status IN ('pendente', 'daferido', 'indeferido')),
url_Documento_Identificacao TEXT NOT NULL,
urlDeclaracaoRenda TEXT NOT NULL,
url_Termo_Responsabilidade TEXT NOT NULL)
"""

INSERIR = """
INSERT INTO inscricao (data_inscricao, status, url_Documento_Identificacao, urlDeclaracaoRenda, url_Termo_Responsabilidade) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
id_inscricao, id_aluno, id_edital, data_inscricao, status, url_Documento_Identificacao, urlDeclaracaoRenda, url_Termo_Responsabilidade 
FROM inscricao
ORDER BY data_inscricao
""" 

OBTER_POR_ID = """
SELECT
id_inscricao, id_aluno, id_edital, data_inscricao, status, url_Documento_Identificacao, urlDeclaracaoRenda, url_Termo_Responsabilidade
FROM inscricao
WHERE id_inscricao = ?
""" 

ATUALIZAR = """
UPDATE inscricao
SET status = ?, url_Documento_Identificacao = ?, urlDeclaracaoRenda = ?, url_Termo_Responsabilidade = ?
WHERE id_inscricao = ?
"""

EXCLUIR = """
DELETE FROM inscricao
WHERE id_inscricao = ?
"""