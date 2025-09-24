"""
Script para verificar a estrutura da tabela aluno
"""

from util.db_util import get_connection

def verificar_estrutura_tabela():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(aluno)")
            colunas = cursor.fetchall()
            
            print("Estrutura da tabela 'aluno':")
            print("=" * 50)
            for coluna in colunas:
                print(f"Nome: {coluna[1]}, Tipo: {coluna[2]}, Não Nulo: {bool(coluna[3])}, Default: {coluna[4]}")
            
            print("\n" + "=" * 50)
            print("Lista das colunas:")
            nomes_colunas = [coluna[1] for coluna in colunas]
            print(nomes_colunas)
            
            # Verificar se as colunas necessárias existem
            colunas_necessarias = ['estado', 'complemento']
            for coluna in colunas_necessarias:
                if coluna in nomes_colunas:
                    print(f"✅ Coluna '{coluna}' encontrada")
                else:
                    print(f"❌ Coluna '{coluna}' NÃO encontrada")
                    
    except Exception as e:
        print(f"Erro ao verificar estrutura: {e}")

if __name__ == "__main__":
    verificar_estrutura_tabela()
