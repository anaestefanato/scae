from repo import usuario_repo, inscricao_repo, auxilio_repo

# Simular usuario logado
usuario_logado = {'id': 1, 'matricula': 'aluno123', 'completo': True}

# Teste
try:
    print("1. Buscando aluno...")
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    print(f"Aluno: {aluno}")
    
    print("\n2. Buscando inscrições...")
    inscricoes = inscricao_repo.obter_por_aluno(usuario_logado['id'])
    print(f"Total inscrições: {len(inscricoes)}")
    
    print("\n3. Buscando auxílios...")
    auxilios_por_aluno = auxilio_repo.obter_por_aluno(usuario_logado['id'])
    print(f"Total auxílios: {len(auxilios_por_aluno)}")
    
    print("\n4. Agrupando auxílios...")
    inscricoes_com_auxilios = {}
    for auxilio in auxilios_por_aluno:
        id_inscricao = auxilio['id_inscricao']
        if id_inscricao not in inscricoes_com_auxilios:
            inscricoes_com_auxilios[id_inscricao] = {
                'edital_titulo': auxilio.get('edital_titulo', 'Edital sem título'),
                'auxilios': []
            }
        inscricoes_com_auxilios[id_inscricao]['auxilios'].append(auxilio)
    
    print(f"\nInscrições com auxílios: {inscricoes_com_auxilios}")
    
    print("\n✅ SUCESSO!")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
