CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS auxilio_material (
id_auxilio_material INTEGER FOREIGN KEY REFERENCES auxilio(id_auxilio) ON DELETE CASCADE)
"""

INSERIR = """
INSERT INTO auxilio_material (id_auxilio_material)
VALUES (?)
"""

OBTER_TODOS = """
SELECT
id_auxilio_material
FROM auxilio_material
ORDER BY id_auxilio_material
"""

OBTER_POR_ID = """
SELECT
id_auxilio_material
FROM auxilio_material
WHERE id_auxilio_material = ?
"""

ATUALIZAR = """
UPDATE auxilio_material
SET id_auxilio_material = ?
WHERE id_auxilio_material = ?
"""

EXCLUIR = """
DELETE FROM auxilio_material
WHERE id_auxilio_material = ?
"""