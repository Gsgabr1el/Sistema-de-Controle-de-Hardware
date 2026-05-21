from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from schemas import LoginRequest
from auth.auth import verificar_senha, criar_token
from repository.usuario import buscar_por_username
from exceptions import UnauthorizedError


router = APIRouter()

# Controle de Acesso
@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    username = payload.username
    senha = payload.senha
    user = buscar_por_username(db, username)

    if not user or not verificar_senha(senha, str(user.senha_hash)):
        raise UnauthorizedError("Credenciais inválidas")

    token = criar_token(str(user.username))
    return {"access_token": token}