from app.models.local import Local


def test_create_local(client):
    """Testa a criação de um local"""
    response = client.post("/dados/local?nome=Instituto de Computação")
    
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Instituto de Computação"
    assert "local_id" in data

    client.delete(f"/dados/local/{data['local_id']}")  # Limpar após o teste

def test_create_coordenada(client, db_session):
    """Testa a criação de coordenada para um local existente"""
    # Criar local para teste
    response1 = client.post("/dados/local?nome=Biblioteca Central")

    data1 = response1.json()
    
    # Criar coordenada
    response2 = client.post(f"/dados/coordenada?lat=-22.8158&lng=-47.0679&id_local={data1['local_id']}")
    
    assert response2.status_code == 200
    data2 = response2.json()
    assert float(data2["lat"]) == -22.8158
    assert float(data2["lng"]) == -47.0679
    assert data2["local_id"] == data1['local_id']

    client.delete(f"/dados/coordenada/{data2['id']}")  # Limpar coordenada após o teste
    client.delete(f"/dados/local/{data1['local_id']}")  # Limpar após o teste