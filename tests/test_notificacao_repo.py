import sys 
import os

from data import usuario_repo 
from data.notificacao_repo import *
import notificacao_repo
from usuario_model import Usuario

class TestNotificacaoRepo:
    def test_criar_tabela_notificacao(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        # Act
    resultado = criar_tabela()
    # Assert
    assert resultado == True, "A tabela de notificações não foi criada com sucesso."

    def test_inserir_notificacao(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()

        criar_tabela()
        notificacao = Notificacao(
            id_notificacao=1,
            id_usuario='user123',
            mensagem='Teste de notificação',
            data_envio='2023-10-01',
            tipo='pendente'
        )
        # Act
        resultado = inserir(notificacao)
        # Assert
        assert resultado == True, "A notificação não foi inserida com sucesso."
    
    def test_obter_por_id_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        notificacao = Notificacao(
            id_notificacao=0,
            id_usuario=id_usuario,
            mensagem='Notificação de teste',
            data_envio='2023-10-01',
            tipo='pendente'
        )
        id_notificacao = inserir(notificacao)
        # Act
        resultado = obter_por_id(id_notificacao)
        # Assert
        assert resultado is not None, "A notificação não foi encontrada pelo ID."
        assert resultado.id_notificacao == 1, "O ID da notificação retornada não é o esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        criar_tabela()
        # Act
        id_inexistente = 999
        resultado = obter_por_id(id_inexistente)
        # Assert
        assert resultado is None, "A busca por uma notificação inexistente deveria retornar None."

    def test_obter_recurso_por_pagina_primeira_pagina(self, test_db, lista_notificacoes_exemplo, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        notificacao_repo.criar_tabela()
        criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)

        for i, notificacao in enumerate(lista_notificacoes_exemplo, start=1):
            notificacao.id_usuario = i
            inserir(notificacao)
        
        # Act
        pagina_notificacoes = obter_por_pagina(1, 4)

        # Assert
        assert len(pagina_notificacoes) == 4, "Deveria retornar 4 notificações na primeira página"
        assert all(isinstance(i, Notificacao) for i in pagina_notificacoes), "Todos os itens da página devem ser do tipo Notificação"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [i.id_notificacao for i in pagina_notificacoes]
        assert ids_retornados == ids_esperados, "Os IDs das notificações retornadas não são os esperados."

    def test_obter_recursos_por_pagina_terceira_pagina(self, test_db, lista_notificacoes_exemplo, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
                
        for i, notificacao in enumerate(lista_notificacoes_exemplo, start=1):
            notificacao.id_usuario = i
            notificacao.id_notificacao = i
            inserir(notificacao)
        
        # Act
        pagina_notificacao = obter_por_pagina(3, 4)

        # Assert
        assert len(pagina_notificacao) == 2, "Deveria retornar 2 notificações na terceira página"
        assert all(isinstance(i, Notificacao) for i in pagina_notificacao), "Todos os itens da página devem ser do tipo Notificação"
        ids_esperados = [9, 10]
        ids_retornados = [i.id_recurso for i in pagina_notificacao]
        assert ids_retornados == ids_esperados, "Os IDs das notificações retornadas na terceira página não são os esperados."

    def test_atualizar_recurso_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        criar_tabela()
        
        usuario = Usuario(1, "Usuario", "fulano@gmail.com", "senha@123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        notificacao = Notificacao(
            id_notificacao= id_notificacao,
            id_usuario=id_usuario,
            mensagem='Notificação de teste',
            data_envio='2023-10-01',
            tipo='pendente'
        )
        id_notificacao = inserir(notificacao)
        notificacao_atualizado = Notificacao(
            id_notificacao=id_notificacao,
            id_usuario=id_usuario,
            mensagem='Notificação de teste atualizada',
            data_envio='2023-10-02',
            tipo='enviada'
        )
  
        # Act
        resultado = atualizar(notificacao_atualizado)
        # Assert
        assert resultado == True, "A notificação não foi atualizado com sucesso."
        notificacao_db = obter_por_id(id_notificacao)
        assert notificacao_db is not None, "A notificação atualizado não foi encontrada no banco de dados."

    
    def test_atualizar_notificacao_inexistente(self, test_db):
        # Arrange
        notificacao_inexistente = Notificacao(
            id_notificacao=9999,  # ID que não existe
            id_usuario=1,   
            mensagem='Notificação inexistente',
            data_envio='2023-10-01',
            tipo='pendente'
        )
        # Act
        resultado = atualizar(notificacao_inexistente)
        # Assert
        assert resultado == False, "A atualização da notificação inexistente deveria ter falhado."

    def test_excluir_notificacao_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        criar_tabela()
        
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        notificacao = Notificacao(
            id_notificacao=0,
            id_usuario=id_usuario,
            mensagem='Notificação de teste',
            data_envio='2023-10-01',
            tipo='pendente'
        )
        id_notificacao = inserir(notificacao)
        # Act
        resultado = excluir(id_notificacao)
        # Assert
        assert resultado == True, "A notificação não foi deletada com sucesso."

    