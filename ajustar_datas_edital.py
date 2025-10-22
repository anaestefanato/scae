from util.db_util import get_connection
from datetime import date, timedelta

print("=== AJUSTANDO DATAS DE EDITAIS ===\n")

# Ajustar o Edital ID 3 para ter inscrições abertas AGORA
hoje = date.today()
inicio_inscricao = (hoje - timedelta(days=5)).strftime('%Y-%m-%d')  # Começou 5 dias atrás
fim_inscricao = (hoje + timedelta(days=30)).strftime('%Y-%m-%d')  # Termina daqui a 30 dias

with get_connection() as conn:
    cursor = conn.cursor()
    
    # Atualizar edital ID 3
    cursor.execute("""
        UPDATE edital 
        SET data_inicio_inscricao = ?, 
            data_fim_inscricao = ?
        WHERE id_edital = 3
    """, (inicio_inscricao, fim_inscricao))
    
    conn.commit()
    
    print(f"✓ Edital ID 3 atualizado:")
    print(f"  - Início das inscrições: {inicio_inscricao}")
    print(f"  - Fim das inscrições: {fim_inscricao}")
    print(f"  - Data de hoje: {hoje.strftime('%Y-%m-%d')}")
    
    # Verificar o edital
    cursor.execute("SELECT * FROM edital WHERE id_edital = 3")
    edital = cursor.fetchone()
    
    print(f"\n✓ Edital verificado:")
    print(f"  - ID: {edital['id_edital']}")
    print(f"  - Título: {edital['titulo']}")
    print(f"  - Status: {edital['status']}")
    print(f"  - Inscrições: {edital['data_inicio_inscricao']} a {edital['data_fim_inscricao']}")

print("\n=== EDITAL AJUSTADO COM SUCESSO ===")
