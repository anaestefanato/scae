from dataclasses import dataclass
from model.auxilio_model import Auxilio

@dataclass
class AuxilioTransporte(Auxilio):
    tipo_transporte: str
    tipo_onibus: str = None
    gasto_passagens_dia: float = None
    gasto_van_mensal: float = None
    urlCompResidencia: str = None
    urlPasseEscolarFrente: str = None
    urlPasseEscolarVerso: str = None
    urlComprovanteRecarga: str = None
    urlComprovantePassagens: str = None
    urlContratoTransporte: str = None
