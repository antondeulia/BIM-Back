from typing import Any
from sqlmodel import Session, select

from app.models.assistant_model import Assistant


class AssistantRepository():
    def __init__(
            self,
            session: Session
    ):
        self.session = session

    def create_assistant(
            self,
            user_id: int,
            name: str | None,
            desc: str | None,
            provider: str,
            model: str,
            temperature: float
    ):
        assistant = Assistant(
            user_id=user_id,
            name=name,
            desc=desc,
            provider=provider,
            model=model,
            temperature=temperature
        )

        self.session.add(assistant)
        self.session.commit()
        self.session.refresh(assistant)

        return assistant
    
    def get_by_user_id(
            self,
            user_id: int
    ):
        assistants = self.session.exec(
            select(Assistant).where(Assistant.user_id == user_id)
        ).all()

        return assistants
    
    def get_by_id(
            self,
            id: int,
    ):
        assistant = self.session.exec(
            select(Assistant).where(Assistant.id == id)
        ).first()

        return assistant
    
    def update(
            self,
            assistant: Assistant,
            updates: dict[str, Any]
    ):
        self.session.add(assistant)
        self.session.commit()
        self.session.refresh(assistant)

        return assistant