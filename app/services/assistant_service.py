from fastapi import HTTPException
from sqlmodel import Session

from app.models.assistant_model import Assistant
from app.repositories.assistant_dataset_repository import AssistantDatasetRepository
from app.repositories.assistant_repository import AssistantRepository
from app.repositories.chat_message_repository import ChatMessageRepository
from app.schemas.assistant_schema import UpdateAssistantRequest
from app.services.llm.llm_service import LLMService
from app.services.pinecone_service import PineconeService


class AssistantService():
    def __init__(
            self,
            assistant_repo: AssistantRepository,
            assistant_dataset_repo: AssistantDatasetRepository,
            chat_message_repo: ChatMessageRepository,
            pc_service: PineconeService,
            llm_service: LLMService
    ):
        self.assistant_repo = assistant_repo
        self.assistant_dataset_repo = assistant_dataset_repo
        self.chat_message_repo = chat_message_repo
        self.pc_service = pc_service
        self.llm_service = llm_service

    def create_assistant(
            self,
            user_id: int,
            name: str | None,
            desc: str | None,
            provider: str,
            model: str,
            temperature: float,
    ):
        return self.assistant_repo.create_assistant(
            user_id,
            name,
            desc,
            provider,
            model,
            temperature
        )
    
    def get_by_user_id(
            self,
            user_id: int
    ):
        return self.assistant_repo.get_by_user_id(
            user_id
        )
    
    def get_by_id(
            self,
            id: int,
    ):
        assistant = self.assistant_repo.get_by_id(id)
        if not assistant:
            raise HTTPException(status_code=404, detail="Assistant not found")
        
        return assistant
    
    def attach_dataset(self, assistant_id: int, dataset_ids: list[int]):
        return self.assistant_dataset_repo.sync(assistant_id, dataset_ids)

    def get_assistant_datasets(self, assistant_id: int) -> list[int]:
        return self.assistant_dataset_repo.get_datasets(assistant_id)

    async def chat(self, assistant_id: int, user_message: str, user_id: int):
        assistant = self.assistant_repo.get_by_id(assistant_id)
        if not assistant:
            raise HTTPException(status_code=404, detail="Assistant does not exist")

        self.chat_message_repo.add(assistant_id, "user", user_message, user_id=user_id)

        dataset_ids = self.assistant_dataset_repo.get_datasets(assistant_id)

        chunk_texts: list[str] | list = self.pc_service.search(dataset_ids, user_message)
        context = "\n\n".join(chunk_texts)

        messages = [
            {"role": "system", "content": assistant.desc or "You are an AI assistant."},
            {"role": "system", "content": f"You answer strictly based on the retrieved context; if the context contains a definition or explanation, restate it naturally and concisely without meta-phrases like “in this context,” and if it contradicts common knowledge you still follow the context; if the context lacks the answer, say the information is not available; always keep a natural, human-like tone.. Relevant context:\n{context}"},
            {"role": "user", "content": user_message},
        ]

        answer = await self.llm_service.chat(
            provider=assistant.provider,
            messages=messages,
            model=assistant.model,
            temperature=assistant.temperature,
        )

        self.chat_message_repo.add(assistant_id, "assistant", answer, user_id=user_id)

        return {
            "answer": answer,
            "sources": chunk_texts
        }
    
    def get_chat_messages(
            self,
            assistant_id: int
    ):
        return self.chat_message_repo.get_by_assistant_id(assistant_id)
    
    def get_all_chat_messages(
            self,
            user_id: int
    ):
        return self.chat_message_repo.get_all_chat_messages(user_id)
    
    def delete_chat_message(
            self,
            chat_message_id: int
    ):
        return self.chat_message_repo.delete_by_id(chat_message_id)
    
    def delete_chat_messages(
            self,
            assistant_id: int
    ):
        return self.chat_message_repo.delete_by_assistant_id(assistant_id)
    
    def update(
            self,
            id: int,
            data: UpdateAssistantRequest
    ):
        assistant = self.assistant_repo.get_by_id(id)
        if not assistant:
            raise HTTPException(status_code=404, detail="Assistant not found")
        
        updates = {
            "name": data.name,
            "desc": data.desc,
            "provider": data.provider,
            "model": data.model,
            "temperature": data.temperature
        }

        for key, value in updates.items():
            if value is not None:
                setattr(assistant, key, value)

        return self.assistant_repo.update(assistant, updates)