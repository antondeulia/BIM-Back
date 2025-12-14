from datetime import datetime
from fastapi import HTTPException
from app.models.user_model import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.utils.jwt import create_access_token, create_refresh_token
from app.utils.pwd import hash_password, verify_password


class AuthService():
    def __init__(
            self,
            user_repository: UserRepository,
            refresh_token_repo: RefreshTokenRepository
    ):
        self.user_repository = user_repository
        self.refresh_token_repo = refresh_token_repo

    def sign_up(self, email: str, password: str):
        if self.user_repository.get_by_email(email):
            raise HTTPException(status_code=409, detail="User with this email already exists")

        print(password)
        hashed_password = hash_password(password)
        print(hash_password)

        user = self.user_repository.create(
            email,
            hashed_password,
            )
        
        if user.id:
            return self.return_tokens(user.id)
    
    def sign_in(self, email: str, password: str | None):
        user: User | None = self.user_repository.get_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not user.hashed_password:
            raise HTTPException(status_code=400, detail="Please log in with your provider or create password")

        if password:
            pw = verify_password(password, user.hashed_password)
            if not pw:
                raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if user.id:
            return self.return_tokens(user_id=user.id)
        
    def refresh(
        self,
        token: str
    ):
        stored = self.refresh_token_repo.get_one(token)
        if not stored:
            raise HTTPException(status_code=401, detail="Refresh Token not found")
        
        if stored.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired")

        self.refresh_token_repo.delete(token)

        new_token = create_refresh_token()
        new_refresh_token = self.refresh_token_repo.create(
            token=new_token,
            user_id=stored.user_id
        )

        access_token = create_access_token(user_id=stored.user_id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token
        }

    def logout(
        self,
        token: str
    ):
        stored = self.refresh_token_repo.get_one(token)
        if not stored:
            raise HTTPException(status_code=404, detail="Refresh token not found")

        self.refresh_token_repo.delete(token)
        return {
            "status": "ok",
            "message": "Refresh token deleted successfully"
        }

    # Google:
    def get_or_create_google_user(
    self,
    email: str,
    google_sub: str,
    ) -> User:
        user = self.user_repository.get_by_google_sub(google_sub)
        if user:
            return user

        user = self.user_repository.get_by_email(email)

        if user:
            user.provider = "google"
            user.google_sub = google_sub
            self.user_repository.update(
                user,
                provider="google",
                google_sub=google_sub
            )
            return user
        else:
            return self.user_repository.create(
                email, provider="google", google_sub=google_sub, hashed_password=None)
        
    def google_auth(
            self,
            email: str,
            google_sub: str
    ):
        user: User = self.get_or_create_google_user(
            email=email,
            google_sub=google_sub,
        )

        if user.id:
            return self.return_tokens(user_id=user.id)

        

    def return_tokens(
            self,
            user_id: int
    ):
        access_token = create_access_token(user_id)

        token = create_refresh_token()
        refresh_token = self.refresh_token_repo.create(
            token=token,
            user_id=user_id
        )
        return {
            "status": "ok",
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        