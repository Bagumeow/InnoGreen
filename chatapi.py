from fastapi import APIRouter
from fastapi.responses import JSONResponse
from chatbot import Chatbot
from uuid import uuid4
from pydantic import BaseModel

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post('/predict/')
async def predict(message: Message):
    response = Chatbot(str(uuid4()))
    ans = response(message)
    return JSONResponse(content={"answer": ans})
