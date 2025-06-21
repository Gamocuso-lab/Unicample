from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel
from typing import List, Optional

from app.db.session import get_session
from app.models.ranking import Ranking
from app.services.rankingService import RankingService
from app.schemas.rankingSchema import RankingCreate

router = APIRouter()

@router.get("/", response_model=List[Ranking])
async def get_ranking(
    nome: Optional[str] = None, 
    session: Session = Depends(get_session)
):
    """
    Obtém a lista das melhores pontuações.
    Pode ser o ranking global ou o ranking de um jogador específico.
    - Para o ranking global: /ranking
    - Para o ranking de um jogador: /ranking?nome=NOME_DO_JOGADOR
    """
    try:
        ranking_service = RankingService()
        ranking_list = await ranking_service.obter_ranking(session, nome_jogador=nome)
        return ranking_list
    except Exception as e:
        print(f"Erro ao obter ranking: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar o ranking.")


@router.post("/", response_model=Ranking, status_code=201)
async def add_ranking_entry(
    ranking_data: RankingCreate, 
    session: Session = Depends(get_session)
):
    """
    Adiciona uma nova pontuação ao ranking.
    Esta rota deve ser chamada ao final de um jogo.
    """
    try:
        ranking_service = RankingService()
        nova_entrada = await ranking_service.adicionar_pontuacao(
            session=session,
            nome_jogador=ranking_data.nome,
            pontuacao=ranking_data.pontuacao
        )
        return nova_entrada
    except Exception as e:
        print(f"Erro ao adicionar pontuação ao ranking: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao salvar a pontuação.")