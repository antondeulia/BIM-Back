import os
import re
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.document_repository import DocumentRepository
from app.services.pinecone_service import PineconeService
from app.utils import chunker
from app.utils.file_text_extractors import extract_text_from_file


class DocumentService():
    def __init__(
            self,
            document_repo: DocumentRepository,
            dataset_repo: DatasetRepository,
            chunk_repo: ChunkRepository,
            pc_service: PineconeService
    ):
        self.document_repo = document_repo
        self.dataset_repo = dataset_repo
        self.chunk_repo = chunk_repo
        self.pc_service = pc_service

    def create_text_doc(
            self,
            dataset_id: int,
            content: str,
            user_id: int
    ):
        dataset = self.dataset_repo.get_by_id(dataset_id)
        if not dataset:
            raise HTTPException(status_code=404, detail="The dataset you are trying to add a document for does not exist")
        
        return self.embed_text(dataset_id, content, type="text", user_id=user_id)

    
    def create_file_doc(
        self,
        dataset_id: int,
        file: UploadFile,
        user_id: int
    ):
        ALLOWED_MIME_TYPES = {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
        }

        if file.content_type in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}"
            )

        dataset = self.dataset_repo.get_by_id(dataset_id)
        if not dataset:
            raise HTTPException(status_code=404, detail="The dataset you are trying to add a document for does not exist")

        ext = os.path.splitext(file.filename)[1].lower() # type: ignore
        filename = f"{uuid4()}{ext}"
        path = f"uploads/{filename}"
        os.makedirs("uploads", exist_ok=True)

        with open(path, "wb") as f:
            f.write(file.file.read())

        text = extract_text_from_file(path, file.content_type)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from file"
            )
        
        text = text.replace("\f", " ")
        text = re.sub(r"\n{2,}", "\n\n", text)
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

        return self.embed_text(
            dataset_id,
            content=text,
            type="file",
            user_id=user_id
        )

    def get_by_dataset_id(self, dataset_id):
        return self.document_repo.get_by_dataset_id(dataset_id)
    
    def get_by_user_id(self, user_id):
        return self.document_repo.get_by_user_id(user_id)
    
    def embed_text(
            self,
            dataset_id: int,
            content: str,
            type: str,
            user_id: int
    ):
        doc = self.document_repo.create_text_doc(
            dataset_id,
            content,
            type=type,
            user_id=user_id
        )

        assert doc.id is not None
        
        chunks: list[str] = chunker.chunk_text(content)
        records = []

        for chunk_text in chunks:
            chunk = self.chunk_repo.create(
                doc_id=doc.id,
                content=chunk_text
            )

            records.append(
                {
                    "_id": str(chunk.id),
                    "chunk_text": chunk_text,
                    "doc_id": doc.id,
                    "dataset_id": dataset_id,
                }
            )

        if records:
            self.pc_service.upsert_records(records)

        return doc
    
    def delete(self, id: int):
        document = self.document_repo.get_by_id(id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return self.document_repo.delete(document)