import sys 
import os 
from repo import inscricao_repo
from repo.inscricao_repo import *
from model.inscricao_model import Inscricao
from repo import usuario_repo
from repo import aluno_repo
from model.aluno_model import Aluno
from repo import edital_repo
from model.edital_model import Edital

class TestInscricaoRepo:
    def test_criar_tabela_inscricao(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        # Act
    resultado = criar_tabela()
    # Assert
    assert resultado == True, "A tabela de inscrições não foi criada com sucesso."

    def test_inserir_inscricao(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        criar_tabela()
        inscricao = Inscricao(
            id_inscricao=1,
            id_aluno=1,
            id_edital=1,
            data_inscricao='2023-10-01',
            status='pendente',
            urlDocumentoIdentificacao='http://example.com/doc1',
            urlDeclaracaoRenda='http://example.com/renda1',
            urlTermoResponsabilidade='http://example.com/termo1'
        )
        # Act
        resultado = inserir(inscricao)
        # Assert
        assert resultado == True, "A inscrição não foi inserida com sucesso."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        criar_tabela()
        aluno = Aluno(0, "Aluno Teste", "aluno@email.com", "senha", "aluno", "11111111111", "2000-01-01", "Pai", "Rua", "Banco", "123", "4567-8", 1500.0, "MAT123")
        id_aluno = aluno_repo.inserir(aluno)
        edital = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo_teste.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)
        inscricao = Inscricao(
            id_inscricao=0,  
            id_aluno=id_aluno,  
            id_edital=id_edital,  
            data_inscricao='2023-10-01',
            status='pendente',
            urlDocumentoIdentificacao='http://example.com/doc1',
            urlDeclaracaoRenda='http://example.com/renda1',
            urlTermoResponsabilidade='http://example.com/termo1'
        )
        id_inscricao = inserir(inscricao)
        # Act
        resultado = obter_por_id(id_inscricao)
        # Assert
        assert resultado is not None, "A inscrição não foi encontrada pelo ID."
        assert resultado.id_inscricao == 1, "O ID da inscrição retornada não é o esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        criar_tabela()
        # Act
        id_inexistente = 999
        resultado = obter_por_id(id_inexistente)
        # Assert
        assert resultado is None, "A busca por uma inscrição inexistente deveria retornar None."

    def test_obter_inscricoes_por_pagina_primeira_pagina(self, test_db, lista_inscricoes_exemplo, lista_alunos_exemplo, lista_editais_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        criar_tabela()

        for aluno in lista_alunos_exemplo:
            aluno_repo.inserir(aluno)
        
        for edital in lista_editais_exemplo:
            edital_repo.inserir(edital)
        
        for i, inscricao in enumerate(lista_inscricoes_exemplo, start=1):
            inscricao.id_aluno = i
            inscricao.id_edital = i
            inserir(inscricao)
        
        # Act
        pagina_inscricoes = obter_por_pagina(1, 4)

        # Assert
        assert len(pagina_inscricoes) == 4, "Deveria retornar 4 inscrições na primeira página"
        assert all(isinstance(i, Inscricao) for i in pagina_inscricoes), "Todos os itens da página devem ser do tipo Inscricao"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [i.id_inscricao for i in pagina_inscricoes]
        assert ids_retornados == ids_esperados, "Os IDs das inscrições retornadas não são os esperados."

    def test_obter_inscricoes_por_pagina_terceira_pagina(self, test_db, lista_inscricoes_exemplo, lista_alunos_exemplo, lista_editais_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        criar_tabela()

        for aluno in lista_alunos_exemplo:
            aluno_repo.inserir(aluno)
        
        for edital in lista_editais_exemplo:
            edital_repo.inserir(edital)
        
        for i, inscricao in enumerate(lista_inscricoes_exemplo, start=1):
            inscricao.id_aluno = i
            inscricao.id_edital = i
            inserir(inscricao)
        
        # Act
        pagina_inscricoes = obter_por_pagina(3, 4)

        # Assert
        assert len(pagina_inscricoes) == 2, "Deveria retornar 2 inscrições na terceira página"
        assert all(isinstance(i, Inscricao) for i in pagina_inscricoes), "Todos os itens da página devem ser do tipo Inscricao"
        ids_esperados = [9, 10]
        ids_retornados = [i.id_inscricao for i in pagina_inscricoes]
        assert ids_retornados == ids_esperados, "Os IDs das inscrições retornadas na terceira página não são os esperados."

    def test_atualizar_inscricao_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        criar_tabela()
        
        aluno = Aluno(0, "Aluno Teste", "fulano@email.com", "senha", "aluno", "11111111111", "2000-01-01", "Pai Teste", "Rua Teste", "Banco Teste", "1234", "56789", 1500.00, "ALUNO_TESTE")
        id_aluno = aluno_repo.inserir(aluno)
        edital = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo_teste.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)
        inscricao = Inscricao(
            id_inscricao=0,  
            id_aluno=id_aluno,  
            id_edital=id_edital,  
            data_inscricao='2023-10-01',
            status='pendente',
            urlDocumentoIdentificacao='http://example.com/doc1',
            urlDeclaracaoRenda='http://example.com/renda1',
            urlTermoResponsabilidade='http://example.com/termo1'
        )
        id_inscricao = inserir(inscricao)
        inscricao_atualizada = Inscricao(
            id_inscricao=id_inscricao,
            id_aluno=id_aluno,
            id_edital=id_edital,
            data_inscricao='2023-10-02',
            status='deferido',
            urlDocumentoIdentificacao='http://example.com/doc1_updated',
            urlDeclaracaoRenda='http://example.com/renda1_updated',
            urlTermoResponsabilidade='http://example.com/termo1_updated'
        )
        # Act
        resultado = atualizar(inscricao_atualizada)
        # Assert
        assert resultado == True, "A inscrição não foi atualizada com sucesso."
        inscricao_db = obter_por_id(id_inscricao)
        assert inscricao_db is not None, "A inscrição atualizada não foi encontrada no banco de dados."

    
    def test_atualizar_inscricao_inexistente(self, test_db):
        # Arrange
        inscricao_inexistente = Inscricao(
            id_inscricao=9999,  # ID que não existe
            id_aluno=1,
            id_edital=1,
            data_inscricao='2023-10-01',
            status='pendente',
            urlDocumentoIdentificacao='http://example.com/doc1',
            urlDeclaracaoRenda='http://example.com/renda1',
            urlTermoResponsabilidade='http://example.com/termo1'
        )
        # Act
        resultado = atualizar(inscricao_inexistente)
        # Assert
        assert resultado == False, "A atualização da inscrição inexistente deveria ter falhado."

    def test_excluir_inscricao_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        criar_tabela()
        
        aluno = Aluno(0, "Aluno Teste", "fulano@email.com", "senha", "aluno", "11111111111", "2000-01-01", "Pai Teste", "Rua Teste", "Banco Teste", "1234", "56789", 1500.00, "ALUNO_TESTE")
        id_aluno = aluno_repo.inserir(aluno)
        edital = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo_teste.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)
        inscricao = Inscricao(
            id_inscricao=0,  
            id_aluno=id_aluno,  
            id_edital=id_edital,  
            data_inscricao='2023-10-01',
            status='pendente',
            urlDocumentoIdentificacao='http://example.com/doc1',
            urlDeclaracaoRenda='http://example.com/renda1',
            urlTermoResponsabilidade='http://example.com/termo1'
        )
        id_inscricao = inserir(inscricao)
        # Act
        resultado = excluir(id_inscricao)
        # Assert
        assert resultado == True, "A inscrição não foi deletada com sucesso."

    def test_excluir_inscricao_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        aluno_repo.criar_tabela()
        edital_repo.criar_tabela()
        criar_tabela()
        id_inexistente = 9999  
        # Act   
        resultado = excluir(id_inexistente)
        # Assert
        assert resultado == False, "A exclusão de uma inscrição inexistente deveria ter falhado."
