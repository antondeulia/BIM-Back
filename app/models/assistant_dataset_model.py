from sqlmodel import Field, SQLModel

class AssistantDataset(SQLModel, table=True):
    __tablename__ = "assistant_datasets" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    assistant_id: int = Field(index=True)
    dataset_id: int = Field(index=True)