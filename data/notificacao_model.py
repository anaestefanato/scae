from dataclasses import dataclass


@dataclass
class Notificacao:
    id_notificacao: int
    id_usuario_destinatario: int
    titulo: str
    dataEnvio: str
    tipo: str