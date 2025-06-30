from dataclasses import dataclass
@dataclass
class Recurso:
    id_recurso: int
    id_inscricao: int
    id_assistente: int
    descricao: str
    data_envio: str
    data_resposta: str
    status: str
