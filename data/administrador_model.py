from dataclasses import dataclass
from data.usuario_model import Usuario


@dataclass
class Administrador(Usuario):
    id_usuario: int
    matricula: str