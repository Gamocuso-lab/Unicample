from pydantic import BaseModel

class CoordenadaResponse(BaseModel):
    lat: int
    lng: int

class RodadaResponse(BaseModel):
    tentativas: int
    dificuldade: int
    imagem: str
    coordenada: CoordenadaResponse

class JogoResponse(BaseModel):
    id: int
    pontuacao: int
    tempo: int
    finalizado: bool
    id_rodada_atual: int | None = None
    rodadas: list[RodadaResponse]
