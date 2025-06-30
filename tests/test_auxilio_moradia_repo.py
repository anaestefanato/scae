# test_auxilio_moradia.py

from data import auxilio_repo
from data.auxilio_model import Auxilio
from data.auxilio_moradia_model import AuxilioMoradia
from data.auxilio_moradia_repo import AuxilioMoradiaRepo
from data import edital_repo
from data import inscricao_repo

class TestAuxilioMoradiaRepo:
    def test_criar_tabela_auxilio_moradia(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        resultado = AuxilioMoradiaRepo.criar_tabela()
        assert resultado == True, "A tabela de auxílios moradia não foi criada com sucesso."

    def test_inserir_auxilio_moradia(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioMoradiaRepo.criar_tabela()

        auxilio_moradia = AuxilioMoradia(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao="Auxílio moradia",
            valor_mensal=300.00,
            data_inicio="2023-02-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio moradia",
            url_comp_residencia_fixa="http://fixa.com",
            url_comp_residencia_alugada="http://alugada.com",
            url_contrato_aluguel_cid_campus="http://campus.com",
            url_contrato_aluguel_cid_natal="http://natal.com"
        )

        id_inserido = AuxilioMoradiaRepo.inserir(auxilio_moradia)
        assert id_inserido is not None

    def test_obter_por_id_existente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioMoradiaRepo.criar_tabela()

        auxilio_moradia = AuxilioMoradia(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao="Teste",
            valor_mensal=350.00,
            data_inicio="2023-01-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio moradia",
            url_comp_residencia_fixa="http://fixa.com",
            url_comp_residencia_alugada="http://alugada.com",
            url_contrato_aluguel_cid_campus="http://campus.com",
            url_contrato_aluguel_cid_natal="http://natal.com"
        )

        id_inserido = AuxilioMoradiaRepo.inserir(auxilio_moradia)
        obj = AuxilioMoradiaRepo.obter_por_id(id_inserido)
        assert obj is not None
        assert obj.id_auxilio == id_inserido

    def test_obter_por_id_inexistente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioMoradiaRepo.criar_tabela()

        resultado = AuxilioMoradiaRepo.obter_por_id(9999)
        assert resultado is None

    def test_atualizar_auxilio_moradia_existente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioMoradiaRepo.criar_tabela()

        auxilio_moradia = AuxilioMoradia(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao="Original",
            valor_mensal=400.00,
            data_inicio="2023-01-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio moradia",
            url_comp_residencia_fixa="http://fixa-original.com",
            url_comp_residencia_alugada="http://alugada-original.com",
            url_contrato_aluguel_cid_campus="http://campus-original.com",
            url_contrato_aluguel_cid_natal="http://natal-original.com"
        )

        id_inserido = AuxilioMoradiaRepo.inserir(auxilio_moradia)
        auxilio_moradia.id_auxilio = id_inserido
        auxilio_moradia.url_comp_residencia_fixa = "http://fixa-novo.com"
        auxilio_moradia.url_comp_residencia_alugada = "http://alugada-novo.com"
        auxilio_moradia.url_contrato_aluguel_cid_campus = "http://campus-novo.com"
        auxilio_moradia.url_contrato_aluguel_cid_natal = "http://natal-novo.com"

        atualizado = AuxilioMoradiaRepo.atualizar(auxilio_moradia)
        assert atualizado

    def test_excluir_auxilio_moradia_existente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioMoradiaRepo.criar_tabela()

        auxilio_moradia = AuxilioMoradia(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao="Excluir",
            valor_mensal=250.00,
            data_inicio="2023-01-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio moradia",
            url_comp_residencia_fixa="http://fixa.com",
            url_comp_residencia_alugada="http://alugada.com",
            url_contrato_aluguel_cid_campus="http://campus.com",
            url_contrato_aluguel_cid_natal="http://natal.com"
        )

        id_inserido = AuxilioMoradiaRepo.inserir(auxilio_moradia)
        sucesso = AuxilioMoradiaRepo.excluir(id_inserido)
        assert sucesso

    def test_excluir_auxilio_moradia_inexistente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioMoradiaRepo.criar_tabela()

        sucesso = AuxilioMoradiaRepo.excluir(99999)
        assert not sucesso
