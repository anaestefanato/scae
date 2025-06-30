import sys
import os

from data import usuario_repo
from data import inscricao_repo
from data.inscricao_repo import *
from recurso_model import Recurso
from usuario_model import Usuario

class TestRecursoRepo:
    def test_criar_tabela_recurso(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        # Act
    resultado = criar_tabela()
    # Assert
    assert resultado == True, "A tabela de recursos não foi criada com sucesso."

    def test_inserir_recurso(self, test_db):
    # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        recurso = Recurso(
            id_recurso=1,
            id_inscricao=1,
            id_assistente_social=1,
            descricao='Recurso de teste',
            data_envio='2023-10-01',
            data_resposta='2023-10-02',
            status='pendente'
        )
    # Act
    resultado = inserir()
    # Assert
    assert resultado == True, "O recurso não foi inserida com sucesso."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        id_inscricao = inscricao_repo.inserir(inscricao)
        inscricao = Inscricao(id_inscricao=0, id_aluno=1, id_edital=1, data_inscricao='2023-10-01', status='pendente',
            urlDocumentoIdentificacao='http://example.com/doc1',
            urlDeclaracaoRenda='http://example.com/renda1',
            urlTermoResponsabilidade='http://example.com/termo1'
        )
        recurso = Recurso(
            id_recurso=0,
            id_inscricao=id_inscricao,
            id_assistente_social=id_usuario,
            descricao='Recurso de teste',
            data_envio='2023-10-01',
            data_resposta='2023-10-02',
            status='pendente'
        )
        id_recurso = inserir(recurso)
        # Act
        resultado = obter_por_id(id_recurso)
        # Assert
        assert resultado is not None, "O recurso não foi encontrada pelo ID."
        assert resultado.id_inscricao == 1, "O ID do recurso retornada não é o esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        # Act
        id_inexistente = 999
        resultado = obter_por_id(id_inexistente)
        # Assert
        assert resultado is None, "A busca por um recurso inexistente deveria retornar None."

    def test_obter_recurso_por_pagina_primeira_pagina(self, test_db, lista_recursos_exemplo, lista_usuarios_exemplo, lista_inscricoes_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        
        for incricao in lista_inscricoes_exemplo:
            inscricao_repo.inserir(incricao)
        
        for i, recurso in enumerate(lista_recursos_exemplo, start=1):
            recurso.id_aluno = i
            recurso.id_edital = i
            inserir(recurso)
        
        # Act
        pagina_recursos = obter_por_pagina(1, 4)

        # Assert
        assert len(pagina_recursos) == 4, "Deveria retornar 4 recursos na primeira página"
        assert all(isinstance(i, Recurso) for i in pagina_recursos), "Todos os itens da página devem ser do tipo Recurso"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [i.id_recurso for i in pagina_recursos]
        assert ids_retornados == ids_esperados, "Os IDs dos recursos retornadas não são os esperados."

    def test_obter_recursos_por_pagina_terceira_pagina(self, test_db, lista_recursos_exemplo, lista_usuarios_exemplo, lista_inscricoes_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        
        for inscricao in lista_inscricoes_exemplo:
            inscricao_repo.inserir(inscricao)
        
        for i, recurso in enumerate(lista_recursos_exemplo, start=1):
            recurso.id_usuario = i
            recurso.id_inscricao = i
            inserir(recurso)
        
        # Act
        pagina_recursos = obter_por_pagina(3, 4)

        # Assert
        assert len(pagina_recursos) == 2, "Deveria retornar 2 recursos na terceira página"
        assert all(isinstance(i, Recurso) for i in pagina_recursos), "Todos os itens da página devem ser do tipo Recurso"
        ids_esperados = [9, 10]
        ids_retornados = [i.id_recurso for i in pagina_recursos]
        assert ids_retornados == ids_esperados, "Os IDs dos recursos retornadas na terceira página não são os esperados."

    def test_atualizar_recurso_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        
        usuario = Usuario(1, "Usuario", "fulano@gmail.com", "senha@123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        incricao = Inscricao (id_inscricao=0,  
            id_aluno=1,  
            id_edital=id_edital,  
            data_inscricao='2023-10-01',
            status='pendente',
            urlDocumentoIdentificacao='http://example.com/doc1',
            urlDeclaracaoRenda='http://example.com/renda1',
            urlTermoResponsabilidade='http://example.com/termo1')
        id_inscricao = inscricao_repo.inserir(inscricao)
        recurso = Recurso(
            id_recurso=id_recurso,
            id_inscricao=id_inscricao,
            id_assistente_social=id_usuario,
            descricao='Recurso de teste',
            data_envio='2023-10-01',
            data_resposta='2023-10-02',
            status='pendente'
        )
        id_recurso = inserir(recurso)
        recurso_atualizado = Recurso(
            id_recurso = id_recurso,
            id_inscricao=id_inscricao,
            id_assistente_social=id_usuario,
            descricao='Recurso de teste atualizado',
            data_envio='2023-10-02',
            data_resposta='2023-10-10',
            status='respondido')
        # Act
        resultado = atualizar(recurso_atualizado)
        # Assert
        assert resultado == True, "O recurso não foi atualizado com sucesso."
        recurso_db = obter_por_id(id_recurso)
        assert recurso_db is not None, "O recurso atualizado não foi encontrada no banco de dados."

    
    def test_atualizar_recurso_inexistente(self, test_db):
        # Arrange
        recurso_inexistente = Recurso(
            id_recurso=9999,  # ID que não existe
            id_usuario=1,
            id_inscricao=1,
            descricao='Recurso inexistente',
            data_envio='2023-10-01',    
            data_resposta='2023-10-02',
            status='pendente'
        )
        # Act
        resultado = atualizar(recurso_inexistente)
        # Assert
        assert resultado == False, "A atualização do recurso inexistente deveria ter falhado."

    def test_excluir_recurso_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        inscricao = Inscricao(1,
            id_aluno=1, 
            id_edital=1,
            data_inscricao='2023-10-01',
            status='pendente',
            urlDocumentoIdentificacao='http://example.com/doc1',
            urlDeclaracaoRenda='http://example.com/renda1',
            urlTermoResponsabilidade='http://example.com/termo1')
        id_inscricao = inscricao_repo.inserir(inscricao)
        recurso = Recurso(
            id_recurso=id_recurso,
            id_inscricao=id_inscricao,
            id_assistente_social=id_usuario,
            descricao='Recurso de teste',
            data_envio='2023-10-01',
            data_resposta='2023-10-02',
            status='pendente'
        )
        id_recurso = inserir(recurso)
        # Act
        resultado = excluir(id_recurso)
        # Assert
        assert resultado == True, "O recurso não foi deletado com sucesso."

    def test_excluir_recurso_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        id_inexistente = 9999  
        # Act   
        resultado = excluir(id_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um recurso inexistente deveria ter falhado."
