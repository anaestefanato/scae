from dataclasses import dataclass
from data.auxilio_model import Auxilio

@dataclass
class AuxilioMoradia(Auxilio):
    id_auxilio: int
    url_comp_residencia_fixa: str
    url_comp_residencia_alugada: str
    url_contrato_aluguel_cid_campus: str
    url_contrato_aluguel_cid_natal: str
