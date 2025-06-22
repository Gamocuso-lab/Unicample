from fastapi import HTTPException
import os
from fastapi import Request
from fastapi.responses import HTMLResponse
from app.services.rodadaService import RodadaService
from app.services.streetviewService import StreetviewService
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

    async def create_jogo(self, session: Session):
        """
        Cria um novo jogo e uma rodada inicial.
        """
        try:
            novo_jogo = Jogo(pontuacao=0, tempo=180)

            # Adiciona o novo jogo à sessão
            session.add(novo_jogo)

            # Confirma a transação
            session.commit()

            # Atualiza o objeto com o ID gerado pelo banco
            session.refresh(novo_jogo)

            await self.cria_rodada(session, novo_jogo.id)

            return novo_jogo
        except Exception as e:
            print(f"Erro ao criar jogo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def seleciona_local(self, session: Session) -> Local:
        """
        Seleciona um registro aleatório da tabela Locais.

        Args:
            session (Session): Sessão do banco de dados.

        Returns:
            Local: Um registro aleatório da tabela Locais.
        """
        # Consulta para selecionar todos os IDs da tabela Locais
        try: 
            statement = select(Local.id)
            result = session.exec(statement).all()

            if not result:
                raise ValueError("Nenhum local encontrado no banco de dados.")

            # Seleciona um ID aleatório
            random_id = random.choice(result)

            # Busca o registro correspondente ao ID aleatório
            local = session.get(Local, random_id)

            return local
        except Exception as e:
            print(f"Erro ao selecionar local: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

    async def seleciona_coordenada(self, session: Session, id_local: int) -> Coordenada:
        """
        Seleciona uma coordenada associada a um local específico.

        Args:
            session (Session): Sessão do banco de dados.
            id_local (int): ID do local para o qual a coordenada deve ser selecionada.

        Returns:
            Coordenada: A coordenada associada ao local especificado.
        """
        # Consulta para selecionar uma coordenada associada ao local
        try:
            statement = select(Coordenada).where(Coordenada.id_local == id_local)
            coordenadas = session.exec(statement).all()

            if not coordenadas:
                raise ValueError("Nenhuma coordenada encontrada para o local especificado.")

            coordenada = random.choice(coordenadas) 
            return coordenada
        except Exception as e:
            print(f"Erro ao selecionar coordenada: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

    async def seleciona_imagem(self, session: Session, id_local: int) -> Imagem:
        """
        Seleciona uma imagem associada a um local específico.

        Args:
            session (Session): Sessão do banco de dados.
            id_local (int): ID do local para o qual a imagem deve ser selecionada.

        Returns:
            Imagem: A imagem associada ao local especificado.
        """
        # Consulta para selecionar uma imagem associada ao local
        try:
            statement = select(Imagem).where(Imagem.id_local == id_local)
            imagens = session.exec(statement).all()

            if not imagens:
                raise ValueError("Nenhuma imagem encontrada para o local especificado.")

            imagem = random.choice(imagens) 
            return imagem
        except Exception as e:
            print(f"Erro ao selecionar imagem: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

    async def cria_rodada(self, session: Session, id_jogo: int) -> Rodada:
        """
        Cria uma nova rodada associada a um jogo existente.

        Args:
            session (Session): Sessão do banco de dados.
            id_jogo (int): ID do jogo ao qual a rodada será associada.
        Returns:
            Rodada: A nova rodada criada.
        """
        try:
            local = await self.seleciona_local(session)

            imagem = await self.seleciona_imagem(session, local.id)
            coordenada = await self.seleciona_coordenada(session, local.id)

            nova_rodada = Rodada(id_jogo=id_jogo, pontuacao=0, tentativas=4, dificuldade=4, id_imagem=imagem.id, id_coordenada=coordenada.id)

            # Adiciona a nova rodada à sessão
            session.add(nova_rodada)

            # Confirma a transação
            session.commit()

            # Atualiza o objeto com o ID gerado pelo banco
            session.refresh(nova_rodada)

            return nova_rodada
        except Exception as e:
            print(f"Erro ao criar rodada: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
    async def get_jogo_info(self, session: Session, id_jogo: int) -> JogoResponse:
        """
        Obtém as informações de um jogo específico.
        Args:
            session (Session): Sessão do banco de dados.
            id_jogo (int): ID do jogo a ser buscado.
        Returns:
            JogoResponse: Informações do jogo, incluindo pontuação, tempo e rodadas.
        Raises:
            ValueError: Se o jogo não for encontrado.
        """
        # Busca o jogo pelo ID

        jogo_info = JogoResponse(
            id=id_jogo,
            pontuacao=0,
            tempo=180,
            finalizado=False,
            id_rodada_atual=0,
            rodadas=[]
        )

        jogo = session.get(Jogo, id_jogo)

        if not jogo:
            raise ValueError("Jogo não encontrado.")

        jogo_info.pontuacao = jogo.pontuacao
        jogo_info.tempo = jogo.tempo
        jogo_info.finalizado = jogo.finalizado

        rodada_statement = select(Rodada).where(Rodada.id_jogo == id_jogo).order_by(Rodada.id.desc())

        rodadas = session.exec(rodada_statement).all()

        rodada_atual = rodadas[0] if rodadas else None

        jogo_info.id_rodada_atual = rodada_atual.id if rodada_atual else None

        jogo_info.rodadas = []

        for rodada in rodadas:
            coordenada = session.get(Coordenada, rodada.id_coordenada)
            imagem = session.get(Imagem, rodada.id_imagem)

            jogo_info.rodadas.append({
                "tentativas": rodada.tentativas,
                "dificuldade": rodada.dificuldade,
                "imagem": imagem.path if imagem else None,
                "coordenada": {
                    "lat": coordenada.lat if coordenada else None,
                    "lng": coordenada.lng if coordenada else None
                }
            })

        return jogo_info

    async def adiciona_pontuacao(self, session: Session, id_jogo: int, rodada_id: int):
        """
        Adiciona pontuação a um jogo existente.
        """
        jogo = session.get(Jogo, id_jogo)

        rodada = session.get(Rodada, rodada_id)

        if not jogo:
            raise ValueError("Jogo não encontrado.")
        
        if not rodada:
            raise ValueError("Rodada não encontrada.")

        jogo.pontuacao += rodada.dificuldade*30

        session.add(jogo)

        session.commit()

        return jogo
    
    async def chute(self, session: Session, id_jogo: int, local: str):
        """
        Processa o chute do jogador e atualiza a pontuação.
        """
        jogo = session.get(Jogo, id_jogo)

        if not jogo:
            raise ValueError("Jogo não encontrado.")

        # Rodada Service para utilizar métodos relacionados à rodada
        rodadaService = RodadaService()

        rodada_id = rodadaService.get_dados_rodada_atual(session, id_jogo).get("id_rodada")

        # Verifica se o chute está correto
        acerto = rodadaService.verifica_acerto(session, rodada_id, local)

        if acerto:
            await self.adiciona_pontuacao(session, id_jogo, rodada_id)
            await self.cria_rodada(session, id_jogo)
            return True
        else:
            rodada = rodadaService.diminui_dificuldade(session, rodada_id)
            if rodada.tentativas <= 0:
                # Se não houver mais tentativas, cria uma nova rodada
                await self.cria_rodada(session, id_jogo)
        
        return False
    
    async def get_rodada_streetview(self, session: Session, id_jogo: int, request: Request) -> HTMLResponse:
        """
        Orquestra a criação da visualização do Street View para a rodada atual.
        """
        # 1. Instanciar os serviços necessários
        rodada_service = RodadaService()
        streetview_service = StreetviewService()

        # 2. Obter os dados da rodada atual usando o RodadaService
        dados_rodada = rodada_service.get_dados_rodada_atual(session, id_jogo)

        # 3. Lógica do blur (agora reside aqui, no JogoService)
        blur_level = dados_rodada.get("blur_level", 1)

        # 4. Obter a localização
        local_str = dados_rodada.get("local")
        if not local_str:
            raise ValueError("Localização não fornecida pela rodada.")

        # 5. Obter a chave da API
        api_key = os.getenv("STREET_VIEW_KEY")

        # 6. Chamar o StreetviewService para gerar o HTML final
        return streetview_service.get_streetview_image(
            local=local_str,
            key=api_key,
            request=request,
            blur_level=blur_level
        )
    
    async def get_rodada_imagem(self, session: Session, id_jogo: int) -> str:
        """
        Obtém a imagem da rodada atual de um jogo.
        """
        rodada_service = RodadaService()

        # 2. Obter os dados da rodada atual usando o RodadaService
        dados_rodada = rodada_service.get_dados_rodada_atual(session, id_jogo)

        return dados_rodada.get("imagem")
    
    async def finalizar_jogo(self, session: Session, id_jogo: int) -> JogoResponse:
        """
        Finaliza um jogo, retornando as informações do jogo finalizado.
        """
        jogo = session.get(Jogo, id_jogo)

        if not jogo:
            raise ValueError("Jogo não encontrado.")

        jogo.finalizado = True

        session.add(jogo)

        session.commit()
        
        return await self.get_jogo_info(session, id_jogo)