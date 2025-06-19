from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Localizacao(SQLModel, table=True):
    __tablename__ = "localizacoes"

    id: int = Field(primary_key=True)
    dificuldade : int = Field(index=True, nullable=False)
    imagem : str = Field(index=True, nullable=False)
    id_local : int = Field(index=True, foreign_key="locais.id")

    # Relacionamentos
    rodadas: list["Rodada"] = Relationship(back_populates="localizacao")
    local : "Local" = Relationship(back_populates="localizacao")