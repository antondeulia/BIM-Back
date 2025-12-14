from sqlmodel import SQLModel, Field
from datetime import datetime

class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages" # type: ignore

    user_id: int

    id: int | None = Field(default=None, primary_key=True)
    assistant_id: int = Field(index=True)
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
