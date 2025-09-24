"""
Script de migração para adicionar a coluna 'complemento' na tabela aluno
"""

from util.db_util import get_connection

def migrar_adicionar_coluna_complemento():
    """
    Adiciona a coluna 'complemento' na tabela aluno se ela não existir
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar se a coluna já existe
            cursor.execute("PRAGMA table_info(aluno)")
            colunas = [coluna[1] for coluna in cursor.fetchall()]
            
            if 'complemento' not in colunas:
                print("Adicionando coluna 'complemento' na tabela aluno...")
                cursor.execute("ALTER TABLE aluno ADD COLUMN complemento TEXT DEFAULT ''")
                
                print("Coluna 'complemento' adicionada com sucesso!")
            else:
                print("Coluna 'complemento' já existe na tabela aluno.")
                
    except Exception as e:
        print(f"Erro durante a migração: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== MIGRAÇÃO: Adicionando coluna 'complemento' ===")
    sucesso = migrar_adicionar_coluna_complemento()
    if sucesso:
        print("=== MIGRAÇÃO CONCLUÍDA COM SUCESSO ===")
    else:
        print("=== ERRO NA MIGRAÇÃO ===")
