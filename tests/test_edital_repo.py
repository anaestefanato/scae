import sys 
import os 
from data import edital_repo
from data.edital_repo import *
from data.edital_model import Edital

class TestEditalRepo:
    def test_criar_tabela_edital(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de editais não foi criada com sucesso."

    def test_inserir_edital(self, test_db):
        # Arrange
        criar_tabela()
        edital_teste = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo_teste.pdf", "ativo")
        # Act
        id_edital_inserido = inserir(edital_teste)
        # Assert
        edital_db = obter_por_id(id_edital_inserido)
        assert edital_db is not None, "O edital não foi inserido não pode ser None."
        assert edital_db.titulo == "Edital Teste", "O título do edital inserido não corresponde ao esperado."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        criar_tabela()
        edital_teste = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo_teste.pdf", "ativo")
        id_edital_inserido = inserir(edital_teste)
        # Act
        edital_db = obter_por_id(id_edital_inserido)
        # Assert
        assert edital_db is not None, "O edital não foi encontrado no banco de dados."
        assert edital_db.id_edital == id_edital_inserido, "O ID do edital obtido não corresponde ao esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_edital_inexistente = 999
        # Act
        edital_db = obter_por_id(id_edital_inexistente)
        # Assert
        assert edital_db is None, "A busca por um edital inexistente deveria retornar None."
    
    def test_obter_todos_editais(self, test_db):
        # Arrange
        criar_tabela()
        edital1 = Edital(0, "Edital 1", "Descrição do edital 1", "2023-01-01", "2023-12-31", "arquivo1.pdf", "ativo")
        edital2 = Edital(1, "Edital 2", "Descrição do edital 2", "2023-02-01", "2023-12-31", "arquivo2.pdf", "ativo")
        inserir(edital1)
        inserir(edital2)
        # Act
        editais_db = obter_todos()
        # Assert
        assert len(editais_db) >= 2, "Deveria haver pelo menos dois editais no banco de dados."
        assert any(e.titulo == "Edital 1" for e in editais_db), "O edital 'Edital 1' não foi encontrado na lista."
        assert any(e.titulo == "Edital 2" for e in editais_db), "O edital 'Edital 2' não foi encontrado na lista."

    def test_atualizar_edital_existente(self, test_db):
        # Arrange
        criar_tabela()
        edital_teste = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo_teste.pdf", "ativo")
        id_edital_inserido = inserir(edital_teste)
        edital_teste.id_edital = id_edital_inserido
        edital_teste.titulo = "Edital Teste Atualizado"
        # Act
        resultado = atualizar(edital_teste)
        # Assert
        assert resultado == True, "A atualização do edital deveria ter sido bem-sucedida."
        edital_db = obter_por_id(id_edital_inserido)
        assert edital_db.titulo == "Edital Teste Atualizado", "O título do edital atualizado não corresponde ao esperado."


    def test_atualizar_edital_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        edital_teste = Edital(999, "Edital Inexistente", "Descrição do edital inexistente", "2023-01-01", "2023-12-31", "arquivo_inexistente.pdf", "ativo")
        # Act
        resultado = atualizar(edital_teste)
        # Assert
        assert resultado == False, "A atualização de um edital inexistente deveria falhar."
        edital_db = obter_por_id(edital_teste.id_edital)
        assert edital_db is None, "O edital inexistente não deveria ter sido encontrado no banco de dados."


    def test_excluir_edital_existente(self, test_db):
        # Arrange
        criar_tabela()
        edital_teste = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo_teste.pdf", "ativo")
        id_edital_inserido = inserir(edital_teste)
        # Act
        resultado = excluir(id_edital_inserido)
        # Assert
        assert resultado == True, "A exclusão do edital deveria ter sido bem-sucedida."
        edital_db = obter_por_id(id_edital_inserido)
        assert edital_db is None, "O edital ainda existe no banco de dados após a exclusão."


    def test_excluir_edital_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_edital_inexistente = 999
        # Act
        resultado = excluir(id_edital_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um edital inexistente deveria falhar."
        edital_db = obter_por_id(id_edital_inexistente)
        assert edital_db is None, "O edital inexistente não deveria ter sido encontrado no banco de dados."