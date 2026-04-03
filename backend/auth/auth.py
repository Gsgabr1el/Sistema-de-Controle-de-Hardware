from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Usuario
from sqlalchemy.orm import Session
from exceptions import UnauthorizedError

SECRET_KEY = "sistema-de-controle-de-hardware"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash: str):
    return pwd_context.verify(senha, hash)


def criar_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials  
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        print("ERRO TOKEN:", e)
        raise UnauthorizedError("Token inválido")


# Gestor do Sistema

def criar_gestor_sistema(db: Session):
    usuario_existente = db.query(Usuario).filter(Usuario.username == "Admin").first()

    if usuario_existente:
        print("Usuário Admin já existe")
        return usuario_existente

    gestor = Usuario(
        username="Admin",
        senha_hash=gerar_hash("ejQTL0MV7Q0oChX17H8E")
    )

    db.add(gestor)
    db.commit()
    db.refresh(gestor)

    print("Usuário Admin criado com sucesso")

    return gestor