CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS auxilio_transporte (
id_auxilio_transporte INTEGER FOREIGN KEY REFERENCES auxilio(id_auxilio) ON DELETE CASCADE)
"""

INSERIR = """
INSERT INTO auxilio_transporte (id_auxilio_transporte)
VALUES (?)
"""

OBTER_TODOS = """
SELECT
id_auxilio_transporte
FROM auxilio_transporte
ORDER BY id_auxilio_transporte
"""

ATUALIZAR = """
UPDATE auxilio_transporte
SET id_auxilio_transporte = ?
WHERE id_auxilio_transporte = ?
"""

EXCLUIR = """
DELETE FROM auxilio_transporte
WHERE id_auxilio_transporte = ?
"""