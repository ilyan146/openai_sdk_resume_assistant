# type: ignore


from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from openai_sdk_resume_assistant.backend.app.models.chat_schemas import ChatMemory, ChatMessage


class MongoDAL:
    def __init__(self, mongo_mem_collection: AsyncIOMotorClient):
        self._mongo_mem_collection = mongo_mem_collection

    async def create_chat_memory(self, chat_name: str, session=None) -> str:
        response = await self._mongo_mem_collection.insert_one({"chat_name": chat_name, "chat_messages": []}, session=session)
        return str(response.inserted_id)

    async def get_chat_memory(self, id: str | ObjectId, session=None) -> ChatMemory:
        doc = await self._mongo_mem_collection.find_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return ChatMemory.from_doc(doc) if doc else None

    async def add_message_to_chat(self, chat_id: str | ObjectId, role: str, content: str, session=None) -> ChatMemory | None:
        """Add a new message to an existing chat"""
        message = ChatMessage(role=role, content=content)
        doc = await self._mongo_mem_collection.find_one_and_update(
            {"_id": ObjectId(chat_id)},
            {"$push": {"chat_messages": message.model_dump()}},
            return_document=ReturnDocument.AFTER,
            session=session,
        )
        return ChatMemory.from_doc(doc) if doc else None

    async def get_all_chats(self, limit: int = 50, session=None) -> list[ChatMemory]:
        """Get all chat memories"""
        cursor = self._mongo_mem_collection.find({}, session=session).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [ChatMemory.from_doc(doc) for doc in docs]
