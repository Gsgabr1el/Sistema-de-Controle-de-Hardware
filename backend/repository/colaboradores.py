from sqlalchemy.orm import Session, joinedload
from models import Colaborador, Ativo
from exceptions import DomainError


def create_colaboradores(db: Session):
    pass


def listar_colaboradores(db: Session):
    return db.query(Colaborador).options(joinedload(Colaborador.ativos)).all()


def buscar_por_id(db: Session, colaborador_id: int):
    return (
        db.query(Colaborador)
        .options(joinedload(Colaborador.ativos))
        .filter(Colaborador.id == colaborador_id)
        .first()
    )


def criar_colaborador(db: Session, nome: str, email: str, departamento: str):
    colab = Colaborador(nome=nome, email=email, departamento=departamento)
    db.add(colab)
    db.commit()
    db.refresh(colab)
    return colab


def editar_colaborador(db: Session, colab_id: int, nome: str, email: str, departamento: str):
    colab = buscar_por_id(db, colab_id)
    if not colab:
        raise DomainError("Colaborador não encontrado", status_code=404)

    if nome:
        colab.nome = nome
    if email:
        colab.email = email
    if departamento:
        colab.departamento = departamento

    db.commit()
    db.refresh(colab)
    return colab


def excluir_colaborador(db: Session, colab_id: int):
    colab = buscar_por_id(db, colab_id)
    if not colab:
        raise DomainError("Colaborador não encontrado", status_code=404)

    # Opção A: Bloquear se houver ativos vinculados
    ativos_vinculados = db.query(Ativo).filter(Ativo.colaborador_id == colab_id).count()
    if ativos_vinculados > 0:
        raise DomainError(
            "Impossível excluir colaborador: existem ativos vinculados a ele.",
            status_code=409,
        )

    db.delete(colab)
    db.commit()
    return True