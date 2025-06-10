from dataclasses import dataclass


@dataclass
class Auxilio:
    id_auxilio: int
    id_edital: int
    id_inscricao: int
    descricao: str
    valorMensal: float
    dataInicio: str
    dataFim: str
    tipo_auxilio: str