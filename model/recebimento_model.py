from dataclasses import dataclass
from typing import Optional


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
    data_confirmacao: Optional[str] = None
    comprovante_transporte: Optional[str] = None
    comprovante_moradia: Optional[str] = None
