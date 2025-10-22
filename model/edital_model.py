from dataclasses import dataclass
from typing import Optional

@dataclass
class Edital:
    id_edital: int
    titulo: str
    descricao: str
    data_publicacao: str
    arquivo: str
    status: str
    data_inicio_inscricao: Optional[str] = None
    data_fim_inscricao: Optional[str] = None
    data_inicio_vigencia: Optional[str] = None
    data_fim_vigencia: Optional[str] = None