from dataclasses import dataclass


@dataclass
class Auxilio:
    id_auxilio: int
    id_edital: int
    id_inscricao: int
    descricao: str
    valor_mensal: float
    data_inicio: str
    data_fim: str
    tipo_auxilio: str