from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from app.db.session import get_session
from app.models.jogo import Jogo
from app.services.jogoService import JogoService
from app.schemas.jogoSchema import JogoResponse

router = APIRouter()

base_url = "/jogo"

@router.post(base_url + "/create", response_model=int)
async def createJogo(session: Session = Depends(get_session)):
    jogo_service = JogoService()
    novo_jogo = await jogo_service.create_jogo(session)
    return novo_jogo.id

@router.get(base_url + "/{jogo_id}")
async def get_jogo_info(jogo_id: int, session: Session = Depends(get_session)) -> JogoResponse:
    jogo_service = JogoService()
    jogo_info = await jogo_service.get_jogo_info(session, jogo_id)
    return jogo_info

@router.get(base_url + "/{jogo_id}/{local}")
async def chute(jogo_id: int, local: str, session: Session = Depends(get_session)):
    jogo_service = JogoService()
    resultado = await jogo_service.chute(session, jogo_id, local)
    return resultado