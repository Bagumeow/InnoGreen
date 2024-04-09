import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from Chatbot import chatbot
from uuid import uuid4
from pydantic import BaseModel

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post('/predict/')
async def predict(message: Message):
    response = chatbot.Chatbot(str(uuid4()))
    ans = response(message.message)
    return JSONResponse(content={"answer": ans})