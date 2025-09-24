from typing import Optional, List
from model.chamado_model import Chamado
from sql.chamado_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela recurso: {e}")
        return False
    
def inserir(chamado: Chamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            chamado.id_usuario_criador,
            chamado.id_administrador_responsavel,
            chamado.titulo,
            chamado.descricao,
            chamado.categoria,
            chamado.data_criacao,
            chamado.data_ultima_atualizacao,
            chamado.status
        ))
        return cursor.lastrowid

def obter_por_usuario(id_usuario: int) -> List[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_USUARIO, (id_usuario,))
        rows = cursor.fetchall()
        chamados = []
        for row in rows:
            chamado = Chamado(
                id_chamado=row["id_chamado"],
                id_usuario_criador=row["id_usuario_criador"],
                id_administrador_responsavel=row["id_administrador_responsavel"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                categoria=row["categoria"],
                data_criacao=row["data_criacao"],
                data_ultima_atualizacao=row["data_ultima_atualizacao"],
                status=row["status"]
            )
            chamados.append(chamado)
        return chamados

def obter_estatisticas_usuario(id_usuario: int) -> dict:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ESTATISTICAS_USUARIO, (id_usuario,))
        row = cursor.fetchone()
        if row:
            return {
                'total': row['total'],
                'abertos': row['abertos'],
                'em_andamento': row['em_andamento'],
                'resolvidos': row['resolvidos']
            }
        return {
            'total': 0,
            'abertos': 0,
            'em_andamento': 0,
            'resolvidos': 0
        }

def inserir_dados_exemplo(id_usuario: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Executar cada INSERT separadamente
            comandos = [
                "INSERT INTO chamado (id_usuario_criador, id_administrador_responsavel, titulo, descricao, categoria, data_criacao, data_ultima_atualizacao, status) VALUES (?, NULL, 'Erro ao anexar documento', 'Não estou conseguindo anexar o comprovante de residência na inscrição do auxílio moradia. O sistema apresenta erro ao fazer upload do arquivo PDF.', 'erro', datetime('now', '-2 hours', 'localtime'), NULL, 'aberto')",
                "INSERT INTO chamado (id_usuario_criador, id_administrador_responsavel, titulo, descricao, categoria, data_criacao, data_ultima_atualizacao, status) VALUES (?, 1, 'Dúvida sobre prazo de inscrição', 'Gostaria de saber se haverá prorrogação do prazo de inscrição para o auxílio material didático.', 'duvida', datetime('now', '-1 day', 'localtime'), datetime('now', '-1 hour', 'localtime'), 'em-andamento')",
                "INSERT INTO chamado (id_usuario_criador, id_administrador_responsavel, titulo, descricao, categoria, data_criacao, data_ultima_atualizacao, status) VALUES (?, NULL, 'Não recebi a confirmação por email', 'Fiz a inscrição no auxílio alimentação ontem, mas ainda não recebi o email de confirmação da inscrição.', 'outros', datetime('now', '-1 day', 'localtime'), NULL, 'aberto')",
                "INSERT INTO chamado (id_usuario_criador, id_administrador_responsavel, titulo, descricao, categoria, data_criacao, data_ultima_atualizacao, status) VALUES (?, 1, 'Problema ao acessar histórico', 'A página do histórico de recebimentos voltou a funcionar normalmente após a manutenção.', 'erro', datetime('now', '-2 days', 'localtime'), datetime('now', '-2 days', 'localtime'), 'resolvido')",
                "INSERT INTO chamado (id_usuario_criador, id_administrador_responsavel, titulo, descricao, categoria, data_criacao, data_ultima_atualizacao, status) VALUES (?, 1, 'Atualização de dados cadastrais', 'Dados atualizados com sucesso no sistema.', 'outros', datetime('now', '-3 days', 'localtime'), datetime('now', '-3 days', 'localtime'), 'resolvido')"
            ]
            
            for comando in comandos:
                cursor.execute(comando, (id_usuario,))
            
            conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir dados de exemplo de chamados: {e}")
        return False

def obter_por_id(id: int) -> Optional[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Chamado(
                id_chamado=row["id_chamado"],
                id_usuario_criador=row["id_usuario_criador"],
                id_administrador_responsavel=row["id_administrador_responsavel"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                categoria=row["categoria"],
                data_criacao=row["data_criacao"],
                data_ultima_atualizacao=row["data_ultima_atualizacao"],
                status=row["status"]
            )
        return None

def obter_por_pagina(pagina: int, limit: int) -> List[Chamado]:
    offset = (pagina - 1) * limit
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PAGINA, (limit, offset))
        rows = cursor.fetchall()
        return [
            Chamado(
                id_chamado=row["id_chamado"],
                id_usuario_criador=row["id_usuario_criador"],
                id_administrador_responsavel=row["id_administrador_responsavel"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                categoria=row["categoria"],
                data_criacao=row["data_criacao"],
                data_ultima_atualizacao=row["data_ultima_atualizacao"],
                status=row["status"]
            )
            for row in rows
        ]

def atualizar(chamado: Chamado) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            chamado.titulo,
            chamado.descricao,
            chamado.categoria,
            chamado.status,
            chamado.id_chamado
        ))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0

def obter_todos_com_usuario() -> List[dict]:
    """Obtém todos os chamados com informações do usuário para o admin"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                c.id_chamado,
                c.id_usuario_criador,
                c.id_administrador_responsavel,
                c.titulo,
                c.descricao,
                c.categoria,
                c.data_criacao,
                c.data_ultima_atualizacao,
                c.status,
                u.nome as usuario_nome,
                u.email as usuario_email,
                u.matricula as usuario_matricula
            FROM chamado c
            INNER JOIN usuario u ON c.id_usuario_criador = u.id_usuario
            ORDER BY c.data_criacao DESC
        """)
        rows = cursor.fetchall()
        chamados = []
        for row in rows:
            chamado = {
                'id_chamado': row["id_chamado"],
                'id_usuario_criador': row["id_usuario_criador"],
                'id_administrador_responsavel': row["id_administrador_responsavel"],
                'titulo': row["titulo"],
                'descricao': row["descricao"],
                'categoria': row["categoria"],
                'data_criacao': row["data_criacao"],
                'data_ultima_atualizacao': row["data_ultima_atualizacao"],
                'status': row["status"],
                'usuario_nome': row["usuario_nome"],
                'usuario_email': row["usuario_email"],
                'usuario_matricula': row["usuario_matricula"]
            }
            chamados.append(chamado)
        return chamados

