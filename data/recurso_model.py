from dataclasses import dataclass


@dataclass
class Recurso:
    d_recurso: int
    id_inscricao: int
    id_assistente_social: int
    descricao: str
    data_envio: str
    data_resposta: str
    status: str