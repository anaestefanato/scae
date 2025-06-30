from dataclasses import dataclass
@dataclass
class Notificacao:
    id_notificacao: int | None  # Pode ser None antes de inserir no banco
    id_usuario_destinatario: int
    titulo: str
    data_envio: str
    tipo: str
