"""
Script para criar arquivos PDF fictícios para teste de upload
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def criar_pdf_teste(caminho, titulo, conteudo):
    """Cria um PDF de teste simples"""
    c = canvas.Canvas(caminho, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, titulo)
    c.setFont("Helvetica", 12)
    
    y = 700
    for linha in conteudo:
        c.drawString(100, y, linha)
        y -= 20
    
    c.save()
    print(f"✓ PDF criado: {caminho}")

# Criar diretório para arquivos de teste
pasta_teste = "test_uploads"
os.makedirs(pasta_teste, exist_ok=True)

# Criar documentos obrigatórios
criar_pdf_teste(
    os.path.join(pasta_teste, "documento_identificacao.pdf"),
    "Documento de Identificação",
    [
        "RG: 12.345.678-9",
        "Nome: Aluno Teste da Silva",
        "CPF: 123.456.789-01",
        "Data de Nascimento: 15/05/2000",
        "",
        "Este é um documento fictício para teste."
    ]
)

criar_pdf_teste(
    os.path.join(pasta_teste, "anexo_1_declaracao_renda.pdf"),
    "Anexo I - Termo Comprobatório de Declaração de Renda",
    [
        "DECLARAÇÃO DE RENDA FAMILIAR",
        "",
        "Declaro para os devidos fins que a renda familiar",
        "per capita é de R$ 1.200,00 (mil e duzentos reais).",
        "",
        "Número de pessoas na residência: 4",
        "Renda total familiar: R$ 4.800,00",
        "",
        "Assinatura: _______________________",
        "Data: 14/10/2025"
    ]
)

criar_pdf_teste(
    os.path.join(pasta_teste, "anexo_3_termo_responsabilidade.pdf"),
    "Anexo III - Termo de Responsabilidade",
    [
        "TERMO DE RESPONSABILIDADE",
        "",
        "Eu, Aluno Teste da Silva, CPF 123.456.789-01,",
        "declaro estar ciente das normas e regulamentos",
        "do Programa de Assistência Estudantil do IFES.",
        "",
        "Comprometo-me a:",
        "- Utilizar os recursos conforme destinação prevista",
        "- Apresentar documentação quando solicitado",
        "- Cumprir os prazos estabelecidos",
        "",
        "Assinatura: _______________________",
        "Data: 14/10/2025"
    ]
)

# Criar documento de comprovante de residência para transporte
criar_pdf_teste(
    os.path.join(pasta_teste, "comprovante_residencia.pdf"),
    "Comprovante de Residência",
    [
        "CONTA DE ENERGIA ELÉTRICA",
        "",
        "Nome: Aluno Teste da Silva",
        "Endereço: Rua das Flores, 123",
        "Bairro: Centro",
        "Cidade: Cachoeiro de Itapemirim - ES",
        "CEP: 29300-970",
        "",
        "Vencimento: 10/10/2025",
        "Valor: R$ 150,00"
    ]
)

print("\n✓ Todos os arquivos PDF de teste foram criados com sucesso!")
print(f"✓ Localização: {os.path.abspath(pasta_teste)}")
