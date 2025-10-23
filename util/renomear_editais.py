"""
Script para renomear todos os editais seguindo o padrão:
Edital {número}/{ano} - Programa de Assistência Estudantil
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repo import edital_repo

def renomear_editais():
    """Renomeia todos os editais para o padrão uniforme"""
    
    # Obter todos os editais
    editais = edital_repo.obter_todos()
    
    print(f"Total de editais no banco: {len(editais)}\n")
    
    # Mapeamento de ano para número do edital
    editais_por_ano = {
        2020: [],
        2021: [],
        2022: [],
        2023: [],
        2024: [],
        2025: []
    }
    
    # Agrupar editais por ano
    for edital in editais:
        ano = int(edital.data_publicacao.split('-')[0])
        if ano in editais_por_ano:
            editais_por_ano[ano].append(edital)
    
    # Renomear editais
    for ano, lista_editais in sorted(editais_por_ano.items()):
        if not lista_editais:
            continue
            
        # Ordenar editais do mesmo ano por data de publicação
        lista_editais.sort(key=lambda e: e.data_publicacao)
        
        for idx, edital in enumerate(lista_editais, start=1):
            numero_edital = str(idx).zfill(3)  # 001, 002, 003, etc.
            novo_titulo = f"Edital {numero_edital}/{ano} - Programa de Assistência Estudantil"
            
            # Atualizar se o título for diferente
            if edital.titulo != novo_titulo:
                titulo_antigo = edital.titulo
                edital.titulo = novo_titulo
                
                try:
                    edital_repo.atualizar(edital)
                    print(f"✅ Renomeado: '{titulo_antigo}'")
                    print(f"   → '{novo_titulo}'\n")
                except Exception as e:
                    print(f"❌ Erro ao renomear '{titulo_antigo}': {e}\n")
            else:
                print(f"ℹ️  Já está correto: '{novo_titulo}'\n")
    
    print("✅ Processo de renomeação concluído!")

if __name__ == "__main__":
    print("Renomeando editais para padrão uniforme...\n")
    print("=" * 70)
    print()
    renomear_editais()
