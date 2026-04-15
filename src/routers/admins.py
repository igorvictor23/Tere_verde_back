from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.auth import verifica_senha, senha_criptografada
from routers.queries import get_superuser, get_user_login, get_user, get_all_users
from auth.token import create_token, decode_token
from DB.config import get_db
from models.models import Admin
from schemas.schemas_routes import (
    LoginAdmin,
    CreateAdminReq,
    LoginResponseToken,
    AdminResponse,
    FetchAdminsResponse,
    UpdateAdminReq
)


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("/",status_code=status.HTTP_200_OK,response_model=list[FetchAdminsResponse])
def fetch_admins(db : Session = Depends(get_db),payload: dict = Depends(decode_token)):

    user = get_superuser(db,payload["sub"])

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso Restrito!")

    admins = get_all_users(db)

    return admins



@router.post("/login", status_code=status.HTTP_200_OK,response_model=LoginResponseToken)
def login(credenciais: LoginAdmin,db: Session = Depends(get_db)):

    user = get_user_login(db,credenciais.email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email ou Senha incorretos!")

    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email ou Senha incorretos!")

    if verifica_senha(credenciais.senha,user.senha):
        token = create_token(user.id)
        return {"usuario": user.nome,
                "token": {"access_token": token, "token_type": "bearer"}}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email ou Senha incorretos")


@router.post('/', status_code=status.HTTP_201_CREATED,response_model=AdminResponse)
def create_admin(credenciais: CreateAdminReq,db: Session = Depends(get_db), payload: dict = Depends(decode_token)):

    user = get_superuser(db,payload["sub"])

    if user:
        novo_admin = Admin(nome=credenciais.nome,email=credenciais.email,senha=senha_criptografada(credenciais.senha))
        try:
            db.add(novo_admin)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email já cadastrado!")

        return {"usuario": novo_admin.nome}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso Restrito!")


@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update_admin(credenciais : UpdateAdminReq, id : int,db: Session = Depends(get_db), payload: dict = Depends(decode_token)):

    admin = get_superuser(db,payload["sub"])

    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Acesso Restrito!")

    user = get_user(db,id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado!")

    if credenciais.email:
        user.email = credenciais.email

    if credenciais.senha:
        user.senha = senha_criptografada(credenciais.senha)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado!")

    return


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int, db: Session = Depends(get_db), payload: dict = Depends(decode_token)):

    user = get_superuser(db,payload["sub"])

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso Restrito!")

    deleted_user = get_user(db,id)

    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuário não encontrado!")


    deleted_user.ativo = False
    db.commit()

    return
