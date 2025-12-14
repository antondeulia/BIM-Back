from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users" # pyright: ignore[reportAssignmentType]

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str | None = Field(default=None)

    provider: str | None = Field(default=None)
    google_sub: str | None = Field(default=None)
