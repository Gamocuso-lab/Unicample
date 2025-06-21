from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Rodada(SQLModel, table=True):
    __tablename__ = "rodadas"

    id: int = Field(primary_key=True, index=True)
    tentativas: int = Field(nullable=False)
    id_jogo: int = Field(foreign_key="jogos.id", index=True)
    dificuldade : int = Field(nullable=False)
    id_imagem : int = Field(default=None, foreign_key="imagens.id")
    id_coordenada: Optional[int] = Field(default=None, foreign_key="coordenadas.id")

    # Relacionamentos
    jogo: "Jogo" = Relationship(back_populates="rodadas")
    imagem : "Imagem" = Relationship(back_populates="rodadas")
    coordenada: "Coordenada" = Relationship(back_populates="rodadas")