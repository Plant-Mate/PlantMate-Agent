from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.chat_message import ChatMessage
from app.models.chat_message_request import ChatMessageRequest
from app.services.chat_message_service import ChatMessageService
from app.services.agents.chatbot_agent import ChatbotAgent
from app.dependencies import get_chat_message_service
from bson import ObjectId

router = APIRouter(prefix="/api/chat-messages", tags=["chat_messages"])


# @router.post("/chat")
# async def chat_with_plant(msg: ChatMessage,service: ChatMessageService = Depends(get_chat_message_service)):
#    user_id = str(ObjectId())
#    user_msg = ChatMessage(
#        id=user_id,
#        plant_id=msg.plant_id,
#        message_type="user",
#        content=msg.content
#    )
#    saved_user_msg = await service.create_message(user_msg)
#    result = await ChatbotAgent.run(saved_user_msg)
#    bot_content = ""
#    if hasattr(result.output, "content"):
#        bot_content = result.output.content
#    else:
#        bot_content = str(result.output)
#    bot_id = str(ObjectId())
#    bot_msg = ChatMessage(
#        id=bot_id,
#        plant_id=result.plant_id,
#        message_type="assistant",
#        content=bot_content
#    )
#    saved_bot_msg = await service.create_message(bot_msg)
#    return saved_bot_msg 
    

@router.post("/{plant_id}", response_model=ChatMessage)
async def create_message(plant_id: str, msg: ChatMessageRequest, service: ChatMessageService = Depends(get_chat_message_service)):
    message = msg.to_chat_message(plant_id)
    return await service.create_message(message)


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
