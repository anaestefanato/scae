from dataclasses import dataclass


@dataclass
class Recebimento:
    id_recebimento: int
    id_auxilio: int
    mes_referencia: str
    ano_referencia: int
    valor: float
    data_recebimento: str
    status: str
    observacoes: str = ""