import secrets
import time
import jwt

SECRET = "secret"
ALGO = "HS256"

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": int(time.time()) + 360000
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALGO])

def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)