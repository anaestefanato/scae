CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS administrador (
id_usuario INTEGER PRIMARY KEY,
tipo_admin TEXT NOT NULL,
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

"""

INSERIR = """
INSERT INTO administrador (id_usuario, tipo_admin) 
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT
ad.id_usuario, 
    u.nome, 
    u.email, 
    u.senha, 
    u.perfil, 
    ad.tipo_admin 
FROM administrador ad
INNER JOIN usuario u ON ad.id_usuario = u.id_usuario
ORDER BY ad.tipo_admin
""" 

OBTER_POR_ID = """
SELECT 
    ad.id_usuario, 
    u.nome, 
    u.email, 
    u.senha, 
    u.perfil, 
    ad.tipo_admin 
FROM administrador ad
INNER JOIN usuario u ON ad.id_usuario = u.id_usuario
WHERE ad.id_usuario = ?
"""


ATUALIZAR = """
UPDATE administrador
SET tipo_admin = ?
WHERE id_usuario = ?
"""

EXCLUIR = """
DELETE FROM administrador
WHERE id_usuario = ?
"""