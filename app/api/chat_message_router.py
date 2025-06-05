from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.chat_message import ChatMessage
from app.services.chat_message_service import ChatMessageService
# from app.services.agents.chatbot_agent import ChatbotAgent
from app.dependencies import get_chat_message_service

router = APIRouter(prefix="/api/chat-messages", tags=["chat_messages"])


# @router.post("/chat")
# def chat_with_plant(request: ChatRequest, agent: ChatbotAgent):
#     result = agent.run_sync(f"{request.plant_name}：{request.user_message}")
#     return {"reply": result.output}


@router.post("/", response_model=ChatMessage)
async def create_message(msg: ChatMessage, service: ChatMessageService = Depends(get_chat_message_service)):
    return await service.create_message(msg)


@router.get("/{message_id}", response_model=ChatMessage)
async def get_message(message_id: str, service: ChatMessageService = Depends(get_chat_message_service)):
    msg = await service.get_message(message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


@router.get("/by-plant/{plant_id}", response_model=List[ChatMessage])
async def list_by_plant(plant_id: str, service: ChatMessageService = Depends(get_chat_message_service)):
    return await service.list_messages_by_plant(plant_id)


@router.delete("/{message_id}")
async def delete_message(message_id: str, service: ChatMessageService = Depends(get_chat_message_service)):
    success = await service.delete_message(message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"success": True}


@router.delete("/by-plant/{plant_id}")
async def delete_all_by_plant(plant_id: str, service: ChatMessageService = Depends(get_chat_message_service)):
    count = await service.delete_messages_by_plant(plant_id)
    return {"deleted_count": count}
