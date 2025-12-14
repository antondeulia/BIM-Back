from typing import Sequence
from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.dataset_model import Dataset


class DatasetRepository():
    def __init__(
            self,
            session: Session
    ):
        self.session = session

    def create(
            self,
            title: str,
            desc: str | None,
            image_url: str | None,
            user_id: int
    ) -> Dataset:
        dataset = Dataset(
            title=title,
            desc=desc,
            image_url=image_url,
            user_id=user_id
        )

        self.session.add(dataset)
        self.session.commit()
        self.session.refresh(dataset)

        return dataset
    
    def get_by_user_id(
            self,
            user_id: int
    ) -> Sequence[Dataset]:
        datasets = self.session.exec(
            select(Dataset).where(Dataset.user_id == user_id)
        ).all()

        return datasets
    
    def get_by_id(
            self,
            id: int
    ):
        dataset = self.session.exec(
            select(Dataset).where(Dataset.id == id)
        ).first()

        return dataset
    
    def delete(
            self,
            id: int
    ):
        dataset = self.get_by_id(id)
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        self.session.delete(dataset)
        self.session.commit()

        return {
            "status": "ok"
        }