"""
Script para adicionar editais de exemplo para diferentes anos
"""
from datetime import datetime, timedelta
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.edital_model import Edital
from repo import edital_repo

def adicionar_editais_exemplo():
    """Adiciona editais de exemplo para os anos 2020, 2021, 2022, 2023, 2024, 2025"""
    
    editais_exemplo = [
        # Edital 2020
        Edital(
            id_edital=None,
            titulo="Edital 001/2020 - Programa de Auxílio Estudantil",
            descricao="Primeiro edital do programa de assistência estudantil implantado em 2020.",
            data_publicacao="2020-02-10",
            arquivo="docs/2020/EDITAL_001_2020.pdf",
            status="ativo",
            data_inicio_inscricao="2020-03-01",
            data_fim_inscricao="2020-03-31",
            data_inicio_vigencia="2020-04-01",
            data_fim_vigencia="2020-12-20"
        ),
        # Edital 2021
        Edital(
            id_edital=None,
            titulo="Edital 002/2021 - Assistência Estudantil",
            descricao="Edital para concessão de auxílios aos estudantes em situação de vulnerabilidade no ano de 2021.",
            data_publicacao="2021-01-25",
            arquivo="docs/2021/EDITAL_002_2021.pdf",
            status="ativo",
            data_inicio_inscricao="2021-02-15",
            data_fim_inscricao="2021-03-15",
            data_inicio_vigencia="2021-03-20",
            data_fim_vigencia="2021-12-15"
        ),
        # Edital 2022
        Edital(
            id_edital=None,
            titulo="Edital 001/2022 - Programa de Assistência Estudantil",
            descricao="Edital para concessão de auxílios estudantis no ano de 2022, incluindo auxílio alimentação, transporte e moradia.",
            data_publicacao="2022-01-15",
            arquivo="docs/2022/EDITAL_001_2022.pdf",
            status="ativo",
            data_inicio_inscricao="2022-02-01",
            data_fim_inscricao="2022-02-28",
            data_inicio_vigencia="2022-03-01",
            data_fim_vigencia="2022-12-31"
        ),
        # Edital 2023
        Edital(
            id_edital=None,
            titulo="Edital 002/2023 - Auxílio Permanência Estudantil",
            descricao="Processo seletivo para concessão de auxílio permanência aos estudantes em situação de vulnerabilidade socioeconômica no ano de 2023.",
            data_publicacao="2023-01-20",
            arquivo="docs/2023/EDITAL_002_2023.pdf",
            status="ativo",
            data_inicio_inscricao="2023-02-10",
            data_fim_inscricao="2023-03-10",
            data_inicio_vigencia="2023-03-15",
            data_fim_vigencia="2023-12-20"
        ),
        # Edital 2024
        Edital(
            id_edital=None,
            titulo="Edital 003/2024 - Programa de Assistência ao Estudante",
            descricao="Edital referente ao programa de assistência estudantil do ano de 2024, contemplando diversos tipos de auxílios.",
            data_publicacao="2024-01-10",
            arquivo="docs/2024/EDITAL_003_2024.pdf",
            status="ativo",
            data_inicio_inscricao="2024-02-05",
            data_fim_inscricao="2024-03-05",
            data_inicio_vigencia="2024-03-10",
            data_fim_vigencia="2024-12-15"
        ),
        # Edital 2025 (atual, mas com inscrições encerradas)
        Edital(
            id_edital=None,
            titulo="Edital 001/2025 - Auxílio Estudantil",
            descricao="Edital para inscrição no Programa de Assistência Estudantil 2025, com auxílios de alimentação, transporte e moradia.",
            data_publicacao="2025-01-05",
            arquivo="docs/2025/EDITAL_001_2025.pdf",
            status="ativo",
            data_inicio_inscricao="2025-01-15",
            data_fim_inscricao="2025-02-15",
            data_inicio_vigencia="2025-03-01",
            data_fim_vigencia="2025-12-31"
        )
    ]
    
    # Verificar se já existem editais
    editais_existentes = edital_repo.obter_todos()
    
    print(f"Editais existentes no banco: {len(editais_existentes)}")
    
    # Adicionar apenas se não existirem editais com os mesmos títulos
    for edital in editais_exemplo:
        # Verificar se já existe edital com esse título
        existe = any(e.titulo == edital.titulo for e in editais_existentes)
        
        if not existe:
            try:
                id_edital = edital_repo.inserir(edital)
                if id_edital:
                    print(f"✅ Edital '{edital.titulo}' adicionado com ID {id_edital}")
                else:
                    print(f"❌ Erro ao adicionar edital '{edital.titulo}'")
            except Exception as e:
                print(f"❌ Erro ao adicionar edital '{edital.titulo}': {e}")
        else:
            print(f"ℹ️  Edital '{edital.titulo}' já existe no banco")
    
    print("\n✅ Processo concluído!")

if __name__ == "__main__":
    print("Adicionando editais de exemplo para anos 2020 a 2025...\n")
    adicionar_editais_exemplo()
