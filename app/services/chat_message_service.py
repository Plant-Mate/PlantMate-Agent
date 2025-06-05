from typing import List, Optional
from app.models.chat_message import ChatMessage
from app.repositories.chat_message_repository import ChatMessageRepository


class ChatMessageService:
    def __init__(self, chat_repo: ChatMessageRepository):
        self.chat_repo = chat_repo

    async def create_message(self, message: ChatMessage) -> ChatMessage:
        return await self.chat_repo.create(message)

    async def get_message(self, message_id: str) -> Optional[ChatMessage]:
        return await self.chat_repo.find_by_id(message_id)

    async def list_messages_by_plant(self, plant_id: str) -> List[ChatMessage]:
        return await self.chat_repo.list_by_plant(plant_id)

    async def delete_message(self, message_id: str) -> bool:
        return await self.chat_repo.delete_by_id(message_id)

    async def delete_messages_by_plant(self, plant_id: str) -> int:
        return await self.chat_repo.delete_by_plant(plant_id)

    async def create_mock_message(self, message: ChatMessage) -> Optional[ChatMessage]:
        mapping = {
            "今天要不要澆水？": "今天土壤表面還有些乾，你可以摸摸看，如果上層大約3–4公分的地方還是乾的，那我其實會很開心你給我澆一點點水。不過不要一次灌太多水，讓水慢慢滲下去就好。畢竟我比較怕積水。",
            "我家附近有蚜蟲，該怎麼處理才不會傷到你？": "蚜蟲確實容易找上我的嫩芽，會吸走養分讓新葉畸形。你可以先用一盆裝了肥皂水（少量中性洗潔精溶於水中）的稀釋噴霧，對著葉片背面和嫩芽輕輕噴灑，讓蚜蟲軟化後用清水沖洗乾淨。如果情況嚴重，可以準備含有吡蟲啉或啶蟎酯等成分的低毒性農藥，按照包裝濃度去稀釋噴施。但要儘量避免高濃度或高頻度施用，以免影響我的生長和開花。",
            "今天心情怎麼樣？": "今天我的心情很愉快呢！清晨時分曬到溫暖的陽光，感覺全身都充滿活力。土壤雖然還微微乾燥，但不會太渴，這種微乾的感覺對我來說恰到好處，讓我的根系能更健康地呼吸。 "
        }

        if message.content in mapping:
            response_message = ChatMessage(plant_id=message.plant_id, message_type='assistant', content=mapping[message.content])
        else:
            response_message = ChatMessage(plant_id=message.plant_id, message_type='assistant', content=mapping["今天要不要澆水？"])

        await self.chat_repo.create(message)
        return await self.chat_repo.create(response_message)