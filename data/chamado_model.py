from dataclasses import dataclass


@dataclass
class Chamado:
    id_duvida: int
    id_usuario_criador: str
    id_administrador_responsavel: str
    titulo: str
    descricao: str
    dataCriacao: str
    status: str