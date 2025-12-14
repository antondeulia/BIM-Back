from sqlmodel import Field, SQLModel


class Assistant(SQLModel, table=True):
    __tablename__ = "assistants" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    user_id: int

    name: str | None
    desc: str | None

    temperature: float = Field(default=0.7)
    provider: str = "openai"
    model: str = "gpt-4.1"