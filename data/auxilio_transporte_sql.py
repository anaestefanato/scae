CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS auxilio_transporte (
    id_auxilio_transporte INTEGER PRIMARY KEY,
    urlCompResidencia TEXT NOT NULL,
    urlCompTransporte TEXT NOT NULL,
    FOREIGN KEY (id_auxilio_transporte) REFERENCES auxilio(id_auxilio) ON DELETE CASCADE
)

"""

INSERIR = """
INSERT INTO auxilio_transporte (url_CompResidencia, url_CompTransporte)
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT
id_auxilio_transporte, url_CompResidencia, url_CompTransporte
FROM auxilio_transporte at
INNER JOIN auxilio a ON at.id_auxilio_transporte = a.id_auxilio
ORDER BY id_auxilio_transporte
"""

OBTER_POR_ID = """
SELECT
id_auxilio_transporte, url_CompResidencia, url_CompTransporte
FROM auxilio_transporte at
INNER JOIN auxilio a ON at.id_auxilio_transporte = a.id_auxilio
WHERE id_auxilio_transporte = ?
"""

ATUALIZAR = """
UPDATE auxilio_transporte
SET id_auxilio_transporte = ?, url_CompResidencia = ?, url_CompTransporte = ?
WHERE id_auxilio_transporte = ?
"""

EXCLUIR = """
DELETE FROM auxilio_transporte
WHERE id_auxilio_transporte = ?
"""