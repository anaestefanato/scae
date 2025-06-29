import sys 
import os 
from data import assistente_social_repo
from data.assistente_social_repo import *
from data.assistente_social_model import AssistenteSocial

class TestAssistenteSocialRepo:
    def test_criar_tabela_assistente_social(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A tabela de assistentes sociais não foi criada com sucesso."

    def test_inserir_assistente_social(self, test_db):
        # Arrange
        criar_tabela()
        assistente_social_teste = AssistenteSocial(0, "assistente_teste")
        # Act
        id_assistente_social_inserido = inserir(assistente_social_teste)
        # Assert
        assistente_social_db = obter_por_id(id_assistente_social_inserido)
        assert assistente_social_db is not None, "O assistente social não foi inserido não pode ser None."
        assert assistente_social_db.matricula == "assistente_teste", "A matrícula do assistente social inserido não corresponde ao esperado."

    def test_obter_por_id_existente(self, test_db):
        # Arrange
        criar_tabela()
        assistente_social_teste = AssistenteSocial(0, "assistente_teste")
        id_assistente_social_inserido = inserir(assistente_social_teste)
        # Act
        assistente_social_db = obter_por_id(id_assistente_social_inserido)
        # Assert
        assert assistente_social_db is not None, "O assistente social não foi encontrado no banco de dados."
        assert assistente_social_db.id_usuario == id_assistente_social_inserido, "O ID do assistente social obtido não corresponde ao esperado."
        assert assistente_social_db.matricula == assistente_social_teste.matricula, "A matrícula do assistente social obtido não corresponde ao esperado."

    def test_obter_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_assistente_social_inexistente = 999
        # Act
        assistente_social_db = obter_por_id(id_assistente_social_inexistente)
        # Assert
        assert assistente_social_db is None, "A busca por um assistente social inexistente deveria retornar None."
    
    def test_obter_todos_assistentes_sociais(self, test_db):
        # Arrange
        criar_tabela()
        assistente_social1 = AssistenteSocial(0, "assistente1")
        assistente_social2 = AssistenteSocial(0, "assistente2")
        inserir(assistente_social1)
        inserir(assistente_social2)
        # Act
        assistentes_sociais_db = obter_todos()
        # Assert
        assert len(assistentes_sociais_db) >= 2, "Deveria haver pelo menos dois assistentes sociais no banco de dados."
        assert any(a.matricula == "assistente1" for a in assistentes_sociais_db), "O assistente social 'assistente1' não foi encontrado na lista."
        assert any(a.matricula == "assistente2" for a in assistentes_sociais_db), "O assistente social 'assistente2' não foi encontrado na lista."

    def test_atualizar_assistente_social_existente(self, test_db):
        # Arrange
        criar_tabela()
        assistente_social_teste = AssistenteSocial(0, "assistente_teste")
        id_assistente_social_inserido = inserir(assistente_social_teste)
        assistente_social_teste.id_usuario = id_assistente_social_inserido
        assistente_social_teste.matricula = "assistente_atualizado"
        # Act
        resultado = atualizar(assistente_social_teste)
        # Assert
        assert resultado == True, "A atualização do assistente social falhou."
        assistente_social_db = obter_por_id(id_assistente_social_inserido)
        assert assistente_social_db.matricula == "assistente_atualizado", "A matrícula do assistente social atualizado não corresponde ao esperado."

    def test_atualizar_assistente_social_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        assistente_social_teste = AssistenteSocial(999, "assistente_inexistente")
        # Act
        resultado = atualizar(assistente_social_teste)
        # Assert
        assert resultado == False, "A atualização de um assistente social inexistente deveria falhar."

    def test_excluir_assistente_social_existente(self, test_db):
        # Arrange
        criar_tabela()
        assistente_social_teste = AssistenteSocial(0, "assistente_teste")
        id_assistente_social_inserido = inserir(assistente_social_teste)
        # Act
        resultado = excluir(id_assistente_social_inserido)
        # Assert
        assert resultado == True, "A exclusão do assistente social deveria ser bem-sucedida."
        assistente_social_db = obter_por_id(id_assistente_social_inserido)
        assert assistente_social_db is None, "O assistente social deveria ter sido excluído e não pode ser encontrado no banco de dados."
    
    def test_excluir_assistente_social_inexistente(self, test_db):
        # Arrange
        criar_tabela()
        id_assistente_social_inexistente = 999
        # Act
        resultado = excluir(id_assistente_social_inexistente)
        # Assert
        assert resultado == False, "A exclusão de um assistente social inexistente deveria retornar False."
        