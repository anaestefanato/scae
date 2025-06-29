import sys 
import os 
from data import auxilio_repo
from data.auxilio_repo import *
from data.auxilio_model import Auxilio
from data import usuario_repo
from data import edital_repo
from data import inscricao_repo
from data.edital_model import Edital
from data.inscricao_model import Inscricao

class TestAuxilioRepo:
    def test_criar_tabela_auxilio(self, test_db):
        # Arrange
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de auxílios não foi criada com sucesso."

    def test_inserir_auxilio(self, test_db):
        # Arrange
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        edital_teste = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo_teste.pdf", "ativo")
        id_edital_inserido = edital_repo.inserir(edital_teste)
        inscricao_teste = Inscricao(0, id_edital_inserido, 0, "2023-01-01", "pendente", "http://example.com/doc1", "http://example.com/renda1", "http://example.com/termo1")
        id_inscricao_inserida = inscricao_repo.inserir(inscricao_teste)
        auxilio_teste = Auxilio(0, id_edital_inserido, id_inscricao_inserida, "auxilio teste", 1000.00, "2023-01-01", "2023-12-31", "auxilio moradia")
        # Act
        id_auxilio_inserido = inserir(auxilio_teste)
        # Assert
        auxilio_db = obter_por_id(id_auxilio_inserido)
        assert auxilio_db is not None, "O auxílio não foi inserido não pode ser None."
        assert auxilio_db.id_auxilio == id_auxilio_inserido, "O ID do auxílio inserido não corresponde ao esperado."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        edital_teste = Edital(0, "Edital Teste", "Descrição do edital teste", "2023-01-01", "2023-12-31", "arquivo.pdf", "ativo")
        id_edital = edital_repo.inserir(edital_teste)

        inscricao_teste = Inscricao(0, id_edital, 0, "2023-01-01", "pendente", "url1", "url2", "url3")
        id_inscricao = inscricao_repo.inserir(inscricao_teste)

        auxilio_teste = Auxilio(0, id_edital, id_inscricao, "auxilio teste", 1000.00, "2023-01-01", "2023-12-31", "auxilio moradia")
        id_auxilio = inserir(auxilio_teste)
        id_auxilio_inserido = inserir(auxilio_teste)
        # Act
        auxilio_db = obter_por_id(id_auxilio_inserido)
        # Assert
        assert auxilio_db is not None, "O auxílio não foi encontrado no banco de dados."
        assert auxilio_db.id_auxilio == id_auxilio_inserido, "O ID do auxílio obtido não corresponde ao esperado."
    
    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        id_auxilio_inexistente = 999
        # Act
        auxilio_db = obter_por_id(id_auxilio_inexistente)
        # Assert
        assert auxilio_db is None, "A busca por um auxílio inexistente deveria retornar None."

    def test_obter_todos_auxilios(self, test_db):
        # Arrange
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()

        edital_teste = Edital(0, "Edital Teste", "Descrição", "2023-01-01", "2023-12-31", "arquivo.pdf", "ativo")
        id_edital = edital_repo.inserir(edital_teste)

        inscricao_teste = Inscricao(0, id_edital, 0, "2023-01-01", "pendente", "url1", "url2", "url3")
        id_inscricao = inscricao_repo.inserir(inscricao_teste)

        auxilio1 = Auxilio(0, id_edital, id_inscricao, "auxilio 1", 1500.00, "2023-01-01", "2023-12-31", "auxilio transporte")
        auxilio2 = Auxilio(0, id_edital, id_inscricao, "auxilio 2", 2000.00, "2023-01-01", "2023-12-31", "auxilio material")

        inserir(auxilio1)
        inserir(auxilio2)

        # Act
        auxilios_db = obter_todos()

        # Assert
        assert len(auxilios_db) == 2
        assert auxilios_db[0].descricao == "auxilio 1"
        assert auxilios_db[1].descricao == "auxilio 2"


    def test_atualizar_auxilio_existente(self, test_db):
        # Arrange
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        auxilio_teste = Auxilio(0, 0, 0, "auxilio teste", 1000.00, "2023-01-01", "2023-12-31", "auxilio moradia")
        id_auxilio_inserido = inserir(auxilio_teste)
        auxilio_atualizado = Auxilio(id_auxilio_inserido, 0, 0, "auxilio atualizado", 1500.00, "2023-01-01", "2023-12-31", "auxilio transporte")
        
        # Act
        resultado = atualizar(auxilio_atualizado)

        # Assert
        assert resultado == True, "A atualização do auxílio não foi bem-sucedida."
        auxilio_db = obter_por_id(id_auxilio_inserido)
        assert auxilio_db.descricao == "auxilio atualizado", "A descrição do auxílio atualizado não corresponde ao esperado."

    def test_atualizar_auxilio_inexistente(self, test_db):
        # Arrange
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        auxilio_teste = Auxilio(0, 0, 999, "auxilio inexistente", 1000.00, "2023-01-01", "2023-12-31", "auxilio moradia")
        # Act
        resultado = atualizar(auxilio_teste)
        # Assert
        assert resultado == False, "A atualização de um auxílio inexistente deveria retornar False."

    def test_excluir_auxilio_existente(self, test_db):
        # Arrange
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        auxilio_teste = Auxilio(0, 0, 0, "auxilio_teste", 1000.00, "2023-01-01", "2023-12-31", "auxilio moradia")
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