import sys 
import os 
from data import usuario_repo
from data.usuario_repo import *
from data.usuario_model import Usuario

class TestUsuarioRepo:
    def test_criar_tabela_usuario(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de usuários não foi criada com sucesso."

    
    def test_inserir_usuario(self, test_db):
        # Arrange
        criar_tabela()
        usuario_teste = Usuario(0, "Usuario Teste" , "fulano@gmail.com", "123456", "assistente")
        # Act
        id_usuario_inserido = inserir(usuario_teste)
        # Assert
        usuario_db = obter_por_id(id_usuario_inserido)
        assert usuario_db is not None, "O usuário não foi inserido não pode ser None."
        assert usuario_db.nome == "Usuario Teste", "O nome do usuário inserido não corresponde ao esperado."
        assert usuario_db.email == "fulano@gmail.com", "O email do usuário inserido deve ser None."
        assert usuario_db.senha == "123456", "A senha do usuário inserido deve ser None."
        assert usuario_db.tipo_usuario == "assistente", "O tipo de usuário do usuário inserido deve ser None."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        criar_tabela()
        usuario_teste = Usuario(0, "Usuario Teste", "joaosilva@email.com", "123456", "administrador")
        id_usuario_inserido = inserir(usuario_teste)
        # Act
        usuario_db = obter_por_id(id_usuario_inserido)
        # Assert
        assert usuario_db is not None, "O usuário não foi encontrado no banco de dados."
        assert usuario_db.id_usuario == id_usuario_inserido, "O ID do usuário obtido não corresponde ao esperado."
        assert usuario_db.nome == usuario_teste.nome, "O nome do usuário obtido não corresponde ao esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_usuario_inexistente = 999
        # Act
        usuario_db = obter_por_id(id_usuario_inexistente)
        # Assert
        assert usuario_db is None, "A busca por um usuário inexistente deveria retornar None."

    def test_obter_usuario_por_email_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        id_usuario_inserido = usuario_repo.inserir(usuario_exemplo)
        # Act
        usuario_db = usuario_repo.obter_usuario_por_email(usuario_exemplo.email)
        # Assert
        assert usuario_db is not None, "O usuário buscado por email deveria ser diferente de None"
        assert usuario_db.email == usuario_exemplo.email, "O email do usuário buscado deveria ser igual ao email do usuário inserido"
    
    def test_obter_usuario_por_email_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        # Act
        usuario_db = usuario_repo.obter_usuario_por_email("inexistente@email.com")
        # Assert
        assert usuario_db is None, "O usuário buscado por email inexistente deveria retornar None"
                                

    def test_atualizar_usuario_existente(self, test_db):
        # Arrange
        criar_tabela()
        usuario_teste = Usuario(0, "Usuario Teste", "fulano@gmail.com", "123456", "assistente")
        id_usuario_inserido = inserir(usuario_teste)
        usuario_inserido = obter_por_id(id_usuario_inserido)
        # Act
        usuario_inserido.nome = "Usuario Atualizado"
        usuario_inserido.email = "joaosilva@email.com"
        usuario_inserido.tipo_usuario = "administrador"
        resultado = atualizar(usuario_inserido)
        # Assert
        assert resultado == True, "A atualização do usuário falhou."
        usuario_db = obter_por_id(id_usuario_inserido)
        assert usuario_db.nome == "Usuario Atualizado", "O nome do usuário atualizado não corresponde ao esperado."
        assert usuario_db.email == "joaosilva@email.com", "O email do usuário atualizado não corresponde ao esperado."
        assert usuario_db.tipo_usuario == "administrador", "O tipo de usuário atualizado não corresponde ao esperado."

    def test_atualizar_usuario_inexistente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        usuario_exemplo.id = 999  # ID que não existe
        # Act
        resultado = usuario_repo.atualizar(usuario_exemplo)
        # Assert
        assert resultado == False, "A atualização de um usuário inexistente deveria retornar False"
    

    def test_excluir_usuario_existente(self, test_db):
        # Arrange
        criar_tabela()
        usuario_teste = Usuario(0, "Usuario Teste", "joaosilva@email.com", "123456", "administrador")
        id_usuario_inserido = inserir(usuario_teste)
        # Act
        resultado = excluir(id_usuario_inserido)
        # Assert
        assert resultado == True, "A exclusão do usuário falhou."
        usuario_db = obter_por_id(id_usuario_inserido)
        assert usuario_db == None, "O usuário não foi excluído corretamente, ainda existe no banco de dados."

    def test_excluir_usuario_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_usuario_inexistente = 999  # ID que não existe
        # Act
        resultado = excluir(id_usuario_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um usuário inexistente deveria retornar False."



    # def test_obter_por_pagina(self, test_db):
    #     # Arrange
    #     criar_tabela()
    #     for i in range(10):
    #         usuario = Usuario(0, f"Usuario {i+1}")
    #         inserir(usuario)
    #     # Act
    #     usuario1 = obter_por_pagina(1, 10)
    #     usuario2 = obter_por_pagina(2, 4)
    #     usuario3 = obter_por_pagina(3, 4)
    #     # Assert
    #     assert len(usuario1) == 10, "A primeira página deve conter 10 usuários."
    #     assert len(usuario2) == 4, "A segunda página deve conter 4 usuários."
    #     assert len(usuario3) == 2, "A terceira página deve conter 2 usuários."
    #     assert usuario3[0].nome == 8, "O primeiro usuário da terceira página deve ser o 8."