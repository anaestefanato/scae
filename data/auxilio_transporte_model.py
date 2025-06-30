from dataclasses import dataclass
from data.auxilio_model import Auxilio

@dataclass
class AuxilioTransporte(Auxilio):
    urlCompResidencia: str
    urlCompTransporte: str
