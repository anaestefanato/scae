from repo import aluno_repo, usuario_repo

print("=" * 80)
print("TESTANDO ATUALIZAÇÃO DE DADOS DO ALUNO")
print("=" * 80)

# Testar com o aluno 20221imi015
matricula = "20221imi015"

print(f"\n1. Buscando dados do aluno com matrícula: {matricula}")
aluno = aluno_repo.obter_por_matricula(matricula)

if aluno:
    print("✓ Aluno encontrado na tabela aluno!")
    print(f"  Nome: {aluno.nome}")
    print(f"  Matrícula: {aluno.matricula}")
    print(f"  Email: {aluno.email}")
    print(f"  CPF: {aluno.cpf if aluno.cpf else 'Não informado'}")
    print(f"  Curso: {aluno.curso if aluno.curso else 'Não informado'}")
else:
    print("⚠ Aluno NÃO encontrado na tabela aluno")
    print("  Buscando dados básicos na tabela usuario...")
    
    usuario = usuario_repo.obter_usuario_por_matricula(matricula)
    if usuario:
        print("✓ Usuário encontrado na tabela usuario!")
        print(f"  Nome: {usuario.nome}")
        print(f"  Matrícula: {usuario.matricula}")
        print(f"  Email: {usuario.email}")
    else:
        print("✗ Usuário NÃO encontrado")

print("\n" + "=" * 80)
print("VERIFICANDO OUTROS ALUNOS APROVADOS")
print("=" * 80)

alunos_aprovados = aluno_repo.obter_alunos_aprovados()
print(f"\nTotal de alunos aprovados: {len(alunos_aprovados)}\n")

for aluno_dict in alunos_aprovados[:3]:
    mat = aluno_dict['matricula']
    print(f"Testando: {aluno_dict['nome']} ({mat})")
    
    aluno_completo = aluno_repo.obter_por_matricula(mat)
    if aluno_completo:
        print(f"  ✓ Tem dados completos na tabela aluno")
    else:
        print(f"  ⚠ NÃO tem dados completos na tabela aluno")
    print()

print("=" * 80)
