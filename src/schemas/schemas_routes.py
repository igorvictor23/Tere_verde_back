from pydantic import BaseModel, Field, EmailStr, FutureDate
from typing import Optional, Literal
from datetime import date,datetime

class CreateAdminReq(BaseModel):
    nome : str = Field(...,max_length=200,description="Nome do administrador")
    email : EmailStr = Field(...,max_length=200,description="Email do administrador")
    senha : str = Field(...,max_length=72,description="Senha do administrador")


class AdminResponse(BaseModel):
    usuario : str = Field(...,max_length=200,description="Nome do usuário criado")

    class Config:
        orm_mode = True


class LoginAdmin(BaseModel):
    email : EmailStr = Field(...,max_length=200,description="Email do administrador")
    senha : str = Field(...,description="Senha do administrador")


class LoginResponseToken(BaseModel):
    usuario : str = Field(...,max_length=200,description="Mensagem para o usuário")
    token : dict = Field(...,description="Token do administrador")

    class Config:
        orm_mode = True


class FetchAdminsResponse(BaseModel):
    id : int = Field(...,description="ID do administrador")
    nome : str = Field(...,description="Nome do administrador")
    email : EmailStr = Field(...,description="Email do administrador")
    ativo : bool = Field(...,description="Status do administrador")

    class Config:
        orm_mode = True


class UpdateAdminReq(BaseModel):
    email : Optional[EmailStr] = Field(None,max_length=200,description="Email do administrador")
    senha : Optional[str] = Field(None,description="Senha do administrador")



class CreateEventReq(BaseModel):
    titulo : str = Field(...,max_length=200,description="Titulo do evento")
    descricao : Optional[str] = Field(None,max_length=200,description="Descricao do evento")
    data : FutureDate = Field(...,description="Data do evento")
    parque : Literal["PARNASO", "Três Picos", "Montanhas de Teresópolis"] = Field(...,description="Parque do evento")


class CreateEventResponse(BaseModel):
    titulo : str = Field(...,description="Titulo do evento")
    parque : str = Field(...,description="Parque do evento")

    class Config:
        orm_mode = True

class EventResponse(CreateEventResponse):
    data: date
    descricao: Optional[str] = Field(None)



class GetEventsResponse(EventResponse):
    id: int
    nome_admin: str



class UpdateEventReq(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200, description="Titulo do evento")
    descricao: Optional[str] = Field(None, max_length=200, description="Descricao do evento")
    data: Optional[FutureDate] = Field(None, description="Data do evento")
    parque: Optional[Literal["PARNASO", "Três Picos", "Montanhas de Teresópolis"]] = Field(None, description="Parque do evento")



class LogsResponse(BaseModel):
    operacao : str
    data: datetime
    usuario : str
    id_evento : Optional[int] = Field(None)
    titulo_evento : str

    class Config:
        orm_mode = True


class WeatherResponse(BaseModel):
    temperatura : float = Field(...,description="Temperatura do dia do evento")
    emoji : str = Field(...,description="Emoji da condição climática")


class WeatherReq(BaseModel):
    data : date = Field(...,description="Data do evento")


class Message(BaseModel):
    mensagem: str