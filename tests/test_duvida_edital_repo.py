import pytest
import data.usuario_repo as usuario_repo
import data.edital_repo as edital_repo
import data.duvida_edital_repo as duvida_repo
from data.usuario_model import Usuario
from data.edital_model import Edital
from data.duvida_edital_model import DuvidaEdital

class TestDuvidaEditalRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = duvida_repo.criar_tabela()
        # Assert
        assert resultado is True, "A tabela de dúvidas de edital não foi criada com sucesso."

    def test_inserir_duvida_edital(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()    # cria tabela usuario
        edital_repo.criar_tabela()     # cria tabela edital
        duvida_repo.criar_tabela()     # cria tabela duvida edital

        usuario = Usuario(0, "Aluno Teste", "aluno@teste.com", "senha123", 1)
        id_aluno = usuario_repo.inserir(usuario)

        edital = Edital(0, "Edital Teste", "Descrição do edital", "2023-01-01", "2023-12-31", "arquivo.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)

        duvida = DuvidaEdital(0, id_edital, id_aluno, "Quando abre?", "Já está aberto", "2023-01-01", "2023-01-02", "respondido")
        
        # Act
        id_duvida = duvida_repo.inserir(duvida)
        duvida_db = duvida_repo.obter_por_id(id_duvida)

        # Assert
        assert duvida_db is not None, "A dúvida não foi inserida corretamente."
        assert duvida_db.pergunta == "Quando abre?", "A pergunta inserida não corresponde à esperada."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        edital_repo.criar_tabela()
        duvida_repo.criar_tabela()

        usuario = Usuario(0, "Aluno Teste", "aluno@teste.com", "senha123", 1)
        id_aluno = usuario_repo.inserir(usuario)

        edital = Edital(0, "Edital Teste", "Descrição do edital", "2023-01-01", "2023-12-31", "arquivo.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)

        duvida = DuvidaEdital(0, id_edital, id_aluno, "Quando abre?", None, "2023-01-01", None, "pendente")
        id_duvida = duvida_repo.inserir(duvida)

        # Act
        duvida_db = duvida_repo.obter_por_id(id_duvida)

        # Assert
        assert duvida_db is not None, "A dúvida não foi encontrada no banco de dados."
        assert duvida_db.id_duvida == id_duvida, "O ID da dúvida obtida não corresponde ao esperado."

    def test_obter_duvidas_por_pagina_primeira_pagina(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        edital_repo.criar_tabela()
        duvida_repo.criar_tabela()

        usuario = Usuario(0, "Aluno Teste", "aluno@teste.com", "senha123", 1)
        id_aluno = usuario_repo.inserir(usuario)
        edital = Edital(0, "Edital Teste", "Descrição do edital", "2023-01-01", "2023-12-31", "arquivo.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)
        duvidas = [
            DuvidaEdital(0, id_edital, id_aluno, f"Pergunta {i}", None, "2023-01-01", None, "pendente")
            for i in range(1, 11)
        ]
        for duvida in duvidas:
            duvida_repo.inserir(duvida)
        # Act
        pagina_duvidas = duvida_repo.obter_por_pagina(1, 5)
        # Assert
        assert len(pagina_duvidas) == 5, "A primeira página deve conter 5 dúvidas."
        
    def test_obter_duvidas_por_pagina_terceira_pagina(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        edital_repo.criar_tabela()
        duvida_repo.criar_tabela()

        usuario = Usuario(0, "Aluno Teste", "aluno@teste.com", "senha123", 1)
        id_aluno = usuario_repo.inserir(usuario)
        edital = Edital(0, "Edital Teste", "Descrição do edital", "2023-01-01", "2023-12-31", "arquivo.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)
        duvidas = [
            DuvidaEdital(0, id_edital, id_aluno, f"Pergunta {i}", None, "2023-01-01", None, "pendente")
            for i in range(1, 21)
        ]
        for duvida in duvidas:
            duvida_repo.inserir(duvida)
        # Act
        pagina_duvidas = duvida_repo.obter_por_pagina(3, 5)
        # Assert
        assert len(pagina_duvidas) == 5, "A terceira página deve conter 5 dúvidas."

    def test_atualizar_duvida_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        edital_repo.criar_tabela()
        duvida_repo.criar_tabela()

        usuario = Usuario(0, "Aluno Teste", "aluno@teste.com", "senha123", 1)
        id_aluno = usuario_repo.inserir(usuario)

        edital = Edital(0, "Edital Teste", "Descrição do edital", "2023-01-01", "2023-12-31", "arquivo.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)

        duvida = DuvidaEdital(0, id_edital, id_aluno, "Quando abre?", None, "2023-01-01", None, "pendente")
        id_duvida = duvida_repo.inserir(duvida)

        # Atualizar dúvida
        duvida_atualizada = DuvidaEdital(id_duvida, id_edital, id_aluno, "Quando fecha?", "Fechou ontem", "2023-01-01", "2023-01-02", "respondido")

        # Act
        resultado = duvida_repo.atualizar(duvida_atualizada)
        duvida_db = duvida_repo.obter_por_id(id_duvida)

        # Assert
        assert resultado is True, "A atualização da dúvida deveria ter sido bem-sucedida."
        assert duvida_db.pergunta == "Quando fecha?", "A pergunta da dúvida atualizada não corresponde ao esperado."
        assert duvida_db.resposta == "Fechou ontem", "A resposta da dúvida atualizada não corresponde ao esperado."
        assert duvida_db.status == "respondido", "O status da dúvida atualizada não corresponde ao esperado."

    def test_atualizar_duvida_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        edital_repo.criar_tabela()
        duvida_repo.criar_tabela()

        duvida = DuvidaEdital(999, 1, 1, "Pergunta X", "Resposta", "2023-01-01", "2023-01-02", "respondido")

        # Act
        resultado = duvida_repo.atualizar(duvida)
        duvida_db = duvida_repo.obter_por_id(999)

        # Assert
        assert resultado is False, "A atualização de uma dúvida inexistente deveria falhar."
        assert duvida_db is None, "A dúvida inexistente não deveria ter sido encontrada no banco de dados."

    def test_excluir_duvida_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        edital_repo.criar_tabela()
        duvida_repo.criar_tabela()

        usuario = Usuario(0, "Aluno Teste", "aluno@teste.com", "senha123", 1)
        id_aluno = usuario_repo.inserir(usuario)

        edital = Edital(0, "Edital Teste", "Descrição do edital", "2023-01-01", "2023-12-31", "arquivo.pdf", "ativo")
        id_edital = edital_repo.inserir(edital)

        duvida = DuvidaEdital(0, id_edital, id_aluno, "Quando abre?", None, "2023-01-01", None, "pendente")
        id_duvida = duvida_repo.inserir(duvida)

        # Act
        resultado = duvida_repo.excluir(id_duvida)
        duvida_db = duvida_repo.obter_por_id(id_duvida)

        # Assert
        assert resultado is True, "A exclusão da dúvida deveria ter sido bem-sucedida."
        assert duvida_db is None, "A dúvida ainda existe no banco de dados após a exclusão."

    def test_excluir_duvida_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        edital_repo.criar_tabela()
        duvida_repo.criar_tabela()

        id_duvida_inexistente = 999

        # Act
        resultado = duvida_repo.excluir(id_duvida_inexistente)
        duvida_db = duvida_repo.obter_por_id(id_duvida_inexistente)

        # Assert
        assert resultado is False, "A exclusão de uma dúvida inexistente deveria falhar."
        assert duvida_db is None, "A dúvida inexistente não deveria ter sido encontrada no banco de dados."
