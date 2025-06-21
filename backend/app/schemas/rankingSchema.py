from pydantic import BaseModel

class RankingCreate(BaseModel):
    nome: str
    pontuacao: int