from dataclasses import dataclass

from data.auxilio_model import Auxilio


@dataclass
class AuxilioAlimentacao(Auxilio):
    id_auxilio: int
