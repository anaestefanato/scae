from dataclasses import dataclass
@dataclass
class Chamado:
    id_chamado: int | None  # Pode ser None antes de inserir no banco
    id_usuario_criador: int
    id_administrador_responsavel: int | None  # Pode ser None se ainda não atribuído
    titulo: str
    descricao: str
    categoria: str  # erro, duvida, sugestao, outros
    data_criacao: str
    data_ultima_atualizacao: str | None
    status: str  # aberto, em-andamento, resolvido