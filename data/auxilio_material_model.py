from dataclasses import dataclass

from data.auxilio_model import Auxilio


@dataclass
class AuxilioMaterial(Auxilio):
    id_auxilio: int
