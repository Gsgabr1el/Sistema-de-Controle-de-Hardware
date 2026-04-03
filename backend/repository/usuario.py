from sqlalchemy.orm import Session
from models import Usuario
from auth.auth import gerar_hash

def buscar_por_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()