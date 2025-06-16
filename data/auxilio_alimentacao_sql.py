CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS auxilio_alimentacao (
    id_auxilio_alimentacao INTEGER FOREIGN KEY REFERENCES auxilio(id_auxilio) ON DELETE CASCADE,
"""

INSERIR = """
INSERT INTO auxilio_alimentacao (id_auxilio_alimentacao)
VALUES (?)
"""

OBTER_TODOS = """
SELECT 
id_auxilio_alimentacao
FROM auxilio_alimentacao
ORDER BY id_auxilio_alimentacao
"""

OBTER_POR_ID = """
SELECT
id_auxilio_alimentacao
FROM auxilio_alimentacao
WHERE id_auxilio_alimentacao = ?
"""


ATUALIZAR = """                   # Verificar se a atualização é necessária
UPDATE auxilio_alimentacao
SET id_auxilio_alimentacao = ?
WHERE id_auxilio_alimentacao = ?
"""

EXCLUIR = """
DELETE FROM auxilio_alimentacao
WHERE id_auxilio_alimentacao = ?
"""