from app.routes import admin
from fastapi import FastAPI
app = FastAPI()

app.include_router(admin.router, prefix="/admin")

@app.get("/")
async def root():
    return {"message": "Welcome to the admin Microservice"}
@app.get("/health")
async def health_check():
    return {"status": "healthy"}