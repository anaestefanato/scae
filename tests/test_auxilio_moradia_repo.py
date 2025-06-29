import sys 
import os 
from data import auxilio_moradia_repo
from data.auxilio_moradia_repo import *
from data.auxilio_moradia_model import AuxilioMoradia

class TestAuxilioMoradiaRepo:
    def test_criar_tabela_auxilio_moradia(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de auxílios de moradia não foi criada com sucesso."

    def test_inserir_auxilio_moradia(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_moradia_teste = AuxilioMoradia(0, "auxilio_moradia_teste", 1200.00)
        # Act
        id_auxilio_moradia_inserido = inserir(auxilio_moradia_teste)
        # Assert
        auxilio_moradia_db = obter_por_id(id_auxilio_moradia_inserido)
        assert auxilio_moradia_db is not None, "O auxílio de moradia não foi inserido não pode ser None."
        assert auxilio_moradia_db.nome == "auxilio_moradia_teste", "O nome do auxílio de moradia inserido não corresponde ao esperado."
    
    def test_obter_por_id_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_moradia_teste = AuxilioMoradia(0, "auxilio_moradia_teste", 1200.00)
        id_auxilio_moradia_inserido = inserir(auxilio_moradia_teste)
        # Act
        auxilio_moradia_db = obter_por_id(id_auxilio_moradia_inserido)
        # Assert
        assert auxilio_moradia_db is not None, "O auxílio de moradia não foi encontrado no banco de dados."
        assert auxilio_moradia_db.id_auxilio == id_auxilio_moradia_inserido, "O ID do auxílio de moradia obtido não corresponde ao esperado."
    
    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_auxilio_moradia_inexistente = 999
        # Act
        auxilio_moradia_db = obter_por_id(id_auxilio_moradia_inexistente)
        # Assert
        assert auxilio_moradia_db is None, "A busca por um auxílio de moradia inexistente deveria retornar None."

    def test_obter_auxilios_moradia_por_pagina_primeira_pagina(self, test_db, lista_auxilios_moradia_exemplo):
        # Arrange
        auxilio_moradia_repo.criar_tabela()
        lista_auxilios_moradia_exemplo = [
            AuxilioMoradia(1, "Auxilio Moradia 1", 1000.00),
            AuxilioMoradia(2, "Auxilio Moradia 2", 1500.00),
            AuxilioMoradia(3, "Auxilio Moradia 3", 2000.00),
            AuxilioMoradia(4, "Auxilio Moradia 4", 2500.00),
            AuxilioMoradia(5, "Auxilio Moradia 5", 3000.00)
        ]
        for auxilio in lista_auxilios_moradia_exemplo:
            auxilio_moradia_repo.inserir(auxilio)
        # Act
        pagina_auxilios_moradia = auxilio_moradia_repo.obter_auxilios_moradia_por_pagina(1, 4)
        # Assert
        assert len(pagina_auxilios_moradia) == 4, "Deveria retornar 4 auxílios de moradia na primeira página"
        assert all(isinstance(u, AuxilioMoradia) for u in pagina_auxilios_moradia), "Todos os itens da página devem ser do tipo AuxilioMoradia"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id_auxilio for u in pagina_auxilios_moradia]
        assert ids_esperados == ids_retornados, "Os IDs dos auxílios de moradia na primeira página não estão corretos"

    def test_obter_auxilios_moradia_por_pagina_terceira_pagina(self, test_db, lista_auxilios_moradia_exemplo):
        # Arrange
        auxilio_moradia_repo.criar_tabela()
        lista_auxilios_moradia_exemplo = [
            AuxilioMoradia(1, "Auxilio Moradia 1", 1000.00),
            AuxilioMoradia(2, "Auxilio Moradia 2", 1500.00),
            AuxilioMoradia(3, "Auxilio Moradia 3", 2000.00),
            AuxilioMoradia(4, "Auxilio Moradia 4", 2500.00),
            AuxilioMoradia(5, "Auxilio Moradia 5", 3000.00)
        ]
        for auxilio in lista_auxilios_moradia_exemplo:
            auxilio_moradia_repo.inserir(auxilio)
        # Act
        pagina_auxilios_moradia = auxilio_moradia_repo.obter_auxilios_moradia_por_pagina(3, 2)
        # Assert
        assert len(pagina_auxilios_moradia) == 1, "Deveria retornar apenas 1 auxílio de moradia na terceira página"
        assert all(isinstance(u, AuxilioMoradia) for u in pagina_auxilios_moradia), "Todos os itens da página devem ser do tipo AuxilioMoradia"
        ids_esperados = [5]
        ids_retornados = [u.id_auxilio for u in pagina_auxilios_moradia]
        assert ids_esperados == ids_retornados, "O ID do auxílio de moradia na terceira página não está correto"

    def test_atualizar_auxilio_moradia_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_moradia_teste = AuxilioMoradia(0, "auxilio_moradia_teste", 1200.00)
        id_auxilio_moradia_inserido = inserir(auxilio_moradia_teste)
        auxilio_moradia_teste_atualizado = AuxilioMoradia(id_auxilio_moradia_inserido, "auxilio_moradia_atualizado", 1500.00)
        # Act
        resultado_atualizacao = atualizar(auxilio_moradia_teste_atualizado)
        # Assert
        assert resultado_atualizacao == True, "A atualização do auxílio de moradia não foi bem-sucedida."
        auxilio_moradia_db = obter_por_id(id_auxilio_moradia_inserido)
        assert auxilio_moradia_db.nome == "auxilio_moradia_atualizado", "O nome do auxílio de moradia atualizado não corresponde ao esperado."
        assert auxilio_moradia_db.valor == 1500.00, "O valor do auxílio de moradia atualizado não corresponde ao esperado."
    
    def test_atualizar_auxilio_moradia_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_moradia_teste = AuxilioMoradia(999, "auxilio_moradia_inexistente", 1200.00)
        # Act
        resultado_atualizacao = atualizar(auxilio_moradia_teste)
        # Assert
        assert resultado_atualizacao == False, "A atualização de um auxílio de moradia inexistente deveria retornar False."
    
    def test_excluir_auxilio_moradia_existente(self, test_db):
        # Arrange
        criar_tabela()
        auxilio_moradia_teste = AuxilioMoradia(0, "auxilio_moradia_teste", 1200.00)
        id_auxilio_moradia_inserido = inserir(auxilio_moradia_teste)
        # Act
        resultado_exclusao = excluir(id_auxilio_moradia_inserido)
        # Assert
        assert resultado_exclusao == True, "A exclusão do auxílio de moradia deveria ser bem-sucedida."
    
    def test_excluir_auxilio_moradia_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_auxilio_moradia_inexistente = 999
        # Act
        resultado_exclusao = excluir(id_auxilio_moradia_inexistente)
        # Assert
        assert resultado_exclusao == False, "A exclusão de um auxílio de moradia inexistente deveria retornar False."