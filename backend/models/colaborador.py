from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    departamento = Column(String)
    
    ativos = relationship("Ativo", back_populates="colaborador", cascade="all, delete-orphan")