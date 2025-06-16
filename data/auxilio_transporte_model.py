from dataclasses import dataclass

from data.auxilio_model import Auxilio


@dataclass
class AuxilioTransporte(Auxilio):
    id_auxilio: int
    urlCompResidencia: str
    urlCompTransporte: str