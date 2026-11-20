from fastapi import FastAPI
from api.routes import inventory as inventory_router
from core.database import Base, engine
from models import inventory as _models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Inventory Orchestrator API",
    version="1.0.0",
)

app.include_router(inventory_router.router)


@app.get("/health", tags=["System Status"])
def health_check():
    return {
        "status": "healthy",
        "system": "Inventory Orchestrator Engine",
    }