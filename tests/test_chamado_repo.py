from repo import chamado_repo
from model.chamado_model import Chamado
from repo import usuario_repo
from model.usuario_model import Usuario
from model.administrador_model import Administrador
from repo import administrador_repo, chamado_repo

class TestChamadoRepo:

    def test_criar_tabela_chamado(self, test_db):
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        resultado = chamado_repo.criar_tabela()
        assert resultado == True

    def test_inserir_chamado(self, test_db):
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        chamado_repo.criar_tabela()

        usuario = Usuario(1, "Fulano", "fulano@ifes.edu.br", "123", "aluno")
        admin = Administrador(2, "Ciclano", "ciclano@ifes.edu.br", "123", "admin", "CHAVE")

        id_usuario = usuario_repo.inserir(usuario)
        id_admin = administrador_repo.inserir(admin)

        chamado = Chamado(0, id_usuario, id_admin, "Teste", "Chamado Teste", "2023-10-01", "em_andamento")
        id_chamado = chamado_repo.inserir(chamado)
        assert id_chamado is not None

    def test_obter_por_id_existente(self, test_db):
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        chamado_repo.criar_tabela()

        usuario = Usuario(1, "Fulano", "fulano@ifes.edu.br", "123", "aluno")
        admin = Administrador(2, "Ciclano", "ciclano@ifes.edu.br", "123", "admin", "CHAVE")

        id_usuario = usuario_repo.inserir(usuario)
        id_admin = administrador_repo.inserir(admin)

        chamado = Chamado(0, id_usuario, id_admin, "Teste", "Chamado Teste", "2023-10-01", "em_andamento")
        id_chamado = chamado_repo.inserir(chamado)

        resultado = chamado_repo.obter_por_id(id_chamado)
        assert resultado is not None
        assert resultado.id_chamado == id_chamado

    def test_obter_por_id_inexistente(self, test_db):
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        chamado_repo.criar_tabela()

        resultado = chamado_repo.obter_por_id(9999)
        assert resultado is None

    def test_obter_por_pagina(self, test_db):
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        chamado_repo.criar_tabela()

        usuario = Usuario(1, "Usu1", "a1@ifes.edu.br", "123", "aluno")
        admin = Administrador(2, "Adm1", "b1@ifes.edu.br", "123", "admin", "CH1")
        id_usuario = usuario_repo.inserir(usuario)
        id_admin = administrador_repo.inserir(admin)

        for i in range(1, 6):
            chamado = Chamado(0, id_usuario, id_admin, f"Titulo {i}", "Descricao", "2023-10-01", "em_andamento")
            chamado_repo.inserir(chamado)

        resultados = chamado_repo.obter_por_pagina(1, 3)
        assert len(resultados) == 3
        assert all(isinstance(c, Chamado) for c in resultados)

    def test_atualizar_chamado(self, test_db):
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        chamado_repo.criar_tabela()

        usuario = Usuario(1, "Fulano", "fulano@ifes.edu.br", "123", "aluno")
        admin = Administrador(2, "Ciclano", "ciclano@ifes.edu.br", "123", "admin", "CHAVE")

        id_usuario = usuario_repo.inserir(usuario)
        id_admin = administrador_repo.inserir(admin)

        chamado = Chamado(0, id_usuario, id_admin, "Antigo", "Desc antiga", "2023-10-01", "em_andamento")
        id_chamado = chamado_repo.inserir(chamado)

        chamado_atualizado = Chamado(id_chamado, id_usuario, id_admin, "Novo", "Desc nova", "2023-10-01", "concluído")
        resultado = chamado_repo.atualizar(chamado_atualizado)
        assert resultado == True

        chamado_db = chamado_repo.obter_por_id(id_chamado)
        assert chamado_db.titulo == "Novo"
        assert chamado_db.status == "concluído"

    def test_excluir_chamado(self, test_db):
        usuario_repo.criar_tabela()
        administrador_repo.criar_tabela()
        chamado_repo.criar_tabela()

        usuario = Usuario(1, "Fulano", "fulano@ifes.edu.br", "123", "aluno")
        admin = Administrador(2, "Ciclano", "ciclano@ifes.edu.br", "123", "admin", "CHAVE")

        id_usuario = usuario_repo.inserir(usuario)
        id_admin = administrador_repo.inserir(admin)

        chamado = Chamado(0, id_usuario, id_admin, "Excluir", "Teste excluir", "2023-10-01", "em_andamento")
        id_chamado = chamado_repo.inserir(chamado)

        resultado = chamado_repo.excluir(id_chamado)
        assert resultado == True
        assert chamado_repo.obter_por_id(id_chamado) is None

    def test_excluir_chamado_inexistente(self, test_db):
        chamado_repo.criar_tabela()
        resultado = chamado_repo.excluir(9999)
        assert resultado == False
