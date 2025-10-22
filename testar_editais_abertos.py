from repo import edital_repo
from datetime import date

print("=== TESTANDO EDITAIS ABERTOS ===\n")

editais_abertos = edital_repo.obter_editais_abertos()

if editais_abertos:
    print(f"Encontrados {len(editais_abertos)} editais abertos:\n")
    for edital in editais_abertos:
        print(f"ID: {edital['id_edital']}")
        print(f"Título: {edital['titulo']}")
        print(f"Status: {edital['status']}")
        print(f"Período de Inscrição: {edital['data_inicio_inscricao']} a {edital['data_fim_inscricao']}")
        print(f"Valor Médio: R$ {edital['valor_medio']:.2f}")
        print(f"Descrição: {edital['descricao'][:100]}...")
        print("-" * 80)
else:
    print("Nenhum edital aberto encontrado.")
    print("\n=== VERIFICANDO TODOS OS EDITAIS ===\n")
    todos = edital_repo.obter_todos()
    if todos:
        print(f"Total de editais no banco: {len(todos)}\n")
        for edital in todos:
            print(f"ID: {edital.id_edital} | Título: {edital.titulo}")
            print(f"Status: {edital.status}")
            print(f"Período de Inscrição: {edital.data_inicio_inscricao} a {edital.data_fim_inscricao}")
            hoje = date.today().strftime('%Y-%m-%d')
            print(f"Data de hoje: {hoje}")
            if edital.data_inicio_inscricao and edital.data_fim_inscricao:
                if edital.data_inicio_inscricao <= hoje <= edital.data_fim_inscricao:
                    print("✓ Dentro do período de inscrição")
                else:
                    print(f"✗ Fora do período de inscrição (início: {edital.data_inicio_inscricao}, fim: {edital.data_fim_inscricao})")
            else:
                print("✗ Período de inscrição não definido")
            print("-" * 80)
