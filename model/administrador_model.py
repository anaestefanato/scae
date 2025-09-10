from dataclasses import dataclass
from model.usuario_model import Usuario


@dataclass
class Administrador(Usuario):
    id_usuario: int
    tipo_admin: str