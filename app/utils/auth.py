from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config.di import get_user_repository
from app.repositories.user_repository import UserRepository
from app.utils.jwt import decode_token

bearer_scheme = HTTPBearer()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_repo: UserRepository = Depends(get_user_repository)
) -> int:
    token = creds.credentials

    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except:
        raise HTTPException(401, "Invalid or expired access token")

    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(401, "User not found")

    if user.id:
        return user.id
    else:
        raise ValueError("User without ID")
