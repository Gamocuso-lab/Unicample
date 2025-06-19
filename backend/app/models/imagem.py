from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Imagem(SQLModel, table=True):
    __tablename__ = "imagens"

    id: int = Field(primary_key=True)
    path: str = Field(index=True, nullable=False)
    id_local: int = Field(default=None, foreign_key="locais.id")

    # Relacionamentos
    local : "Local" = Relationship(back_populates="imagem")
    rodadas: List["Rodada"] = Relationship(back_populates="imagem")
