from sqlalchemy.orm import Session
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
    return db.query(Ativo).all()


def buscar_por_codigo(db: Session, codigo_ativo: int):
    return db.query(Ativo).filter(Ativo.codigo_ativo == codigo_ativo).first()


def buscar_por_nome_ou_codigo(db: Session, termo: str):
    if termo.isdigit():
        ativos_nome = db.query(Ativo).filter(Ativo.nome.ilike(f"%{termo}%")).all()
        ativos_codigo = db.query(Ativo).filter(Ativo.codigo_ativo == int(termo)).all()

        ativos = {ativo.id: ativo for ativo in ativos_nome}
        ativos.update({ativo.id: ativo for ativo in ativos_codigo})
        return list(ativos.values())

    return db.query(Ativo).filter(Ativo.nome.ilike(f"%{termo}%")).all()
