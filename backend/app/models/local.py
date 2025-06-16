from sqlmodel import SQLModel, Field, Relationship

class Local(SQLModel, table=True):
    __tablename__ = "locais"

    id: int = Field(primary_key=True)
    nome: str = Field(index=True, nullable=False)

    # Relacionamentos
    localizacao: list["Localizacao"] = Relationship(back_populates="local")