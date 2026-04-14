from DB.config import Base
from sqlalchemy import Column, Integer, String, Boolean,Text, Date, DateTime,CheckConstraint, ForeignKey
from sqlalchemy.sql import func


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    nome = Column(String(200),nullable=False)
    email = Column(String(200),nullable=False,unique=True)
    senha = Column(Text,nullable=False)
    ativo = Column(Boolean,nullable=False,default=True)
    super = Column(Boolean,nullable=False,default=False)



class Evento(Base):
    __tablename__ = 'eventos'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200),nullable=False)
    descricao = Column(Text,nullable=True)
    data = Column(Date,nullable=False)
    parque = Column(String(100),CheckConstraint("parque in ('PARNASO', 'Três Picos', 'Montanhas de Teresópolis')"))
    id_admin = Column(Integer, ForeignKey('admins.id'),nullable=False)



class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    operacao = Column(String(200),nullable=False)
    data = Column(DateTime(timezone=True), server_default=func.now())
    usuario = Column(String(200),nullable=False)
    id_evento = Column(Integer, ForeignKey('eventos.id'),nullable=True)
    titulo_evento = Column(String(200),nullable=False)