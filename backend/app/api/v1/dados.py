from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.models.coordenada import Coordenada
from app.models.imagem import Imagem
from app.models.local import Local


router = APIRouter()
base_url = "/dados"

@router.post(base_url + "/local", response_model=dict)
async def create_local(request: Request, session: Session = Depends(get_session), nome: str = ""):
    """
    Endpoint para criar um novo jogo.
 """
    try:
        # Verificar se o nome foi fornecido
        if not nome:
            raise HTTPException(status_code=400, detail="Nome é obrigatório")
            
        novo_local = Local(nome=nome)
        session.add(novo_local)
        session.commit()
        session.refresh(novo_local)
        
        return {
            "local_id": novo_local.id,
            "nome": novo_local.nome
        }
    except Exception as e:
        # Log do erro para diagnóstico
        print(f"Erro ao criar local: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post(base_url + "/imagem", response_model=dict)
async def create_imagem(request: Request, session: Session = Depends(get_session), path: str = "", id_local: int = None):
    """
    Endpoint para criar um novo jogo.
    """

    nova_imagem = Imagem(path=path, id_local=id_local)

    session.add(nova_imagem)
    session.commit()
    session.refresh(nova_imagem)

    return {
        "id": nova_imagem.id,
        "path": nova_imagem.path,
        "id_local": nova_imagem.id_local
    }

@router.post(base_url + "/coordenada", response_model=dict)
async def create_coordenada(request: Request, session: Session = Depends(get_session), lat: float = None, lng: float = None, id_local: int = None):
    """
    Endpoint para criar um novo jogo.
    """
    try:
        # Validações
        if lat is None or lng is None:
            raise HTTPException(status_code=400, detail="Latitude e longitude são obrigatórios")
        
        if id_local is None:
            raise HTTPException(status_code=400, detail="ID do local é obrigatório")
            
        # Verificar se o local existe
        local = session.get(Local, id_local)
        if not local:
            raise HTTPException(status_code=404, detail=f"Local com ID {id_local} não encontrado")
            
        nova_coordenada = Coordenada(lat=lat, lng=lng, id_local=id_local)
        session.add(nova_coordenada)
        session.commit()
        session.refresh(nova_coordenada)
        
        return {
            "id": nova_coordenada.id,
            "local_id": nova_coordenada.id_local,
            "lat": nova_coordenada.lat,
            "lng": nova_coordenada.lng
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao criar coordenada: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
@router.delete(base_url + "/coordenadas", response_model=dict)
async def delete_all_coordenadas(request: Request, session: Session = Depends(get_session)):
    """
    Endpoint para deletar todas as coordenadas do banco de dados.
    """
    try:
        # Conta quantas coordenadas existem antes de deletar
        count_query = session.query(Coordenada).count()
        coordenadas_count = count_query
        
        # Deleta todas as coordenadas
        session.query(Coordenada).delete()
        session.commit()
        
        return {
            "message": f"{coordenadas_count} coordenadas foram deletadas com sucesso",
            "deleted_count": coordenadas_count
        }
    except Exception as e:
        # Log do erro para diagnóstico
        print(f"Erro ao deletar coordenadas: {str(e)}")
        session.rollback()  # Reverte a transação em caso de erro
        raise HTTPException(status_code=500, detail=f"Erro interno ao deletar coordenadas: {str(e)}")


@router.get(base_url + "/get-coordenadas", response_model=list[Coordenada])
async def get_coordenadas(request: Request, session: Session = Depends(get_session)):
    """
    Endpoint para obter todas as coordenadas.
    """
    try:
        coordenadas = session.query(Coordenada).all()
        return coordenadas
    except Exception as e:
        print(f"Erro ao obter coordenadas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
@router.get(base_url + "/get-locais", response_model=list[Local])
async def get_locais(request: Request, session: Session = Depends(get_session)):
    """
    Endpoint para obter todos os locais.
    """
    try:
        locais = session.query(Local).all()
        return locais
    except Exception as e:
        print(f"Erro ao obter locais: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    
@router.get(base_url + "/get-imagens", response_model=list[Imagem])
async def get_imagens(request: Request, session: Session = Depends(get_session)):
    """
    Endpoint para obter todas as imagens.
    """
    try:
        imagens = session.query(Imagem).all()
        return imagens
    except Exception as e:
        print(f"Erro ao obter imagens: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")