def obter_por_pagina_com_usuario(pagina: int = 1, limit: int = 10, filtro_status: str = None, filtro_categoria: str = None) -> dict:
    """Obtém chamados paginados com informações do usuário e filtros para o admin"""
    offset = (pagina - 1) * limit
    
    # Construir WHERE clause baseado nos filtros
    where_clause = ""
    params = []
    
    if filtro_status:
        where_clause += " AND c.status = ?"
        params.append(filtro_status)
    
    if filtro_categoria:
        where_clause += " AND c.categoria = ?"
        params.append(filtro_categoria)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Query para contar total
        count_query = f"""
            SELECT COUNT(*)
            FROM chamado c
            INNER JOIN usuario u ON c.id_usuario_criador = u.id_usuario
            WHERE 1=1 {where_clause}
        """
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        # Query para obter dados paginados
        data_query = f"""
            SELECT
                c.id_chamado,
                c.id_usuario_criador,
                c.id_administrador_responsavel,
                c.titulo,
                c.descricao,
                c.categoria,
                c.data_criacao,
                c.data_ultima_atualizacao,
                c.status,
                u.nome as usuario_nome,
                u.email as usuario_email,
                u.matricula as usuario_matricula
            FROM chamado c
            INNER JOIN usuario u ON c.id_usuario_criador = u.id_usuario
            WHERE 1=1 {where_clause}
            ORDER BY c.data_criacao DESC
            LIMIT ? OFFSET ?
        """
        
        cursor.execute(data_query, params + [limit, offset])
        rows = cursor.fetchall()
        
        chamados = []
        for row in rows:
            chamado = {
                'id_chamado': row["id_chamado"],
                'id_usuario_criador': row["id_usuario_criador"],
                'id_administrador_responsavel': row["id_administrador_responsavel"],
                'titulo': row["titulo"],
                'descricao': row["descricao"],
                'categoria': row["categoria"],
                'data_criacao': row["data_criacao"],
                'data_ultima_atualizacao': row["data_ultima_atualizacao"],
                'status': row["status"],
                'usuario_nome': row["usuario_nome"],
                'usuario_email': row["usuario_email"],
                'usuario_matricula': row["usuario_matricula"]
            }
            chamados.append(chamado)
        
        total_pages = (total + limit - 1) // limit
        
        return {
            'chamados': chamados,
            'total': total,
            'total_pages': total_pages,
            'current_page': pagina,
            'has_next': pagina < total_pages,
            'has_prev': pagina > 1
        }

def obter_estatisticas_gerais() -> dict:
    """Obtém estatísticas gerais dos chamados para o admin"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'aberto' THEN 1 ELSE 0 END) as abertos,
                SUM(CASE WHEN status = 'em-andamento' THEN 1 ELSE 0 END) as em_andamento,
                SUM(CASE WHEN status = 'resolvido' THEN 1 ELSE 0 END) as resolvidos
            FROM chamado
        """)
        row = cursor.fetchone()
        if row:
            return {
                'total': row['total'],
                'abertos': row['abertos'],
                'em_andamento': row['em_andamento'],
                'resolvidos': row['resolvidos']
            }
        return {
            'total': 0,
            'abertos': 0,
            'em_andamento': 0,
            'resolvidos': 0
        }

def atualizar_status(id_chamado: int, status: str, id_administrador: int = None) -> bool:
    """Atualiza o status de um chamado"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE chamado 
            SET status = ?, 
                data_ultima_atualizacao = datetime('now', 'localtime'),
                id_administrador_responsavel = COALESCE(?, id_administrador_responsavel)
            WHERE id_chamado = ?
        """, (status, id_administrador, id_chamado))
        return cursor.rowcount > 0
