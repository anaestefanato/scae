from dataclasses import dataclass


@dataclass
class Aluno:
    id_usuario: int
    cpf: str
    data_nascimento: str
    filiacao: str
    endereco: str
    nome_banco: str
    agencia_bancaria: str
    numero_conta_bancaria: str
    renda_familiar: float
    matricula: str