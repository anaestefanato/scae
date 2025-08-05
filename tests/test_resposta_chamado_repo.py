import sys
import os
from repo import resposta_chamado_repo
from repo.resposta_chamado_repo import *
from model.resposta_chamado_model import RespostaChamado
from repo import chamado_repo
from repo import usuario_repo
from model.usuario_model import Usuario
from model.chamado_model import Chamado
from model.administrador_model import Administrador
from repo import administrador_repo

class TestRespostaChamadoRepo:
    
    def test_criar_tabela_resposta_chamado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()

        # Act
        resultado = resposta_chamado_repo.criar_tabela()

        # Assert
        assert resultado is True, "A tabela resposta_chamado não foi criada com sucesso."


    def test_inserir_resposta_chamado(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()

        usuario = Usuario(0, "Maria", "maria@email.com", "senha", "usuario")
        id_usuario = usuario_repo.inserir(usuario)
        
        chamado_repo.criar_tabela()
        chamado = Chamado(0, id_usuario, 0, "Dúvida sobre sistema", "descricao", "2023-05-01", "em_andamento")
        chamado_repo.inserir(chamado)

        resposta = RespostaChamado(
            id_resposta=0,
            id_chamado=chamado.id_chamado,
            id_usuario=str(id_usuario),
            mensagem="Sua dúvida foi registrada.",
            data_resposta="2025-07-01",
            status=""
        )
        # Act
        resultado = inserir(resposta)
        # Assert
        assert isinstance(resultado, int), "Deve retornar um ID inteiro"
        assert resultado > 0, "O ID retornado deve ser maior que zero"

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()

        usuario = Usuario(0, "João", "joao@email.com", "123", "usuario")
        id_usuario = usuario_repo.inserir(usuario)

        chamado = Chamado(0, id_usuario, 0, "Dúvida sobre sistema", "descricao", "2023-05-01", "em_andamento")
        id_chamado = chamado_repo.inserir(chamado)

        resposta = RespostaChamado(0, id_chamado, str(id_usuario), "Mensagem", "2025-07-01", "")
        id_resposta = inserir(resposta)

        # Act
        resultado = obter_por_id(id_resposta)

        # Assert
        assert resultado is not None, "A resposta deveria ser encontrada pelo ID"
        assert resultado.id_resposta == id_resposta, "O ID retornado está incorreto"

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()
        # Act
        resultado = obter_por_id(999)
        # Assert
        assert resultado is None, "A busca por resposta inexistente deve retornar None"

    def test_obter_respostas_por_pagina_primeira_pagina(self, test_db, lista_usuarios_exemplo, lista_chamados_exemplo, lista_respostas_chamado_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        resposta_chamado_repo.criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        for chamado in lista_chamados_exemplo:
            chamado_repo.inserir(chamado)
        for resposta in lista_respostas_chamado_exemplo:
            resposta_chamado_repo.inserir(resposta)

        # Act
        pagina_respostas = resposta_chamado_repo.obter_por_pagina(1, 3)

        # Assert
        assert len(pagina_respostas) == 3, "Deveria retornar 3 respostas na primeira página"
        assert all(isinstance(r, RespostaChamado) for r in pagina_respostas), "Todos os itens devem ser do tipo RespostaChamado"
        ids_esperados = [1, 2, 3]
        ids_retornados = [r.id_resposta for r in pagina_respostas]
        assert ids_retornados == ids_esperados, "IDs retornados estão incorretos"


    def test_obter_respostas_por_pagina_terceira_pagina(self, test_db, lista_usuarios_exemplo, lista_chamados_exemplo, lista_respostas_chamado_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        resposta_chamado_repo.criar_tabela()

        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir(usuario)
        for chamado in lista_chamados_exemplo:
            chamado_repo.inserir(chamado)
        for resposta in lista_respostas_chamado_exemplo:
            resposta_chamado_repo.inserir(resposta)

        # Act
        pagina_respostas = resposta_chamado_repo.obter_por_pagina(3, 2)

        # Assert
        assert len(pagina_respostas) == 2, "Deveria retornar 2 respostas na terceira página"
        assert all(isinstance(r, RespostaChamado) for r in pagina_respostas), "Todos os itens devem ser do tipo RespostaChamado"
        ids_esperados = [5, 6]
        ids_retornados = [r.id_resposta for r in pagina_respostas]
        assert ids_retornados == ids_esperados, f"IDs retornados incorretos: {ids_retornados}"

    def test_atualizar_resposta_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()

        usuario = Usuario(0, "Ana", "ana@email.com", "123", "usuario")
        id_usuario = usuario_repo.inserir(usuario)

        chamado = Chamado(0, id_usuario, 0, "Dúvida sobre sistema", "descricao", "2023-05-01", "em_andamento")
        id_chamado = chamado_repo.inserir(chamado)

        resposta = RespostaChamado(0, id_chamado, str(id_usuario), "Original", "2025-07-01", "")
        id_resposta = inserir(resposta)

        resposta_atualizada = RespostaChamado(id_resposta, id_chamado, str(id_usuario), "Atualizado", "2025-07-01", "")
        # Act
        resultado = atualizar(resposta_atualizada)

        # Assert
        assert resultado is True, "A resposta não foi atualizada com sucesso"

    def test_atualizar_resposta_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        resposta = RespostaChamado(9999, 1, "1", "Inexistente", "2025-07-01", "")
        # Act
        resultado = atualizar(resposta)
        # Assert
        assert resultado is False, "Atualização de resposta inexistente deveria retornar False"

    def test_excluir_resposta_existente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        chamado_repo.criar_tabela()
        criar_tabela()

        usuario = Usuario(0, "Carlos", "carlos@email.com", "abc", "usuario")
        id_usuario = usuario_repo.inserir(usuario)

        chamado = Chamado(0, id_usuario, 0, "Dúvida sobre sistema", "descricao", "2023-05-01", "em_andamento")
        id_chamado = chamado_repo.inserir(chamado)

        resposta = RespostaChamado(0, id_chamado, str(id_usuario), "Para excluir", "2025-07-01", "")
        id_resposta = inserir(resposta)

        # Act
        resultado = excluir(id_resposta)

        # Assert
        assert resultado is True, "A resposta não foi excluída com sucesso"

    def test_excluir_resposta_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        # Act
        resultado = excluir(9999)
        # Assert
        assert resultado is False, "Exclusão de resposta inexistente deveria retornar False"