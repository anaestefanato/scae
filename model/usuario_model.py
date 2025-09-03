from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id_usuario: int
    nome: str
    matricula: str
    email: str
    senha: str
    tipo_usuario: str
    perfil: str 
    foto: Optional[str] 
    token_redefinicao: Optional[str] 
    data_token: Optional[str] 
    data_cadastro: Optional[str]