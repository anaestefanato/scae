from dataclasses import dataclass
from typing import Optional
@dataclass
class Recurso:
    id_recurso: Optional[int]
    id_inscricao: int
    id_assistente: int
    descricao: str
    data_envio: str
    data_resposta: str
    status: str
