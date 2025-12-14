from fastapi import APIRouter, Depends
from pinecone import ServiceException
from pydantic import BaseModel

from app.config.di import get_assistant_service
from app.models.assistant_model import Assistant
from app.schemas.assistant_schema import AttachDatasetsRequest, ChatRequest, CreateAssistantRequest, UpdateAssistantRequest
from app.services.assistant_service import AssistantService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.get("/")
def get_by_user_id(
    user_id: int = Depends(get_current_user),
    service: AssistantService = Depends(get_assistant_service)
):
    return service.get_by_user_id(user_id)

@router.get("/{id}")
async def get_by_id(
    id: int,
    service: AssistantService = Depends(get_assistant_service),
):
    return service.get_by_id(id)

@router.get("/get-datasets/{assistant_id}")
def get_datasets_for_assistant(
    assistant_id: int,
    service: AssistantService = Depends(get_assistant_service)
):
    return service.get_assistant_datasets(assistant_id)

@router.get("/{assistant_id}/chat-messages")
async def get_chat_messages(
    assistant_id: int,
    service: AssistantService = Depends(get_assistant_service)
):
    return service.get_chat_messages(assistant_id)

@router.get("all-chat-messages")
def get_all_chat_message(
    service: AssistantService = Depends(get_assistant_service),
    user_id: int = Depends(get_current_user)
):
    return service.get_all_chat_messages(
        user_id
    )


@router.post("/")
def create_assistant(
    req: CreateAssistantRequest,
    service: AssistantService = Depends(get_assistant_service),
    user_id: int = Depends(get_current_user)
):
    print(req)

    return service.create_assistant(
        user_id,
        name=req.name,
        provider=req.provider,
        desc=req.desc,
        model=req.model,
        temperature=req.temperature,
    )

@router.put("/{id}")
async def update_assistant(
    id: int,
    req: UpdateAssistantRequest,
    service: AssistantService = Depends(get_assistant_service),
    user_id: int = Depends(get_current_user)
):
    print(req)

    return service.update(
        id,
        data=req
    )

@router.put("/{assistant_id}/datasets")
def attach_dataset(
    assistant_id: int,
    req: AttachDatasetsRequest,
    service: AssistantService = Depends(get_assistant_service),
    user_id: int = Depends(get_current_user)
):
    return service.attach_dataset(assistant_id, req.dataset_ids)

@router.post("/{id}/chat")
async def chat(
    id: int,
    req: ChatRequest,
    service: AssistantService = Depends(get_assistant_service),
    user_id: int = Depends(get_current_user)
):
    return await service.chat(id, req.message, user_id=user_id)

@router.delete("/chat-message/{id}")
def delete_chat_message(
    id: int,
    service: AssistantService = Depends(get_assistant_service),
    user_id: int = Depends(get_current_user)
):
    return service.delete_chat_message(
        chat_message_id=id
    )

@router.delete("/{id}")
def delete_chat_messages(
    id: int,
    service: AssistantService = Depends(get_assistant_service)
):
    return service.delete_chat_messages(
        id
    )