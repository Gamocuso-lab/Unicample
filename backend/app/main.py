from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from app.api.v1.streetview import router as streetview_router
from app.api.v1.jogo import router as jogo_router
from app.api.v1.dados import router as dados_router

app = FastAPI(title="Unicample")

# Rotas da API
app.include_router(api_router)
app.include_router(streetview_router)
app.include_router(jogo_router)
app.include_router(dados_router)