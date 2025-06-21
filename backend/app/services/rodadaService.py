import os
from fastapi import Request
from fastapi.responses import HTMLResponse
from app.services.streetviewService import StreetviewService
from sqlmodel import Session, select
from app.models.rodada import Rodada
from app.models.coordenada import Coordenada
from app.models.local import Local
from app.utils.singleton import SingletonMeta

class RodadaService(metaclass=SingletonMeta):
    """
    Serviço para gerenciar a lógica de uma rodada do jogo.
    """

    def __init__(self):
        pass

    def verifica_acerto(self, session: Session, rodada_id: int, local_chute: str) -> bool:
        """
        Verifica se o nome do local chutado pelo jogador corresponde ao local correto da rodada.

        Args:
            session (Session): A sessão do banco de dados.
            rodada_id (int): O ID da rodada atual.
            local_chute (str): O nome do local que o jogador chutou.

        Returns:
            bool: True se o chute estiver correto, False caso contrário.
            
        Raises:
            ValueError: Se a rodada, coordenada ou local não forem encontrados.
        """
        rodada = session.get(Rodada, rodada_id)
        if not rodada:
            raise ValueError("Rodada não encontrada.")

        coordenada_correta = session.get(Coordenada, rodada.id_coordenada)
        if not coordenada_correta:
            raise ValueError("Coordenada correta para a rodada não encontrada.")
            
        local_correto = session.get(Local, coordenada_correta.id_local)
        if not local_correto:
            raise ValueError("Local correto para a rodada não encontrado.")

        return local_correto.nome.lower() == local_chute.lower()

    def diminui_dificuldade(self, session: Session, rodada_id: int) -> Rodada:
        """
        Reduz a dificuldade e o número de tentativas de uma rodada após um erro do jogador.

        Args:
            session (Session): A sessão do banco de dados.
            rodada_id (int): O ID da rodada a ser atualizada.

        Returns:
            Rodada: O objeto da rodada atualizado.
            
        Raises:
            ValueError: Se a rodada não for encontrada.
        """
        rodada = session.get(Rodada, rodada_id)
        if not rodada:
            raise ValueError("Rodada não encontrada.")

        if rodada.dificuldade > 1:
            rodada.dificuldade -= 1
            
        if rodada.tentativas > 0:
            rodada.tentativas -= 1


        # Adiciona o objeto modificado à sessão para preparar a atualização.
        session.add(rodada)
        
        # Confirma a transação, salvando as alterações no banco de dados.
        session.commit()
        
        # Atualiza o objeto 'rodada' com os dados que acabaram de ser salvos no banco.
        session.refresh(rodada)

        return rodada
    
    def get_dados_rodada_atual(self, session: Session, id_jogo: int) -> dict:
        """
        Busca a rodada atual de um jogo e retorna seus dados essenciais 
        para a visualização.
        """
        # 1. Obter a rodada atual do jogo
        rodada_statement = select(Rodada).where(Rodada.id_jogo == id_jogo).order_by(Rodada.id.desc())
        rodada_atual = session.exec(rodada_statement).first()

        if not rodada_atual:
            raise ValueError("Nenhuma rodada encontrada para este jogo.")

        # 2. Obter a coordenada correta
        coordenada = session.get(Coordenada, rodada_atual.id_coordenada)
        if not coordenada:
            raise ValueError("Coordenada não encontrada para a rodada.")
        
        blur_level = rodada_atual.dificuldade * 4
        # 3. Montar e retornar um dicionário com os dados
        dados_rodada = {
            "local": f"{coordenada.lat},{coordenada.lng}",
            "blur_level": blur_level
        }
        
        return dados_rodada