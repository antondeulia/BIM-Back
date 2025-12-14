import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

from app.config.settings import settings
from app.models.user_model import User
from app.models.refresh_token_model import RefreshToken
from app.models.dataset_model import Dataset
from app.models.document_model import Document
from app.models.chunk_model import Chunk
from app.models.assistant_model import Assistant
from app.models.assistant_dataset_model import AssistantDataset
from app.models.chat_message_model import ChatMessage

load_dotenv()

engine = create_engine(settings.database_url)

def init_db():
    SQLModel.metadata.create_all(engine)

init_db()

def get_session():
    with Session(engine) as session:
        yield session