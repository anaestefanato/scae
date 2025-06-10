from dataclasses import dataclass


@dataclass
class Recurso:
    d_recurso: int
    id_inscricao: int
    id_assistente_social: int
    descricao: str
    dataEnvio: str
    dataResposta: str
    status: str