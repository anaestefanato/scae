import sys 
import os 
from repo import aluno_repo
from repo.aluno_repo import *
from model.aluno_model import Aluno
from repo import usuario_repo

class TestAlunoRepo:
    def test_criar_tabela_aluno(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de alunos não foi criada com sucesso."

    def test_inserir_aluno(self, test_db):
        # Arrange
        criar_tabela()
        aluno_teste = Aluno(0, "Nome", "fulanp@gmail.com", "123456", "aluno", "12345678901", "2000-01-01", "Pai Teste", "Rua Teste", "Banco Teste", "1923", "1234-5", 1500.00, "ALUNO_TESTE")
        # Act
        id_aluno_inserido = inserir(aluno_teste)
        # Assert
        aluno_db = obter_por_id(id_aluno_inserido)
        assert aluno_db is not None, "O aluno não foi inserido não pode ser None."
        assert aluno_db.matricula == "ALUNO_TESTE", "A matrícula do aluno inserido não corresponde ao esperado."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        criar_tabela()
        aluno_teste = Aluno(0, "Nome", "fulano@email.com", "123456", "aluno", "12345678901", "2000-01-01", "Pai Teste", "Rua Teste", "Banco Teste", "1234", "56789", 1500.00, "ALUNO_TESTE")
        id_aluno_inserido = inserir(aluno_teste)
        # Act
        aluno_db = obter_por_id(id_aluno_inserido)
        # Assert
        assert aluno_db is not None, "O aluno não foi encontrado no banco de dados."
        assert aluno_db.id_usuario == id_aluno_inserido, "O ID do aluno obtido não corresponde ao esperado."
        assert aluno_db.matricula == aluno_teste.matricula, "A matrícula do aluno obtido não corresponde ao esperado."
    
    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_aluno_inexistente = 999
        # Act
        aluno_db = obter_por_id(id_aluno_inexistente)
        # Assert
        assert aluno_db is None, "A busca por um aluno inexistente deveria retornar None."
    
    def test_obter_alunos_por_pagina_primeira_pagina(self, test_db, lista_alunos_exemplo):
        # Arrange
        aluno_repo.criar_tabela()
        for aluno in lista_alunos_exemplo:
            aluno_repo.inserir(aluno)
        # Act
        pagina_alunos = aluno_repo.obter_alunos_por_pagina(1, 4)
        # Assert
        assert len(pagina_alunos) == 4, "Deveria retornar 4 alunos na primeira página"
        assert all(isinstance(u, Aluno) for u in pagina_alunos), "Todos os itens da página devem ser do tipo Aluno"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id_usuario for u in pagina_alunos]
        assert ids_esperados == ids_retornados, "Os IDs dos alunos na primeira página não estão corretos"

    def test_obter_alunos_por_pagina_terceira_pagina(self, test_db, lista_alunos_exemplo):
        # Arrange
        aluno_repo.criar_tabela()
        for aluno in lista_alunos_exemplo:
            aluno_repo.inserir(aluno)
        # Act
        pagina_alunos = aluno_repo.obter_alunos_por_pagina(3, 2)
        # Assert
        assert len(pagina_alunos) == 2, "Deveria retornar 2 alunos na terceira página"
        assert all(isinstance(u, Aluno) for u in pagina_alunos), "Todos os itens da página devem ser do tipo Aluno"
        ids_esperados = [5, 6]
        ids_retornados = [u.id_usuario for u in pagina_alunos]
        assert ids_esperados == ids_retornados, f"Os IDs dos alunos na terceira página não estão corretos: {ids_retornados}"

    def test_atualizar_aluno_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        criar_tabela()
        aluno_teste = Aluno(0, "Nome", "fulanp@gmail.com", "123456", "aluno", "12345678901", "2000-01-01", "Pai Teste", "Rua Teste", "Banco Teste", "1923", "1234-5", 1500.00, "ALUNO_TESTE")
        id_aluno_inserido = inserir(aluno_teste)
        aluno_teste.id_usuario = id_aluno_inserido
        aluno_teste.cpf = "12345678901"
        aluno_teste.data_nascimento = "2000-01-01"
        aluno_teste.filiacao = "Pai Teste"
        aluno_teste.endereco = "Rua Teste"
        aluno_teste.nome_banco = "Banco Teste"
        aluno_teste.numero_conta_bancaria = "1234-5"
        aluno_teste.renda_familiar = 1500.00
        aluno_teste.matricula = "ALUNO_TESTE"
        # Act
        resultado = atualizar(aluno_teste)
        # Assert
        assert resultado == True, "A atualização do aluno deveria retornar True"
        aluno_db = obter_por_id(id_aluno_inserido)
        assert aluno_db.cpf == "12345678901", "O CPF do aluno atualizado não confere"
        assert aluno_db.data_nascimento == "2000-01-01", "A data de nascimento do aluno atualizado não confere"

    def test_atualizar_aluno_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        aluno_teste = Aluno(999, "aluno_inexistente", "inexistente@gmail.com", "123456", "aluno", "12345678901", "2000-01-01", "Pai Inexistente", "Rua Inexistente", "Banco Inexistente", "1923", "1234-5", 1500.00, "ALUNO_INEXISTENTE")
        aluno_teste.cpf = "12345678901"
        aluno_teste.data_nascimento = "2000-01-01"
        aluno_teste.filiacao = "Pai Inexistente"
        aluno_teste.endereco = "Rua Inexistente"
        aluno_teste.nome_banco = "Banco Inexistente"
        aluno_teste.numero_conta_bancaria = "0000-0"
        aluno_teste.renda_familiar = 0.00
        aluno_teste.matricula = "ALUNO_INEXISTENTE"
        # Act
        resultado = atualizar(aluno_teste)
        # Assert
        assert resultado == False, "A atualização de um aluno inexistente deveria retornar False"

    def test_excluir_aluno_existente(self, test_db):
        # Arrange
        criar_tabela()
        aluno_teste = Aluno(0, "aluno_teste", "aluno_teste@gmail.com", "123456", "aluno", "12345678901", "2000-01-01", "Pai Teste", "Rua Teste", "Banco Teste", "1923", "1234-5", 1500.00, "ALUNO_TESTE")
        id_aluno_inserido = inserir(aluno_teste)
        # Act
        resultado = excluir(id_aluno_inserido)
        # Assert
        assert resultado == True, "A exclusão do aluno deveria retornar True"
        aluno_db = obter_por_id(id_aluno_inserido)
        assert aluno_db is None, "O aluno deveria ter sido excluído e não pode ser encontrado no banco de dados"

    def test_excluir_aluno_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_aluno_inexistente = 999
        # Act
        resultado = excluir(id_aluno_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um aluno inexistente deveria retornar False"