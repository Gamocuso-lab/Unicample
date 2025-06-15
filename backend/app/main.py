from fastapi import FastAPI
from app.api.v1.routes import router as api_router

app = FastAPI(title="Unicample")

# Rotas da API
app.include_router(api_router)