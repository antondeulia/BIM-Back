from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel

from app.config.di import get_document_service
from app.services.document_service import DocumentService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/document", tags=["document"])

class CreateTextDocRequest(BaseModel):
    dataset_id: int
    content: str

class CreateFileDocRequest(BaseModel):
    dataset_id: int

@router.post("/text")
def create_text_doc(
    req: CreateTextDocRequest,
    service: DocumentService = Depends(get_document_service),
    user_id: int = Depends(get_current_user)
):
    return service.create_text_doc(
        dataset_id=req.dataset_id,
        content=req.content,
        user_id=user_id
    )

@router.post("/file")
def create_file_doc(
    dataset_id: int = Form(...),
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
    user_id: int = Depends(get_current_user)
):
    return service.create_file_doc(
        dataset_id,
        file,
        user_id=user_id
    )
    

@router.post("/media")
def create_media_doc():
    pass

@router.get("/by-dataset/{id}")
def get_by_dataset_id(
    id: int,
    service: DocumentService = Depends(get_document_service),
    user_id: int = Depends(get_current_user)
):
    return service.get_by_dataset_id(id)

@router.get("/by-user-id")
def get_by_user_id(
    service: DocumentService = Depends(get_document_service),
    user_id: int = Depends(get_current_user)
):
    return service.get_by_user_id(user_id)

@router.delete("/{id}")
def delete(
    id: int,
    service: DocumentService = Depends(get_document_service),
    user_id: int = Depends(get_current_user)
):
    return service.delete(id)