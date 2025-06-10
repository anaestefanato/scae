from dataclasses import dataclass


@dataclass
class AuxilioTransporte:
    id_auxilio: int
    urlCompResidencia: str
    urlCompTransporte: str