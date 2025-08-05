from repo import usuario_repo
from repo.notificacao_repo import *
from model.usuario_model import Usuario
from model.notificacao_model import Notificacao

class TestNotificacaoRepo:
    def test_criar_tabela_notificacao(self, test_db):
        usuario_repo.criar_tabela()
        resultado = criar_tabela()
        assert resultado == True, "A tabela de notificações não foi criada com sucesso."

    def test_inserir_notificacao(self, test_db):
        usuario_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(id_usuario=None, nome="Teste", email="teste@email.com", senha="1234", tipo_usuario="aluno")
        id_usuario = usuario_repo.inserir(usuario)
        notificacao = Notificacao(
            id_notificacao=None,
            id_usuario_destinatario=id_usuario,
            titulo="Teste de notificação",
            data_envio="2023-10-01",
            tipo="pendente"
        )
        resultado = inserir(notificacao)
        assert resultado is not None, "A notificação não foi inserida com sucesso."

    def test_obter_por_id_existente(self, test_db):
        usuario_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(id_usuario=None, nome="Teste", email="teste@email.com", senha="1234", tipo_usuario="aluno")
        id_usuario = usuario_repo.inserir(usuario)
        notificacao = Notificacao(
            id_notificacao=None,
            id_usuario_destinatario=id_usuario,
            titulo="Notificação de teste",
            data_envio="2023-10-01",
            tipo="pendente"
        )
        id_notificacao = inserir(notificacao)
        resultado = obter_por_id(id_notificacao)
        assert resultado is not None, "A notificação não foi encontrada pelo ID."
        assert resultado.id_notificacao == id_notificacao, "O ID retornado não é o esperado."

    def test_obter_por_id_inexistente(self, test_db):
        usuario_repo.criar_tabela()
        criar_tabela()
        resultado = obter_por_id(9999)
        assert resultado is None, "A busca por uma notificação inexistente deveria retornar None."

    def test_obter_por_pagina(self, test_db):
        usuario_repo.criar_tabela()
        criar_tabela()
        for i in range(1, 6):
            usuario = Usuario(id_usuario=None, nome=f"Usuário {i}", email=f"user{i}@mail.com", senha="123", tipo_usuario="aluno")
            id_usuario = usuario_repo.inserir(usuario)
            notificacao = Notificacao(
                id_notificacao=None,
                id_usuario_destinatario=id_usuario,
                titulo=f"Notificação {i}",
                data_envio=f"2023-10-0{i}",
                tipo="pendente"
            )
            inserir(notificacao)
        pagina = obter_por_pagina(1, 4)
        assert len(pagina) == 4, "Deveria retornar 4 notificações na primeira página."
        assert all(isinstance(n, Notificacao) for n in pagina), "Todos os itens devem ser do tipo Notificacao."

    def test_atualizar_notificacao_existente(self, test_db):
        usuario_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(id_usuario=None, nome="Usuário", email="email@email.com", senha="1234", tipo_usuario="aluno")
        id_usuario = usuario_repo.inserir(usuario)
        notificacao = Notificacao(
            id_notificacao=None,
            id_usuario_destinatario=id_usuario,
            titulo="Título original",
            data_envio="2023-10-01",
            tipo="pendente"
        )
        id_notificacao = inserir(notificacao)
        notificacao_atualizada = Notificacao(
            id_notificacao=id_notificacao,
            id_usuario_destinatario=id_usuario,
            titulo="Título atualizado",
            data_envio="2023-10-01",
            tipo="concluída"
        )
        resultado = atualizar(notificacao_atualizada)
        assert resultado == True, "A notificação não foi atualizada com sucesso."
        notificacao_db = obter_por_id(id_notificacao)
        assert notificacao_db.titulo == "Título atualizado", "A atualização não foi refletida no banco."

    def test_atualizar_notificacao_inexistente(self, test_db):
        criar_tabela()  # ✅ GARANTE que a tabela exista
        notificacao = Notificacao(
            id_notificacao=9999,
            id_usuario_destinatario=1,
            titulo="Teste",
            data_envio="2023-10-01",
            tipo="pendente"
        )
        resultado = atualizar(notificacao)
        assert resultado == False, "A atualização de uma notificação inexistente deveria falhar."


    def test_excluir_notificacao_existente(self, test_db):
        usuario_repo.criar_tabela()
        criar_tabela()
        usuario = Usuario(id_usuario=None, nome="Usuário", email="email@email.com", senha="1234", tipo_usuario="aluno")
        id_usuario = usuario_repo.inserir(usuario)
        notificacao = Notificacao(
            id_notificacao=None,
            id_usuario_destinatario=id_usuario,
            titulo="Notificação para excluir",
            data_envio="2023-10-01",
            tipo="pendente"
        )
        id_notificacao = inserir(notificacao)
        resultado = excluir(id_notificacao)
        assert resultado == True, "A notificação não foi excluída com sucesso."
        assert obter_por_id(id_notificacao) is None, "A notificação ainda existe após a exclusão."

    def test_excluir_notificacao_inexistente(self, test_db):
        criar_tabela()
        resultado = excluir(9999)
        assert resultado == False, "Excluir uma notificação inexistente deveria retornar False."
