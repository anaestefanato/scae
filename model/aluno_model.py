from dataclasses import dataclass

from model.usuario_model import Usuario


@dataclass
class Aluno(Usuario):
    id_usuario: int
    cpf: str
    telefone: str
    curso: str
    data_nascimento: str
    filiacao: str
    cep: str
    cidade: str
    bairro: str
    rua: str
    numero: str
    estado: str
    complemento: str
    nome_banco: str
    agencia_bancaria: str
    numero_conta_bancaria: str
    renda_familiar: float
    quantidade_pessoas: int
    renda_per_capita: float 
    situacao_moradia: str
    aprovado: bool = False
