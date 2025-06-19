from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Coordenada(SQLModel, table=True):
    __tablename__ = "coordenadas"

    id: int = Field(index=True, primary_key=True)
    lat: float = Field(nullable=False)
    lng: float = Field(nullable=False)
    id_local: int = Field(default=None, foreign_key="locais.id")

    # Relacionamentos
    local: "Local" = Relationship(back_populates="coordenada")
    rodadas: List["Rodada"] = Relationship(back_populates="coordenada")