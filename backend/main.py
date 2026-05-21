from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from exceptions import DomainError
from auth.auth import criar_gestor_sistema
from routers.auth import router as auth_router
from routers.ativos import router as ativos_router
from routers.colaboradores import router as colaboradores_router
from routers.movimentacoes import router as movimentacoes_router


def inicializar_banco():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        criar_gestor_sistema(db)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_banco()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router (auth_router)
app.include_router (ativos_router)
app.include_router (colaboradores_router)
app.include_router (movimentacoes_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho para a pasta frontend
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")

app.mount("/frontend", StaticFiles(directory=FRONTEND_PATH), name="frontend")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))


@app.exception_handler(DomainError)
def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code},
    )


# Comentario de Alteração A5 Praticando
