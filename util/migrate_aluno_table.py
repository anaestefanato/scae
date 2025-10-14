"""
Script de migração para adicionar novos campos na tabela aluno
Executar apenas uma vez para atualizar o banco de dados existente
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.db_util import get_connection

def adicionar_campos_aluno():
    """Adiciona os novos campos na tabela aluno"""
    
    campos_novos = [
        ("ano_ingresso", "INTEGER"),
        ("ano_conclusao_previsto", "INTEGER"),
        ("bolsa_pesquisa", "TEXT"),
        ("cad_unico", "TEXT"),
        ("bolsa_familia", "TEXT")
    ]
    
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar quais colunas já existem
            cursor.execute("PRAGMA table_info(aluno)")
            colunas_existentes = [row[1] for row in cursor.fetchall()]
            
            # Adicionar apenas as colunas que não existem
            for campo, tipo in campos_novos:
                if campo not in colunas_existentes:
                    sql = f"ALTER TABLE aluno ADD COLUMN {campo} {tipo}"
                    cursor.execute(sql)
                    print(f"✓ Coluna '{campo}' adicionada com sucesso")
                else:
                    print(f"○ Coluna '{campo}' já existe")
            
            conn.commit()
            print("\n✅ Migração concluída com sucesso!")
            return True
            
    except Exception as e:
        print(f"\n❌ Erro na migração: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRAÇÃO DA TABELA ALUNO")
    print("=" * 60)
    print("\nAdicionando novos campos para o formulário de inscrição...\n")
    
    adicionar_campos_aluno()
