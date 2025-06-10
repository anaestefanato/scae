from dataclasses import dataclass


@dataclass
class Inscricao:
    id_inscricao: int
    id_aluno: int
    id_edital: int
    dataInscricao: str
    status: str
    urlDocumentoIdentificacao: str
    urlDeclaracaoRenda: str
    urlTermoResponsabilidade: str