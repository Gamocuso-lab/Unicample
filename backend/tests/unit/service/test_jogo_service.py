# tests/unit/services/test_jogo_service.py
import pytest
from app.services.jogoService import JogoService
from app.models.jogo import Jogo

@pytest.mark.asyncio
async def test_finalizar_jogo(db_session):
    """Testa finalização de jogo"""
    # Criar jogo para teste
    jogo = Jogo(pontuacao=100, tempo=120, finalizado=False)
    db_session.add(jogo)
    db_session.commit()
    
    # Chamar método de serviço
    service = JogoService()
    jogo_finalizado = await service.finalizar_jogo(db_session, jogo.id)
    
    # Verificar resultado
    assert jogo_finalizado is not None
    assert jogo_finalizado.finalizado == True