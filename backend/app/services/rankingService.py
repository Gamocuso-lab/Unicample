from sqlmodel import Session, select
from typing import List, Optional
from app.models.ranking import Ranking
from app.utils.singleton import SingletonMeta

class RankingService(metaclass=SingletonMeta):
    """
    Serviço para gerenciar a lógica de negócio do ranking de jogadores.
    """

    async def adicionar_pontuacao(self, session: Session, nome_jogador: str, pontuacao: int) -> Ranking:
        """
        Cria e salva uma nova entrada no ranking.
        Esta função deve ser chamada ao final de um jogo.

        Args:
            session (Session): A sessão do banco de dados.
            nome_jogador (str): O nome do jogador que concluiu o jogo.
            pontuacao (int): A pontuação final obtida no jogo.

        Returns:
            Ranking: O objeto da nova entrada do ranking que foi salvo.
        """
        nova_entrada = Ranking(nome=nome_jogador, pontuacao=pontuacao)
        session.add(nova_entrada)
        session.commit()
        session.refresh(nova_entrada)
        return nova_entrada

    async def obter_ranking(
        self, 
        session: Session, 
        nome_jogador: Optional[str] = None, 
        limite: int = 10
    ) -> List[Ranking]:
        """
        Busca as melhores pontuações no ranking.

        Args:
            session (Session): A sessão do banco de dados.
            nome_jogador (Optional[str]): Se fornecido, busca o ranking apenas para este jogador.
                                          Se não, busca o ranking geral (global).
            limite (int): O número máximo de resultados a serem retornados.

        Returns:
            List[Ranking]: Uma lista de objetos Ranking, ordenados pela maior pontuação.
        """
        statement = select(Ranking)

        if nome_jogador:
            statement = statement.where(Ranking.nome == nome_jogador)

        statement = statement.order_by(Ranking.pontuacao.desc()).limit(limite)

        resultados = session.exec(statement).all()
        
        return resultados