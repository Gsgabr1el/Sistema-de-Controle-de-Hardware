from sqlalchemy.orm import Session
from models import Movimentacao, TipoMovimentacao, StatusAtivo
from repository.ativo import buscar_por_codigo
from repository.colaboradores import buscar_por_id as buscar_colaborador
from exceptions import BadRequestError, ConflictError, NotFoundError

def registrar_entrega(db: Session, codigo_ativo: int, colaborador_id: int):
    ativo = buscar_por_codigo(db, codigo_ativo)
    colaborador = buscar_colaborador(db, colaborador_id)


    if not ativo:
        raise NotFoundError("Ativo não encontrado")

    if not colaborador:
        raise NotFoundError("Colaborador não encontrado")

    if ativo.status == StatusAtivo.DESCARTE:
        raise ConflictError("Ativo descartado")

    if ativo.status != StatusAtivo.DISPONIVEL:
        raise ConflictError("Ativo não disponível")

    ativo.colaborador_id = colaborador_id
    ativo.codigo_ativo = codigo_ativo
    ativo.status = StatusAtivo.EM_USO

   
    mov = Movimentacao(
        tipo=TipoMovimentacao.ENTREGA,
        codigo_ativo=codigo_ativo,
        ativo_id=ativo.id,  
        colaborador_id=colaborador_id
    )

    db.add(mov)
    db.commit()
    db.refresh(mov)

    return mov


def registrar_devolucao(db: Session, codigo_ativo: int, novo_status: StatusAtivo):
    ativo = buscar_por_codigo(db, codigo_ativo)

    if not ativo:
        raise NotFoundError("Ativo não encontrado")

    tipo_mov = TipoMovimentacao.DEVOLUCAO
    colaborador_id = ativo.colaborador_id

    if ativo.status == StatusAtivo.EM_USO:
        ativo.colaborador_id = None

    elif ativo.status == StatusAtivo.DISPONIVEL:
        if novo_status not in (StatusAtivo.MANUTENCAO, StatusAtivo.DESCARTE):
            raise BadRequestError("Só é permitido mudar de DISPONIVEL para MANUTENCAO ou DESCARTE")

    else:
        if ativo.status == StatusAtivo.DESCARTE:
            raise BadRequestError("Ativo descartado não pode ser movimentado")

        if novo_status != StatusAtivo.DESCARTE:
            raise BadRequestError("Transição inválida")

    if novo_status == StatusAtivo.MANUTENCAO:
        tipo_mov = TipoMovimentacao.MANUTENCAO
    elif novo_status == StatusAtivo.DESCARTE:
        tipo_mov = TipoMovimentacao.DESCARTE
        ativo.colaborador_id = None

    ativo.status = novo_status

    mov = Movimentacao(
        tipo=tipo_mov,
        ativo_id=ativo.id,
        codigo_ativo=codigo_ativo,         
        colaborador_id=colaborador_id       
    )

    db.add(mov)
    db.commit()
    db.refresh(mov)

    return mov


def listar_movimentacoes(db: Session):
    return db.query(Movimentacao).order_by(Movimentacao.data_hora.desc()).all()
