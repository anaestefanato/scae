from dataclasses import dataclass

from data.auxilio_model import Auxilio

@dataclass
class AuxilioMoradia(Auxilio):
    id_auxilio: int
    urlCompResidenciaFixa: str
    urlCompResidenciaAlugada: str
    urlContratoAluguelCidCampus: str
    urlContratoAluguelCidNatal: str