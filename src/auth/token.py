
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from schemas.schema_env import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def create_token(id):
    payload = {"sub": str(id)}
    iat = datetime.now(timezone.utc)
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload['iat'] = iat
    payload['exp'] = exp
    return jwt.encode(payload,settings.SECRET_JWT,algorithm=settings.ALGORITHM)

def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_JWT, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expirado!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token inválido!!")

