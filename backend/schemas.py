from pydantic import BaseModel
from models import StatusAtivo


class LoginRequest(BaseModel):
    username: str
    senha: str


class AtivoCreateRequest(BaseModel):
    nome: str
    codigo_ativo: int
    descricao: str


class BuscaAtivoRequest(BaseModel):
    termo: str


class EntregaRequest(BaseModel):
    codigo_ativo: int
    colaborador_id: int


class DevolucaoRequest(BaseModel):
    codigo_ativo: int
    status: StatusAtivo


class ColaboradorRequest(BaseModel):
    colaborador_id: int
