from dataclasses import dataclass


@dataclass
class Notificacao:
    id_notificacao: int
    id_usuario_destinatario: int
    titulo: str
    data_envio: str
    tipo: str