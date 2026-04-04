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


class ColaboradorCreateRequest(BaseModel):
    nome: str
    email: str
    departamento: str


class ColaboradorUpdateRequest(BaseModel):
    nome: str | None = None
    email: str | None = None
    departamento: str | None = None


# --- Response Schemas ---

class AtivoSimples(BaseModel):
    codigo_ativo: int
    nome: str
    status: str

    class Config:
        from_attributes = True


class ColaboradorResponse(BaseModel):
    id: int
    nome: str
    email: str
    departamento: str
    ativos: list[AtivoSimples] = []

    class Config:
        from_attributes = True


class AtivoResponse(BaseModel):
    id: str
    codigo_ativo: int
    nome: str
    descricao: str | None = None
    status: str
    colaborador: ColaboradorResponse | None = None

    class Config:
        from_attributes = True
