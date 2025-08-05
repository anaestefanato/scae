import sys
import os
from repo import recurso_repo
from repo.recurso_repo import *
from model.recurso_model import Recurso
from repo import inscricao_repo
from repo import usuario_repo
from model.usuario_model import Usuario
from model.inscricao_model import Inscricao

class TestRecursoRepo:
    def test_criar_tabela_recurso(self, test_db):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
       # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de recursos não foi criada com sucesso."

    def test_inserir_recurso(self, test_db):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
        criar_tabela()
        recurso = Recurso(
            id_recurso=1,
            id_inscricao=1,
            id_assistente=1,
            descricao="Justificativa do recurso",
            data_envio="2023-10-01",
            data_resposta="2023-10-05",
            status="pendente"
        )
        # Act
        resultado = inserir(recurso)
        # Assert
        assert resultado is not None, "O recurso não foi inserido com sucesso."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()  # recurso_repo.criar_tabela()
        
        # Inserir dados mínimos nas tabelas referenciadas
        usuario = Usuario(0, "Nome", "email@email.com", "senha123", "assistente")
        id_usuario = usuario_repo.inserir(usuario)

        inscricao = Inscricao(
            id_inscricao=0,
            id_aluno=1,  # pode ser fictício se não tiver FK forte
            id_edital=1,
            data_inscricao="2023-09-01",
            status="pendente",
            urlDocumentoIdentificacao="url_doc",
            urlDeclaracaoRenda="url_renda",
            urlTermoResponsabilidade="url_termo"
        )
        id_inscricao = inscricao_repo.inserir(inscricao)

        recurso = Recurso(
            id_recurso=0,
            id_inscricao=id_inscricao,
            id_assistente=id_usuario,
            descricao="Justificativa do recurso",
            data_envio="2023-10-01",
            data_resposta="2023-10-05",
            status="pendente"
        )

        
        recurso = Recurso(
            id_recurso=0,
            id_inscricao=1,      # só valores fictícios
            id_assistente=1,     # só valores fictícios
            descricao="Justificativa do recurso",
            data_envio="2023-10-01",
            data_resposta="2023-10-05",
            status="pendente"
        )
        
        id_gerado = inserir(recurso)
        
        # Act
        resultado = obter_por_id(id_gerado)
        
        # Assert
        assert resultado is not None, "O recurso deveria ser encontrado pelo ID."
        assert resultado.id_recurso == id_gerado, "O ID do recurso encontrado está incorreto."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
        criar_tabela()
        # Act
        resultado = obter_por_id(999)
        # Assert
        assert resultado is None, "A busca por um recurso inexistente deveria retornar None."

    def test_obter_recursos_por_pagina_primeira_pagina(self, test_db, lista_usuarios_exemplo, lista_inscricoes_exemplo, lista_recursos_exemplo):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
        recurso_repo.criar_tabela()
        for inscricao in lista_inscricoes_exemplo:
            inscricao_repo.inserir(inscricao)
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        for recurso in lista_recursos_exemplo:
            recurso_repo.inserir(recurso)
        # Act
        pagina_recursos = recurso_repo.obter_por_pagina(1, 4)
        # Assert
        assert len(pagina_recursos) == 4, "Deveria retornar 4 recursos na primeira página"
        assert all(isinstance(r, Recurso) for r in pagina_recursos), "Todos os itens da página devem ser do tipo Recurso"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [r.id_recurso for r in pagina_recursos]
        assert ids_esperados == ids_retornados, "Os IDs dos recursos na primeira página não estão corretos"


    def test_obter_recursos_por_pagina_terceira_pagina(self, test_db, lista_usuarios_exemplo, lista_inscricoes_exemplo, lista_recursos_exemplo):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
        recurso_repo.criar_tabela()
        for inscricao in lista_inscricoes_exemplo:
            inscricao_repo.inserir(inscricao)
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        for recurso in lista_recursos_exemplo:
            recurso_repo.inserir(recurso)
        # Act
        pagina_recursos = recurso_repo.obter_por_pagina(3, 2)
        # Assert
        assert len(pagina_recursos) == 2, "Deveria retornar 2 recursos na terceira página"
        assert all(isinstance(r, Recurso) for r in pagina_recursos), "Todos os itens da página devem ser do tipo Recurso"
        ids_esperados = [5, 6]
        ids_retornados = [r.id_recurso for r in pagina_recursos]
        assert ids_esperados == ids_retornados, f"Os IDs dos recursos na terceira página não estão corretos: {ids_retornados}"

    def test_atualizar_recurso_existente(self, test_db):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
        criar_tabela()
        recurso = Recurso(0, 1, 1, "Texto original", "2023-10-01", "2023-10-02", "pendente")
        id_recurso = inserir(recurso)
        recurso_atualizado = Recurso(id_recurso, 1, 1, "Texto atualizado", "2023-10-01", "2023-10-02", "respondido")
        # Act
        resultado = atualizar(recurso_atualizado)
        # Assert
        assert resultado is True, "O recurso não foi atualizado com sucesso."

    def test_atualizar_recurso_inexistente(self, test_db):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
        recurso = Recurso(9999, 1, 1, "Texto inexistente", "2023-10-01", "2023-10-02", "rejeitado")
        # Act
        resultado = atualizar(recurso)
        # Assert
        assert resultado is False, "Atualização de recurso inexistente deveria falhar."

    def test_excluir_recurso_existente(self, test_db):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
        criar_tabela()
        recurso = Recurso(0, 1, 1, "Para excluir", "2023-10-01", "2023-10-02", "pendente")
        id_recurso = inserir(recurso)
        # Act
        resultado = excluir(id_recurso)
        # Assert
        assert resultado is True, "O recurso não foi excluído com sucesso."

    def test_excluir_recurso_inexistente(self, test_db):
        # Arrange
        inscricao_repo.criar_tabela()
        usuario_repo.criar_tabela()
        criar_tabela()
        # Act
        resultado = excluir(9999)
        # Assert
        assert resultado is False, "A exclusão de recurso inexistente deveria falhar."