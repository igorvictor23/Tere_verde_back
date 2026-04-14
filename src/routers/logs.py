from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from routers.queries import get_all_logs,get_superuser
from schemas.schemas_routes import LogsResponse
from auth.token import decode_token
from DB.config import get_db




router = APIRouter(
    prefix="/logs",
    tags=["logs"]
)

@router.get("/",status_code=status.HTTP_200_OK,response_model=list[LogsResponse])
def get_logs(db: Session = Depends(get_db), payload: dict = Depends(decode_token)):

    user = get_superuser(db,payload["sub"])

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Acesso Restrito!")

    logs = get_all_logs(db)

    return logs