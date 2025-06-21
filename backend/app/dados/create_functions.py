import requests
import json


# Configuração base
BASE_URL = "http://localhost:8000/dados"  # Ajuste para seu servidor
HEADERS = {"Content-Type": "application/json"}

# Diretório onde seus arquivos TXT estão localizados
DATA_DIR = "dados_locais"

def create_local(nome):
    """Cria um novo local."""
    url = f"{BASE_URL}/local"
    params = {"nome": nome}
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        print(f"Local '{nome}' criado com sucesso! ID: {response.json()['local_id']}")
        return response.json()["local_id"]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar local '{nome}': {e}")
        if response is not None:
            print(f"Detalhes da resposta de erro: {response.text}")
        return None

def create_coordenada(lat, lng, id_local):
    """Cria uma nova coordenada para um local."""
    url = f"{BASE_URL}/coordenada"
    params = {
        "lat": lat,
        "lng": lng,
        "id_local": id_local
    }
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        print(f"Coordenada criada: {lat}, {lng} para local {id_local}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar coordenada {lat}, {lng} para local {id_local}: {e}")
        if response is not None:
            print(f"Detalhes da resposta de erro: {response.text}")
        return False

def create_imagem(path, id_local):
    """Adiciona uma imagem para um local."""
    url = f"{BASE_URL}/imagem"
    params = {
        "path": path,
        "id_local": id_local
    }
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        print(f"Imagem adicionada: {path} para local {id_local}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao adicionar imagem {path} para local {id_local}: {e}")
        if response is not None:
            print(f"Detalhes da resposta de erro: {response.text}")
        return False