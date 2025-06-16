from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

class Rodada(SQLModel, table=True):
    __tablename__ = "rodadas"

    id: int = Field(primary_key=True)
    numero: int = Field(index=True, nullable=False)
    id_localizacao: int = Field(index=True, foreign_key="localizacoes.id")
    id_jogo: int = Field(foreign_key="jogos.id")

    # Relacionamentos
    jogo: "Jogo" = Relationship(back_populates="rodadas")
    localizacao: "Localizacao" = Relationship(back_populates="rodadas")