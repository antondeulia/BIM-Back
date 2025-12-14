from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.config.di import get_dataset_repo
from app.repositories.dataset_repository import DatasetRepository
from app.utils.auth import get_current_user

router = APIRouter(prefix="/datasets", tags=["datasets"])

class CreateDatasetRequest(BaseModel):
    title: str
    desc: str | None
    image_url: str | None

@router.post("/")
def create_dataset(
    req: CreateDatasetRequest,
    service: DatasetRepository = Depends(get_dataset_repo),
    user_id: int = Depends(get_current_user)
):
    return service.create(
        title=req.title,
        desc=req.desc,
        image_url=req.image_url,
        user_id=user_id
    )

@router.get("/")
def get_by_user_id(
    service: DatasetRepository = Depends(get_dataset_repo),
    user_id: int = Depends(get_current_user)
):
    return service.get_by_user_id(user_id)

@router.get("/{id}")
def get_by_id(
    id: int,
    repo: DatasetRepository = Depends(get_dataset_repo)
):
    return repo.get_by_id(id)

@router.delete("/{id}")
def delete(
    id: int,
    repo: DatasetRepository = Depends(get_dataset_repo)
):
    return repo.delete(id)