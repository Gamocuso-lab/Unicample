from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session

router = APIRouter()

baseUrl = "/api/v1"

@router.get(baseUrl + "/")
def root(session : Session = Depends(get_session)):
    return {"message": "API está rodando!"}