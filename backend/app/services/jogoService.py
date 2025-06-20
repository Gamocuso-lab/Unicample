from backend.app.services.rodadaService import RodadaService
from sqlmodel import Session, select
from app.models.coordenada import Coordenada
from app.models.imagem import Imagem
from app.models.jogo import Jogo
from app.models.local import Local
from app.models.rodada import Rodada
from app.schemas.jogoSchema import JogoResponse
from app.utils.singleton import SingletonMeta
import random

class JogoService(metaclass=SingletonMeta):
    """
    Serviço para gerenciar jogos.
    """

    def __init__(self):
        pass

    def create_jogo(self, session: Session):
        """
        Cria um novo jogo e uma rodada inicial.
        """
        novo_jogo = Jogo(pontuacao=0, tempo=180)

        # Adiciona o novo jogo à sessão
        session.add(novo_jogo)

        # Confirma a transação
        session.commit()

        # Atualiza o objeto com o ID gerado pelo banco
        session.refresh(novo_jogo)

        self.cria_rodada(session, novo_jogo.id)

        return novo_jogo
    
    def seleciona_local(self, session: Session) -> Local:
        """
        Seleciona um registro aleatório da tabela Locais.

        Args:
            session (Session): Sessão do banco de dados.

        Returns:
            Local: Um registro aleatório da tabela Locais.
        """
        # Consulta para selecionar todos os IDs da tabela Locais
        statement = select(Local.id)
        result = session.exec(statement).all()

        if not result:
            raise ValueError("Nenhum local encontrado no banco de dados.")

        # Seleciona um ID aleatório
        random_id = random.choice(result)

        # Busca o registro correspondente ao ID aleatório
        local = session.get(Local, random_id)

        return local

    def seleciona_coordenada(self, session: Session, local_id: int) -> Coordenada:
        """
        Seleciona uma coordenada associada a um local específico.

        Args:
            session (Session): Sessão do banco de dados.
            local_id (int): ID do local para o qual a coordenada deve ser selecionada.

        Returns:
            Coordenada: A coordenada associada ao local especificado.
        """
        # Consulta para selecionar uma coordenada associada ao local
        statement = select(Coordenada).where(Coordenada.local_id == local_id)
        coordenadas = session.exec(statement).all()

        if not coordenadas:
            raise ValueError("Nenhuma coordenada encontrada para o local especificado.")

        coordenada = random.choice(coordenadas) 
        return coordenada

    def seleciona_imagem(self, session: Session, local_id: int) -> Imagem:
        """
        Seleciona uma imagem associada a um local específico.

        Args:
            session (Session): Sessão do banco de dados.
            local_id (int): ID do local para o qual a imagem deve ser selecionada.

        Returns:
            Imagem: A imagem associada ao local especificado.
        """
        # Consulta para selecionar uma imagem associada ao local
        statement = select(Imagem).where(Imagem.local_id == local_id)
        imagens = session.exec(statement).all()

        if not imagens:
            raise ValueError("Nenhuma imagem encontrada para o local especificado.")

        imagem = random.choice(imagens) 
        return imagem

    def cria_rodada(self, session: Session, jogo_id: int) -> Rodada:
        """
        Cria uma nova rodada associada a um jogo existente.

        Args:
            session (Session): Sessão do banco de dados.
            jogo_id (int): ID do jogo ao qual a rodada será associada.
        Returns:
            Rodada: A nova rodada criada.
        """

        local = self.seleciona_local(session)

        imagem = self.seleciona_imagem(session, local.id)
        coordenada = self.seleciona_coordenada(session, local.id)

        nova_rodada = Rodada(jogo_id=jogo_id, pontuacao=0, tentativas=4, dificuldade=5, imagem_id=imagem.id, coordenada_id=coordenada.id)

        # Adiciona a nova rodada à sessão
        session.add(nova_rodada)

        # Confirma a transação
        session.commit()

        # Atualiza o objeto com o ID gerado pelo banco
        session.refresh(nova_rodada)

        return nova_rodada
    
    def get_jogo_info(self, session: Session, jogo_id: int) -> JogoResponse:
        """
        Obtém as informações de um jogo específico.
        Args:
            session (Session): Sessão do banco de dados.
            jogo_id (int): ID do jogo a ser buscado.
        Returns:
            JogoResponse: Informações do jogo, incluindo pontuação, tempo e rodadas.
        Raises:
            ValueError: Se o jogo não for encontrado.
        """
        # Busca o jogo pelo ID

        jogo_info = JogoResponse(
            id=jogo_id,
            pontuacao=0,
            tempo=180,
            rodada_atual=None
        )

        jogo = session.get(Jogo, jogo_id)

        if not jogo:
            raise ValueError("Jogo não encontrado.")

        jogo_info.pontuacao = jogo.pontuacao
        jogo_info.tempo = jogo.tempo

        rodada_statement = select(Rodada).where(Rodada.jogo_id == jogo_id).order_by(Rodada.id.desc())

        rodadas = session.exec(rodada_statement).all()

        rodada_atual = rodadas[0] if rodadas else None

        jogo_info.id_rodada_atual = rodada_atual.id if rodada_atual else None

        jogo_info.rodadas = []

        for rodada in rodadas:
            coordenada = session.get(Coordenada, rodada.coordenada_id)
            imagem = session.get(Imagem, rodada.imagem_id)

            jogo_info.rodadas.append({
                "tentativas": rodada.tentativas,
                "dificuldade": rodada.dificuldade,
                "imagem": imagem.url if imagem else None,
                "coordenada": {
                    "lat": coordenada.lat if coordenada else None,
                    "lng": coordenada.lng if coordenada else None
                }
            })

        return jogo_info

    def adiciona_pontuacao(self, session: Session, jogo_id: int, rodada_id: int):
        """
        Adiciona pontuação a um jogo existente.
        """
        jogo = session.get(Jogo, jogo_id)

        rodada = session.get(Rodada, rodada_id)

        if not jogo:
            raise ValueError("Jogo não encontrado.")
        
        if not rodada:
            raise ValueError("Rodada não encontrada.")

        jogo.pontuacao += rodada.dificuldade*30

        # Atualiza o jogo na sessão
        session.add(jogo)

        # Confirma a transação
        session.commit()

        return jogo
    
    def chute(self, session: Session, jogo_id: int, rodada_id: int, local: str):
        """
        Processa o chute do jogador e atualiza a pontuação.
        """
        jogo = session.get(Jogo, jogo_id)

        if not jogo:
            raise ValueError("Jogo não encontrado.")

        # Rodada Service para utilizar métodos relacionados à rodada
        rodadaService = RodadaService()

        # Verifica se o chute está correto
        acerto = rodadaService.verifica_acerto(session, rodada_id, local)

        if acerto:
            self.adiciona_pontuacao(session, jogo_id, rodada_id)
            return True
        else:
            rodadaService.diminui_dificuldade(session, rodada_id)
        
        return False