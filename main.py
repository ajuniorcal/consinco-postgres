from fastapi import FastAPI
from fastapi import APIRouter
from database import Base, engine
from routers.healthcheck import router as health_router
from routers.etl_router import router as etl_router   # ← AGORA CORRETO

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Consinco ETL API",
    version="1.0.0",
    description="ETL do desafio técnico"
)

# Routers
app.include_router(health_router)
app.include_router(etl_router)

@app.get("/")
def root():
    return {"message": "ETL Consinco API Running on port 5000"}
