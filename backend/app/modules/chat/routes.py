from fastapi import APIRouter, HTTPException
from .schemas import ChatRequest, ChatResponse
from .services import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Принимает сообщение пользователя и возвращает ответ ассистента,
    основанный на анализе базы данных отелей и номеров.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Сообщение не может быть пустым")

    result = await chat_service.process_message(request.message)
    return ChatResponse(reply=result["reply"], sql_query=result.get("sql_query"))