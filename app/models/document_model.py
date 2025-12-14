from datetime import datetime
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    __tablename__ = "documents" # type: ignore

    user_id: int = Field(...)

    id: int | None = Field(default=None, primary_key=True)
    dataset_id: int = Field(index=True)

    type: str = Field(default="text")

    content: str
    source: str | None = None

    created_at: datetime = Field(default_factory=datetime.now)