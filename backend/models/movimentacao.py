from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base
from .enums import TipoMovimentacao

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    tipo = Column(Enum(TipoMovimentacao, native_enum=False, create_constraint=False))

    ativo_id = Column(Integer, ForeignKey("ativos.id"))
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=True)

    ativo = relationship("Ativo")
    colaborador = relationship("Colaborador")
    codigo_ativo = Column(Integer) 