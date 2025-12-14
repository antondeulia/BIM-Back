from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, asc, desc, select

from app.models.chat_message_model import ChatMessage

class ChatMessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, assistant_id: int, role: str, content: str, user_id: int) -> ChatMessage:
        msg = ChatMessage(
            assistant_id=assistant_id,
            role=role,
            content=content,
            created_at=datetime.utcnow(),
            user_id=user_id
        )
        self.session.add(msg)
        self.session.commit()
        self.session.refresh(msg)
        return msg

    def get_by_assistant_id(self, assistant_id: int, limit: int = 20):
        query = (
            select(ChatMessage)
            .where(ChatMessage.assistant_id == assistant_id)
            .order_by(asc(ChatMessage.created_at))
            .limit(limit)
        )
        return list(self.session.exec(query))
    
    def get_all_chat_messages(
            self,
            user_id: int
    ):
        chat_messages = self.session.exec(
            select(ChatMessage).where(ChatMessage.user_id == user_id)
        ).all()

        return chat_messages
    
    def delete_by_id(
            self,
            id: int
    ):
        chat_message = self.session.exec(
            select(ChatMessage).where(ChatMessage.id == id)
        ).first()
        
        self.session.delete(chat_message)
        self.session.commit()
        self.session.refresh(chat_message)

        return {
            "status": "ok"
        }
    
    def delete_by_assistant_id(
            self,
            assistant_id: int
    ):
        chat_messages = self.session.exec(
            select(ChatMessage).where(ChatMessage.assistant_id == assistant_id)
        ).all()

        for chat_message in chat_messages:
            self.session.delete(chat_message)
            self.session.commit()

        return {
            "status": "ok"
        }
