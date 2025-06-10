from dataclasses import dataclass


@dataclass
class DuvidaEdital:
    id_duvida: int
    id_edital: int
    id_aluno: int
    pergunta: str
    resposta: str
    dataPergunta: str
    dataResposta: str
    status: str