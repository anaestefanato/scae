CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS chamado (
    id_chamado INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario_criador INTEGER NOT NULL,
    id_administrador_responsavel INTEGER NULL,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL DEFAULT 'outros',
    data_criacao DATE NOT NULL,
    data_ultima_atualizacao DATE NULL,
    status TEXT NOT NULL DEFAULT 'aberto' CHECK (status IN ('aberto', 'em-andamento', 'resolvido')),
    FOREIGN KEY (id_usuario_criador) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_administrador_responsavel) REFERENCES administrador(id_usuario) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO chamado (
    id_usuario_criador,
    id_administrador_responsavel,
    titulo,
    descricao,
    categoria,
    data_criacao,
    data_ultima_atualizacao,
    status
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_POR_USUARIO = """
SELECT
    c.id_chamado,
    c.id_usuario_criador,
    c.id_administrador_responsavel,
    c.titulo,
    c.descricao,
    c.categoria,
    c.data_criacao,
    c.data_ultima_atualizacao,
    c.status
FROM chamado c
WHERE c.id_usuario_criador = ?
ORDER BY c.data_criacao DESC
"""

OBTER_ESTATISTICAS_USUARIO = """
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN status = 'aberto' THEN 1 ELSE 0 END) as abertos,
    SUM(CASE WHEN status = 'em-andamento' THEN 1 ELSE 0 END) as em_andamento,
    SUM(CASE WHEN status = 'resolvido' THEN 1 ELSE 0 END) as resolvidos
FROM chamado
WHERE id_usuario_criador = ?
"""

INSERIR_DADOS_EXEMPLO = """
INSERT INTO chamado (id_usuario_criador, id_administrador_responsavel, titulo, descricao, categoria, data_criacao, data_ultima_atualizacao, status) VALUES 
(?, NULL, 'Erro ao anexar documento', 'Não estou conseguindo anexar o comprovante de residência na inscrição do auxílio moradia. O sistema apresenta erro ao fazer upload do arquivo PDF.', 'erro', datetime('now', '-2 hours', 'localtime'), NULL, 'aberto'),
(?, 1, 'Dúvida sobre prazo de inscrição', 'Gostaria de saber se haverá prorrogação do prazo de inscrição para o auxílio material didático.', 'duvida', datetime('now', '-1 day', 'localtime'), datetime('now', '-1 hour', 'localtime'), 'em-andamento'),
(?, NULL, 'Não recebi a confirmação por email', 'Fiz a inscrição no auxílio alimentação ontem, mas ainda não recebi o email de confirmação da inscrição.', 'outros', datetime('now', '-1 day', 'localtime'), NULL, 'aberto'),
(?, 1, 'Problema ao acessar histórico', 'A página do histórico de recebimentos voltou a funcionar normalmente após a manutenção.', 'erro', datetime('now', '-2 days', 'localtime'), datetime('now', '-2 days', 'localtime'), 'resolvido'),
(?, 1, 'Atualização de dados cadastrais', 'Dados atualizados com sucesso no sistema.', 'outros', datetime('now', '-3 days', 'localtime'), datetime('now', '-3 days', 'localtime'), 'resolvido')
"""

OBTER_POR_ID = """
SELECT
    id_chamado,
    id_usuario_criador,
    id_administrador_responsavel,
    titulo,
    descricao,
    categoria,
    data_criacao,
    data_ultima_atualizacao,
    status
FROM chamado
WHERE id_chamado = ?
"""

OBTER_POR_PAGINA = """
SELECT
    c.id_chamado,
    c.id_usuario_criador,
    c.id_administrador_responsavel,
    c.titulo,
    c.descricao,
    c.categoria,
    c.data_criacao,
    c.data_ultima_atualizacao,
    c.status
FROM chamado c
ORDER BY c.data_criacao DESC
LIMIT ? OFFSET ?
"""

ATUALIZAR = """
UPDATE chamado
SET titulo = ?, descricao = ?, categoria = ?, data_ultima_atualizacao = datetime('now', 'localtime'), status = ?
WHERE id_chamado = ?
"""

EXCLUIR = """
DELETE FROM chamado
WHERE id_chamado = ?
"""
