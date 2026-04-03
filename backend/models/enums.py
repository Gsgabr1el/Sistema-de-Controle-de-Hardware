import enum

class StatusAtivo(str, enum.Enum):
    DISPONIVEL = "DISPONIVEL"
    EM_USO = "EM_USO"
    MANUTENCAO = "MANUTENCAO"
    DESCARTE = "DESCARTE"

class TipoMovimentacao(str, enum.Enum):
    ENTREGA = "ENTREGA"
    DEVOLUCAO = "DEVOLUCAO"
    MANUTENCAO = "MANUTENCAO"
    DESCARTE = "DESCARTE"
