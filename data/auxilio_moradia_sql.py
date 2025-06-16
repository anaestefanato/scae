CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS auxilio_moradia (
id_auxilio_moradia INTEGER FOREIGN KEY REFERENCES auxilio(id_auxilio) ON DELETE CASCADE,
url_CompResidenciaFixa TEXT NOT NULL,
url_CompResidenciaAlugada TEXT NOT NULL,
url_ContratoAluguelCidCampus TEXT NOT NULL,
url_ContratoAluguelCidNatal TEXT NOT NULL)
"""

INSERIR = """
INSERT INTO auxilio_moradia (url_CompResidenciaFixa, url_CompResidenciaAlugada, url_ContratoAluguelCidCampus, url_ContratoAluguelCidNatal)
VALUES (?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
id_auxilio_moradia, url_CompResidenciaFixa, url_CompResidenciaAlugada, url_ContratoAluguelCidCampus, url_ContratoAluguelCidNatal
FROM auxilio_moradia
ORDER BY id_auxilio_moradia
"""

ATUALIZAR = """
UPDATE auxilio_moradia
SET id_auxilio_moradia = ?, url_CompResidenciaFixa = ?, url_CompResidenciaAlugada = ?, url_ContratoAluguelCidCampus = ?, url_ContratoAluguelCidNatal = ?
WHERE id_auxilio_moradia = ?
"""

EXCLUIR = """
DELETE FROM auxilio_moradia
WHERE id_auxilio_moradia = ?
"""