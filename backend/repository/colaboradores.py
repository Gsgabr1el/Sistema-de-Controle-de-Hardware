from sqlalchemy.orm import Session
from models import Colaborador

def create_colaboradores(db: Session):
    if db.query(Colaborador).count() > 0:
        return

    colaboradores = []

    for i in range(1, 41):
        colaboradores.append(
            Colaborador(
                nome=f"Colaborador {i}",
                email=f"colaborador{i}@empresa.com",
                departamento="TI"
            )
        )

    db.add_all(colaboradores)
    db.commit()


def listar_colaboradores(db: Session):
    return db.query(Colaborador).all()


def buscar_por_id(db: Session, colaborador_id: int):
    return db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()