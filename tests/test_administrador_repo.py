import sys 
import os 
from data import administrador_repo
from data.administrador_repo import *
from data.administrador_model import Administrador

class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de administradores não foi criada com sucesso."

    def test_inserir_administrador(self, test_db):
        # Arrange
        criar_tabela()
        administrador_teste = Administrador(0, "admin_teste")
        # Act
        id_administrador_inserido = inserir(administrador_teste)
        # Assert
        administrador_db = obter_por_id(id_administrador_inserido)
        assert administrador_db is not None, "O administrador não foi inserido não pode ser None."
        assert administrador_db.matricula == "admin_teste", "A matrícula do administrador inserido não corresponde ao esperado."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        criar_tabela()
        administrador_teste = Administrador(0, "admin_teste")
        id_administrador_inserido = inserir(administrador_teste)
        # Act
        administrador_db = obter_por_id(id_administrador_inserido)
        # Assert
        assert administrador_db is not None, "O administrador não foi encontrado no banco de dados."
        assert administrador_db.id_usuario == id_administrador_inserido, "O ID do administrador obtido não corresponde ao esperado."
        assert administrador_db.matricula == administrador_teste.matricula, "A matrícula do administrador obtido não corresponde ao esperado."
    
    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_administrador_inexistente = 999
        # Act
        administrador_db = obter_por_id(id_administrador_inexistente)
        # Assert
        assert administrador_db is None, "A busca por um administrador inexistente deveria retornar None."
    
    def test_obter_todos_administradores(self, test_db):
        # Arrange
        criar_tabela()
        administrador1 = Administrador(0, "admin1")
        administrador2 = Administrador(0, "admin2")
        inserir(administrador1)
        inserir(administrador2)
        # Act
        administradores_db = obter_todos()
        # Assert
        assert len(administradores_db) >= 2, "Deveria haver pelo menos dois administradores no banco de dados."
        assert any(a.matricula == "admin1" for a in administradores_db), "O administrador 'admin1' não foi encontrado na lista."
        assert any(a.matricula == "admin2" for a in administradores_db), "O administrador 'admin2' não foi encontrado na lista."

    def test_atualizar_administrador_existente(self, test_db):
        # Arrange
        criar_tabela()
        administrador_teste = Administrador(0, "admin_teste")
        id_administrador_inserido = inserir(administrador_teste)
        administrador_teste.id_usuario = id_administrador_inserido
        administrador_teste.matricula = "admin_atualizado"
        # Act
        resultado = atualizar(administrador_teste)
        # Assert
        assert resultado == True, "A atualização do administrador deveria ser bem-sucedida."
        administrador_db = obter_por_id(id_administrador_inserido)
        assert administrador_db.matricula == "admin_atualizado", "A matrícula do administrador atualizado não corresponde ao esperado."
    
    def test_atualizar_administrador_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        administrador_teste = Administrador(999, "admin_inexistente")
        # Act
        resultado = atualizar(administrador_teste)
        # Assert
        assert resultado == False, "A atualização de um administrador inexistente deveria falhar."
    
    def test_excluir_administrador_existente(self, test_db):
        # Arrange
        criar_tabela()
        administrador_teste = Administrador(0, "admin_teste")
        id_administrador_inserido = inserir(administrador_teste)
        # Act
        resultado = excluir(id_administrador_inserido)
        # Assert
        assert resultado == True, "A exclusão do administrador deveria ser bem-sucedida."
        administrador_db = obter_por_id(id_administrador_inserido)
        assert administrador_db is None, "O administrador deveria ter sido excluído do banco de dados."
    
    def test_excluir_administrador_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_administrador_inexistente = 999
        # Act
        resultado = excluir(id_administrador_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um administrador inexistente deveria falhar."