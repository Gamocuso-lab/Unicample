from sqlmodel import SQLModel, Field, Relationship

class Local(SQLModel, table=True):
    __tablename__ = "locais"

    id: int = Field(primary_key=True)
    nome: str = Field(index=True, nullable=False)

    # Relacionamentos com nomes diferentes
    coordenada: list["Coordenada"] = Relationship(back_populates="local")
    imagem: list["Imagem"] = Relationship(back_populates="local")