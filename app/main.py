from app.routes import admin
from fastapi import FastAPI
from app.config import settings
app = FastAPI()

app.include_router(admin.router, prefix="/admin")

@app.get("/")
async def root():
    return {"message": "Welcome to the admin Microservice"}
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

#print(settings.CASSANDRA_HOST, settings.CASSANDRA_PORT, settings.CASSANDRA_KEYSPACE)
