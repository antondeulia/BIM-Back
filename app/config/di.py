from fastapi import Depends
from sqlmodel import Session
from app.config.db import get_session
from app.models import document_model
from app.repositories.assistant_dataset_repository import AssistantDatasetRepository
from app.repositories.assistant_repository import AssistantRepository
from app.repositories.chat_message_repository import ChatMessageRepository
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.services.assistant_service import AssistantService
from app.services.document_service import DocumentService
from app.services.llm.llm_service import LLMService
from app.services.llm.openai_provider import OpenAIProvider
from app.services.pinecone_service import PineconeService

def get_user_repository(
    session: Session = Depends(get_session)
):
    return UserRepository(session)

def get_refresh_token_repository(
    session: Session = Depends(get_session)
):
    return RefreshTokenRepository(session)

def get_dataset_repo(
        session: Session = Depends(get_session)
):
    return DatasetRepository(session)

def get_document_repo(
        session: Session = Depends(get_session)
):
    return DocumentRepository(session)

def get_chunk_repo(
        session: Session = Depends(get_session)
):
    return ChunkRepository(session)

def get_pinecone_service():
    return PineconeService()

def get_document_service(
        document_repo: DocumentRepository = Depends(get_document_repo),
        dataset_repo: DatasetRepository = Depends(get_dataset_repo),
        chunk_repo: ChunkRepository = Depends(get_chunk_repo),
        pc_service: PineconeService = Depends(get_pinecone_service)
):
    return DocumentService(
        document_repo=document_repo,
        dataset_repo=dataset_repo,
        chunk_repo=chunk_repo,
        pc_service=pc_service
    )

def get_assistant_repo(
        session: Session = Depends(get_session)
):
    return AssistantRepository(session)

def get_assistant_dataset_repo(
        session: Session = Depends(get_session)
):
    return AssistantDatasetRepository(session)

def get_chat_message_repo(
        session: Session = Depends(get_session)
):
    return ChatMessageRepository(session)

def get_llm_service() -> LLMService:
    return LLMService()

def get_assistant_service(
        assistant_repo: AssistantRepository = Depends(get_assistant_repo),
        assistant_dataset_repo: AssistantDatasetRepository = Depends(get_assistant_dataset_repo),
        chat_message_repo: ChatMessageRepository = Depends(get_chat_message_repo),
        pc_service: PineconeService = Depends(get_pinecone_service),
        llm_service: LLMService = Depends(get_llm_service)
):
    return AssistantService(
        assistant_repo,
        assistant_dataset_repo,
        chat_message_repo,
        pc_service,
        llm_service
    )

