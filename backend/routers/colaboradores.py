from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from schemas import ColaboradorCreateRequest, ColaboradorResponse, ColaboradorRequest, ColaboradorUpdateRequest
from auth.auth import verificar_token
from repository.colaboradores import listar_colaboradores,buscar_por_id, editar_colaborador, criar_colaborador, excluir_colaborador


router = APIRouter()

 # Controle de Colaboradores/funcionarios 
@router.get("/colaboradores", response_model=list[ColaboradorResponse])
def listar_colaboradores_route(db: Session = Depends(get_db), user=Depends(verificar_token)):
    return listar_colaboradores(db)

@router.post("/colaboradores/busca")
def buscar_colaborador_route(payload: ColaboradorRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    colaborador_id = payload.colaborador_id
    return buscar_por_id(db, colaborador_id)

@router.post("/colaboradores")
def criar_colaborador_route(payload: ColaboradorCreateRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    return criar_colaborador(db, payload.nome, payload.email, payload.departamento)

@router.put("/colaboradores/{id}")
def editar_colaborador_route(id: int, payload: ColaboradorUpdateRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    return editar_colaborador(db, id, payload.nome, payload.email, payload.departamento)

@router.delete("/colaboradores/{id}")
def excluir_colaborador_route(id: int, db: Session = Depends(get_db), user=Depends(verificar_token)):
    return excluir_colaborador(db, id)