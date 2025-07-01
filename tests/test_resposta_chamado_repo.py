import sys
import os
from chamado_model import Chamado
from data import usuario_repo
from data import chamado_repo
from data.resposta_chamado_repo import *
from usuario_model import Usuario

class TestRespostaChamadoRepo:
    def test_criar_tabela_resposta_chamado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de respostas de chamados não foi criada com sucesso."

    def test_inserir_resposta_chamado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()        
        criar_tabela()
        resposta_chamado = RespostaChamado(
            id_resposta=0,  
            id_chamado=1,  
            id_administrador=1, 
            mensagem='Resposta de teste',
            data_resposta='2023-10-01',
            status='pendente'
        )
        # Act
        resultado = inserir(resposta_chamado)
        # Assert
        assert resultado == True, "A resposta do chamado não foi inserida com sucesso."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")        
        id_usuario = usuario_repo.inserir(usuario)
        chamado = Chamado(
            id_chamado=0,  
            id_usuario_criador=id_usuario,
            id_administrador_responsavel=1,
            titulo='Chamado de Teste',
            descricao='Descrição do chamado teste',
            data_criacao='2023-10-01',
            status='em_andamento'
        )
        id_chamado = chamado_repo.inserir(chamado)
        resposta = RespostaChamado(
            id_resposta=0,
            id_chamado=1,
            id_usuario_autor=id_usuario,
            mensagem='Resposta de teste',
            data_resposta='2023-10-01',
        )
        id_resposta_chamado = chamado_repo.inserir(resposta)
        # Act
        resultado = obter_por_id(id_resposta_chamado)
        # Assert
        assert resultado is not None, "A resposta do chamado não foi encontrada pelo ID."
        assert resultado.id_resposta_chamado == 1, "O ID da resposta do chamado retornada não é o esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()
        # Act
        id_inexistente = 999
        resultado = obter_por_id(id_inexistente)
        # Assert
        assert resultado is None, "A busca por uma resposta do chamado inexistente deveria retornar None."

    def test_obter_resposta_por_pagina_primeira_pagina(self, test_db, lista_respostas_chamados_exemplo, lista_usuarios_exemplo, lista_chamados_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        
        for chamado in lista_chamados_exemplo:
            chamado_repo.inserir(chamado)
        
        for i, resposta_chamado in enumerate(lista_respostas_chamados_exemplo, start=1):
            resposta_chamado.id_aluno = i
            resposta_chamado.id_edital = i
            inserir(resposta_chamado)
        
        # Act
        pagina_respostas_chamados = obter_por_pagina(1, 4)

        # Assert
        assert len(pagina_respostas_chamados) == 4, "Deveria retornar 4 respostas de chamados na primeira página"
        assert all(isinstance(i, RespostaChamado) for i in pagina_respostas_chamados), "Todos os itens da página devem ser do tipo RespostaChamado"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [i.id_resposta_chamado for i in pagina_respostas_chamados]
        assert ids_retornados == ids_esperados, "Os IDs das respostas de chamados retornadas não são os esperados."

    def test_obter_resposta_por_pagina_terceira_pagina(self, test_db, lista_respostas_chamados_exemplo, lista_usuarios_exemplo, lista_chamados_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        
        for chamado in lista_chamados_exemplo:
            chamado_repo.inserir(chamado)
        
        for i, resposta_chamado in enumerate(lista_respostas_chamados_exemplo, start=1):
            resposta_chamado.id_aluno = i
            resposta_chamado.id_edital = i
            inserir(resposta_chamado)
        
        # Act
        pagina_respostas_chamados = obter_por_pagina(3, 4)

        # Assert
        assert len(pagina_respostas_chamados) == 2, "Deveria retornar 2 respostas de chamados na terceira página"
        assert all(isinstance(i, RespostaChamado) for i in pagina_respostas_chamados), "Todos os itens da página devem ser do tipo RespostaChamado"
        ids_esperados = [9, 10]
        ids_retornados = [i.id_resposta_chamado for i in pagina_respostas_chamados]
        assert ids_retornados == ids_esperados, "Os IDs das respostas de chamados retornadas na terceira página não são os esperados."

    def test_atualizar_resposta_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")        
        id_usuario = usuario_repo.inserir(usuario)
        chamado = Chamado(1, 1, 1, 'Chamado de Teste', 'Descrição do chamado teste', '2023-10-01', 'em_andamento')
        id_chamado = chamado_repo.inserir(chamado)
        resposta = RespostaChamado(
            id_resposta_chamado=0,
            id_chamado=1,
            id_usuario_autor=id_usuario,
            mensagem='Resposta de teste',
            data_resposta='2023-10-01',
        )
        id_resposta_chamado = chamado_repo.inserir(resposta)
        resposta_atualizada = RespostaChamado(
            id_resposta_chamado=id_resposta_chamado,
            id_chamado=id_chamado,
            id_usuario_autor=id_usuario,
            mensagem='Resposta de teste atualizada',
            data_resposta='2023-10-02',
        )
        
        # Act
        resultado = atualizar(resposta_atualizada)
        # Assert
        assert resultado == True, "A resposta do chamado não foi atualizada com sucesso."
        resposta_db = obter_por_id(id_resposta_chamado)
        assert resposta_db is not None, "A resposta do chamado atualizada não foi encontrada no banco de dados."

    
    def test_atualizar_resposta_inexistente(self, test_db):
        # Arrange
        resposta_inexistente = RespostaChamado(
            id_resposta_chamado=9999,  # ID inexistente
            id_chamado=1,
            id_usuario_autor=1,
            mensagem='Resposta inexistente',
            data_resposta='2023-10-01',
        )
        # Act
        resultado = atualizar(resposta_inexistente)
        # Assert
        assert resultado == False, "A atualização da resposta do chamado inexistente deveria ter falhado."

    def test_excluir_resposta_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()
        
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")        
        id_usuario = usuario_repo.inserir(usuario)
        chamado = Chamado(1, 1, 1, 'Chamado de Teste', 'Descrição do chamado teste', '2023-10-01', 'em_andamento')
        id_chamado = chamado_repo.inserir(chamado)
        resposta = RespostaChamado(
            id_resposta_chamado=0,
            id_chamado=id_chamado,
            id_usuario_autor=id_usuario,
            mensagem='Resposta de teste',
            data_resposta='2023-10-01',
        )
        id_resposta = inserir(resposta)
        # Act
        resultado = excluir(id_resposta)
        # Assert
        assert resultado == True, "A resposta do chamado não foi deletada com sucesso."

    def test_excluir_resposta_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()
        id_inexistente = 9999  
        # Act   
        resultado = excluir(id_inexistente)
        # Assert
        assert resultado == False, "A exclusão de uma resposta inexistente deveria ter falhado."
