from unittest.mock import patch, MagicMock
from app.models.jogo import Jogo
from app.models.rodada import Rodada
from app.models.local import Local
from app.models.coordenada import Coordenada
from app.models.imagem import Imagem
import pytest

def test_create_jogo(client, db_session):
    """Testa a criação de um novo jogo"""
    # Configuração do mock para simular dados de teste

    # Criar dados de teste
    
    # Fazer chamada API
    response = client.post("/jogo/create")
    
    # Verificar resultado
    assert response.status_code == 200
    jogo_id = response.json()
    
    # Verificar se o jogo foi criado no banco
    jogo = client.get(f"/jogo/infos?id_jogo={jogo_id}").json()
    assert jogo["id"] is not None
    
    # Verificar se foi criada u

def test_get_jogo_info(client, db_session):
    """Testa obter informações de um jogo"""
    # Criar jogo de teste
    response = client.post("/jogo/create")

    jogo_id = response.json()
    
    # Fazer chamada API
    response = client.get(f"/jogo/infos?id_jogo={jogo_id}")

    # Verificar resultado
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == jogo_id
    assert data["pontuacao"] == 0