"""
Script de migração para adicionar a coluna 'estado' na tabela aluno
"""

import sqlite3
from util.db_util import get_connection

def migrar_adicionar_coluna_estado():
    """
    Adiciona a coluna 'estado' na tabela aluno se ela não existir
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar se a coluna já existe
            cursor.execute("PRAGMA table_info(aluno)")
            colunas = [coluna[1] for coluna in cursor.fetchall()]
            
            if 'estado' not in colunas:
                print("Adicionando coluna 'estado' na tabela aluno...")
                cursor.execute("ALTER TABLE aluno ADD COLUMN estado TEXT DEFAULT ''")
                
                # Atualizar registros existentes com valor padrão (ES - Espírito Santo)
                cursor.execute("UPDATE aluno SET estado = 'ES' WHERE estado = '' OR estado IS NULL")
                
                print("Coluna 'estado' adicionada com sucesso!")
                print("Registros existentes foram atualizados com 'ES' como padrão.")
            else:
                print("Coluna 'estado' já existe na tabela aluno.")
                
    except Exception as e:
        print(f"Erro durante a migração: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== MIGRAÇÃO: Adicionando coluna 'estado' ===")
    sucesso = migrar_adicionar_coluna_estado()
    if sucesso:
        print("=== MIGRAÇÃO CONCLUÍDA COM SUCESSO ===")
    else:
        print("=== ERRO NA MIGRAÇÃO ===")
