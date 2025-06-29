CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS administrador (
id_usuario INTEGER PRIMARY KEY,
matricula TEXT NOT NULL,
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

"""

INSERIR = """
INSERT INTO administrador (id_usuario, matricula) 
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT 
id_usuario, matricula 
FROM administrador ad
INNER JOIN usuario u ON ad.id_usuario = u.id_usuario
ORDER BY matricula
""" 

OBTER_POR_ID = """
SELECT 
    ad.id_usuario, 
    u.nome, 
    u.email, 
    u.senha, 
    u.tipo_usuario, 
    ad.matricula 
FROM administrador ad
INNER JOIN usuario u ON ad.id_usuario = u.id_usuario
WHERE ad.id_usuario = ?
"""


ATUALIZAR = """
UPDATE administrador
SET matricula = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM administrador
WHERE id_usuario = ?
"""