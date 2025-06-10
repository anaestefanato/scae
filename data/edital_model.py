from dataclasses import dataclass


@dataclass
class Edital:
    id_edital: int
    titulo: str
    descricao: str
    dataPublicacao: str
    dataEncerramento: str
    arquivo: str
    status: str