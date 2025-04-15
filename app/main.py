from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat 
from app.config import Settings
app = FastAPI(
    title="Chatbot Microservice",
    description="Chatbot powered by Llama 3 via Ollama",
    version="1.0.0"
)


# CORS (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this to your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print(f"Chatbot is running on {Settings.OLLAMA_BASE_URL}")

# Routes
app.include_router(chat.router, prefix="/api/chat")

@app.get("/")
def health_check():
    return {"status": "Chatbot is running ✅"}

