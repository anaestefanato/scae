from datetime import datetime
import pytest
import os
import sys
import tempfile

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

@pytest.fixture
def test_db():
    import tempfile, os

    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['TEST_DATABASE_PATH'] = db_path

    # Fecha o descritor do arquivo antes de usar
    os.close(db_fd)

    yield db_path

    # Após o teste, remove o arquivo se ele existir
    if os.path.exists(db_path):
        try:
            os.unlink(db_path)
        except PermissionError:
            print(f"⚠️  Arquivo {db_path} ainda está em uso.")


@pytest.fixture
def usuario_exemplo():
    # Cria um usuário de exemplo para os testes
    from data.usuario_model import Usuario
    usuario = Usuario(0, "Usuário Teste", "joaosilva@email.com", "123456", "administrador")
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    # Cria uma lista de 10 usuários de exemplo para os testes
    from data.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Usuário {i:02d}", f"usuario{i:02d}@email.com", "123456", 0)
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def lista_alunos_exemplo():
    # Cria uma lista de 10 alunos de exemplo para os testes
    from data.aluno_model import Aluno
    alunos = []
    for i in range(1, 11):
        aluno = Aluno(0, f"Aluno {i:02d}", f"aluno{i:02d}@email.com", f"123456{i:02d}", "aluno", f"1234567890{i:02d}", datetime(2000, 1, i).date(), f"Pai {i:02d}", "Rua A", "Banco A", "1234", "56789", 1500.00, f"ALUNO{i:02d}")
        alunos.append(aluno)
    return alunos

@pytest.fixture
def lista_auxilios_moradia_exemplo():
    # Cria uma lista de 10 auxílios de moradia de exemplo para os testes
    from data.auxilio_moradia_model import AuxilioMoradia
    auxilios_moradia = []
    for i in range(1, 11):
        auxilio = AuxilioMoradia(0, f"Auxilio Moradia {i:02d}", 1000.00 * i)
        auxilios_moradia.append(auxilio)
    return auxilios_moradia

import pytest
from data.auxilio_transporte_model import AuxilioTransporte

@pytest.fixture
def lista_auxilios_transporte_exemplo():
    auxilios_transporte = []
    for i in range(1, 11):
        auxilio = AuxilioTransporte(
            id_auxilio=0,
            id_edital=1,
            id_inscricao=1,
            descricao=f"Auxilio Transporte {i:02d}",
            valor_mensal=500.00 * i,
            data_inicio="2023-01-01",
            data_fim="2023-12-31",
            tipo_auxilio="auxilio transporte",
            urlCompResidencia=f"http://example.com/res{i}",
            urlCompTransporte=f"http://example.com/trans{i}"
        )
        auxilios_transporte.append(auxilio)
    return auxilios_transporte

@pytest.fixture
def lista_inscricoes_exemplo():
    # Cria uma lista de 10 inscrições de exemplo para os testes
    from data.inscricao_model import Inscricao
    inscricoes = []
    for i in range(1, 11):
        inscricao = Inscricao(
            id_inscricao=i,
            id_aluno=i,
            id_edital=i,
            data_inscricao=datetime(2023, 1, i).date(),
            status="pendente",
            urlDocumentoIdentificacao=f"http://example.com/doc{i}.pdf",
            urlDeclaracaoRenda=f"http://example.com/renda{i}.pdf",
            urlTermoResponsabilidade=f"http://example.com/termo{i}.pdf"
        )
        inscricoes.append(inscricao)
    return inscricoes

@pytest.fixture
def lista_editais_exemplo():
    # Cria uma lista de 10 editais de exemplo para os testes
    from data.edital_model import Edital
    editais = []
    for i in range(1, 11):
        edital = Edital(
            id_edital=i,
            titulo=f"Edital {i:02d}",
            descricao=f"Descrição do edital {i:02d}",
            data_publicacao=datetime(2023, 1, i).date(),
            data_encerramento=datetime(2023, 12, i).date(),
            arquivo=f"http://example.com/edital{i}.pdf",
            status="ativo"
        )
        editais.append(edital)
    return editais

# @pytest.fixture
# def lista_categorias_exemplo():
#     # Cria uma lista de 10 categorias de exemplo para os testes
#     from models.categoria import Categoria
#     categorias = []
#     for i in range(1, 11):
#         categoria = Categoria(0, f"Categoria {i:02d}")
#         categorias.append(categoria)
#     return categorias

# @pytest.fixture
# def produto_exemplo():
#     # Cria um produto de exemplo para os testes
#     from models.produto import Produto
#     produto = Produto(0, "Produto Teste", "Descrição do produto teste.", 10.0, 5, "produto.jpg", 1)
#     return produto

# @pytest.fixture
# def lista_produtos_exemplo(categoria_exemplo):
#     # Cria uma lista de 10 produtos de exemplo para os testes
#     from models.produto import Produto
#     produtos = []
#     for i in range(1, 11):
#         produto = Produto(0, f"Produto {i:02d}", f"Descrição do produto {i:02}.", 10.0*i, 5*i, f"produto{i}.jpg", i)
#         produtos.append(produto)
#     return produtos

# @pytest.fixture
# def usuario_exemplo():
#     # Cria um usuário de exemplo para os testes
#     from models.usuario import Usuario
#     usuario = Usuario(0, "Usuário Teste", "123.456.789-00", "(28) 99999-0000", "usuario@email.com", datetime(2000, 1, 1).date(), "123456", 0)
#     return usuario

# @pytest.fixture
# def lista_usuarios_exemplo():
#     # Cria uma lista de 10 usuários de exemplo para os testes
#     from models.usuario import Usuario
#     usuarios = []
#     for i in range(1, 11):
#         usuario = Usuario(0, f"Usuário {i:02d}", f"123.456.789-{i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", datetime(2000, 1, i).date(), "123456", 0)
#         usuarios.append(usuario)
#     return usuarios

# @pytest.fixture
# def endereco_exemplo():
#     # Cria um endereço de exemplo para os testes
#     from models.endereco import Endereco
#     endereco = Endereco(0, "Rua Teste", "123", "Casa", "Bairro Teste", "Cidade Teste", "Estado Teste", "12345-678", 1)
#     return endereco

# @pytest.fixture
# def lista_enderecos_exemplo():
#     # Cria uma lista de 10 endereços de exemplo para os testes
#     from models.endereco import Endereco
#     enderecos = []
#     for i in range(1, 11):
#         endereco = Endereco(0, f"Rua {i:02d}", f"{i*3}", f"Apto 2{i:02d}", f"Bairro {i:02d}", f"Cidade {i:02d}", f"Estado {i:02d}", f"12345-0{i:02d}", i)
#         enderecos.append(endereco)
#     return enderecos