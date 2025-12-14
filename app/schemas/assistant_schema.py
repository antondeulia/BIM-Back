from pydantic import BaseModel


class AttachDatasetsRequest(BaseModel):
    dataset_ids: list[int]

class UpdateAssistantRequest(BaseModel):
    name: str | None = None
    desc: str | None = None
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None


class CreateAssistantRequest(BaseModel):
    name: str | None
    desc: str | None = None

    temperature: float = 0.7
    provider: str = "openai"
    model: str = "gpt-4.1"

    
class ChatRequest(BaseModel):
    message: str