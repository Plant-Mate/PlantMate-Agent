from app.db.mongodb import db
from repositories.plant_repository import PlantRepository
from repositories.chat_message_repository import ChatMessageRepository
from services.plant_service import PlantService
from services.chat_message_service import ChatMessageService


def get_plant_service():
    repo = PlantRepository(db)
    return PlantService(repo)

def get_chat_message_service():
    repo = ChatMessageRepository(db)
    return ChatMessageService(repo)
