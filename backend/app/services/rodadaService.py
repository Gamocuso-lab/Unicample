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
            
        local_correto = session.get(Local, coordenada_correta.local_id)
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