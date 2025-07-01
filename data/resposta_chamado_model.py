from dataclasses import dataclass

@dataclass
class RespostaChamado:
    id_resposta: int
    id_chamado: int
    id_usuario: str
    mensagem: str
    data_resposta: str
    status: str