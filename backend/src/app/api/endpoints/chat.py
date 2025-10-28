from fastapi import APIRouter, Depends

from app.models.chat_schemas import QuestionRequest
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask")
async def ask_resume_question(request: QuestionRequest, service: ChatService = Depends(ChatService)):
    response = await service.get_agent_response(request.question)
    return {"response": response}
