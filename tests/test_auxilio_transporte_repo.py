import sys 
import os 
from data import auxilio_transporte_repo
from data.auxilio_transporte_repo import *
from data.auxilio_transporte_model import AuxilioTransporte

class TestAuxilioTransporteRepo:
    def test_criar_tabela_auxilio_transporte(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de auxílios de transporte não foi criada com sucesso."
    
    def test_inserir_auxilio_transporte(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_transporte_teste = AuxilioTransporte(0, "auxilio_transporte_teste", 500.00)
        # Act
        id_auxilio_transporte_inserido = inserir(auxilio_transporte_teste)
        # Assert
        auxilio_transporte_db = obter_por_id(id_auxilio_transporte_inserido)
        assert auxilio_transporte_db is not None, "O auxílio de transporte não foi inserido não pode ser None."
        assert auxilio_transporte_db.nome == "auxilio_transporte_teste", "O nome do auxílio de transporte inserido não corresponde ao esperado."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_transporte_teste = AuxilioTransporte(0, "auxilio_transporte_teste", 500.00)
        id_auxilio_transporte_inserido = inserir(auxilio_transporte_teste)
        # Act
        auxilio_transporte_db = obter_por_id(id_auxilio_transporte_inserido)
        # Assert
        assert auxilio_transporte_db is not None, "O auxílio de transporte não foi encontrado no banco de dados."
        assert auxilio_transporte_db.id_auxilio == id_auxilio_transporte_inserido, "O ID do auxílio de transporte obtido não corresponde ao esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_auxilio_transporte_inexistente = 999
        # Act
        auxilio_transporte_db = obter_por_id(id_auxilio_transporte_inexistente)
        # Assert
        assert auxilio_transporte_db is None, "A busca por um auxílio de transporte inexistente deveria retornar None."

    def test_obter_auxilios_transporte_por_pagina_primeira_pagina(self, test_db, lista_auxilios_transporte_exemplo):
        # Arrange 
        auxilio_transporte_repo.criar_tabela()
        lista_auxilios_transporte_exemplo = [
            AuxilioTransporte(1, "Auxilio Transporte 1", 300.00),
            AuxilioTransporte(2, "Auxilio Transporte 2", 400.00),
            AuxilioTransporte(3, "Auxilio Transporte 3", 500.00),
            AuxilioTransporte(4, "Auxilio Transporte 4", 600.00),
            AuxilioTransporte(5, "Auxilio Transporte 5", 700.00)
        ]   
        for auxilio in lista_auxilios_transporte_exemplo:
            auxilio_transporte_repo.inserir(auxilio)
        # Act
        pagina_auxilios_transporte = auxilio_transporte_repo.obter_auxilios_transporte_por_pagina(1, 4)
        # Assert
        assert len(pagina_auxilios_transporte) == 4, "Deveria retornar 4 auxílios de transporte na primeira página"
        assert all(isinstance(a, AuxilioTransporte) for a in pagina_auxilios_transporte), "Todos os itens da página devem ser do tipo AuxilioTransporte"    

    def test_obter_auxilios_transporte_por_pagina_terceira_pagina(self, test_db, lista_auxilios_transporte_exemplo):
        # Arrange
        auxilio_transporte_repo.criar_tabela()
        lista_auxilios_transporte_exemplo = [
            AuxilioTransporte(1, "Auxilio Transporte 1", 300.00),
            AuxilioTransporte(2, "Auxilio Transporte 2", 400.00),
            AuxilioTransporte(3, "Auxilio Transporte 3", 500.00),
            AuxilioTransporte(4, "Auxilio Transporte 4", 600.00),
            AuxilioTransporte(5, "Auxilio Transporte 5", 700.00)
        ]
        for auxilio in lista_auxilios_transporte_exemplo:
            auxilio_transporte_repo.inserir(auxilio)
        # Act
        pagina_auxilios_transporte = auxilio_transporte_repo.obter_auxilios_transporte_por_pagina(3, 2)
        # Assert
        assert len(pagina_auxilios_transporte) == 1, "Deveria retornar 1 auxílio de transporte na terceira página"
        assert all(isinstance(a, AuxilioTransporte) for a in pagina_auxilios_transporte), "Todos os itens da página devem ser do tipo AuxilioTransporte"
    
    def test_atualizar_auxilio_transporte_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_transporte_teste = AuxilioTransporte(0, "auxilio_transporte_teste", 500.00)
        id_auxilio_transporte_inserido = inserir(auxilio_transporte_teste)
        auxilio_transporte_teste.nome = "auxilio_transporte_atualizado" 
        auxilio_transporte_teste.id_auxilio = id_auxilio_transporte_inserido
        # Act
        resultado = atualizar(auxilio_transporte_teste)
        # Assert
        assert resultado == True, "A atualização do auxílio de transporte falhou."
        auxilio_transporte_db = obter_por_id(id_auxilio_transporte_inserido)
        assert auxilio_transporte_db.nome == "auxilio_transporte_atualizado", "O nome do auxílio de transporte atualizado não corresponde ao esperado."

    def test_atualizar_auxilio_transporte_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_transporte_teste = AuxilioTransporte(999, "auxilio_transporte_inexistente", 500.00)
        # Act
        resultado = atualizar(auxilio_transporte_teste)
        # Assert
        assert resultado == False, "A atualização de um auxílio de transporte inexistente deveria retornar False"
    
    def test_excluir_auxilio_transporte_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_transporte_teste = AuxilioTransporte(0, "auxilio_transporte_teste", 500.00)
        id_auxilio_transporte_inserido = inserir(auxilio_transporte_teste)  
        # Act
        resultado = excluir(id_auxilio_transporte_inserido)
        # Assert
        assert resultado == True, "A exclusão do auxílio de transporte deveria ser bem-sucedida."
    
    def test_excluir_auxilio_transporte_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_auxilio_transporte_inexistente = 999
        # Act
        resultado = excluir(id_auxilio_transporte_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um auxílio de transporte inexistente deveria retornar False."
