from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    pinecone_api_key: str
    openai_api_key: str
    gemini_api_key: str
    google_client_id: str
    google_client_secret: str
    
    class Config():
        env_file = ".env"

settings = Settings() # type: ignore