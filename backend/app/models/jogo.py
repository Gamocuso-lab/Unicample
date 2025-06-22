from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List


class Jogo(SQLModel, table=True):
    __tablename__ = "jogos"
    
    id: int = Field(primary_key=True)
    pontuacao: int = Field(index=True, nullable=False)
    tempo: int = Field(index=True, nullable=False)
    finalizado: bool = Field(default=False, nullable=False)

    # Relacionamentos
    rodadas: List["Rodada"] = Relationship(back_populates="jogo")
