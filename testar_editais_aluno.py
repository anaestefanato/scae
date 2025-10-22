"""
Script para testar a funcionalidade de listagem de editais para alunos
"""
from datetime import date, datetime
from repo import edital_repo

def testar_editais():
    print("=" * 60)
    print("TESTE: Listagem de Editais para Alunos")
    print("=" * 60)
    
    # Obter todos os editais visíveis
    editais = edital_repo.obter_editais_visiveis_alunos()
    
    print(f"\n✓ Total de editais visíveis: {len(editais)}")
    
    if not editais:
        print("\n⚠️  AVISO: Nenhum edital encontrado no banco de dados!")
        print("   Execute o script de migração para adicionar editais de teste.")
        return
    
    # Processar cada edital
    hoje = date.today()
    print(f"\n📅 Data atual: {hoje.strftime('%d/%m/%Y')}")
    print("\n" + "=" * 60)
    
    for i, edital in enumerate(editais, 1):
        print(f"\nEdital {i}:")
        print(f"  ID: {edital.id_edital}")
        print(f"  Título: {edital.titulo}")
        print(f"  Descrição: {edital.descricao[:60]}...")
        print(f"  Status: {edital.status}")
        print(f"  Data de Publicação: {edital.data_publicacao}")
        
        # Verificar período de inscrição
        if edital.data_inicio_inscricao and edital.data_fim_inscricao:
            print(f"  Período de Inscrição:")
            print(f"    Início: {edital.data_inicio_inscricao}")
            print(f"    Fim: {edital.data_fim_inscricao}")
            
            try:
                data_inicio = datetime.strptime(edital.data_inicio_inscricao, '%Y-%m-%d').date()
                data_fim = datetime.strptime(edital.data_fim_inscricao, '%Y-%m-%d').date()
                
                inscricoes_abertas = data_inicio <= hoje <= data_fim
                
                if inscricoes_abertas:
                    print(f"  ✓ INSCRIÇÕES ABERTAS")
                    dias_restantes = (data_fim - hoje).days
                    print(f"    {dias_restantes} dia(s) restante(s)")
                else:
                    if hoje < data_inicio:
                        dias_faltam = (data_inicio - hoje).days
                        print(f"  ⏳ Inscrições abrirão em {dias_faltam} dia(s)")
                    else:
                        print(f"  ✗ INSCRIÇÕES ENCERRADAS")
            except Exception as e:
                print(f"  ⚠️  Erro ao processar datas: {e}")
        else:
            print(f"  ⚠️  Sem período de inscrição definido")
        
        # Verificar período de vigência
        if edital.data_inicio_vigencia and edital.data_fim_vigencia:
            print(f"  Vigência dos Auxílios:")
            print(f"    Início: {edital.data_inicio_vigencia}")
            print(f"    Fim: {edital.data_fim_vigencia}")
        
        print(f"  Arquivo: {edital.arquivo}")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("RESUMO:")
    print("=" * 60)
    
    # Contar editais por status de inscrição
    abertas = 0
    encerradas = 0
    sem_periodo = 0
    
    for edital in editais:
        if edital.data_inicio_inscricao and edital.data_fim_inscricao:
            try:
                data_inicio = datetime.strptime(edital.data_inicio_inscricao, '%Y-%m-%d').date()
                data_fim = datetime.strptime(edital.data_fim_inscricao, '%Y-%m-%d').date()
                
                if data_inicio <= hoje <= data_fim:
                    abertas += 1
                else:
                    encerradas += 1
            except:
                sem_periodo += 1
        else:
            sem_periodo += 1
    
    print(f"Total de editais: {len(editais)}")
    print(f"  • Com inscrições abertas: {abertas}")
    print(f"  • Com inscrições encerradas: {encerradas}")
    print(f"  • Sem período definido: {sem_periodo}")
    print("\n✓ Teste concluído com sucesso!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        testar_editais()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
