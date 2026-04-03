from sqlalchemy import Column, Integer, String, Enum
from database import Base
from .enums import StatusAtivo
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import uuid

class Ativo(Base):
    __tablename__ = "ativos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=True)
    colaborador = relationship("Colaborador")
    codigo_ativo = Column(Integer, unique=True)
    nome = Column(String)
    descricao = Column(String)
    status = Column(Enum(StatusAtivo, native_enum=False, create_constraint=False), default=StatusAtivo.DISPONIVEL)
