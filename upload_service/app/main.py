from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.health import router as health_router

app = FastAPI()

# Ajouter les routes avec APIRouter
app.include_router(upload_router, prefix="/files", tags=["uploadfile"])
app.include_router(health_router, prefix="/status", tags=["Health Check"])
