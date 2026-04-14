from sqlalchemy import select
from models.models import Admin,Evento,Log

def get_superuser(db,id):
    query = select(Admin.super).where(Admin.id == id)
    return db.execute(query).scalar()

def get_user_login(db, email):
    query = select(Admin.id, Admin.nome, Admin.ativo, Admin.senha).where(Admin.email == email)
    return db.execute(query).first()


def get_user(db, id):
    query = select(Admin).where(Admin.id == id)
    return db.execute(query).scalars().first()


def get_active_user(db, id):
    query = select(Admin.ativo, Admin.nome).where(Admin.id == id)
    return db.execute(query).first()


def get_all_users(db):
    query = select(Admin.id, Admin.nome,Admin.email,Admin.ativo).where(Admin.ativo == True, Admin.super == False)
    return db.execute(query).all()


def get_all_events_private(db):
    query = select(Evento.id,Evento.titulo, Evento.descricao,
                   Evento.data, Evento.parque, Admin.nome.label("nome_admin")).join(Admin)
    return db.execute(query).all()

def get_event(db, id):
    query = select(Evento).where(Evento.id == id)
    return db.execute(query).scalars().first()

def get_all_logs(db):
    query = select(Log)
    return db.execute(query).scalars().all()

def get_all_events_public(db):
    query = select(Evento.titulo,Evento.descricao,Evento.data, Evento.parque)
    return db.execute(query).all()