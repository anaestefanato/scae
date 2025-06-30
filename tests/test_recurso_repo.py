import sys
import os

from data import usuario_repo
from data import inscricao_repo
from data.inscricao_repo import *
from recurso_model import Recurso

class TestInscricaoRepo:
    def test_criar_tabela_recurso(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        # Act
    resultado = criar_tabela()
    # Assert
    assert resultado == True, "A tabela de recursos não foi criada com sucesso."

    def test_inserir_recurso(self, test_db):
    # Arrange
        usuario_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        criar_tabela()
        recurso = Recurso(
            id_recurso=1,
            id_inscricao=1,
            id_assistente_social=1,
            descricao='Recurso de teste',
            data_envio='2023-10-01',
            data_resposta='2023-10-02',
            status='pendente'
        )
    # Act
    resultado = inserir()
    # Assert
    assert resultado == True, "O recurso não foi inserida com sucesso."