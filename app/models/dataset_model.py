from datetime import datetime
from sqlmodel import Field, SQLModel


class Dataset(SQLModel, table=True):
    __tablename__ = "datasets" # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(...)
    desc: str | None = Field(default=None)
    image_url: str | None = Field(default=None)

    user_id: int = Field(..., index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)