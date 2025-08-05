from repo import auxilio_repo
from model.auxilio_model import Auxilio
from model.auxilio_transporte_model import AuxilioTransporte
from repo.auxilio_transporte_repo import AuxilioTransporteRepo
from repo import edital_repo
from repo import inscricao_repo

class TestAuxilioTransporteRepo:
    def test_criar_tabela_auxilio_transporte(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        resultado = AuxilioTransporteRepo.criar_tabela()
        assert resultado == True, "A tabela de auxílios de transporte não foi criada com sucesso."

    def test_inserir_auxilio_transporte(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioTransporteRepo.criar_tabela()

        auxilio_transporte = AuxilioTransporte(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao="teste",
            valor_mensal=123.45,
            data_inicio="2023-02-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio transporte",
            urlCompResidencia="http://r.com",
            urlCompTransporte="http://t.com"
        )

        id_inserido = AuxilioTransporteRepo.inserir(auxilio_transporte)
        assert id_inserido is not None

    def test_obter_por_id_existente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioTransporteRepo.criar_tabela()

        auxilio_transporte = AuxilioTransporte(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao="teste",
            valor_mensal=123.45,
            data_inicio="2023-02-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio transporte",
            urlCompResidencia="http://r.com",
            urlCompTransporte="http://t.com"
        )

        id_inserido = AuxilioTransporteRepo.inserir(auxilio_transporte)
        obj = AuxilioTransporteRepo.obter_por_id(id_inserido)
        assert obj is not None
        assert obj.id_auxilio == id_inserido

    def test_obter_por_id_inexistente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioTransporteRepo.criar_tabela()

        resultado = AuxilioTransporteRepo.obter_por_id(9999)
        assert resultado is None

    def test_atualizar_auxilio_transporte_existente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioTransporteRepo.criar_tabela()

        auxilio_transporte = AuxilioTransporte(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao="original",
            valor_mensal=200.00,
            data_inicio="2023-01-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio transporte",
            urlCompResidencia="http://original.com/res",
            urlCompTransporte="http://original.com/trans"
        )

        id_inserido = AuxilioTransporteRepo.inserir(auxilio_transporte)
        auxilio_transporte.id_auxilio = id_inserido
        auxilio_transporte.descricao = "atualizado"
        auxilio_transporte.urlCompResidencia = "http://novo.com/res"
        auxilio_transporte.urlCompTransporte = "http://novo.com/trans"

        atualizado = AuxilioTransporteRepo.atualizar(auxilio_transporte)
        assert atualizado

    def test_excluir_auxilio_transporte_existente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioTransporteRepo.criar_tabela()

        auxilio_transporte = AuxilioTransporte(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao="excluir teste",
            valor_mensal=500.00,
            data_inicio="2023-01-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio transporte",
            urlCompResidencia="http://res.com",
            urlCompTransporte="http://trans.com"
        )

        id_inserido = AuxilioTransporteRepo.inserir(auxilio_transporte)
        sucesso = AuxilioTransporteRepo.excluir(id_inserido)
        assert sucesso

    def test_excluir_auxilio_transporte_inexistente(self, test_db):
        edital_repo.criar_tabela()
        inscricao_repo.criar_tabela()
        auxilio_repo.criar_tabela()
        AuxilioTransporteRepo.criar_tabela()

        sucesso = AuxilioTransporteRepo.excluir(99999)
        assert not sucesso
