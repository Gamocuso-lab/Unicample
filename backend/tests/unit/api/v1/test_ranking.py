from app.models.ranking import Ranking


def test_get_ranking(client, db_session):
    """Testa obtenção do ranking global"""
    # Inserir alguns dados de ranking

    client.delete("/ranking/delete")

    ranking_data1 = {
        "nome": "Jogador1",
        "pontuacao": 1000000
    }

    ranking_data2 = {
        "nome": "Jogador2",
        "pontuacao": 2000000
    }

    response1 = client.post("/ranking/adicionar", json=ranking_data1)
    response2 = client.post("/ranking/adicionar", json=ranking_data2)
    
    # Obter ranking
    response = client.get("/ranking")
    
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert {"nome": "Jogador1", "pontuacao": 1000000, "id": response1.json()["id"]} in data
    assert {"nome": "Jogador2", "pontuacao": 2000000, "id": response2.json()["id"]} in data
    # Verificar ordenação (maior pontu
    client.delete("/ranking/delete")

def test_adicionar_pontuacao(client):
    """Testa adição de nova pontuação no ranking"""
    ranking_data = {
        "nome": "NovoJogador",
        "pontuacao": 300
    }
    
    response = client.post("/ranking/adicionar", json=ranking_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "NovoJogador"
    assert data["pontuacao"] == 300