from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str
    chat_id: str | None = None


class UploadFilesResponse(BaseModel):
    pdf_count: int
    text_count: int
    errors: list[str]
    success: bool


class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    role: str = Field(..., description="Role of the message sender, e.g., 'user' or 'agent'")
    content: str
    timestamp: datetime = datetime.utcnow()  # type: ignore


class ChatMemory(BaseModel):
    id: str
    chat_name: str
    chat_messages: list[ChatMessage] = Field(default_factory=list)

    @staticmethod
    def from_doc(doc) -> "ChatMemory":  # To convert back to pydantic model
        return ChatMemory(
            id=str(doc["_id"]),
            chat_name=doc["chat_name"],
            chat_messages=[ChatMessage(**msg) for msg in doc.get("chat_messages", [])],
        )


class ChatNameResponse(BaseModel):
    id: str
    chat_name: str
