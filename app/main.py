from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
from app.database.postgre import init_db
from app.routers import camera_route, evento_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Criando tabelas no banco de dados...")
    await init_db()
    yield


app = FastAPI(
    title="API DE CAMERAS",
    description="API para análise e criação das câmeras",
    lifespan=lifespan,
)


app.include_router(camera_route.router)
app.include_router(evento_route.router)


@app.get("/")
async def health_check():
    return {
        "status": "Healthy",
        "timestamp": datetime.now(timezone.utc),
        "version": "1.0.0",
    }
