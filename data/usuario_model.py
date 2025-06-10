from dataclasses import dataclass


@dataclass
class Usuario:
    id_usuario: int
    nome: str
    email: str
    senha: str
    tipo_usuario: str