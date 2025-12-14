from sqlalchemy import Float
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import ARRAY
from typing import List


class Chunk(SQLModel, table=True):
    __tablename__ = "chunks" # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    doc_id: int = Field(index=True)

    content: str
    embedding: List[float] | None = Field(
        default=None, sa_column=Column(ARRAY(Float))
    )
