from dataclasses import dataclass
from model.auxilio_model import Auxilio

@dataclass
class AuxilioTransporte(Auxilio):
    urlCompResidencia: str
    urlCompTransporte: str
