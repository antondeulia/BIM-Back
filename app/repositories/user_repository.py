from sqlmodel import Session, select

from app.models.user_model import User


class UserRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.exec(
            select(User).where(User.email == email)
        ).first()
    
    def create(
            self,
            email: str,
            hashed_password: str | None,
            provider: str | None = None,
            google_sub: str | None = None,

    ):
        user = User(
            email=email,
            hashed_password=hashed_password
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
    
    def update(
            self,
            user: User,
            email: str | None = None,
            hashed_password: str | None = None,
            provider: str | None = None,
            google_sub: str | None = None
    ):
        if email is not None:
            user.email = email

        if hashed_password is not None:
            user.hashed_password = hashed_password

        if provider is not None:
            user.provider = provider

        if google_sub is not None:
            user.google_sub = google_sub

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_by_id(self, id: int):
        return self.session.exec(
            select(User).where(User.id == id)
        ).first()
    
    def get_by_google_sub(
            self,
            google_sub: str
    ):
        return self.session.exec(
            select(User).where(User.google_sub == google_sub)
        ).first()
    

