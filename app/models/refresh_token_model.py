from datetime import datetime
from sqlmodel import Field, SQLModel


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    token: str = Field(unique=True, index=True)
    expires_at: datetime