from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.jogo import Jogo
from app.models.rodada import Rodada
from app.services.jogoService import JogoService
from app.schemas.jogoSchema import JogoResponse


router = APIRouter()

base_url = "/jogo"

@router.post(base_url + "/create", response_model=int)
async def createJogo(session: Session = Depends(get_session)):
    try:
        jogo_service = JogoService()
        novo_jogo = await jogo_service.create_jogo(session)
        return novo_jogo.id
    except Exception as e:
        print(f"Erro ao criar jogo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get(base_url + "/infos")
async def get_jogo_info(id_jogo: int, session: Session = Depends(get_session)) -> JogoResponse:
    try:
        jogo_service = JogoService()
        jogo_info = await jogo_service.get_jogo_info(session, id_jogo)
        return jogo_info
    except Exception as e:
        print(f"Erro ao criar jogo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get(base_url + "/chute")
async def chute(id_jogo: int, local: str, session: Session = Depends(get_session)) -> bool:
    jogo_service = JogoService()
    resultado = await jogo_service.chute(session, id_jogo, local)
    return resultado

@router.get(base_url + "/{id_jogo}/streetview", response_class=HTMLResponse)
async def get_jogo_streetview(id_jogo: int, request: Request, session: Session = Depends(get_session)):
    """
    Endpoint principal para visualizar a rodada atual de um jogo.
    """
    jogo_service = JogoService()
    return await jogo_service.get_rodada_streetview(session, id_jogo, request)

@router.get(base_url + "/imagem") 
async def get_jogo_imagem(id_jogo: int, session: Session = Depends(get_session)):
    """
    Endpoint para obter a imagem da rodada atual de um jogo.
    """
    jogo_service = JogoService()
    imagem = await jogo_service.get_rodada_imagem(session, id_jogo)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada para o jogo especificado.")
    return {"imagem": imagem}

@router.get(base_url + "/rodadas")
async def get_rodadas(session: Session = Depends(get_session)):
    """
    Endpoint para obter todas as rodadas de um jogo.
    """
    rodadas = session.exec(select(Rodada)).all()
    return rodadas

@router.put(base_url + "/finalizar")
async def finalizar_jogo(id_jogo: int, session: Session = Depends(get_session)):
    """
    Endpoint para finalizar um jogo.
    """
    jogo_service = JogoService()
    try:
        jogo = await jogo_service.finalizar_jogo(session, id_jogo)
        return jogo
    except Exception as e:
        print(f"Erro ao finalizar jogo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")