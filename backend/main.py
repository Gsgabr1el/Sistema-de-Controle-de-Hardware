from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from exceptions import DomainError, UnauthorizedError
from repository.ativo import criar_ativo, listar_ativos, buscar_por_nome_ou_codigo
from repository.movimentacao import registrar_entrega, registrar_devolucao, listar_movimentacoes
from repository.usuario import buscar_por_username
from auth.auth import verificar_senha, criar_token, verificar_token, criar_gestor_sistema
from utils.datetime_utils import converter_horario
from schemas import (
    LoginRequest,
    AtivoCreateRequest,
    BuscaAtivoRequest,
    EntregaRequest,
    DevolucaoRequest,
    ColaboradorRequest,
    ColaboradorCreateRequest,
    ColaboradorUpdateRequest,
    AtivoResponse,
    ColaboradorResponse,
)
from repository.colaboradores import (
    create_colaboradores,
    listar_colaboradores,
    buscar_por_id,
    criar_colaborador,
    editar_colaborador,
    excluir_colaborador,
)

def inicializar_banco():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        create_colaboradores(db)
        criar_gestor_sistema(db)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_banco()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho para a pasta frontend
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))


@app.exception_handler(DomainError)
def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code},
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def normalizar_movimentacao(mov):
    mov.data_hora = converter_horario(mov.data_hora)
    return mov


                            # ROTAS


 # Controle de Acesso
@app.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    username = payload.username
    senha = payload.senha
    user = buscar_por_username(db, username)

    if not user or not verificar_senha(senha, str(user.senha_hash)):
        raise UnauthorizedError("Credenciais inválidas")

    token = criar_token(str(user.username))
    return {"access_token": token}


 # Controle de Ativos
@app.post("/ativos")
def criar(payload: AtivoCreateRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    nome = payload.nome
    codigo_ativo = payload.codigo_ativo
    descricao = payload.descricao
    return criar_ativo(db, nome, codigo_ativo, descricao)

@app.post("/ativos/busca", response_model=list[AtivoResponse])
def buscar_ativos(payload: BuscaAtivoRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    termo = payload.termo
    return buscar_por_nome_ou_codigo(db, termo)

@app.get("/ativos", response_model=list[AtivoResponse])
def listar_ativos_route(db: Session = Depends(get_db), user=Depends(verificar_token)):
    return listar_ativos(db)


 # Controle de Vinculação
@app.post("/entrega")
def entrega(payload: EntregaRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    codigo_ativo = payload.codigo_ativo
    colaborador_id = payload.colaborador_id
    return normalizar_movimentacao(registrar_entrega(db, codigo_ativo, colaborador_id))

@app.post("/devolucao")
def devolucao(payload: DevolucaoRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    codigo_ativo = payload.codigo_ativo
    status = payload.status
    return normalizar_movimentacao(registrar_devolucao(db, codigo_ativo, status))


 # Controle de Colaboradores/funcionarios 
@app.get("/colaboradores", response_model=list[ColaboradorResponse])
def listar_colaboradores_route(db: Session = Depends(get_db), user=Depends(verificar_token)):
    return listar_colaboradores(db)

@app.post("/colaboradores/busca")
def buscar_colaborador_route(payload: ColaboradorRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    colaborador_id = payload.colaborador_id
    return buscar_por_id(db, colaborador_id)

@app.post("/colaboradores")
def criar_colaborador_route(payload: ColaboradorCreateRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    return criar_colaborador(db, payload.nome, payload.email, payload.departamento)

@app.put("/colaboradores/{id}")
def editar_colaborador_route(id: int, payload: ColaboradorUpdateRequest, db: Session = Depends(get_db), user=Depends(verificar_token)):
    return editar_colaborador(db, id, payload.nome, payload.email, payload.departamento)

@app.delete("/colaboradores/{id}")
def excluir_colaborador_route(id: int, db: Session = Depends(get_db), user=Depends(verificar_token)):
    return excluir_colaborador(db, id)


# Controle de Movimentações
@app.get("/movimentacoes")
def listar_movimentacoes_route(db: Session = Depends(get_db), user=Depends(verificar_token)):
    movs = listar_movimentacoes(db)
    return [normalizar_movimentacao(mov) for mov in movs]
