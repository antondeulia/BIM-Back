from sqlmodel import Session, select
from app.models.document_model import Document


class DocumentRepository():
    def __init__(
            self,
            session: Session
    ):
        self.session = session

    def create_text_doc(self, dataset_id: int, content: str, type: str, user_id: int):
        document = Document(
            user_id=user_id,
            dataset_id=dataset_id,
            content=content,
            type=type
        )

        self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return document
    
    def create_doc(
            self,
            dataset_id: int,
            content: str,
            user_id: int
    ):
        document = Document(
            user_id=user_id,
            dataset_id=dataset_id,
            content=content,
        )

        self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return document
    
    def get_by_dataset_id(self, dataset_id: int):
        documents = self.session.exec(
            select(Document).where(Document.dataset_id == dataset_id)
        ).all()

        return documents
    
    def get_by_user_id(self, user_id: int):
        documents = self.session.exec(
            select(Document).where(Document.user_id == user_id)
        ).all()

        return documents
    
    def get_by_id(self, id: int):
        document = self.session.exec(
            select(Document).where(Document.id == id)
        ).first()
        
        return document
    
    def delete(self, document: Document):
        self.session.delete(document)
        self.session.commit()

        return {
            "status": "ok",
            "message": "Document deleted successfully!"
        }
