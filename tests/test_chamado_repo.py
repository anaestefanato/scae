import sys 
import os

from administrador_model import Administrador
from data import administrador_repo
from data import usuario_repo
from chamado_repo import *
from usuario_model import Usuario


class TestChamadoRepo:
    def test_criar_tabela_chamado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        # Act
    resultado = criar_tabela()
    # Assert
    assert resultado == True, "A tabela de chamados não foi criada com sucesso."

    def test_inserir_chamado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        criar_tabela()
        chamado = Chamado(
            id_duvida=1,
            id_usuario_criador=1,
            id_administrador=1,
            titulo='Teste de Chamado',
            descricao='Descrição do chamado teste',
            data_criacao='2023-10-01',
            status='em_andamento'
        )
        # Act
        resultado = inserir(chamado)
        # Assert
        assert resultado == True, "O chamado não foi inserida com sucesso."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        administrador = Administrador(2, "Admin Teste", "ciclano@gmail.com", "senha123", "admin", "ADMIN1234")
        id_admin = administrador_repo.inserir(administrador)
        chamado = chamado(
            id_chamado=0,  
            id_usuario_criador=id_usuario,
            id_administrador_responsavel=id_admin,
            titulo='Chamado de Teste',
            descricao='Descrição do chamado teste',
            data_criacao='2023-10-01',
            status='em_andamento'
        )
        id_chamado = inserir(chamado)
        # Act
        resultado = obter_por_id(id_chamado)
        # Assert
        assert resultado is not None, "O chamado não foi encontrado pelo ID."
        assert resultado.id_chamado == 1, "O ID do chamado retornado não é o esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        criar_tabela()
        # Act
        id_inexistente = 999
        resultado = obter_por_id(id_inexistente)
        # Assert
        assert resultado is None, "A busca por um chamado inexistente deveria retornar None."

    def test_obter_chamados_por_pagina_primeira_pagina(self, test_db, lista_chamados_exemplo, lista_usuarios_exemplo, lista_admin_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        
        for admin in lista_admin_exemplo:
            administrador_repo.inserir(admin)
        
        for i, chamado in enumerate(lista_chamados_exemplo, start=1):
            chamado.id_usuario_criador = i
            chamado.id_administrador_responsavel = i
            inserir(chamado)
        
        # Act
        pagina_chamados = obter_por_pagina(1, 4)

        # Assert
        assert len(pagina_chamados) == 4, "Deveria retornar 4 chamados na primeira página"
        assert all(isinstance(i, chamado) for i in pagina_chamados), "Todos os itens da página devem ser do tipo Chamado"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [i.id_chamado for i in pagina_chamados]
        assert ids_retornados == ids_esperados, "Os IDs dos chamados retornados não são os esperados."

    def test_obter_chamados_por_pagina_terceira_pagina(self, test_db, lista_chamados_exemplo, lista_usuarios_exemplo, lista_admin_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        
        for admin in lista_admin_exemplo:
            administrador_repo.inserir(admin)
        
        for i, chamado in enumerate(lista_chamados_exemplo, start=1):
            chamado.id_usuario_criador = i
            chamado.id_administrador_responsavel = i
            inserir(chamado)
        
        # Act
        pagina_chamados= obter_por_pagina(3, 4)

        # Assert
        assert len(pagina_chamados) == 2, "Deveria retornar 2 chamados na terceira página"
        assert all(isinstance(i, chamado) for i in pagina_chamados), "Todos os itens da página devem ser do tipo Chamado"
        ids_esperados = [9, 10]
        ids_retornados = [i.id_chamado for i in pagina_chamados]
        assert ids_retornados == ids_esperados, "Os IDs dos chamados retornados na terceira página não são os esperados."

    def test_atualizar_chamado_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        criar_tabela()
        
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        administrador = Administrador(2, "Admin Teste", "ciclano@gmail.com", "senha123", "admin", "ADMIN1234")
        id_administrador = administrador_repo.inserir(administrador)
        chamado = Chamado(
            id_chamado=id_chamado,
            id_usuario_criador=id_usuario,
            id_administrador_responsavel=id_administrador,
            titulo='Chamado de Teste',
            descricao='Descrição do chamado teste',
            data_criacao='2023-10-01',
            status='pendente',
        )
        id_chamado = inserir(chamado)
        chamado_atualizado = Chamado(
            id_chamado=id_chamado,
            id_usuario_criador=id_usuario,
            id_administrador_responsavel=id_administrador,
            titulo='Chamado Atualizado',
            descricao='Descrição do chamado atualizado',
            data_criacao='2023-10-01',
            status='concluído'
        )
        # Act
        resultado = atualizar(chamado_atualizado)
        # Assert
        assert resultado == True, "O chamado não foi atualizado com sucesso."
        chamado_db = obter_por_id(id_chamado)
        assert chamado_db is not None, "O chamado atualizado não foi encontrada no banco de dados."

    
    def test_atualizar_chamado_inexistente(self, test_db):
        # Arrange
        chamado_inexistente = Chamado(
            id_chamado=9999,  # ID que não existe
            id_usuario_criador=1,
            id_administrador_responsavel=1,
            titulo='Chamado Inexistente',
            descricao='Descrição do chamado inexistente',
            data_criacao='2023-10-01',
            status='pendente'
        )
        # Act
        resultado = atualizar(chamado_inexistente)
        # Assert
        assert resultado == False, "A atualização do chamado inexistente deveria ter falhado."

    def test_excluir_chamado_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        criar_tabela()
        
        usuario = Usuario(1, "Usuario Teste", "fulano@gmail.com", "senha123", "aluno")
        id_usuario = usuario_repo.inserir(usuario)
        administrador = Administrador(2, "Admin Teste", "ciclano@gmail.com", "senha123", "admin", "ADMIN1234")
        id_administrador = administrador_repo.inserir(administrador)
        chamado = chamado(
            id_chamado=0,  
            id_usuario_criador=id_usuario,
            id_administrador_responsavel=id_administrador,
            titulo='Chamado de Teste',
            descricao='Descrição do chamado teste',
            data_criacao='2023-10-01',
            status='em_andamento'  
        )
        id_chamado = inserir(chamado)
        # Act
        resultado = excluir(id_chamado)
        # Assert
        assert resultado == True, "O chamado não foi deletado com sucesso."

    def test_excluir_chamado_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        criar_tabela()
        id_inexistente = 9999  
        # Act   
        resultado = excluir(id_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um chamado inexistente deveria ter falhado."
