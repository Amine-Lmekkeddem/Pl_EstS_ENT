from fastapi import APIRouter, HTTPException, Depends, Request
from app.services.ChatBot import generate_response
from app.auth.jwt import verify_token
from app.models import Chat_request,Chat_responce

router = APIRouter()

# depend: str = Depends(verify_token)
@router.post("/", response_model=Chat_responce.ChatResponse)
async def chat_with_bot(request: Chat_request.ChatRequest):
    try:
        print("request", request.question)
        reply = generate_response(request.question)
        print("reply", reply)
        return {"response": reply}
    except Exception as e:
        print("error", e)
        raise HTTPException(status_code=500, detail=str(e))