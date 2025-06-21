from fastapi import FastAPI, BackgroundTasks
from app.api.v1.routes import router as api_router
from app.api.v1.streetview import router as streetview_router
from app.api.v1.jogo import router as jogo_router
from app.api.v1.dados import router as dados_router
from app.dados.read_documents import process_data_from_unified_files

app = FastAPI(title="Unicample")

# Rotas da API
app.include_router(api_router)
app.include_router(streetview_router)
app.include_router(jogo_router)
app.include_router(dados_router)

@app.post("/admin/import-data")
async def import_data(background_tasks: BackgroundTasks):
    """Endpoint para importar dados em segundo plano"""
    background_tasks.add_task(process_data_from_unified_files, "app/dados/documents")
    return {"message": "Importação de dados iniciada em segundo plano"}

