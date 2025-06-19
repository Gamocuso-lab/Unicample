from sqlmodel import SQLModel
from app.db.session import engine

def init_db():
    import app.models  # Garante que os models estão carregados
    SQLModel.metadata.create_all(engine)

def reset_db():
    import app.models 
    SQLModel.metadata.drop_all(engine, checkfirst=True)     # Remove todas as tabelas
    SQLModel.metadata.create_all(engine) 