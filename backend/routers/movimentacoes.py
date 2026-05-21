from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from schemas import EntregaRequest, DevolucaoRequest
from auth.auth import verificar_token
from repository.movimentacao import listar_movimentacoes, registrar_entrega, registrar_devolucao
from utils.datetime_utils import converter_horario

def normalizar_movimentacao(mov):
    mov.data_hora = converter_horario(mov.data_hora)
    return mov

router = APIRouter()

# Controle de Movimentações
@router.get("/movimentacoes")
def listar_movimentacoes_route(db: Session = Depends(get_db), user=Depends(verificar_token)):
    movs = listar_movimentacoes(db)
    return [normalizar_movimentacao(mov) for mov in movs]


@router.post("/entrega")
def entrega(payload: EntregaRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    codigo_ativo = payload.codigo_ativo
    colaborador_id = payload.colaborador_id
    return normalizar_movimentacao(registrar_entrega(db, codigo_ativo, colaborador_id))

@router.post("/devolucao")
def devolucao(payload: DevolucaoRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    codigo_ativo = payload.codigo_ativo
    status = payload.status
    return normalizar_movimentacao(registrar_devolucao(db, codigo_ativo, status))
