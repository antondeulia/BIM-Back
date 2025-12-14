from pydantic import BaseModel, Field


class SignUpRequest(BaseModel):
    email: str
    password: str

class SignInRequest(BaseModel):
    email: str
    password: str | None = Field(default=None)

class GoogleAuthRequest(BaseModel):
    email: str
    google_sub: str