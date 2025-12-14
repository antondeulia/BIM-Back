from sqlmodel import Session

from app.models.chunk_model import Chunk


class ChunkRepository():
    def __init__(
            self,
            session: Session
    ):
        self.session = session

    def create(
            self,
            doc_id: int,
            content: str
    ):
        chunk = Chunk(
            doc_id=doc_id,
            content=content,
        )

        self.session.add(chunk)
        self.session.commit()
        self.session.refresh(chunk)

        return chunk