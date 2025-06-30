from dataclasses import dataclass

@dataclass
class Edital:
    id_edital: int
    titulo: str
    descricao: str
    data_publicacao: str
    data_encerramento: str
    arquivo: str
    status: str