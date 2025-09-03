from dataclasses import dataclass

from model.usuario_model import Usuario


@dataclass
class AssistenteSocial(Usuario):
    id_usuario: int
    numero: str
