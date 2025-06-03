from fastapi import APIRouter
from app.models.chat_request import ChatRequest
# from app.services.agents.chatbot_agent import chatbot_agent

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Hello World"}

# @router.post("/chat")
# def chat_with_plant(request: ChatRequest):
#     result = chatbot_agent.run_sync(f"{request.plant_name}：{request.user_message}")
#     return {"reply": result.output}
