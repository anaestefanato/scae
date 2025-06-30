import sys 
import os

from data import usuario_repo 
from data.notificacao_repo import *

class TestNotificacaoRepo:
    def test_criar_tabela_notificacao(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        # Act
    resultado = criar_tabela()
    # Assert
    assert resultado == True, "A tabela de inscrições não foi criada com sucesso."

    def test_inserir_notificacao(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()

        criar_tabela()
        notificacao = Notificacao(
            id_notificacao=1,
            id_usuario='user123',
            mensagem='Teste de notificação',
            data_envio='2023-10-01',
            status='pendente'
        )
        # Act
        resultado = inserir(notificacao)
        # Assert
        assert resultado == True, "A inscrição não foi inserida com sucesso."