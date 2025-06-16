from sqlmodel import SQLModel, Field
from typing import Optional, List

class Ranking(SQLModel, table=True):
    __tablename__ = "rankings"

    id: int = Field(primary_key=True)
    nome: str = Field(index=True, nullable=False)
    pontuacao: int = Field(index=True, nullable=False)

