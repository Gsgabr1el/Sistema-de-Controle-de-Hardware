from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from models import Ativo, StatusAtivo
from exceptions import ConflictError

def criar_ativo(db: Session, nome: str, codigo_ativo: int, descricao: str):
    existente = db.query(Ativo).filter(Ativo.codigo_ativo == codigo_ativo).first()
    if existente:
        raise ConflictError("Ativo já existe")

    ativo = Ativo(
        nome=nome,
        codigo_ativo=codigo_ativo,
        descricao=descricao
    )
    try:
        db.add(ativo)
        db.commit()
        db.refresh(ativo)
        return ativo
    except IntegrityError:
        db.rollback()
        raise ConflictError("Ativo já existe")


def listar_ativos(db: Session):
    return db.query(Ativo).options(joinedload(Ativo.colaborador)).all()


def buscar_por_codigo(db: Session, codigo_ativo: int):
    return db.query(Ativo).options(joinedload(Ativo.colaborador)).filter(Ativo.codigo_ativo == codigo_ativo).first()


def buscar_por_nome_ou_codigo(db: Session, termo: str):
    if termo.isdigit():
        termo_num = int(termo)
        ativos = db.query(Ativo).options(joinedload(Ativo.colaborador)).filter(
            (Ativo.nome.ilike(f"%{termo}%")) | (Ativo.codigo_ativo == termo_num)
        ).all()
        return ativos

    return db.query(Ativo).options(joinedload(Ativo.colaborador)).filter(Ativo.nome.ilike(f"%{termo}%")).all()
