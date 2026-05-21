from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from schemas import AtivoCreateRequest, BuscaAtivoRequest, AtivoResponse
from auth.auth import verificar_token
from repository.ativo import criar_ativo, listar_ativos, buscar_por_nome_ou_codigo

router = APIRouter()

 # Controle de Ativos
@router.post("/ativos")
def criar(payload: AtivoCreateRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    nome = payload.nome
    codigo_ativo = payload.codigo_ativo
    descricao = payload.descricao
    return criar_ativo(db, nome, codigo_ativo, descricao)

@router.post("/ativos/busca", response_model=list[AtivoResponse])
def buscar_ativos(payload: BuscaAtivoRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    termo = payload.termo
    return buscar_por_nome_ou_codigo(db, termo)

@router.get("/ativos", response_model=list[AtivoResponse])
def listar_ativos_route(db: Session = Depends(get_db), user=Depends(verificar_token)):
    return listar_ativos(db)

