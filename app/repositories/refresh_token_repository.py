from datetime import datetime, timedelta
from sqlmodel import Session, select

from app.models.refresh_token_model import RefreshToken


class RefreshTokenRepository():
    def __init__(
        self,
        session: Session
    ):
        self.session = session

    def create(
        self,
        user_id: int,
        token: str
    ):
        expires_at = datetime.utcnow() + timedelta(days=30)
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )

        self.session.add(refresh_token)
        self.session.commit()
        self.session.refresh(refresh_token)
        return refresh_token
    
    def get_one(
        self,
        token: str
    ):
        return self.session.exec(
            select(RefreshToken).where(RefreshToken.token == token)
        ).first()
    
    def delete(
        self,
        token: str
    ):
        refresh_token = self.get_one(token)

        if refresh_token:
            self.session.delete(refresh_token)
            self.session.commit()

