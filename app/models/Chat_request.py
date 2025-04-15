from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question : str 