import sys 
import os 
from data import auxilio_repo
from data.auxilio_repo import *
from data.auxilio_model import Auxilio

class TestAuxilioRepo:
    def test_criar_tabela_auxilio(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de auxílios não foi criada com sucesso."

    def test_inserir_auxilio(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_teste = Auxilio(0, "auxilio_teste", 1000.00)
        # Act
        id_auxilio_inserido = inserir(auxilio_teste)
        # Assert
        auxilio_db = obter_por_id(id_auxilio_inserido)
        assert auxilio_db is not None, "O auxílio não foi inserido não pode ser None."
        assert auxilio_db.nome == "auxilio_teste", "O nome do auxílio inserido não corresponde ao esperado."
    
    def test_obter_por_id_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_teste = Auxilio(0, "auxilio_teste", 1000.00)
        id_auxilio_inserido = inserir(auxilio_teste)
        # Act
        auxilio_db = obter_por_id(id_auxilio_inserido)
        # Assert
        assert auxilio_db is not None, "O auxílio não foi encontrado no banco de dados."
        assert auxilio_db.id_auxilio == id_auxilio_inserido, "O ID do auxílio obtido não corresponde ao esperado."
    
    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_auxilio_inexistente = 999
        # Act
        auxilio_db = obter_por_id(id_auxilio_inexistente)
        # Assert
        assert auxilio_db is None, "A busca por um auxílio inexistente deveria retornar None."

    def test_obter_todos_auxilios(self, test_db):
        # Arrange
        criar_tabela()
        auxilio1 = Auxilio(0, "auxilio1", 1500.00)
        auxilio2 = Auxilio(0, "auxilio2", 2000.00)
        inserir(auxilio1)
        inserir(auxilio2)
        # Act
        auxilios_db = obter_todos()
        # Assert
        assert len(auxilios_db) >= 2, "Deveria haver pelo menos dois auxílios no banco de dados."
        assert any(a.nome == "auxilio1" for a in auxilios_db), "O auxílio 'auxilio1' não foi encontrado na lista."
        assert any(a.nome == "auxilio2" for a in auxilios_db), "O auxílio 'auxilio2' não foi encontrado na lista."

    def test_atualizar_auxilio_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_teste = Auxilio(0, "auxilio_teste", 1000.00)
        id_auxilio_inserido = inserir(auxilio_teste)
        auxilio_atualizado = Auxilio(id_auxilio_inserido, "auxilio_atualizado", 1500.00)
        # Act
        resultado = atualizar(auxilio_atualizado)
        # Assert
        assert resultado == True, "A atualização do auxílio não foi bem-sucedida."
        auxilio_db = obter_por_id(id_auxilio_inserido)
        assert auxilio_db.nome == "auxilio_atualizado", "O nome do auxílio atualizado não corresponde ao esperado."
        assert auxilio_db.valor_mensal == 1500.00, "O valor mensal do auxílio atualizado não corresponde ao esperado."

    def test_atualizar_auxilio_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_teste = Auxilio(999, "auxilio_inexistente", 1000.00)
        # Act
        resultado = atualizar(auxilio_teste)
        # Assert
        assert resultado == False, "A atualização de um auxílio inexistente deveria retornar False."

    def test_excluir_auxilio_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_teste = Auxilio(0, "auxilio_teste", 1000.00)
        id_auxilio_inserido = inserir(auxilio_teste)
        # Act
        resultado = excluir(id_auxilio_inserido)
        # Assert
        assert resultado == True, "A exclusão do auxílio deveria ser bem-sucedida."
        auxilio_db = obter_por_id(id_auxilio_inserido)
        assert auxilio_db is None, "O auxílio deveria ter sido excluído e não pode ser encontrado no banco de dados."
    
    def test_excluir_auxilio_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_auxilio_inexistente = 999
        # Act
        resultado = excluir(id_auxilio_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um auxílio inexistente deveria retornar False."