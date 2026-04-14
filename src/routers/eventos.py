from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from routers.queries import get_all_events_public, get_active_user,get_event,get_all_events_private
from auth.token import decode_token
from DB.config import get_db
from models.models import Evento,Log
from schemas.schemas_routes import (
    EventResponse,
    GetEventsResponse,
    CreateEventReq,
    UpdateEventReq,
    CreateEventResponse
)


router = APIRouter(
    prefix="/eventos",
    tags=["eventos"]
)


@router.get("/",status_code=status.HTTP_200_OK,response_model=list[EventResponse])
def get_events_public(db: Session = Depends(get_db)):

    eventos = get_all_events_public(db)

    return eventos

@router.get("/admin_events",response_model=list[GetEventsResponse],status_code=status.HTTP_200_OK)
def get_events_admin(db: Session = Depends(get_db),payload: dict = Depends(decode_token)):

    user = get_active_user(db,payload["sub"])

    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Acesso Restrito!")

    eventos = get_all_events_private(db)

    return eventos


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CreateEventResponse)
def create_event(dados: CreateEventReq, db: Session = Depends(get_db),payload: dict = Depends(decode_token)):

    user = get_active_user(db,payload["sub"])

    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Você não pode realizar essa ação!")

    novo_evento = Evento(titulo=dados.titulo,descricao=dados.descricao,
                         data=dados.data,parque=dados.parque,id_admin=int(payload["sub"]))

    db.add(novo_evento)
    db.flush()

    novo_log = Log(
        operacao="insert",
        usuario=user.nome,
        id_evento=novo_evento.id,
        titulo_evento=novo_evento.titulo
    )
    db.add(novo_log)

    db.commit()

    return {"titulo": novo_evento.titulo, "parque": novo_evento.parque}




@router.put("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def update_event(dados: UpdateEventReq,id: int, db: Session = Depends(get_db), payload: dict = Depends(decode_token)):

    user = get_active_user(db,payload["sub"])

    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Acesso Restrito!")

    evento = get_event(db, id)

    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Evento não encontrado!")


    if dados.titulo:
        evento.titulo = dados.titulo

    if dados.descricao:
        evento.descricao = dados.descricao

    if dados.parque:
        evento.parque = dados.parque

    if dados.data:
        evento.data = dados.data

    novo_log = Log(
        operacao="update",
        usuario=user.nome,
        id_evento=evento.id,
        titulo_evento=evento.titulo
    )
    db.add(novo_log)

    db.commit()

    return


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_event(id: int, db: Session = Depends(get_db), payload: dict = Depends(decode_token)):

    user = get_active_user(db, payload["sub"])

    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso Restrito!")

    evento = get_event(db, id)

    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado!")

    novo_log = Log(
        operacao="delete",
        usuario=user.nome,
        id_evento=evento.id,
        titulo_evento=evento.titulo
    )
    db.add(novo_log)

    db.delete(evento)

    db.commit()

    return