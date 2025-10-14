CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS auxilio_transporte (
    id_auxilio_transporte INTEGER PRIMARY KEY,
    tipo_transporte TEXT NOT NULL,
    tipo_onibus TEXT,
    gasto_passagens_dia REAL,
    gasto_van_mensal REAL,
    urlCompResidencia TEXT,
    urlPasseEscolarFrente TEXT,
    urlPasseEscolarVerso TEXT,
    urlComprovanteRecarga TEXT,
    urlComprovantePassagens TEXT,
    urlContratoTransporte TEXT,
    
    FOREIGN KEY (id_auxilio_transporte) REFERENCES auxilio(id_auxilio) ON DELETE CASCADE
)
"""

INSERIR = """
INSERT INTO auxilio_transporte (
    id_auxilio_transporte, 
    tipo_transporte, 
    tipo_onibus, 
    gasto_passagens_dia, 
    gasto_van_mensal,
    urlCompResidencia, 
    urlPasseEscolarFrente,
    urlPasseEscolarVerso,
    urlComprovanteRecarga,
    urlComprovantePassagens,
    urlContratoTransporte
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT
    at.id_auxilio_transporte,
    at.tipo_transporte,
    at.tipo_onibus,
    at.gasto_passagens_dia,
    at.gasto_van_mensal,
    at.urlCompResidencia,
    at.urlPasseEscolarFrente,
    at.urlPasseEscolarVerso,
    at.urlComprovanteRecarga,
    at.urlComprovantePassagens,
    at.urlContratoTransporte,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio
FROM auxilio_transporte at
INNER JOIN auxilio a ON at.id_auxilio_transporte = a.id_auxilio
ORDER BY at.id_auxilio_transporte
"""

OBTER_POR_ID = """
SELECT
    at.id_auxilio_transporte,
    at.tipo_transporte,
    at.tipo_onibus,
    at.gasto_passagens_dia,
    at.gasto_van_mensal,
    at.urlCompResidencia,
    at.urlPasseEscolarFrente,
    at.urlPasseEscolarVerso,
    at.urlComprovanteRecarga,
    at.urlComprovantePassagens,
    at.urlContratoTransporte,
    a.id_edital,
    a.id_inscricao,
    a.descricao,
    a.valor_mensal,
    a.data_inicio,
    a.data_fim,
    a.tipo_auxilio
FROM auxilio_transporte at
INNER JOIN auxilio a ON at.id_auxilio_transporte = a.id_auxilio
WHERE at.id_auxilio_transporte = ?
"""

ATUALIZAR = """
UPDATE auxilio_transporte
SET tipo_transporte = ?, 
    tipo_onibus = ?, 
    gasto_passagens_dia = ?, 
    gasto_van_mensal = ?,
    urlCompResidencia = ?, 
    urlPasseEscolarFrente = ?,
    urlPasseEscolarVerso = ?,
    urlComprovanteRecarga = ?,
    urlComprovantePassagens = ?,
    urlContratoTransporte = ?
WHERE id_auxilio_transporte = ?
"""

EXCLUIR = """
DELETE FROM auxilio_transporte
WHERE id_auxilio_transporte = ?
"""
